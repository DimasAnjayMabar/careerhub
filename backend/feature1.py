"""
feature1.py
Service agregasi untuk fitur "Peta Kompetensi Dunia Kerja".

Modul ini TIDAK menyimpan state sendiri dan TIDAK merender apa pun.
Semua fungsi menerima state (responden, skill, pencapaian, prodi, bidang)
dari main.py, lalu mengembalikan struktur dict yang siap dikirim via SSE
atau dibaca endpoint REST fallback.

Schema responden (denormalized, tanpa responden_id):
{
    "angkatan": int,
    "prodi_id": int,
    "bidang_id": int,
    "waktu_kerja_pertama_bulan": int,
    "status_kesesuaian": "sesuai" | "sebagian sesuai" | "tidak sesuai",
    "saran_mahasiswa": str,
    "skill_dibutuhkan_hard": [skill_id, ...],
    "skill_dibutuhkan_soft": [skill_id, ...],
    "pencapaian_sertifikasi": [pencapaian_id, ...],
    "pencapaian_kompetisi":   [pencapaian_id, ...],
    "pencapaian_proyek":      [pencapaian_id, ...],
}
"""

from collections import Counter, defaultdict


# =========================================================
# HELPER INTERNAL
# =========================================================

def _skill_map(skill_state: list[dict]) -> dict[int, dict]:
    return {s["skill_id"]: s for s in skill_state}


def _pencapaian_map(pencapaian_state: list[dict]) -> dict[int, dict]:
    return {p["pencapaian_id"]: p for p in pencapaian_state}


def _prodi_map(prodi_state: list[dict]) -> dict[int, str]:
    return {p["prodi_id"]: p["nama_prodi"] for p in prodi_state}


def _bidang_map(bidang_state: list[dict]) -> dict[int, str]:
    return {b["bidang_id"]: b["nama_bidang"] for b in bidang_state}


# =========================================================
# AGREGASI PER BIDANG
# =========================================================

def top_hard_skills_per_bidang(
    responden: list[dict],
    skill_state: list[dict],
    bidang_state: list[dict],
    top_n: int = 5,
) -> dict[str, list[dict]]:
    """Top N hard skill yang dibutuhkan, per bidang pekerjaan."""
    skill_map = _skill_map(skill_state)
    result: dict[str, list[dict]] = {}

    for b in bidang_state:
        counter: Counter[str] = Counter()
        for r in responden:
            if r["bidang_id"] != b["bidang_id"]:
                continue
            for sid in r.get("skill_dibutuhkan_hard", []):
                s = skill_map.get(sid)
                if s and s["jenis_skill"] == "hard":
                    counter[s["nama_skill"]] += 1
        result[b["nama_bidang"]] = [
            {"skill": nama, "jumlah": jml} for nama, jml in counter.most_common(top_n)
        ]

    return result


def top_soft_skills_per_bidang(
    responden: list[dict],
    skill_state: list[dict],
    bidang_state: list[dict],
    top_n: int = 5,
) -> dict[str, list[dict]]:
    """Top N soft skill yang dibutuhkan, per bidang pekerjaan."""
    skill_map = _skill_map(skill_state)
    result: dict[str, list[dict]] = {}

    for b in bidang_state:
        counter: Counter[str] = Counter()
        for r in responden:
            if r["bidang_id"] != b["bidang_id"]:
                continue
            for sid in r.get("skill_dibutuhkan_soft", []):
                s = skill_map.get(sid)
                if s and s["jenis_skill"] == "soft":
                    counter[s["nama_skill"]] += 1
        result[b["nama_bidang"]] = [
            {"skill": nama, "jumlah": jml} for nama, jml in counter.most_common(top_n)
        ]

    return result


def sertifikasi_per_bidang(
    responden: list[dict],
    pencapaian_state: list[dict],
    bidang_state: list[dict],
    top_n: int = 3,
) -> dict[str, list[dict]]:
    """Top N sertifikasi paling sering dimiliki alumni, per bidang."""
    p_map = _pencapaian_map(pencapaian_state)
    result: dict[str, list[dict]] = {}

    for b in bidang_state:
        counter: Counter[str] = Counter()
        for r in responden:
            if r["bidang_id"] != b["bidang_id"]:
                continue
            for pid in r.get("pencapaian_sertifikasi", []):
                p = p_map.get(pid)
                if p and p["jenis"] == "sertifikasi":
                    counter[p["nama_pencapaian"]] += 1
        result[b["nama_bidang"]] = [
            {"sertifikasi": nama, "jumlah": jml} for nama, jml in counter.most_common(top_n)
        ]

    return result


def matriks_prodi_bidang(
    responden: list[dict],
    prodi_state: list[dict],
    bidang_state: list[dict],
) -> dict[str, dict[str, int]]:
    """Matriks jumlah alumni: Prodi (baris) × Bidang (kolom)."""
    prodi_map = _prodi_map(prodi_state)
    bidang_map = _bidang_map(bidang_state)

    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in responden:
        nama_prodi = prodi_map.get(r["prodi_id"], "Tidak diketahui")
        nama_bidang = bidang_map.get(r["bidang_id"], "Tidak diketahui")
        matrix[nama_prodi][nama_bidang] += 1

    return {p: dict(row) for p, row in matrix.items()}


# =========================================================
# ENTRY POINT UNTUK SSE / REST
# =========================================================

def get_all(
    responden: list[dict],
    skill_state: list[dict],
    pencapaian_state: list[dict],
    prodi_state: list[dict],
    bidang_state: list[dict],
    top_n: int = 5,
) -> dict:
    """
    Payload feature1 untuk SSE `init` / `feature1-update` dan REST fallback.

    ⚠️ `meta` TIDAK diisi di sini — diisi oleh main.py (meta_block).
    """
    return {
        "hard":   top_hard_skills_per_bidang(responden, skill_state, bidang_state, top_n),
        "soft":   top_soft_skills_per_bidang(responden, skill_state, bidang_state, top_n),
        "sert":   sertifikasi_per_bidang(responden, pencapaian_state, bidang_state, 3),
        "matrix": matriks_prodi_bidang(responden, prodi_state, bidang_state),
    }