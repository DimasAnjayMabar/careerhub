"""
upload.py
Service untuk memproses upload Excel GForm → state terstruktur.

⚠️ Modul ini TIDAK menyimpan master data (PRODI, BIDANG, SKILL, PENCAPAIAN).
Master data disediakan oleh main.py dan diteruskan sebagai parameter.

⚠️ Normalisasi skill/pencapaian/prodi/bidang didelegasikan ke normalizer.py:
- Alias manual + fuzzy match + auto-insert (approved).
- Tidak ada konsep "pending".
- Tidak ada prodi/bidang hardcode; semua dari data Excel.

Tanggung jawab modul ini:
- split_multi_value()      : pecah sel multi-value jadi list[str]
- parse_waktu()            : "0.1" → 0 (bulan, dibulatkan)
- normalize_status()       : "sebagian" → "sebagian sesuai"
- derive_skill_gap()       : turunkan skill_gap dari data (inferred gap)
- ingest_excel()           : entry point — bytes → (responden, summary)

Efek samping:
- skill_state, pencapaian_state, prodi_state, bidang_state, alias_map
  MUTABLE — normalizer menambah entitas baru & alias baru ke dalamnya.
"""

from __future__ import annotations

import io
import re
from collections import Counter, defaultdict

import pandas as pd

import normalizer


# =========================================================
# PLACEHOLDER KOSONG
# =========================================================

_PLACEHOLDER_EMPTY = {"", "-", "n/a", "na", "none", "tidak ada", "tidak"}


# =========================================================
# UTIL: SPLIT, PARSE, NORMALIZE STATUS
# =========================================================

def split_multi_value(raw) -> list[str]:
    """
    Pecah sel multi-value jadi list bersih.
    Delimiter: , ; \\n | dan ' dan '
    Melindungi koma di dalam kurung: 'Python (NumPy, Pandas)'
    '/' TIDAK di-split (bagian istilah: UI/UX, CI/CD).
    """
    if raw is None:
        return []
    if isinstance(raw, float) and pd.isna(raw):
        return []
    text = str(raw).strip()
    if not text or text.lower() in _PLACEHOLDER_EMPTY:
        return []

    text = text.replace("\n", ",").replace(";", ",").replace("|", ",")
    text = re.sub(r"\s+dan\s+", ",", text, flags=re.IGNORECASE)

    protected: list[str] = []

    def _protect(m):
        protected.append(m.group(0))
        return f"__PROTECTED_{len(protected) - 1}__"

    text = re.sub(r"\([^)]*\)", _protect, text)

    parts = [p.strip() for p in text.split(",")]

    restored = []
    for p in parts:
        m = re.fullmatch(r"__PROTECTED_(\d+)__", p)
        if m:
            restored.append(protected[int(m.group(1))])
        else:
            restored.append(p)

    return [p for p in restored if p]


def parse_waktu(raw) -> int:
    """'0.1' → 0 ; '3' → 3 ; '4 bulan' → 4 ; kosong → 0."""
    if raw is None:
        return 0
    if isinstance(raw, float) and pd.isna(raw):
        return 0
    text = str(raw).strip().lower()
    if not text or text in _PLACEHOLDER_EMPTY:
        return 0
    m = re.search(r"-?\d+(?:[.,]\d+)?", text)
    if not m:
        return 0
    try:
        return int(round(float(m.group(0).replace(",", "."))))
    except ValueError:
        return 0


def normalize_status(raw) -> str:
    """'sebagian' / 'sebagian sesuai' / 'sesuai' / 'tidak sesuai' → enum."""
    if raw is None:
        return "tidak sesuai"
    text = normalizer.normalize_for_lookup(str(raw))
    if text in _PLACEHOLDER_EMPTY:
        return "tidak sesuai"
    if "tidak" in text:
        return "tidak sesuai"
    if "sebagian" in text or "cukup" in text or "partial" in text:
        return "sebagian sesuai"
    if "sesuai" in text or "match" in text:
        return "sesuai"
    return "tidak sesuai"


# =========================================================
# DERIVE SKILL GAP (untuk feature2)
# =========================================================

def derive_skill_gap(
    responden: list[dict],
    threshold: float = 0.5,
    min_responden: int = 5,
) -> None:
    """
    Hitung skill_gap per responden (in-place).

    gap_R = skill_dominan_bidang(R) − skill_yang_disebut_R

    - skill_dominan_bidang: skill yang disebut ≥ threshold responden
      di bidang yang sama.
    - Bidang dengan < min_responden di-skip (gap = []) agar tidak bias.
    """
    bidang_freq: dict[int, Counter] = defaultdict(Counter)
    bidang_count: Counter = Counter()

    for r in responden:
        bid = r["bidang_id"]
        bidang_count[bid] += 1
        disebut = set(r.get("skill_dibutuhkan_hard", [])) | set(r.get("skill_dibutuhkan_soft", []))
        for sid in disebut:
            bidang_freq[bid][sid] += 1

    skill_dominan: dict[int, set[int]] = {}
    for bid, freq in bidang_freq.items():
        n = bidang_count[bid]
        if n < min_responden:
            skill_dominan[bid] = set()
        else:
            skill_dominan[bid] = {sid for sid, f in freq.items() if f / n >= threshold}

    for r in responden:
        disebut = set(r.get("skill_dibutuhkan_hard", [])) | set(r.get("skill_dibutuhkan_soft", []))
        r["skill_gap"] = sorted(skill_dominan.get(r["bidang_id"], set()) - disebut)


# =========================================================
# INGESTION
# =========================================================

COLUMN_ALIASES = {
    "angkatan":    ["angkatan", "alumni dari angkatan", "tahun angkatan", "tahun lulus"],
    "prodi":       ["program studi", "prodi", "program studi apa"],
    "bidang":      ["bidang pekerjaan", "pekerjaan", "bidang"],
    "waktu":       ["waktu tunggu", "berapa bulan", "bulan waktu tunggu"],
    "hard_skill":  ["hard skill", "hard skill apa saja"],
    "soft_skill":  ["soft skill", "soft skill apa saja"],
    "sertifikasi": ["sertifikasi"],
    "kompetisi":   ["kompetisi", "lomba"],
    "proyek":      ["proyek", "project"],
    "status":      ["sesuai", "kesesuaian"],
    "saran":       ["saran"],
}


def _pick(row: dict, keys: list[str]):
    norm = {normalizer.normalize_for_lookup(str(k)): v for k, v in row.items()}
    for k in keys:
        kn = normalizer.normalize_for_lookup(k)
        for rk, rv in norm.items():
            if kn in rk:
                return rv
    return None


def ingest_row(
    row: dict,
    skill_state: list[dict],
    pencapaian_state: list[dict],
    prodi_state: list[dict],
    bidang_state: list[dict],
    alias_map: dict[str, str],
    resolutions_log: list[dict],
) -> dict:
    """
    Konversi 1 baris GForm → record responden denormalized.

    resolutions_log: list eksternal untuk audit (diisi hasil resolve_*).
    """
    # --- prodi ---
    prodi_res = normalizer.resolve_prodi(
        _pick(row, COLUMN_ALIASES["prodi"]), prodi_state, alias_map
    )
    resolutions_log.append(prodi_res)
    if prodi_res["prodi_id"] is None:
        raise ValueError("Prodi kosong / tidak valid")

    # --- bidang ---
    bidang_res = normalizer.resolve_bidang(
        _pick(row, COLUMN_ALIASES["bidang"]), bidang_state, alias_map
    )
    resolutions_log.append(bidang_res)
    if bidang_res["bidang_id"] is None:
        raise ValueError("Bidang kosong / tidak valid")

    # --- hard skill ---
    hard_ids: list[int] = []
    for name in split_multi_value(_pick(row, COLUMN_ALIASES["hard_skill"])):
        res = normalizer.resolve_skill(name, "hard", skill_state, alias_map)
        resolutions_log.append(res)
        if res["skill_id"] and res["skill_id"] not in hard_ids:
            hard_ids.append(res["skill_id"])

    # --- soft skill ---
    soft_ids: list[int] = []
    for name in split_multi_value(_pick(row, COLUMN_ALIASES["soft_skill"])):
        res = normalizer.resolve_skill(name, "soft", skill_state, alias_map)
        resolutions_log.append(res)
        if res["skill_id"] and res["skill_id"] not in soft_ids:
            soft_ids.append(res["skill_id"])

    # --- pencapaian ---
    def _resolve_pencapaian_list(raw, jenis):
        ids: list[int] = []
        for name in split_multi_value(raw):
            res = normalizer.resolve_pencapaian(name, jenis, pencapaian_state, alias_map)
            resolutions_log.append(res)
            if res["pencapaian_id"] and res["pencapaian_id"] not in ids:
                ids.append(res["pencapaian_id"])
        return ids

    sert_ids = _resolve_pencapaian_list(_pick(row, COLUMN_ALIASES["sertifikasi"]), "sertifikasi")
    komp_ids = _resolve_pencapaian_list(_pick(row, COLUMN_ALIASES["kompetisi"]), "kompetisi")
    proy_ids = _resolve_pencapaian_list(_pick(row, COLUMN_ALIASES["proyek"]), "proyek")

    return {
        "angkatan": int(_pick(row, COLUMN_ALIASES["angkatan"]) or 0),
        "prodi_id": prodi_res["prodi_id"],
        "bidang_id": bidang_res["bidang_id"],
        "waktu_kerja_pertama_bulan": parse_waktu(_pick(row, COLUMN_ALIASES["waktu"])),
        "status_kesesuaian": normalize_status(_pick(row, COLUMN_ALIASES["status"])),
        "saran_mahasiswa": str(_pick(row, COLUMN_ALIASES["saran"]) or "").strip(),
        "skill_dibutuhkan_hard": hard_ids,
        "skill_dibutuhkan_soft": soft_ids,
        "skill_gap": [],
        "pencapaian_sertifikasi": sert_ids,
        "pencapaian_kompetisi": komp_ids,
        "pencapaian_proyek": proy_ids,
    }


def ingest_sheet(
    rows: list[dict],
    skill_state: list[dict],
    pencapaian_state: list[dict],
    prodi_state: list[dict],
    bidang_state: list[dict],
    alias_map: dict[str, str],
) -> tuple[list[dict], dict]:
    """
    Proses semua baris. Return (responden_list, summary).

    Efek samping:
    - skill_state, pencapaian_state, prodi_state, bidang_state, alias_map
      MUTABLE (ditambah entitas/alias baru).
    """
    responden: list[dict] = []
    resolutions_log: list[dict] = []
    skipped = 0
    errors: list[str] = []

    for i, row in enumerate(rows, start=1):
        try:
            rec = ingest_row(
                row, skill_state, pencapaian_state, prodi_state, bidang_state,
                alias_map, resolutions_log,
            )
            responden.append(rec)
        except Exception as e:
            skipped += 1
            msg = f"baris {i}: {e}"
            errors.append(msg)
            print(f"[ingest] dilewati — {msg}")

    # turunkan skill gap setelah semua baris masuk
    derive_skill_gap(responden, threshold=0.5, min_responden=5)

    # laporan normalisasi
    report = normalizer.build_normalization_report(resolutions_log)

    summary = {
        "jumlah_baris": len(rows),
        "jumlah_diproses": len(responden),
        "jumlah_dilewati": skipped,
        "errors": errors[:20],                       # batasi 20 untuk ringkas
        "skill_gap_dihitung": sum(1 for r in responden if r.get("skill_gap")),
        "normalisasi": {
            "total_resolusi": report["total"],
            "baru": report["baru"],
            "alias": report["alias"],
            "exact": report["exact"],
            "fuzzy": report["fuzzy"],
            "kosong": report["kosong"],
            "detail_baru": report["detail_baru"][:20],
            "detail_fuzzy": report["detail_fuzzy"][:20],
        },
        "total_skill_master": len(skill_state),
        "total_pencapaian_master": len(pencapaian_state),
        "total_prodi_master": len(prodi_state),
        "total_bidang_master": len(bidang_state),
        "total_alias": len(alias_map),
    }
    return responden, summary


def ingest_excel(
    file_bytes: bytes,
    skill_state: list[dict],
    pencapaian_state: list[dict],
    prodi_state: list[dict],
    bidang_state: list[dict],
    alias_map: dict[str, str],
) -> tuple[list[dict], dict]:
    """Entry point: bytes Excel → (responden, summary)."""
    df = pd.read_excel(io.BytesIO(file_bytes))
    rows = df.to_dict(orient="records")
    return ingest_sheet(rows, skill_state, pencapaian_state, prodi_state, bidang_state, alias_map)