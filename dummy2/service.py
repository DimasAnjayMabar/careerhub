"""
service.py
In-memory dummy DB mengikuti schema:
Prodi, BidangPekerjaan, Skill, Pencapaian, Responden,
Responden_Skill_Dibutuhkan, Responden_Skill_Gap,
Responden_Pencapaian, LogEksplorasiMahasiswa, LogEksplorasi_Skill
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict, Counter

# =========================================================
# "TABEL" DUMMY
# =========================================================

PRODI = [
    {"prodi_id": 1, "nama_prodi": "Informatika"},
    {"prodi_id": 2, "nama_prodi": "Sistem Informasi"},
    {"prodi_id": 3, "nama_prodi": "Manajemen Bisnis"},
    {"prodi_id": 4, "nama_prodi": "Akuntansi"},
    {"prodi_id": 5, "nama_prodi": "Desain Komunikasi Visual"},
]

BIDANG_PEKERJAAN = [
    {"bidang_id": 1, "nama_bidang": "Software Engineering"},
    {"bidang_id": 2, "nama_bidang": "Data & Analytics"},
    {"bidang_id": 3, "nama_bidang": "Digital Marketing"},
    {"bidang_id": 4, "nama_bidang": "Finance & Accounting"},
    {"bidang_id": 5, "nama_bidang": "UI/UX & Product Design"},
]

# skill_id, nama_skill, jenis_skill, status
SKILL = [
    # HARD
    {"skill_id": 1,  "nama_skill": "Python",                    "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 2,  "nama_skill": "SQL",                       "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 3,  "nama_skill": "JavaScript",                "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 4,  "nama_skill": "Git & Version Control",     "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 5,  "nama_skill": "Data Visualization",        "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 6,  "nama_skill": "Machine Learning",          "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 7,  "nama_skill": "SEO/SEM",                   "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 8,  "nama_skill": "Copywriting",               "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 9,  "nama_skill": "Financial Modeling",        "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 10, "nama_skill": "Excel Advanced",            "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 11, "nama_skill": "Figma",                     "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 12, "nama_skill": "User Research",             "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 13, "nama_skill": "REST API",                  "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 14, "nama_skill": "Cloud (AWS/GCP)",           "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 15, "nama_skill": "Docker",                    "jenis_skill": "hard", "status": "approved"},
    {"skill_id": 16, "nama_skill": "Power BI",                  "jenis_skill": "hard", "status": "approved"},

    # SOFT
    {"skill_id": 51, "nama_skill": "Komunikasi",                "jenis_skill": "soft", "status": "approved"},
    {"skill_id": 52, "nama_skill": "Kerja Tim",                 "jenis_skill": "soft", "status": "approved"},
    {"skill_id": 53, "nama_skill": "Problem Solving",           "jenis_skill": "soft", "status": "approved"},
    {"skill_id": 54, "nama_skill": "Manajemen Waktu",           "jenis_skill": "soft", "status": "approved"},
    {"skill_id": 55, "nama_skill": "Adaptif & Cepat Belajar",   "jenis_skill": "soft", "status": "approved"},
    {"skill_id": 56, "nama_skill": "Kepemimpinan",              "jenis_skill": "soft", "status": "approved"},
    {"skill_id": 57, "nama_skill": "Berpikir Kritis",           "jenis_skill": "soft", "status": "approved"},
    {"skill_id": 58, "nama_skill": "Negosiasi",                 "jenis_skill": "soft", "status": "approved"},

    # pending (dari fitur "tambah lainnya")
    {"skill_id": 91, "nama_skill": "Prompt Engineering",        "jenis_skill": "hard", "status": "pending"},
]

PENCAPAIAN = [
    {"pencapaian_id": 1, "nama_pencapaian": "AWS Certified Cloud Practitioner", "jenis": "sertifikasi"},
    {"pencapaian_id": 2, "nama_pencapaian": "Google Analytics Certificate",     "jenis": "sertifikasi"},
    {"pencapaian_id": 3, "nama_pencapaian": "Microsoft Excel Expert",           "jenis": "sertifikasi"},
    {"pencapaian_id": 4, "nama_pencapaian": "Google UX Design Certificate",     "jenis": "sertifikasi"},
    {"pencapaian_id": 5, "nama_pencapaian": "Hackathon Nasional",               "jenis": "kompetisi"},
    {"pencapaian_id": 6, "nama_pencapaian": "PKM Dikti",                        "jenis": "kompetisi"},
    {"pencapaian_id": 7, "nama_pencapaian": "Capstone Project Industri",        "jenis": "proyek"},
]

# =========================================================
# RESPONDEN (dummy ± 40 record)
# =========================================================
# Struktur: responden_id, angkatan, prodi_id, bidang_id,
#           waktu_kerja_pertama_bulan, status_kesesuaian, saran_mahasiswa

RESPONDEN = [
    # --- Angkatan 2021 (Software Engineering dominant)
    {"responden_id": 1,  "angkatan": 2021, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 2, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Perbanyak latihan coding & project nyata."},
    {"responden_id": 2,  "angkatan": 2021, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Ikut magang sejak semester 5."},
    {"responden_id": 3,  "angkatan": 2021, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 1, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Kuasai Git & CI/CD."},
    {"responden_id": 4,  "angkatan": 2021, "prodi_id": 2, "bidang_id": 2, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Belajar SQL & Python lebih dalam."},
    {"responden_id": 5,  "angkatan": 2021, "prodi_id": 2, "bidang_id": 2, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Latih data storytelling."},
    {"responden_id": 6,  "angkatan": 2021, "prodi_id": 1, "bidang_id": 2, "waktu_kerja_pertama_bulan": 5, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Tambah portofolio dashboard."},
    {"responden_id": 7,  "angkatan": 2021, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 2, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Bangun personal branding."},
    {"responden_id": 8,  "angkatan": 2021, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Kuasai analytics & SEO."},
    {"responden_id": 9,  "angkatan": 2021, "prodi_id": 4, "bidang_id": 4, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Sertifikasi akuntansi membantu."},
    {"responden_id": 10, "angkatan": 2021, "prodi_id": 5, "bidang_id": 5, "waktu_kerja_pertama_bulan": 6, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Perbanyak portfolio UI/UX."},

    # --- Angkatan 2020
    {"responden_id": 11, "angkatan": 2020, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Fokus pada fundamental CS."},
    {"responden_id": 12, "angkatan": 2020, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 2, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Ikut open source."},
    {"responden_id": 13, "angkatan": 2020, "prodi_id": 2, "bidang_id": 2, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Kuasai statistik dasar."},
    {"responden_id": 14, "angkatan": 2020, "prodi_id": 2, "bidang_id": 1, "waktu_kerja_pertama_bulan": 6, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Belajar backend lebih dalam."},
    {"responden_id": 15, "angkatan": 2020, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Aktif di organisasi."},
    {"responden_id": 16, "angkatan": 2020, "prodi_id": 4, "bidang_id": 4, "waktu_kerja_pertama_bulan": 5, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Latih Excel & ERP."},
    {"responden_id": 17, "angkatan": 2020, "prodi_id": 5, "bidang_id": 5, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Buat case study sendiri."},
    {"responden_id": 18, "angkatan": 2020, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 1, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Bangun portofolio GitHub."},
    {"responden_id": 19, "angkatan": 2020, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 7, "status_kesesuaian": "tidak sesuai",   "saran_mahasiswa": "Pertimbangkan minat sejak awal."},
    {"responden_id": 20, "angkatan": 2020, "prodi_id": 4, "bidang_id": 4, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Perbanyak networking."},

    # --- Angkatan 2019
    {"responden_id": 21, "angkatan": 2019, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 2, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Ikut bootcamp tambahan."},
    {"responden_id": 22, "angkatan": 2019, "prodi_id": 1, "bidang_id": 2, "waktu_kerja_pertama_bulan": 5, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Pahami data pipeline."},
    {"responden_id": 23, "angkatan": 2019, "prodi_id": 2, "bidang_id": 2, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Latih komunikasi hasil analisis."},
    {"responden_id": 24, "angkatan": 2019, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Kuasai tools marketing."},
    {"responden_id": 25, "angkatan": 2019, "prodi_id": 4, "bidang_id": 4, "waktu_kerja_pertama_bulan": 6, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Ambil sertifikasi profesi."},
    {"responden_id": 26, "angkatan": 2019, "prodi_id": 5, "bidang_id": 5, "waktu_kerja_pertama_bulan": 5, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Bangun portofolio sejak kuliah."},
    {"responden_id": 27, "angkatan": 2019, "prodi_id": 2, "bidang_id": 1, "waktu_kerja_pertama_bulan": 7, "status_kesesuaian": "tidak sesuai",   "saran_mahasiswa": "Ikuti sertifikasi teknis."},
    {"responden_id": 28, "angkatan": 2019, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 2, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Fokus pada satu stack dulu."},
    {"responden_id": 29, "angkatan": 2019, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Latih public speaking."},
    {"responden_id": 30, "angkatan": 2019, "prodi_id": 4, "bidang_id": 4, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Biasakan analisis data."},

    # --- Angkatan 2022 (lulus 3.5 tahun, sudah kerja ≥6 bulan)
    {"responden_id": 31, "angkatan": 2022, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 2, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Ikut project-based learning."},
    {"responden_id": 32, "angkatan": 2022, "prodi_id": 1, "bidang_id": 1, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Kuasai Docker & cloud."},
    {"responden_id": 33, "angkatan": 2022, "prodi_id": 2, "bidang_id": 2, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Belajar Python & SQL."},
    {"responden_id": 34, "angkatan": 2022, "prodi_id": 2, "bidang_id": 2, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Latih visualisasi data."},
    {"responden_id": 35, "angkatan": 2022, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 2, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Bangun personal brand."},
    {"responden_id": 36, "angkatan": 2022, "prodi_id": 4, "bidang_id": 4, "waktu_kerja_pertama_bulan": 5, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Ambil sertifikasi Excel."},
    {"responden_id": 37, "angkatan": 2022, "prodi_id": 5, "bidang_id": 5, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Perbanyak riset pengguna."},
    {"responden_id": 38, "angkatan": 2022, "prodi_id": 1, "bidang_id": 2, "waktu_kerja_pertama_bulan": 6, "status_kesesuaian": "sebagian sesuai","saran_mahasiswa": "Perdalam ML & statistik."},
    {"responden_id": 39, "angkatan": 2022, "prodi_id": 3, "bidang_id": 3, "waktu_kerja_pertama_bulan": 3, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Kuasai copywriting & SEO."},
    {"responden_id": 40, "angkatan": 2022, "prodi_id": 4, "bidang_id": 4, "waktu_kerja_pertama_bulan": 4, "status_kesesuaian": "sesuai",         "saran_mahasiswa": "Latih analytical thinking."},
]

# =========================================================
# RESPONDEN_SKILL_DIBUTUHKAN (skill yang dibutuhkan di pekerjaan)
# =========================================================
def _mk_dibutuhkan():
    rows = []
    # Bidang 1 (SE): Python, SQL, Git, JavaScript, REST API, Docker, Cloud + soft
    for rid in [1,2,3,11,12,14,18,21,27,28,31,32]:
        for sid in [1,2,3,4,13,15,14,51,52,53,54,55]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # Bidang 2 (Data): Python, SQL, DataViz, ML, PowerBI + soft
    for rid in [4,5,6,13,22,23,33,34,38]:
        for sid in [1,2,5,6,16,51,52,53,57,54]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # Bidang 3 (Digital Marketing): SEO, Copywriting, DataViz, Excel + soft
    for rid in [7,8,15,19,24,29,35,39]:
        for sid in [7,8,5,10,51,52,53,58,55]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # Bidang 4 (Finance): Financial Modeling, Excel, PowerBI + soft
    for rid in [9,16,20,25,30,36,40]:
        for sid in [9,10,16,2,51,52,57,54]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # Bidang 5 (UI/UX): Figma, User Research, Copywriting + soft
    for rid in [10,17,26,37]:
        for sid in [11,12,8,51,52,53,55,57]:
            rows.append({"responden_id": rid, "skill_id": sid})
    return rows

RESPONDEN_SKILL_DIBUTUHKAN = _mk_dibutuhkan()

# =========================================================
# RESPONDEN_SKILL_GAP (skill yang dirasa KURANG saat awal kerja)
# =========================================================
def _mk_gap():
    rows = []
    # SE: gap di Docker, Cloud, Git (umum)
    for rid in [1,2,3,11,12,14,18,21,27,28,31,32]:
        for sid in [15,14,4,13]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # Data: gap di ML, PowerBI, SQL
    for rid in [4,5,6,13,22,23,33,34,38]:
        for sid in [6,16,2,5]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # Marketing: gap di SEO, DataViz
    for rid in [7,8,15,19,24,29,35,39]:
        for sid in [7,5,10]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # Finance: gap di Financial Modeling, PowerBI
    for rid in [9,16,20,25,30,36,40]:
        for sid in [9,16,10]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # UI/UX: gap di User Research, Figma
    for rid in [10,17,26,37]:
        for sid in [12,11,8]:
            rows.append({"responden_id": rid, "skill_id": sid})
    # soft gap umum: Negosiasi, Kepemimpinan
    for rid in range(1, 41):
        for sid in [58, 56]:
            rows.append({"responden_id": rid, "skill_id": sid})
    return rows

RESPONDEN_SKILL_GAP = _mk_gap()

# =========================================================
# RESPONDEN_PENCAPAIAN
# =========================================================
RESPONDEN_PENCAPAIAN = [
    {"responden_id": 1,  "pencapaian_id": 1},
    {"responden_id": 2,  "pencapaian_id": 5},
    {"responden_id": 3,  "pencapaian_id": 1},
    {"responden_id": 4,  "pencapaian_id": 2},
    {"responden_id": 5,  "pencapaian_id": 2},
    {"responden_id": 6,  "pencapaian_id": 7},
    {"responden_id": 7,  "pencapaian_id": 2},
    {"responden_id": 8,  "pencapaian_id": 2},
    {"responden_id": 9,  "pencapaian_id": 3},
    {"responden_id": 10, "pencapaian_id": 4},
    {"responden_id": 11, "pencapaian_id": 1},
    {"responden_id": 13, "pencapaian_id": 2},
    {"responden_id": 15, "pencapaian_id": 2},
    {"responden_id": 17, "pencapaian_id": 4},
    {"responden_id": 18, "pencapaian_id": 6},
    {"responden_id": 21, "pencapaian_id": 1},
    {"responden_id": 23, "pencapaian_id": 2},
    {"responden_id": 26, "pencapaian_id": 4},
    {"responden_id": 31, "pencapaian_id": 1},
    {"responden_id": 32, "pencapaian_id": 1},
    {"responden_id": 33, "pencapaian_id": 2},
    {"responden_id": 37, "pencapaian_id": 4},
    {"responden_id": 39, "pencapaian_id": 2},
]

# =========================================================
# LOG EKSPLORASI (Career Matcher) — dummy histori
# =========================================================
LOG_EKSPLORASI = [
    {"log_id": 1, "bidang_hasil_top1_id": 1, "skor_kecocokan_top1": 0.78, "created_at": "2025-01-10 10:00"},
    {"log_id": 2, "bidang_hasil_top1_id": 2, "skor_kecocokan_top1": 0.65, "created_at": "2025-01-11 14:20"},
    {"log_id": 3, "bidang_hasil_top1_id": 3, "skor_kecocokan_top1": 0.55, "created_at": "2025-01-12 09:15"},
]

LOG_EKSPLORASI_SKILL = [
    {"log_id": 1, "skill_id": 1},
    {"log_id": 1, "skill_id": 2},
    {"log_id": 1, "skill_id": 4},
    {"log_id": 2, "skill_id": 1},
    {"log_id": 2, "skill_id": 5},
    {"log_id": 3, "skill_id": 7},
    {"log_id": 3, "skill_id": 8},
]

# =========================================================
# HELPER / QUERY FUNCTIONS
# =========================================================

def get_prodi_map() -> Dict[int, str]:
    return {p["prodi_id"]: p["nama_prodi"] for p in PRODI}

def get_bidang_map() -> Dict[int, str]:
    return {b["bidang_id"]: b["nama_bidang"] for b in BIDANG_PEKERJAAN}

def get_skill_map() -> Dict[int, dict]:
    return {s["skill_id"]: s for s in SKILL}

def get_all_responden() -> List[dict]:
    return RESPONDEN

def get_responden_by_angkatan(angkatan: int) -> List[dict]:
    return [r for r in RESPONDEN if r["angkatan"] == angkatan]

def get_all_angkatan() -> List[int]:
    return sorted({r["angkatan"] for r in RESPONDEN}, reverse=True)

def get_all_bidang() -> List[dict]:
    return BIDANG_PEKERJAAN

def get_all_skill(jenis: Optional[str] = None, only_approved: bool = True) -> List[dict]:
    res = SKILL
    if only_approved:
        res = [s for s in res if s["status"] == "approved"]
    if jenis:
        res = [s for s in res if s["jenis_skill"] == jenis]
    return res

# ---------- Fitur 1: Peta Kompetensi ----------
def top_hard_skills_per_bidang(top_n: int = 5) -> Dict[str, List[dict]]:
    skill_map = get_skill_map()
    result = {}
    for b in BIDANG_PEKERJAAN:
        bid = b["bidang_id"]
        rid_in_bidang = {r["responden_id"] for r in RESPONDEN if r["bidang_id"] == bid}
        counter = Counter()
        for row in RESPONDEN_SKILL_DIBUTUHKAN:
            if row["responden_id"] in rid_in_bidang:
                s = skill_map[row["skill_id"]]
                if s["jenis_skill"] == "hard":
                    counter[s["nama_skill"]] += 1
        result[b["nama_bidang"]] = [
            {"skill": k, "jumlah": v} for k, v in counter.most_common(top_n)
        ]
    return result

def top_soft_skills_per_bidang(top_n: int = 5) -> Dict[str, List[dict]]:
    skill_map = get_skill_map()
    result = {}
    for b in BIDANG_PEKERJAAN:
        bid = b["bidang_id"]
        rid_in_bidang = {r["responden_id"] for r in RESPONDEN if r["bidang_id"] == bid}
        counter = Counter()
        for row in RESPONDEN_SKILL_DIBUTUHKAN:
            if row["responden_id"] in rid_in_bidang:
                s = skill_map[row["skill_id"]]
                if s["jenis_skill"] == "soft":
                    counter[s["nama_skill"]] += 1
        result[b["nama_bidang"]] = [
            {"skill": k, "jumlah": v} for k, v in counter.most_common(top_n)
        ]
    return result

def sertifikasi_per_bidang(top_n: int = 3) -> Dict[str, List[dict]]:
    penc_map = {p["pencapaian_id"]: p for p in PENCAPAIAN}
    result = {}
    for b in BIDANG_PEKERJAAN:
        bid = b["bidang_id"]
        rid_in_bidang = {r["responden_id"] for r in RESPONDEN if r["bidang_id"] == bid}
        counter = Counter()
        for row in RESPONDEN_PENCAPAIAN:
            if row["responden_id"] in rid_in_bidang:
                p = penc_map[row["pencapaian_id"]]
                if p["jenis"] == "sertifikasi":
                    counter[p["nama_pencapaian"]] += 1
        result[b["nama_bidang"]] = [
            {"sertifikasi": k, "jumlah": v} for k, v in counter.most_common(top_n)
        ]
    return result

def matriks_prodi_bidang() -> Dict[str, Dict[str, int]]:
    prodi_map = get_prodi_map()
    bidang_map = get_bidang_map()
    matrix = defaultdict(lambda: defaultdict(int))
    for r in RESPONDEN:
        matrix[prodi_map[r["prodi_id"]]][bidang_map[r["bidang_id"]]] += 1
    return {k: dict(v) for k, v in matrix.items()}

# ---------- Fitur 2: Analisis Skill Gap ----------
def ranking_skill_gap(top_n: int = 10) -> List[dict]:
    skill_map = get_skill_map()
    counter = Counter()
    for row in RESPONDEN_SKILL_GAP:
        counter[skill_map[row["skill_id"]]["nama_skill"]] += 1
    return [{"skill": k, "jumlah": v} for k, v in counter.most_common(top_n)]

def gap_view_dibutuhkan_vs_kurang(top_n: int = 8) -> List[dict]:
    skill_map = get_skill_map()
    dibutuhkan = Counter()
    kurang = Counter()
    for row in RESPONDEN_SKILL_DIBUTUHKAN:
        dibutuhkan[skill_map[row["skill_id"]]["nama_skill"]] += 1
    for row in RESPONDEN_SKILL_GAP:
        kurang[skill_map[row["skill_id"]]["nama_skill"]] += 1
    all_skills = set(dibutuhkan) | set(kurang)
    rows = []
    for s in all_skills:
        rows.append({
            "skill": s,
            "dibutuhkan": dibutuhkan.get(s, 0),
            "dirasa_kurang": kurang.get(s, 0),
        })
    rows.sort(key=lambda x: x["dirasa_kurang"], reverse=True)
    return rows[:top_n]

def tren_gap_antar_angkatan() -> Dict[int, List[dict]]:
    skill_map = get_skill_map()
    rid_to_angkatan = {r["responden_id"]: r["angkatan"] for r in RESPONDEN}
    result = defaultdict(Counter)
    for row in RESPONDEN_SKILL_GAP:
        ang = rid_to_angkatan[row["responden_id"]]
        result[ang][skill_map[row["skill_id"]]["nama_skill"]] += 1
    # ambil top 5 gap per angkatan
    return {
        ang: [{"skill": k, "jumlah": v} for k, v in c.most_common(5)]
        for ang, c in sorted(result.items(), reverse=True)
    }

def waktu_tunggu_vs_gap() -> List[dict]:
    """Korelasi sederhana: rata-rata waktu tunggu per responden vs jumlah gap-nya."""
    gap_count = Counter()
    for row in RESPONDEN_SKILL_GAP:
        gap_count[row["responden_id"]] += 1
    rows = []
    for r in RESPONDEN:
        rows.append({
            "responden_id": r["responden_id"],
            "angkatan": r["angkatan"],
            "waktu_bulan": r["waktu_kerja_pertama_bulan"],
            "jumlah_gap": gap_count.get(r["responden_id"], 0),
        })
    return rows

# ---------- Fitur 3: Dashboard ----------
def _filter_responden(angkatan=None, bidang_id=None):
    """Helper: filter RESPONDEN berdasarkan angkatan & bidang."""
    res = RESPONDEN
    if angkatan is not None:
        res = [r for r in res if r["angkatan"] == angkatan]
    if bidang_id is not None:
        res = [r for r in res if r["bidang_id"] == bidang_id]
    return res


def kpi_summary(angkatan=None, bidang_id=None) -> dict:
    data = _filter_responden(angkatan, bidang_id)
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


def distribusi_bidang(angkatan=None, bidang_id=None) -> List[dict]:
    data = _filter_responden(angkatan, bidang_id)
    bidang_map = get_bidang_map()
    c = Counter(bidang_map[r["bidang_id"]] for r in data)
    return [{"bidang": k, "jumlah": v} for k, v in c.most_common()]


def distribusi_waktu_tunggu(angkatan=None, bidang_id=None) -> List[dict]:
    data = _filter_responden(angkatan, bidang_id)
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


def kesesuaian_vs_prodi(angkatan=None, bidang_id=None) -> List[dict]:
    data = _filter_responden(angkatan, bidang_id)
    prodi_map = get_prodi_map()
    agg = defaultdict(lambda: {"sesuai": 0, "sebagian sesuai": 0, "tidak sesuai": 0})
    for r in data:
        agg[prodi_map[r["prodi_id"]]][r["status_kesesuaian"]] += 1
    return [{"prodi": k, **v} for k, v in agg.items()]

# ---------- Fitur 4: Career Navigation ----------
def weighted_overlap_score(user_skills: set, bidang_id: int) -> dict:
    """
    Hitung skor kecocokan user vs bidang:
    - Bobot hard skill = 0.7, soft skill = 0.3
    - Skor = (weighted matched) / (weighted total dibutuhkan bidang)
    """
    skill_map = get_skill_map()
    rid_in_bidang = {r["responden_id"] for r in RESPONDEN if r["bidang_id"] == bidang_id}

    # hitung frekuensi skill yang dibutuhkan di bidang tsb
    freq = Counter()
    for row in RESPONDEN_SKILL_DIBUTUHKAN:
        if row["responden_id"] in rid_in_bidang:
            freq[row["skill_id"]] += 1

    if not freq:
        return {"skor": 0.0, "match": [], "gap": [], "total_bobot": 0.0}

    max_freq = max(freq.values())
    total_bobot = 0.0
    matched_bobot = 0.0
    match, gap = [], []

    for sid, f in freq.items():
        s = skill_map[sid]
        bobot_jenis = 0.7 if s["jenis_skill"] == "hard" else 0.3
        bobot_skill = (f / max_freq) * bobot_jenis
        total_bobot += bobot_skill
        if sid in user_skills:
            matched_bobot += bobot_skill
            match.append({"skill_id": sid, "nama_skill": s["nama_skill"], "jenis": s["jenis_skill"]})
        else:
            gap.append({"skill_id": sid, "nama_skill": s["nama_skill"], "jenis": s["jenis_skill"]})

    skor = matched_bobot / total_bobot if total_bobot > 0 else 0.0
    match.sort(key=lambda x: x["jenis"])
    gap.sort(key=lambda x: x["jenis"])
    return {
        "skor": round(skor, 4),
        "match": match,
        "gap": gap,
        "total_bobot": round(total_bobot, 4),
    }

def recommend_bidang_for_skills(user_skills: set, top_n: int = 5) -> List[dict]:
    hasil = []
    for b in BIDANG_PEKERJAAN:
        res = weighted_overlap_score(user_skills, b["bidang_id"])
        hasil.append({
            "bidang_id": b["bidang_id"],
            "nama_bidang": b["nama_bidang"],
            "skor": res["skor"],
            "match": res["match"],
            "gap": res["gap"],
        })
    hasil.sort(key=lambda x: x["skor"], reverse=True)
    return hasil[:top_n]

def catat_log_eksplorasi(bidang_top1_id: int, skor: float, skill_ids: List[int]):
    new_id = (max([l["log_id"] for l in LOG_EKSPLORASI]) + 1) if LOG_EKSPLORASI else 1
    LOG_EKSPLORASI.append({
        "log_id": new_id,
        "bidang_hasil_top1_id": bidang_top1_id,
        "skor_kecocokan_top1": skor,
        "created_at": "2025-01-01 00:00",
    })
    for sid in skill_ids:
        LOG_EKSPLORASI_SKILL.append({"log_id": new_id, "skill_id": sid})

def insight_skill_paling_dicari() -> List[dict]:
    skill_map = get_skill_map()
    c = Counter()
    for row in LOG_EKSPLORASI_SKILL:
        c[skill_map[row["skill_id"]]["nama_skill"]] += 1
    return [{"skill": k, "jumlah": v} for k, v in c.most_common(10)]