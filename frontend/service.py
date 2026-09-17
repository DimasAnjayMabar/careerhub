"""
service.py
Dummy in-memory DB + query helper.
Semua layer (layer1-4.py) hanya boleh ambil data dari sini.
"""
import random
from datetime import date, timedelta

random.seed(42)

# ============================================================
# MASTER DATA
# ============================================================
PRODI = [
    {"prodi_id": "IF",  "nama_prodi": "Informatika",         "fakultas": "Fakultas Teknologi Informasi"},
    {"prodi_id": "SI",  "nama_prodi": "Sistem Informasi",    "fakultas": "Fakultas Teknologi Informasi"},
    {"prodi_id": "DS",  "nama_prodi": "Sains Data",          "fakultas": "Fakultas Teknologi Informasi"},
]

MATA_KULIAH = [
    # Informatika
    {"kode_mk": "IF101", "nama_mk": "Algoritma & Pemrograman", "prodi_id": "IF", "kategori": "inti",     "sks": 4, "kompetensi": "Pemrograman"},
    {"kode_mk": "IF102", "nama_mk": "Struktur Data",           "prodi_id": "IF", "kategori": "inti",     "sks": 3, "kompetensi": "Pemrograman"},
    {"kode_mk": "IF201", "nama_mk": "Basis Data",              "prodi_id": "IF", "kategori": "inti",     "sks": 3, "kompetensi": "Data & Basis Data"},
    {"kode_mk": "IF202", "nama_mk": "Jaringan Komputer",       "prodi_id": "IF", "kategori": "inti",     "sks": 3, "kompetensi": "Infrastruktur"},
    {"kode_mk": "IF301", "nama_mk": "Machine Learning",        "prodi_id": "IF", "kategori": "inti",     "sks": 3, "kompetensi": "AI & ML"},
    {"kode_mk": "IF302", "nama_mk": "Rekayasa Perangkat Lunak","prodi_id": "IF", "kategori": "inti",     "sks": 3, "kompetensi": "RPL"},
    {"kode_mk": "IF303", "nama_mk": "Statistika",              "prodi_id": "IF", "kategori": "pendukung","sks": 2, "kompetensi": "Matematika & Statistik"},
    # Sistem Informasi
    {"kode_mk": "SI101", "nama_mk": "Konsep Sistem Informasi", "prodi_id": "SI", "kategori": "inti",     "sks": 3, "kompetensi": "Analisis Bisnis"},
    {"kode_mk": "SI102", "nama_mk": "Pemrograman Web",         "prodi_id": "SI", "kategori": "inti",     "sks": 3, "kompetensi": "Pemrograman"},
    {"kode_mk": "SI201", "nama_mk": "Analisis Proses Bisnis",  "prodi_id": "SI", "kategori": "inti",     "sks": 3, "kompetensi": "Analisis Bisnis"},
    {"kode_mk": "SI202", "nama_mk": "Basis Data Lanjut",       "prodi_id": "SI", "kategori": "inti",     "sks": 3, "kompetensi": "Data & Basis Data"},
    {"kode_mk": "SI301", "nama_mk": "Manajemen Proyek TI",     "prodi_id": "SI", "kategori": "inti",     "sks": 3, "kompetensi": "Manajemen Proyek"},
    {"kode_mk": "SI302", "nama_mk": "UI/UX Design",            "prodi_id": "SI", "kategori": "inti",     "sks": 3, "kompetensi": "Desain"},
    # Sains Data
    {"kode_mk": "DS101", "nama_mk": "Pengantar Sains Data",    "prodi_id": "DS", "kategori": "inti",     "sks": 3, "kompetensi": "Data & Basis Data"},
    {"kode_mk": "DS102", "nama_mk": "Algoritma & Struktur Data","prodi_id": "DS","kategori": "inti",     "sks": 4, "kompetensi": "Pemrograman"},
    {"kode_mk": "DS201", "nama_mk": "Statistika Inferensia",   "prodi_id": "DS", "kategori": "inti",     "sks": 3, "kompetensi": "Matematika & Statistik"},
    {"kode_mk": "DS202", "nama_mk": "Visualisasi Data",        "prodi_id": "DS", "kategori": "inti",     "sks": 3, "kompetensi": "Visualisasi"},
    {"kode_mk": "DS301", "nama_mk": "Deep Learning",           "prodi_id": "DS", "kategori": "inti",     "sks": 3, "kompetensi": "AI & ML"},
    {"kode_mk": "DS302", "nama_mk": "Big Data",                "prodi_id": "DS", "kategori": "inti",     "sks": 3, "kompetensi": "Data & Basis Data"},
]

CAREER_PATH = [
    {"career_id": "SE",  "nama_career": "Software Engineer"},
    {"career_id": "DA",  "nama_career": "Data Analyst"},
    {"career_id": "DS",  "nama_career": "Data Scientist"},
    {"career_id": "BA",  "nama_career": "Business Analyst"},
    {"career_id": "UX",  "nama_career": "UI/UX Designer"},
    {"career_id": "PM",  "nama_career": "Product Manager"},
]

KOMPETENSI_CAREER = [
    # Software Engineer
    {"career_id": "SE", "nama_kompetensi": "Pemrograman",           "bobot": 0.35},
    {"career_id": "SE", "nama_kompetensi": "RPL",                   "bobot": 0.25},
    {"career_id": "SE", "nama_kompetensi": "Data & Basis Data",     "bobot": 0.20},
    {"career_id": "SE", "nama_kompetensi": "Infrastruktur",         "bobot": 0.20},
    # Data Analyst
    {"career_id": "DA", "nama_kompetensi": "Data & Basis Data",     "bobot": 0.30},
    {"career_id": "DA", "nama_kompetensi": "Matematika & Statistik","bobot": 0.30},
    {"career_id": "DA", "nama_kompetensi": "Visualisasi",           "bobot": 0.25},
    {"career_id": "DA", "nama_kompetensi": "Analisis Bisnis",       "bobot": 0.15},
    # Data Scientist
    {"career_id": "DS", "nama_kompetensi": "AI & ML",               "bobot": 0.35},
    {"career_id": "DS", "nama_kompetensi": "Matematika & Statistik","bobot": 0.30},
    {"career_id": "DS", "nama_kompetensi": "Pemrograman",           "bobot": 0.20},
    {"career_id": "DS", "nama_kompetensi": "Data & Basis Data",     "bobot": 0.15},
    # Business Analyst
    {"career_id": "BA", "nama_kompetensi": "Analisis Bisnis",       "bobot": 0.35},
    {"career_id": "BA", "nama_kompetensi": "Manajemen Proyek",      "bobot": 0.25},
    {"career_id": "BA", "nama_kompetensi": "Data & Basis Data",     "bobot": 0.20},
    {"career_id": "BA", "nama_kompetensi": "Visualisasi",           "bobot": 0.20},
    # UI/UX Designer
    {"career_id": "UX", "nama_kompetensi": "Desain",                "bobot": 0.40},
    {"career_id": "UX", "nama_kompetensi": "Analisis Bisnis",       "bobot": 0.25},
    {"career_id": "UX", "nama_kompetensi": "Pemrograman",           "bobot": 0.20},
    {"career_id": "UX", "nama_kompetensi": "Visualisasi",           "bobot": 0.15},
    # Product Manager
    {"career_id": "PM", "nama_kompetensi": "Manajemen Proyek",      "bobot": 0.30},
    {"career_id": "PM", "nama_kompetensi": "Analisis Bisnis",       "bobot": 0.30},
    {"career_id": "PM", "nama_kompetensi": "Desain",                "bobot": 0.20},
    {"career_id": "PM", "nama_kompetensi": "Data & Basis Data",     "bobot": 0.20},
]

# ============================================================
# GENERATE MAHASISWA + NILAI + IPS + AKTIVITAS
# ============================================================
NAMA_DEPAN = ["Andi","Budi","Citra","Dewi","Eko","Fajar","Gita","Hana","Irfan","Joko",
              "Kartika","Lina","Maya","Nanda","Oscar","Putri","Rizky","Sari","Tono","Umar",
              "Vina","Wahyu","Yuni","Zaki","Ayu","Bima","Cindy","Dimas"]
NAMA_BELAKANG = ["Pratama","Wijaya","Santoso","Lestari","Nugroho","Saputra","Hidayat","Permata",
                 "Ramadhan","Kusuma","Maulana","Anggraini","Firmansyah","Halim","Siregar"]

MAHASISWA = []
NILAI_MATAKULIAH = []
IPSEMESTER = []
AKTIVITAS = []
SKOR_KECOCOKAN = []

NILAI_MAP = {"A": 4.00, "AB": 3.50, "B": 3.00, "BC": 2.50, "C": 2.00, "D": 1.00, "E": 0.00}
NILAI_HURUF = list(NILAI_MAP.keys())

def _rand_nilai(bias=0.0):
    """bias > 0 = cenderung nilai bagus."""
    weights = [max(0.01, 0.35 + bias), max(0.01, 0.25 + bias), max(0.01, 0.20),
               max(0.01, 0.10 - bias), max(0.01, 0.06 - bias), 0.02, 0.01]
    return random.choices(NILAI_HURUF, weights=weights, k=1)[0]

def _generate():
    mhs_id = 1
    for prodi in PRODI:
        for angkatan in [2021, 2022, 2023]:
            for i in range(8):  # 8 mahasiswa per prodi per angkatan = 72 total
                nim = f"{prodi['prodi_id']}{angkatan}{i+1:03d}"
                nama = f"{random.choice(NAMA_DEPAN)} {random.choice(NAMA_BELAKANG)}"
                # profil "kualitas" mahasiswa (0..1)
                kualitas = random.random()
                MAHASISWA.append({
                    "nim": nim, "nama": nama, "prodi_id": prodi["prodi_id"],
                    "angkatan": angkatan, "status": "aktif"
                })

                mk_prodi = [m for m in MATA_KULIAH if m["prodi_id"] == prodi["prodi_id"]]
                # semester yang sudah ditempuh
                max_sem = 2025 - angkatan  # 2021→4, 2022→3, 2023→2
                max_sem = min(max_sem, 8)
                sks_kum = 0
                total_bobot = 0
                for sem in range(1, max_sem + 1):
                    mk_sem = random.sample(mk_prodi, min(len(mk_prodi), 3))
                    bobot_sem = 0
                    sks_sem = 0
                    for mk in mk_sem:
                        nh = _rand_nilai(bias=(kualitas - 0.5))
                        nb = NILAI_MAP[nh]
                        NILAI_MATAKULIAH.append({
                            "nilai_id": f"N{mhs_id}-{mk['kode_mk']}-{sem}",
                            "nim": nim, "kode_mk": mk["kode_mk"],
                            "semester": sem, "nilai_huruf": nh, "nilai_bobot": nb
                        })
                        bobot_sem += nb * mk["sks"]
                        sks_sem += mk["sks"]
                    ip_sem = round(bobot_sem / sks_sem, 2) if sks_sem else 0
                    sks_kum += sks_sem
                    total_bobot += bobot_sem
                    ipk = round(total_bobot / sks_kum, 2) if sks_kum else 0
                    IPSEMESTER.append({
                        "ip_id": f"IP{mhs_id}-{sem}", "nim": nim,
                        "semester": sem, "ip_semester": ip_sem,
                        "ipk_kumulatif": ipk, "sks_kumulatif": sks_kum
                    })

                    # aktivitas non-akademik: probabilitas tergantung kualitas
                    if random.random() < 0.5 + 0.4 * (kualitas - 0.5):
                        jenis = random.choice(["organisasi","sertifikasi","kompetisi","magang"])
                        AKTIVITAS.append({
                            "aktivitas_id": f"A{mhs_id}-{sem}",
                            "nim": nim, "semester": sem, "jenis": jenis,
                            "nama_aktivitas": f"{jenis.title()} {prodi['nama_prodi']} {sem}",
                            "tingkat": random.choice(["kampus","nasional","internasional"]),
                            "tanggal": date(angkatan + sem - 1, random.randint(1,12), random.randint(1,28))
                        })

                # skor kecocokan karier (dummy, diturunkan dari kualitas + noise)
                for cp in CAREER_PATH:
                    skor = max(10, min(98, int(40 + 55 * kualitas + random.randint(-15, 15))))
                    SKOR_KECOCOKAN.append({
                        "skor_id": f"SK{mhs_id}-{cp['career_id']}",
                        "nim": nim, "career_id": cp["career_id"],
                        "skor_kecocokan": skor, "semester_data": max_sem
                    })
                mhs_id += 1

_generate()

# ============================================================
# QUERY HELPERS
# ============================================================
def list_prodi():
    return PRODI

def get_prodi(prodi_id):
    return next((p for p in PRODI if p["prodi_id"] == prodi_id), None)

def list_mahasiswa(prodi_id=None, angkatan=None):
    out = MAHASISWA
    if prodi_id: out = [m for m in out if m["prodi_id"] == prodi_id]
    if angkatan: out = [m for m in out if m["angkatan"] == angkatan]
    return out

def get_mahasiswa(nim):
    return next((m for m in MAHASISWA if m["nim"] == nim), None)

def list_mata_kuliah(prodi_id=None):
    return [mk for mk in MATA_KULIAH if not prodi_id or mk["prodi_id"] == prodi_id]

def list_career():
    return CAREER_PATH

def get_kpi_prodi():
    """KPI per prodi: rata IPK, % tren naik, % sertifikasi/magang, distribusi karier."""
    hasil = []
    for p in PRODI:
        mhs = list_mahasiswa(prodi_id=p["prodi_id"])
        if not mhs: continue
        nims = {m["nim"] for m in mhs}
        # rata IPK terakhir
        ipk_list = []
        for m in mhs:
            ips = [x for x in IPSEMESTER if x["nim"] == m["nim"]]
            if ips:
                ipk_list.append(max(ips, key=lambda x: x["semester"])["ipk_kumulatif"])
        rata_ipk = round(sum(ipk_list)/len(ipk_list), 2) if ipk_list else 0

        # tren naik/turun dari IPS semester terakhir vs sebelumnya
        naik = turun = stagna = 0
        for m in mhs:
            ips = sorted([x for x in IPSEMESTER if x["nim"] == m["nim"]], key=lambda x: x["semester"])
            if len(ips) >= 2:
                d = ips[-1]["ip_semester"] - ips[-2]["ip_semester"]
                if d > 0.1: naik += 1
                elif d < -0.1: turun += 1
                else: stagna += 1
        total_tren = max(1, naik + turun + stagna)

        # % sertifikasi/magang
        pct_sertmag = 0
        if nims:
            punya = {a["nim"] for a in AKTIVITAS if a["nim"] in nims and a["jenis"] in ("sertifikasi","magang")}
            pct_sertmag = round(100 * len(punya) / len(nims), 1)

        # distribusi rekomendasi karier (career dengan skor tertinggi per mahasiswa)
        dist = {}
        for m in mhs:
            skors = [s for s in SKOR_KECOCOKAN if s["nim"] == m["nim"]]
            if skors:
                top = max(skors, key=lambda s: s["skor_kecocokan"])
                cname = next(c["nama_career"] for c in CAREER_PATH if c["career_id"] == top["career_id"])
                dist[cname] = dist.get(cname, 0) + 1

        hasil.append({
            "prodi_id": p["prodi_id"], "nama_prodi": p["nama_prodi"],
            "jumlah_mahasiswa": len(mhs), "rata_ipk": rata_ipk,
            "pct_naik": round(100*naik/total_tren, 1),
            "pct_turun": round(100*turun/total_tren, 1),
            "pct_stagnan": round(100*stagna/total_tren, 1),
            "pct_sertifikasi_magang": pct_sertmag,
            "distribusi_karier": dist,
        })
    return hasil

def get_segmentasi(prodi_id, angkatan=None):
    """
    Kuadran: performa akademik (IPK) vs keaktifan non-akademik (jumlah aktivitas).
    Return list dict per mahasiswa + segmen.
    """
    mhs = list_mahasiswa(prodi_id=prodi_id, angkatan=angkatan)
    if not mhs: return []
    rows = []
    for m in mhs:
        ips = [x for x in IPSEMESTER if x["nim"] == m["nim"]]
        ipk = max(ips, key=lambda x: x["semester"])["ipk_kumulatif"] if ips else 0
        n_akt = len([a for a in AKTIVITAS if a["nim"] == m["nim"]])
        rows.append({"nim": m["nim"], "nama": m["nama"], "angkatan": m["angkatan"],
                     "ipk": ipk, "aktivitas": n_akt})
    # threshold median
    ipk_med = sorted(r["ipk"] for r in rows)[len(rows)//2]
    akt_med = sorted(r["aktivitas"] for r in rows)[len(rows)//2]
    for r in rows:
        hi_a = r["ipk"] >= ipk_med
        hi_n = r["aktivitas"] >= akt_med
        if hi_a and hi_n: r["segmen"] = "Unggul"
        elif hi_a and not hi_n: r["segmen"] = "Berkembang"
        elif not hi_a and hi_n: r["segmen"] = "Perlu Perhatian"
        else: r["segmen"] = "Berisiko"
    return rows

def get_alur_segmen(prodi_id):
    """Dummy alur perpindahan segmen antar semester (aggregate)."""
    return {
        "semester": [1, 2, 3, 4],
        "transisi": [
            {"dari": "Berkembang", "ke": "Unggul", "jumlah": 6},
            {"dari": "Berkembang", "ke": "Berkembang", "jumlah": 9},
            {"dari": "Perlu Perhatian", "ke": "Berkembang", "jumlah": 4},
            {"dari": "Perlu Perhatian", "ke": "Perlu Perhatian", "jumlah": 5},
            {"dari": "Unggul", "ke": "Unggul", "jumlah": 12},
            {"dari": "Berisiko", "ke": "Perlu Perhatian", "jumlah": 3},
        ]
    }

def get_profil_individu(nim):
    m = get_mahasiswa(nim)
    if not m: return None
    ips = sorted([x for x in IPSEMESTER if x["nim"] == nim], key=lambda x: x["semester"])
    nilai = [x for x in NILAI_MATAKULIAH if x["nim"] == nim]
    akt = sorted([a for a in AKTIVITAS if a["nim"] == nim], key=lambda a: a["semester"])

    # radar kompetensi: agregasi nilai per kompetensi
    mk_map = {mk["kode_mk"]: mk for mk in MATA_KULIAH}
    komp = {}
    for n in nilai:
        k = mk_map[n["kode_mk"]]["kompetensi"]
        komp.setdefault(k, []).append(n["nilai_bobot"])
    radar = [{"kompetensi": k, "nilai": round(sum(v)/len(v), 2)} for k, v in komp.items()]

    # heatmap: matkul inti x semester
    heat = []
    for n in nilai:
        mk = mk_map[n["kode_mk"]]
        if mk["kategori"] == "inti":
            heat.append({"matkul": mk["nama_mk"], "semester": n["semester"], "nilai": n["nilai_bobot"]})

    # insight
    if radar:
        top = max(radar, key=lambda x: x["nilai"])
        insight = (f"Kompetensi terkuat: {top['kompetensi']} (rata {top['nilai']}). "
                   f"IPK terakhir {ips[-1]['ipk_kumulatif'] if ips else '-'} "
                   f"dengan {len(akt)} aktivitas non-akademik tercatat.")
    else:
        insight = "Belum ada data nilai."

    tren = "stagnan"
    if len(ips) >= 2:
        d = ips[-1]["ip_semester"] - ips[-2]["ip_semester"]
        tren = "naik" if d > 0.1 else ("turun" if d < -0.1 else "stagnan")

    return {"mahasiswa": m, "ips": ips, "nilai": nilai, "aktivitas": akt,
            "radar": radar, "heatmap": heat, "insight": insight, "tren": tren}

def get_rekomendasi_karier(nim):
    skors = [s for s in SKOR_KECOCOKAN if s["nim"] == nim]
    hasil = []
    for s in skors:
        cp = next(c for c in CAREER_PATH if c["career_id"] == s["career_id"])
        komps = [k for k in KOMPETENSI_CAREER if k["career_id"] == s["career_id"]]
        hasil.append({
            "career_id": cp["career_id"], "nama_career": cp["nama_career"],
            "skor": s["skor_kecocokan"], "kompetensi": komps
        })
    hasil.sort(key=lambda x: x["skor"], reverse=True)
    return hasil

def get_skill_checklist(nim, career_id):
    """Cek skill dimiliki vs dibutuhkan berdasarkan nilai matkul inti."""
    profil = get_profil_individu(nim)
    if not profil: return []
    dimiliki = {r["kompetensi"]: r["nilai"] for r in profil["radar"]}
    out = []
    for k in KOMPETENSI_CAREER:
        if k["career_id"] != career_id: continue
        nilai = dimiliki.get(k["nama_kompetensi"], 0)
        out.append({
            "kompetensi": k["nama_kompetensi"],
            "bobot": k["bobot"],
            "nilai_saat_ini": nilai,
            "status": "✅" if nilai >= 3.0 else ("⚠️" if nilai >= 2.5 else "❌")
        })
    return out