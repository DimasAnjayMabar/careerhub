"""
feature2.py
Service agregasi untuk fitur "Analisis Skill Gap".

⚠️ PENTING — Semantik "gap":
GForm TIDAK menanyakan "skill apa yang dirasa kurang".
skill_gap DITURUNKAN OTOMATIS saat ingestion (lihat upload.py):

    gap_R = skill_dominan_bidang(R) − skill_yang_disebut_R(R)

dengan skill_dominan_bidang = skill yang disebut ≥ 50% responden
di bidang yang sama (minimal 5 responden per bidang).

Jadi "gap" di sini = "skill yang dibutuhkan mayoritas alumni bidang,
tapi TIDAK DISEBUT oleh responden ini" — BUKAN self-assessment.
Label FE harus mencerminkan ini (mis. "Skill Absen", bukan "Dirasa Kurang").

Schema responden:
{
    "angkatan": int,
    "prodi_id": int,
    "bidang_id": int,
    "waktu_kerja_pertama_bulan": int,
    "status_kesesuaian": str,
    "saran_mahasiswa": str,
    "skill_dibutuhkan_hard": [skill_id, ...],
    "skill_dibutuhkan_soft": [skill_id, ...],
    "skill_gap":             [skill_id, ...],   # derived
    "pencapaian_sertifikasi": [...],
    "pencapaian_kompetisi":   [...],
    "pencapaian_proyek":      [...],
}
"""

from collections import Counter, defaultdict


# =========================================================
# HELPER INTERNAL
# =========================================================

def _skill_map(skill_state: list[dict]) -> dict[int, dict]:
    return {s["skill_id"]: s for s in skill_state}


def _semua_skill_disebut(r: dict) -> list[int]:
    """Gabungan hard + soft yang disebut responden."""
    return list(r.get("skill_dibutuhkan_hard", [])) + list(r.get("skill_dibutuhkan_soft", []))


# =========================================================
# AGREGASI
# =========================================================

def ranking_skill_gap(
    responden: list[dict],
    skill_state: list[dict],
    top_n: int = 10,
) -> list[dict]:
    """Skill yang paling sering absen dari jawaban alumni (inferred gap)."""
    skill_map = _skill_map(skill_state)
    counter: Counter[str] = Counter()

    for r in responden:
        for sid in r.get("skill_gap", []):
            s = skill_map.get(sid)
            if s:
                counter[s["nama_skill"]] += 1

    return [{"skill": k, "jumlah": v} for k, v in counter.most_common(top_n)]


def gap_view_dibutuhkan_vs_kurang(
    responden: list[dict],
    skill_state: list[dict],
    top_n: int = 8,
) -> list[dict]:
    """
    Bandingkan frekuensi 'dibutuhkan' vs 'absen' per skill.

    Key output sengaja dipertahankan: 'dibutuhkan' & 'dirasa_kurang'
    (agar FE lama tetap kompatibel), tapi label FE WAJIB diubah
    menjadi 'Dibutuhkan' vs 'Tidak Disebut'.
    """
    skill_map = _skill_map(skill_state)
    dibutuhkan: Counter[str] = Counter()
    absen: Counter[str] = Counter()

    for r in responden:
        for sid in _semua_skill_disebut(r):
            s = skill_map.get(sid)
            if s:
                dibutuhkan[s["nama_skill"]] += 1
        for sid in r.get("skill_gap", []):
            s = skill_map.get(sid)
            if s:
                absen[s["nama_skill"]] += 1

    all_skills = set(dibutuhkan) | set(absen)
    rows = [
        {
            "skill": s,
            "dibutuhkan": dibutuhkan.get(s, 0),
            "dirasa_kurang": absen.get(s, 0),   # nama key dipertahankan demi kompatibilitas
        }
        for s in all_skills
    ]
    rows.sort(key=lambda x: x["dirasa_kurang"], reverse=True)
    return rows[:top_n]


def tren_gap_antar_angkatan(
    responden: list[dict],
    skill_state: list[dict],
    top_n: int = 5,
) -> dict[int, list[dict]]:
    """Top N skill absen per angkatan (untuk line chart antar tahun)."""
    skill_map = _skill_map(skill_state)
    per_angkatan: dict[int, Counter[str]] = defaultdict(Counter)

    for r in responden:
        ang = r["angkatan"]
        for sid in r.get("skill_gap", []):
            s = skill_map.get(sid)
            if s:
                per_angkatan[ang][s["nama_skill"]] += 1

    # urutkan angkatan menaik (2020 → 2022) untuk line chart
    return {
        ang: [{"skill": k, "jumlah": v} for k, v in counter.most_common(top_n)]
        for ang, counter in sorted(per_angkatan.items())
    }


def waktu_tunggu_vs_gap(responden: list[dict]) -> list[dict]:
    """Data titik: waktu tunggu (bulan) vs jumlah skill absen per responden."""
    rows = []
    for r in responden:
        rows.append({
            "angkatan": r["angkatan"],
            "waktu_bulan": r["waktu_kerja_pertama_bulan"],
            "jumlah_gap": len(r.get("skill_gap", [])),
        })
    return rows


# =========================================================
# ENTRY POINT UNTUK SSE / REST
# =========================================================

def get_all(
    responden: list[dict],
    skill_state: list[dict],
    pencapaian_state: list[dict],
    prodi_state: list[dict],
    bidang_state: list[dict],
    top_n: int = 10,
) -> dict:
    from main import meta_block
    """
    Payload lengkap feature2 untuk SSE `init` dan `feature2-update`.

    Struktur:
    {
        "ranking_gap":           [{skill, jumlah}, ...],
        "dibutuhkan_vs_kurang":  [{skill, dibutuhkan, dirasa_kurang}, ...],
        "tren_antar_angkatan":   {2020: [{skill, jumlah}, ...], ...},
        "waktu_tunggu_vs_gap":   [{angkatan, waktu_bulan, jumlah_gap}, ...],
        "meta": {
            "jumlah_responden": int,
            "ada_data_gap": bool,
            "catatan": str,       # ⚠️ caption warning untuk FE
        },
    }
    """
    return {
        "ranking_gap":          ranking_skill_gap(responden, skill_state, top_n),
        "dibutuhkan_vs_kurang": gap_view_dibutuhkan_vs_kurang(responden, skill_state, 8),
        "tren_antar_angkatan":  tren_gap_antar_angkatan(responden, skill_state, 5),
        "waktu_tunggu_vs_gap":  waktu_tunggu_vs_gap(responden),
        "meta": meta_block(len(responden), extra={
            "ada_data_gap": any(r.get("skill_gap") for r in responden),
            "catatan": (
                "'Gap' di sini adalah INFERENSI: skill yang dibutuhkan "
                "mayoritas alumni di bidang yang sama, tapi tidak disebut "
                "oleh responden. Bukan self-assessment."
            )
        })
    }