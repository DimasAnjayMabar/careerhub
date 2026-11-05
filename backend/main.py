"""
main.py
Server utama FastAPI untuk Alumni Skill Tool (offline, plug-and-play).

Filosofi:
- TIDAK ada master hardcode di kode. Master dimuat dari master_storage.json.
- Jika file belum ada, mulai kosong. Upload pertama mengisi master dari Excel
  (semua entitas baru otomatis approved via normalizer.py).
- Tidak ada konsep "pending". Tidak ada review manual.

File state:
- master_storage.json  : {prodi, bidang, skill, pencapaian, alias, meta}
- data_storage.json    : {responden}

Port default: 8001.
Jalankan: uvicorn main:app --reload --port 8001
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import feature1
import feature2
import feature3
import feature4
import normalizer
import upload


# =========================================================
# PATH
# =========================================================

BASE_DIR = os.path.dirname(__file__)
MASTER_FILE = os.path.join(BASE_DIR, "master_storage.json")
DATA_FILE = os.path.join(BASE_DIR, "data_storage.json")


# =========================================================
# STATE GLOBAL (kosong di awal — terisi dari master_storage.json / upload)
# =========================================================

PRODI: list[dict] = []
BIDANG: list[dict] = []
SKILL: list[dict] = []
PENCAPAIAN: list[dict] = []
ALIAS: dict[str, str] = {}

RESPONDEN: list[dict] = []


# =========================================================
# META BLOCK (helper empty state)
# =========================================================

def meta_block(jumlah_responden: int, extra: Optional[dict] = None) -> dict:
    """
    Blok meta standar untuk semua featureN.get_all().
    FE cukup cek `meta.ada_data` untuk empty state.
    """
    ada = jumlah_responden > 0
    meta = {
        "jumlah_responden": jumlah_responden,
        "ada_data": ada,
        "pesan": None if ada else "Belum ada data. Silakan upload Excel terlebih dahulu.",
    }
    if extra:
        meta.update(extra)
    return meta


# =========================================================
# EVENT BUS (SSE)
# =========================================================

class EventBus:
    def __init__(self):
        self._subs: set[asyncio.Queue] = set()

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=100)
        self._subs.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._subs.discard(q)

    async def publish(self, event: str, data: dict) -> None:
        for q in list(self._subs):
            try:
                q.put_nowait((event, data))
            except asyncio.QueueFull:
                pass


bus = EventBus()


# =========================================================
# PERSIST: MASTER
# =========================================================

def _load_master() -> None:
    """
    Load master dari master_storage.json.
    Jika belum ada, mulai kosong (master akan terisi saat upload pertama).
    """
    global PRODI, BIDANG, SKILL, PENCAPAIAN, ALIAS

    if not os.path.exists(MASTER_FILE):
        print("[master] belum ada — mulai kosong (akan terisi saat upload)")
        ALIAS = dict(normalizer.DEFAULT_ALIAS)
        return

    try:
        with open(MASTER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        PRODI = data.get("prodi", [])
        BIDANG = data.get("bidang", [])
        SKILL = data.get("skill", [])
        PENCAPAIAN = data.get("pencapaian", [])
        ALIAS = data.get("alias") or dict(normalizer.DEFAULT_ALIAS)
        print(
            f"[master] dimuat: {len(SKILL)} skill, {len(PENCAPAIAN)} pencapaian, "
            f"{len(ALIAS)} alias, {len(PRODI)} prodi, {len(BIDANG)} bidang"
        )
    except Exception as e:
        print(f"[master] gagal load: {e} — mulai kosong")
        ALIAS = dict(normalizer.DEFAULT_ALIAS)


def _save_master() -> None:
    """Simpan master ke master_storage.json (overwrite)."""
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "prodi": PRODI,
                "bidang": BIDANG,
                "skill": SKILL,
                "pencapaian": PENCAPAIAN,
                "alias": ALIAS,
                "meta": {
                    "total_skill": len(SKILL),
                    "total_pencapaian": len(PENCAPAIAN),
                    "total_alias": len(ALIAS),
                    "total_prodi": len(PRODI),
                    "total_bidang": len(BIDANG),
                },
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(
        f"[master] tersimpan: {len(SKILL)} skill, {len(PENCAPAIAN)} pencapaian, "
        f"{len(ALIAS)} alias, {len(PRODI)} prodi, {len(BIDANG)} bidang"
    )


# =========================================================
# PERSIST: RESPONDEN
# =========================================================

def _load_data() -> None:
    """Load RESPONDEN dari data_storage.json (jika ada)."""
    global RESPONDEN
    if not os.path.exists(DATA_FILE):
        print("[data] belum ada — mulai kosong")
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        RESPONDEN = data.get("responden", [])
        print(f"[data] {len(RESPONDEN)} responden dimuat")
    except Exception as e:
        print(f"[data] gagal: {e}")


def _save_data() -> None:
    """Simpan RESPONDEN ke data_storage.json (overwrite)."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"responden": RESPONDEN}, f, indent=2, ensure_ascii=False)
    print(f"[data] {len(RESPONDEN)} responden tersimpan")


# =========================================================
# PAYLOAD BUILDER (featureN + meta)
# =========================================================

def _payload_feature1() -> dict:
    payload = feature1.get_all(RESPONDEN, SKILL, PENCAPAIAN, PRODI, BIDANG)
    payload["meta"] = meta_block(len(RESPONDEN))
    return payload


def _payload_feature2() -> dict:
    payload = feature2.get_all(RESPONDEN, SKILL, PENCAPAIAN, PRODI, BIDANG)
    payload["meta"] = meta_block(len(RESPONDEN), extra={
        "ada_data_gap": any(r.get("skill_gap") for r in RESPONDEN),
        "catatan": (
            "'Gap' di sini adalah INFERENSI: skill yang dibutuhkan "
            "mayoritas alumni di bidang yang sama, tapi tidak disebut "
            "oleh responden. Bukan self-assessment."
        ),
    })
    return payload


def _payload_feature3() -> dict:
    payload = feature3.get_all(RESPONDEN, SKILL, PENCAPAIAN, PRODI, BIDANG)
    payload["meta"] = meta_block(len(RESPONDEN))
    return payload


def _payload_feature4() -> dict:
    payload = feature4.get_all(RESPONDEN, SKILL, PENCAPAIAN, PRODI, BIDANG)
    payload["meta"] = meta_block(len(RESPONDEN))
    return payload


def _payload_all() -> dict:
    return {
        "feature1": _payload_feature1(),
        "feature2": _payload_feature2(),
        "feature3": _payload_feature3(),
        "feature4": _payload_feature4(),
        "meta": meta_block(len(RESPONDEN)),
    }


# =========================================================
# APP
# =========================================================

app = FastAPI(title="Alumni Skill Tool (Offline, Plug-and-Play)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://0.0.0.0:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _on_startup():
    _load_master()
    _load_data()


# =========================================================
# ROUTES: STATUS
# =========================================================

@app.get("/status")
def status():
    return {
        "ada_data": len(RESPONDEN) > 0,
        "jumlah_responden": len(RESPONDEN),
        "jumlah_skill_master": len(SKILL),
        "jumlah_pencapaian_master": len(PENCAPAIAN),
        "jumlah_alias": len(ALIAS),
        "jumlah_prodi": len(PRODI),
        "jumlah_bidang": len(BIDANG),
    }


# =========================================================
# ROUTES: INGEST
# =========================================================

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    global RESPONDEN

    content = await file.read()
    try:
        new_responden, summary = upload.ingest_excel(
            content, SKILL, PENCAPAIAN, PRODI, BIDANG, ALIAS
        )
    except Exception as e:
        return {"ok": False, "error": str(e)}

    RESPONDEN = new_responden

    # persist: master & data
    _save_master()
    _save_data()

    # broadcast ke semua subscriber
    await bus.publish("feature1-update", _payload_feature1())
    await bus.publish("feature2-update", _payload_feature2())
    await bus.publish("feature3-update", _payload_feature3())
    await bus.publish("feature4-update", _payload_feature4())

    return {"ok": True, "summary": summary}


# =========================================================
# ROUTES: FEATURE 1, 2 (REST fallback)
# =========================================================

@app.get("/feature1/data")
def feature1_data():
    return _payload_feature1()


@app.get("/feature2/data")
def feature2_data():
    return _payload_feature2()


# =========================================================
# ROUTES: FEATURE 3 (filter)
# =========================================================

@app.get("/feature3/filters")
def feature3_filters():
    return feature3.get_filter_options(RESPONDEN, BIDANG)


@app.get("/feature3/data")
def feature3_data(angkatan: Optional[int] = None, bidang_id: Optional[int] = None):
    payload = feature3.get_dashboard(
        RESPONDEN, SKILL, PENCAPAIAN, PRODI, BIDANG,
        angkatan=angkatan, bidang_id=bidang_id,
    )
    payload["meta"] = meta_block(
        len(RESPONDEN),
        extra={"filter": {"angkatan": angkatan, "bidang_id": bidang_id}},
    )
    return payload


# =========================================================
# ROUTES: FEATURE 4 (matcher)
# =========================================================

class MatchRequest(BaseModel):
    skill_ids: list[int]


@app.post("/feature4/match")
def feature4_match(req: MatchRequest):
    result = feature4.match_skills(
        req.skill_ids, RESPONDEN, SKILL, PENCAPAIAN, BIDANG, top_n=5
    )
    if not result.get("ok"):
        return result
    # gabungkan meta dari match_skills (jumlah_user_skill, catatan)
    # dengan meta_block (jumlah_responden, ada_data, pesan)
    match_meta = result.get("meta", {})
    result["meta"] = meta_block(len(RESPONDEN), extra=match_meta)
    return result


# =========================================================
# ROUTES: SSE
# =========================================================

def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/stream")
async def stream():
    async def gen():
        q = bus.subscribe()
        try:
            # snapshot awal — semua feature sekaligus
            yield _sse("init", _payload_all())

            while True:
                try:
                    event, data = await asyncio.wait_for(q.get(), timeout=15)
                    yield _sse(event, data)
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            bus.unsubscribe(q)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )