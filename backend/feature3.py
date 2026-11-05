"""
feature3.py
Service agregasi untuk fitur "Dashboard Tracer Study".

Berbeda dengan feature1 & feature2, feature3 punya FILTER GLOBAL
(angkatan + bidang). Karena itu, modul ini mengekspos:

1. get_filter_options()      → opsi dropdown filter
2. get_dashboard(...)        → KPI + chart, menerima filter
3. get_all(...)              → snapshot awal untuk SSE (tanpa filter)

REST endpoint di main.py:
    GET /feature3/filters     → get_filter_options()
    GET /feature3/data?angkatan=&bidang_id=  → get_dashboard(...)
"""

from collections import Counter, defaultdict


# =========================================================
# HELPER INTERNAL
# =========================================================

def _prodi_map(prodi_state):
    return {p["prodi_id"]: p["nama_prodi"] for p in prodi_state}


def _bidang_map(bidang_state):
    return {b["bidang_id"]: b["nama_bidang"] for b in bidang_state}


def _filter(responden, angkatan=None, bidang_id=None):
    """Filter responden berdasarkan angkatan & bidang (opsional)."""
    res = responden
    if angkatan is not None:
        res = [r for r in res if r["angkatan"] == angkatan]
    if bidang_id is not None:
        res = [r for r in res if r["bidang_id"] == bidang_id]
    return res


# =========================================================
# OPSI FILTER (untuk dropdown FE)
# =========================================================

def get_filter_options(responden, bidang_state):
    """
    Opsi untuk dropdown filter global.

    Return:
    {
        "angkatan": [2022, 2021, 2020, 2019],   # descending
        "bidang":   [{"bidang_id": 1, "nama_bidang": "..."}, ...],
    }
    """
    angkatan_list = sorted({r["angkatan"] for r in responden}, reverse=True)
    return {
        "angkatan": angkatan_list,
        "bidang": [{"bidang_id": b["bidang_id"], "nama_bidang": b["nama_bidang"]}
                   for b in bidang_state],
    }


# =========================================================
# KPI SUMMARY (terpengaruh filter)
# =========================================================

def kpi_summary(responden, angkatan=None, bidang_id=None):
    """
    KPI ringkasan untuk dashboard.

    Return:
    {
        "total_responden": int,
        "avg_waktu_tunggu_bulan": float,
        "persen_sesuai": float,
        "persen_sebagian": float,
        "persen_tidak": float,
        "jumlah_prodi": int,
        "jumlah_bidang": int,
    }
    """
    data = _filter(responden, angkatan, bidang_id)
    total = len(data)

    if total == 0:
        return {
            "total_responden": 0,
            "avg_waktu_tunggu_bulan": 0,
            "persen_sesuai": 0,
            "persen_sebagian": 0,
            "persen_tidak": 0,
            "jumlah_prodi": 0,
            "jumlah_bidang": 0,
        }

    avg_waktu = sum(r["waktu_kerja_pertama_bulan"] for r in data) / total
    sesuai = sum(1 for r in data if r["status_kesesuaian"] == "sesuai")
    sebagian = sum(1 for r in data if r["status_kesesuaian"] == "sebagian sesuai")
    tidak = sum(1 for r in data if r["status_kesesuaian"] == "tidak sesuai")

    return {
        "total_responden": total,
        "avg_waktu_tunggu_bulan": round(avg_waktu, 2),
        "persen_sesuai": round(sesuai / total * 100, 1),
        "persen_sebagian": round(sebagian / total * 100, 1),
        "persen_tidak": round(tidak / total * 100, 1),
        "jumlah_prodi": len({r["prodi_id"] for r in data}),
        "jumlah_bidang": len({r["bidang_id"] for r in data}),
    }


# =========================================================
# CHART DATA (terpengaruh filter)
# =========================================================

def distribusi_bidang(responden, bidang_state, angkatan=None, bidang_id=None):
    """Jumlah alumni per bidang pekerjaan (terfilter)."""
    data = _filter(responden, angkatan, bidang_id)
    b_map = _bidang_map(bidang_state)
    c = Counter(b_map.get(r["bidang_id"], "Tidak diketahui") for r in data)
    return [{"bidang": k, "jumlah": v} for k, v in c.most_common()]


def distribusi_waktu_tunggu(responden, angkatan=None, bidang_id=None):
    """
    Distribusi waktu tunggu dalam 4 bin:
    0-1, 2-3, 4-6, >6 bulan.
    """
    data = _filter(responden, angkatan, bidang_id)
    bins = {"0-1 bulan": 0, "2-3 bulan": 0, "4-6 bulan": 0, ">6 bulan": 0}

    for r in data:
        w = r["waktu_kerja_pertama_bulan"]
        if w <= 1:
            bins["0-1 bulan"] += 1
        elif w <= 3:
            bins["2-3 bulan"] += 1
        elif w <= 6:
            bins["4-6 bulan"] += 1
        else:
            bins[">6 bulan"] += 1

    return [{"range": k, "jumlah": v} for k, v in bins.items()]


def kesesuaian_vs_prodi(responden, prodi_state, angkatan=None, bidang_id=None):
    """
    Tabel silang: Prodi × Status Kesesuaian (terfilter).
    Output: [{prodi, sesuai, sebagian sesuai, tidak sesuai}, ...]
    """
    data = _filter(responden, angkatan, bidang_id)
    p_map = _prodi_map(prodi_state)

    agg = defaultdict(lambda: {"sesuai": 0, "sebagian sesuai": 0, "tidak sesuai": 0})
    for r in data:
        prodi = p_map.get(r["prodi_id"], "Tidak diketahui")
        status = r["status_kesesuaian"]
        if status in agg[prodi]:
            agg[prodi][status] += 1

    return [{"prodi": k, **v} for k, v in agg.items()]


# =========================================================
# ENTRY POINT UNTUK SSE
# =========================================================

def get_all(
    responden,
    skill_state,
    pencapaian_state,
    prodi_state,
    bidang_state,
):
    from main import meta_block
    """
    Snapshot awal feature3 (tanpa filter) untuk SSE `init` / `feature3-update`.

    FE akan:
    1. Pakai ini untuk render pertama (filter = Semua).
    2. Saat user ganti filter, panggil GET /feature3/data?angkatan=&bidang_id=
       untuk re-query (bukan lewat SSE).

    Struktur:
    {
        "filters": { "angkatan": [...], "bidang": [...] },
        "kpi": {...},
        "distribusi_bidang": [...],
        "distribusi_waktu": [...],
        "kesesuaian_prodi": [...],
        "meta": { "jumlah_responden": int },
    }
    """
    return {
        "filters": get_filter_options(responden, bidang_state),
        "kpi": kpi_summary(responden),                       # tanpa filter
        "distribusi_bidang": distribusi_bidang(responden, bidang_state),
        "distribusi_waktu": distribusi_waktu_tunggu(responden),
        "kesesuaian_prodi": kesesuaian_vs_prodi(responden, prodi_state),
        "meta": meta_block(len(responden)),
    }


def get_dashboard(
    responden,
    skill_state,
    pencapaian_state,
    prodi_state,
    bidang_state,
    angkatan=None,
    bidang_id=None,
):
    """
    Data dashboard dengan filter (dipanggil dari REST endpoint).
    Return struktur SAMA dengan get_all() kecuali `filters`
    (supaya FE bisa re-render tanpa mengganti dropdown).
    """
    return {
        "kpi": kpi_summary(responden, angkatan, bidang_id),
        "distribusi_bidang": distribusi_bidang(responden, bidang_state, angkatan, bidang_id),
        "distribusi_waktu": distribusi_waktu_tunggu(responden, angkatan, bidang_id),
        "kesesuaian_prodi": kesesuaian_vs_prodi(responden, prodi_state, angkatan, bidang_id),
        "meta": {
            "jumlah_responden": len(_filter(responden, angkatan, bidang_id)),
            "filter": {"angkatan": angkatan, "bidang_id": bidang_id},
        },
    }