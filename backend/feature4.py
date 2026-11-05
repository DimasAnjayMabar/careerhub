"""
feature4.py
Service untuk fitur "Career Navigation System".

Dua tab:
1. Career Explorer (read-only)  → browse skill per bidang, dari state.
2. Career Matcher (interaktif) → user pilih skill, sistem hitung skor.

⚠️ Catatan LOG:
LOG eksplorasi (anonim) TIDAK berasal dari GForm. Disimpan di memori
modul ini (`_LOG`, `_LOG_SKILL`) agar sederhana untuk tool lokal.
Kalau nanti perlu persist, tambahkan log_storage.json terpisah
(JANGAN campur dengan data_storage.json — lifecycle berbeda).
"""

from collections import Counter
from datetime import datetime

# =========================================================
# STATE LOG (di memori)
# =========================================================

_LOG: list[dict] = []          # {log_id, bidang_hasil_top1_id, skor_kecocokan_top1, created_at}
_LOG_SKILL: list[dict] = []    # {log_id, skill_id}
_LOG_NEXT_ID = 1


# =========================================================
# HELPER INTERNAL
# =========================================================

def _skill_map(skill_state):
    return {s["skill_id"]: s for s in skill_state}


def _bidang_map(bidang_state):
    return {b["bidang_id"]: b["nama_bidang"] for b in bidang_state}


def _freq_skill_per_bidang(responden, bidang_id):
    """Frekuensi skill yang dibutuhkan di bidang tertentu."""
    counter = Counter()
    for r in responden:
        if r["bidang_id"] == bidang_id:
            for sid in r.get("skill_dibutuhkan_hard", []) + r.get("skill_dibutuhkan_soft", []):
                counter[sid] += 1
    return counter


# =========================================================
# TAB 1 — CAREER EXPLORER (read-only)
# =========================================================

def get_card_bidang(
    nama_bidang,
    responden,
    skill_state,
    pencapaian_state,
    bidang_state,
):
    """
    Kartu ringkas untuk 1 bidang: top hard, top soft, sertifikasi.
    Reuse logika feature1 (tapi tanpa import feature1 agar modul tetap mandiri).
    """
    # cari bidang_id
    bid_id = None
    for b in bidang_state:
        if b["nama_bidang"] == nama_bidang:
            bid_id = b["bidang_id"]
            break

    if bid_id is None:
        return {"nama_bidang": nama_bidang, "hard": [], "soft": [], "sertifikasi": []}

    smap = _skill_map(skill_state)
    pmap = {p["pencapaian_id"]: p for p in pencapaian_state}

    hard_counter = Counter()
    soft_counter = Counter()
    sert_counter = Counter()

    for r in responden:
        if r["bidang_id"] != bid_id:
            continue
        for sid in r.get("skill_dibutuhkan_hard", []):
            s = smap.get(sid)
            if s and s["jenis_skill"] == "hard":
                hard_counter[s["nama_skill"]] += 1
        for sid in r.get("skill_dibutuhkan_soft", []):
            s = smap.get(sid)
            if s and s["jenis_skill"] == "soft":
                soft_counter[s["nama_skill"]] += 1
        for pid in r.get("pencapaian_sertifikasi", []):
            p = pmap.get(pid)
            if p and p["jenis"] == "sertifikasi":
                sert_counter[p["nama_pencapaian"]] += 1

    return {
        "nama_bidang": nama_bidang,
        "hard": [{"skill": k, "jumlah": v} for k, v in hard_counter.most_common(5)],
        "soft": [{"skill": k, "jumlah": v} for k, v in soft_counter.most_common(5)],
        "sertifikasi": [{"sertifikasi": k, "jumlah": v} for k, v in sert_counter.most_common(3)],
    }


def browse_bidang(responden, skill_state, pencapaian_state, bidang_state):
    """Semua kartu bidang (untuk render awal tab Explorer)."""
    return {
        "bidang": [b["nama_bidang"] for b in bidang_state],
        "cards": [
            get_card_bidang(b["nama_bidang"], responden, skill_state, pencapaian_state, bidang_state)
            for b in bidang_state
        ],
    }


# =========================================================
# TAB 2 — CAREER MATCHER
# =========================================================

def weighted_overlap_score(user_skills, responden, skill_state, bidang_id):
    """
    Hitung skor kecocokan user vs bidang.

    Bobot:
    - hard skill = 0.7, soft skill = 0.3
    - bobot per skill = (freq / max_freq) * bobot_jenis
    - skor = matched_bobot / total_bobot

    Return:
    {
        "skor": float (0..1),
        "match": [{skill_id, nama_skill, jenis}, ...],
        "gap":   [{skill_id, nama_skill, jenis}, ...],
        "total_bobot": float,
    }
    """
    smap = _skill_map(skill_state)
    freq = _freq_skill_per_bidang(responden, bidang_id)

    if not freq:
        return {"skor": 0.0, "match": [], "gap": [], "total_bobot": 0.0}

    max_freq = max(freq.values())
    total_bobot = 0.0
    matched_bobot = 0.0
    match = []
    gap = []

    for sid, f in freq.items():
        s = smap.get(sid)
        if not s:
            continue
        bobot_jenis = 0.7 if s["jenis_skill"] == "hard" else 0.3
        bobot_skill = (f / max_freq) * bobot_jenis
        total_bobot += bobot_skill

        if sid in user_skills:
            matched_bobot += bobot_skill
            match.append({"skill_id": sid, "nama_skill": s["nama_skill"], "jenis": s["jenis_skill"]})
        else:
            gap.append({"skill_id": sid, "nama_skill": s["nama_skill"], "jenis": s["jenis_skill"]})

    skor = matched_bobot / total_bobot if total_bobot > 0 else 0.0
    # urutkan: hard dulu, lalu soft
    match.sort(key=lambda x: x["jenis"])
    gap.sort(key=lambda x: x["jenis"])

    return {
        "skor": round(skor, 4),
        "match": match,
        "gap": gap,
        "total_bobot": round(total_bobot, 4),
    }


def recommend_bidang(
    user_skills,
    responden,
    skill_state,
    pencapaian_state,
    bidang_state,
    top_n=5,
):
    """
    Rekomendasi top N bidang untuk user_skills (set of skill_id).

    Return list:
    [
        {
            "bidang_id": int,
            "nama_bidang": str,
            "skor": float,
            "match": [...],
            "gap": [...],
        },
        ...
    ]
    """
    hasil = []
    for b in bidang_state:
        res = weighted_overlap_score(user_skills, responden, skill_state, b["bidang_id"])
        hasil.append({
            "bidang_id": b["bidang_id"],
            "nama_bidang": b["nama_bidang"],
            "skor": res["skor"],
            "match": res["match"],
            "gap": res["gap"],
        })
    hasil.sort(key=lambda x: x["skor"], reverse=True)
    return hasil[:top_n]


# =========================================================
# LOG EKSPLORASI
# =========================================================

def catat_log_eksplorasi(bidang_top1_id, skor, skill_ids):
    """Catat eksplorasi anonim ke memori. Return log_id."""
    global _LOG_NEXT_ID
    log_id = _LOG_NEXT_ID
    _LOG_NEXT_ID += 1

    _LOG.append({
        "log_id": log_id,
        "bidang_hasil_top1_id": bidang_top1_id,
        "skor_kecocokan_top1": round(float(skor), 4),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    for sid in skill_ids:
        _LOG_SKILL.append({"log_id": log_id, "skill_id": sid})

    return log_id


def insight_skill_paling_dicari(skill_state, top_n=10):
    """Skill yang paling sering dipilih user di Career Matcher (dari log)."""
    smap = _skill_map(skill_state)
    counter = Counter()
    for row in _LOG_SKILL:
        s = smap.get(row["skill_id"])
        if s:
            counter[s["nama_skill"]] += 1
    return [{"skill": k, "jumlah": v} for k, v in counter.most_common(top_n)]


# =========================================================
# ENTRY POINT UNTUK SSE
# =========================================================

def get_all(responden, skill_state, pencapaian_state, prodi_state, bidang_state):
    """
    Snapshot awal feature4 (tanpa input user) untuk SSE `init` / `feature4-update`.

    ⚠️ `meta` TIDAK diisi di sini — diisi oleh main.py (meta_block).
    """
    hard_skills = [
        {"skill_id": s["skill_id"], "nama_skill": s["nama_skill"]}
        for s in skill_state
        if s["jenis_skill"] == "hard" and s.get("status") == "approved"
    ]
    soft_skills = [
        {"skill_id": s["skill_id"], "nama_skill": s["nama_skill"]}
        for s in skill_state
        if s["jenis_skill"] == "soft" and s.get("status") == "approved"
    ]

    return {
        "explorer": browse_bidang(responden, skill_state, pencapaian_state, bidang_state),
        "skill_options": {"hard": hard_skills, "soft": soft_skills},
        "insight": insight_skill_paling_dicari(skill_state),
    }


# =========================================================
# ENTRY POINT UNTUK REST (matcher)
# =========================================================

def match_skills(
    user_skill_ids,
    responden,
    skill_state,
    pencapaian_state,
    bidang_state,
    top_n=5,
):
    """
    Dipanggil dari POST /feature4/match.
    user_skill_ids: list[int] atau set[int]
    """
    user_skills = set(user_skill_ids)
    if not user_skills:
        return {
            "ok": False,
            "error": "Pilih minimal 1 skill.",
            "hasil": [],
        }

    hasil = recommend_bidang(
        user_skills, responden, skill_state, pencapaian_state, bidang_state, top_n
    )

    log_id = None
    if hasil:
        top1 = hasil[0]
        log_id = catat_log_eksplorasi(top1["bidang_id"], top1["skor"], list(user_skills))

    return {
        "ok": True,
        "hasil": hasil,
        "insight": insight_skill_paling_dicari(skill_state),
        "log_id": log_id,
        "meta": {
            "jumlah_user_skill": len(user_skills),
            "catatan": (
                "Rekomendasi ini adalah agregasi pola alumni, bukan prediksi "
                "personal atau hasil AI. Gunakan sebagai bahan eksplorasi awal."
            ),
        },
    }