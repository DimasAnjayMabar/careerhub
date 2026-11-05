"""
normalizer.py
Algoritma normalisasi plug-and-play untuk skill, pencapaian, prodi, bidang.

Filosofi:
- TIDAK ADA konsep "pending". Semua entitas baru otomatis jadi master (approved).
- Normalisasi berlapis:
    1. Case & whitespace (lowercase, trim, collapse space)
    2. Alias manual (teamwork → kerja tim, py → python, si → sistem informasi, ...)
    3. Fuzzy match ke master (ratio ≥ 0.9) → merge otomatis
    4. Tidak match → buat entitas BARU (approved) + tambah ke master + alias
- Semua otomatis, tanpa review manual.

Modul ini TIDAK menyimpan state. State (master & alias_map) disediakan oleh
main.py dan diteruskan sebagai parameter. Setiap resolve_* mengembalikan dict
berisi hasil + metadata agar mudah diaudit.

Dependensi: hanya stdlib (difflib, re) + pandas (untuk cek NaN).
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Optional

import pandas as pd


# =========================================================
# KONSTANTA
# =========================================================

# Threshold fuzzy match: hanya merge kalau SANGAT mirip.
FUZZY_THRESHOLD = 0.9

# Panjang minimum untuk fuzzy match (hindari "C" vs "C++" merge).
FUZZY_MIN_LEN = 4

# Pengecualian hardcode: pasangan yang TIDAK BOLEH di-merge meski mirip.
# Key = tuple (lower_a, lower_b) yang diurutkan.
FUZZY_BLACKLIST: set[tuple[str, str]] = {
    ("c", "c++"),
    ("c", "c#"),
    ("c++", "c#"),
    ("sql", "nosql"),
    ("java", "javascript"),
    ("ai", "ai ethics"),
    ("r", "r studio"),
    ("go", "google"),
    ("react", "react native"),
}

# Alias manual awal (dapat diperluas dari master_storage.json).
# Key = lowercase teks user, value = lowercase nama master yang dituju.
DEFAULT_ALIAS: dict[str, str] = {
    # --- soft skill ---
    "teamwork": "kerja tim",
    "team work": "kerja tim",
    "kerjasama tim": "kerja tim",
    "kerjasama": "kerja tim",
    "communication": "komunikasi",
    "problem-solving": "problem solving",
    "problem solving skill": "problem solving",
    "time management": "manajemen waktu",
    "leadership": "kepemimpinan",
    "critical thinking": "berpikir kritis",
    "negosiation": "negosiasi",
    "adaptif": "adaptif & cepat belajar",
    "cepat belajar": "adaptif & cepat belajar",
    "public speaking": "komunikasi",
    "presentasi": "komunikasi",
    # --- hard skill ---
    "py": "python",
    "js": "javascript",
    "node.js": "javascript",
    "nodejs": "javascript",
    "git": "git & version control",
    "git version control": "git & version control",
    "dataviz": "data visualization",
    "data visualisation": "data visualization",
    "ml": "machine learning",
    "seo": "seo/sem",
    "sem": "seo/sem",
    "seo sem": "seo/sem",
    "powerbi": "power bi",
    "power-bi": "power bi",
    "restful api": "rest api",
    "restful": "rest api",
    "cloud": "cloud (aws/gcp)",
    "aws": "cloud (aws/gcp)",
    "gcp": "cloud (aws/gcp)",
    "excel": "excel advanced",
    "microsoft excel": "excel advanced",
    # --- design tools → Figma ---
    "canva": "figma",
    "adobe": "figma",
    "photoshop": "figma",
    "illustrator": "figma",
    "sketch": "figma",
    # --- soft skill sinonim ---
    "teliti": "berpikir kritis",
    "kreatif": "problem solving",
    "detail oriented": "berpikir kritis",
    "analitis": "berpikir kritis",
    "analytical": "berpikir kritis",
    "manajemen konflik": "negosiasi",
    "conflict resolution": "negosiasi",
    # --- prodi (singkatan & variasi) ---
    "if": "informatika",
    "teknik informatika": "informatika",
    "informatics": "informatika",
    "si": "sistem informasi",
    "sysinfo": "sistem informasi",
    "information system": "sistem informasi",
    "information systems": "sistem informasi",
    "mb": "manajemen bisnis",
    "manajemen": "manajemen bisnis",
    "business management": "manajemen bisnis",
    "ak": "akuntansi",
    "accounting": "akuntansi",
    "dkv": "desain komunikasi visual",
    "deskomvis": "desain komunikasi visual",
    "visual communication design": "desain komunikasi visual",
    # --- bidang pekerjaan (singkatan & variasi) ---
    "se": "software engineering",
    "software engineer": "software engineering",
    "software developer": "software engineering",
    "software dev": "software engineering",
    "data": "data & analytics",
    "data analyst": "data & analytics",
    "data analytics": "data & analytics",
    "data science": "data & analytics",
    "data scientist": "data & analytics",
    "dm": "digital marketing",
    "digital marketer": "digital marketing",
    "marketing": "digital marketing",
    "fa": "finance & accounting",
    "finance": "finance & accounting",
    "accounting staff": "finance & accounting",
    "ui/ux": "ui/ux & product design",
    "ui ux": "ui/ux & product design",
    "ux": "ui/ux & product design",
    "ui": "ui/ux & product design",
    "product design": "ui/ux & product design",
    "product designer": "ui/ux & product design",
    "ux designer": "ui/ux & product design",
    "ui designer": "ui/ux & product design",
    # --- pencapaian ---
    "aws certified cloud practitioner": "aws certified cloud practitioner",
    "google analytics": "google analytics certificate",
    "excel expert": "microsoft excel expert",
    "google ux": "google ux design certificate",
    "hackathon": "hackathon nasional",
}

# Placeholder kosong → dianggap tidak ada nilai.
PLACEHOLDER_EMPTY = {"", "-", "n/a", "na", "none", "tidak ada", "tidak", "null", "nil"}


# =========================================================
# UTIL: NORMALISASI DASAR
# =========================================================

def normalize_for_lookup(name) -> str:
    """lowercase, trim, collapse whitespace."""
    if name is None:
        return ""
    if isinstance(name, float) and pd.isna(name):
        return ""
    s = str(name).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def is_placeholder(name) -> bool:
    """Cek apakah teks termasuk placeholder kosong."""
    return normalize_for_lookup(name) in PLACEHOLDER_EMPTY


# =========================================================
# UTIL: FUZZY MATCH
# =========================================================

def _ratio(a: str, b: str) -> float:
    """SequenceMatcher ratio (0..1)."""
    return SequenceMatcher(None, a, b).ratio()


def _is_blacklisted(a: str, b: str) -> bool:
    """Cek apakah pasangan (a, b) ada di blacklist fuzzy."""
    pair = tuple(sorted((a.lower(), b.lower())))
    return pair in FUZZY_BLACKLIST


def fuzzy_match(
    key: str,
    candidates: list[str],
    threshold: float = FUZZY_THRESHOLD,
) -> tuple[Optional[str], float]:
    """
    Cari kandidat paling mirip dengan `key` (keduanya sudah lowercase).

    Return: (best_candidate, best_ratio). best_candidate = None jika tidak
    ada yang lolos threshold / blacklist.
    """
    if len(key) < FUZZY_MIN_LEN:
        return None, 0.0

    best: Optional[str] = None
    best_ratio = 0.0

    for c in candidates:
        if len(c) < FUZZY_MIN_LEN:
            continue
        if _is_blacklisted(key, c):
            continue
        r = _ratio(key, c)
        if r > best_ratio:
            best_ratio = r
            best = c

    if best is not None and best_ratio >= threshold:
        return best, best_ratio
    return None, best_ratio


# =========================================================
# HELPER INTERNAL: RESOLVE GENERIK
# =========================================================

def _resolve_generic(
    raw_name,
    state: list[dict],
    name_key: str,
    id_key: str,
    alias_map: dict[str, str],
    *,
    use_fuzzy: bool = True,
    extra_fields: Optional[dict] = None,
) -> dict:
    """
    Resolver generik untuk entitas dengan pola {id_key, name_key, ...}.

    Return dict seragam:
    {
        "<id_key>": int | None,
        "<name_key>": str | None,
        "is_new": bool,
        "match_method": "alias" | "exact" | "fuzzy" | "new" | "empty",
        "raw": str,
        "fuzzy_ratio": float | None,
    }
    """
    def _empty():
        return {
            id_key: None, name_key: None, "is_new": False,
            "match_method": "empty", "raw": str(raw_name), "fuzzy_ratio": None,
        }

    if is_placeholder(raw_name):
        return _empty()

    raw_str = str(raw_name).strip()
    key = normalize_for_lookup(raw_str)

    # --- Lapis 1: alias ---
    alias_target = alias_map.get(key)
    if alias_target:
        target_key = normalize_for_lookup(alias_target)
        for item in state:
            if normalize_for_lookup(item[name_key]) == target_key:
                return {
                    id_key: item[id_key], name_key: item[name_key],
                    "is_new": False, "match_method": "alias",
                    "raw": raw_str, "fuzzy_ratio": None,
                }

    # --- Lapis 2: exact ---
    for item in state:
        if normalize_for_lookup(item[name_key]) == key:
            alias_map[key] = item[name_key]
            return {
                id_key: item[id_key], name_key: item[name_key],
                "is_new": False, "match_method": "exact",
                "raw": raw_str, "fuzzy_ratio": None,
            }

    # --- Lapis 3: fuzzy ---
    if use_fuzzy:
        candidates_by_key: dict[str, dict] = {
            normalize_for_lookup(item[name_key]): item for item in state
        }
        best_key, ratio = fuzzy_match(key, list(candidates_by_key.keys()))
        if best_key is not None:
            item = candidates_by_key[best_key]
            alias_map[key] = item[name_key]
            return {
                id_key: item[id_key], name_key: item[name_key],
                "is_new": False, "match_method": "fuzzy",
                "raw": raw_str, "fuzzy_ratio": round(ratio, 3),
            }

    # --- Lapis 4: baru ---
    new_id = max([item[id_key] for item in state] + [0]) + 1
    new_item = {
        id_key: new_id,
        name_key: raw_str,
        "status": "approved",
        "dibuat_dari": [raw_str],
    }
    if extra_fields:
        new_item.update(extra_fields)
    state.append(new_item)
    alias_map[key] = raw_str

    return {
        id_key: new_id, name_key: raw_str,
        "is_new": True, "match_method": "new",
        "raw": raw_str, "fuzzy_ratio": None,
    }


# =========================================================
# RESOLVE: SKILL
# =========================================================

def resolve_skill(
    raw_name,
    jenis: str,
    skill_state: list[dict],
    alias_map: dict[str, str],
) -> dict:
    """
    Resolve 1 nama skill → skill_id. Auto-insert jika baru.

    Catatan: `jenis` ("hard"/"soft") diperlakukan sebagai bagian dari identitas.
    Skill dengan nama sama tapi jenis beda → dianggap beda entitas.
    """
    # filter state berdasarkan jenis agar fuzzy tidak salah lintas jenis
    # (kita pakai list view, bukan mutasi, lalu resolve ke list asli)
    if is_placeholder(raw_name):
        return {
            "skill_id": None, "nama_skill": None, "is_new": False,
            "match_method": "empty", "raw": str(raw_name), "fuzzy_ratio": None,
        }

    raw_str = str(raw_name).strip()
    key = normalize_for_lookup(raw_str)

    def _match_in_state(predicate):
        for s in skill_state:
            if predicate(s):
                return s
        return None

    # --- alias ---
    alias_target = alias_map.get(key)
    if alias_target:
        target_key = normalize_for_lookup(alias_target)
        s = _match_in_state(
            lambda x: normalize_for_lookup(x["nama_skill"]) == target_key
            and x["jenis_skill"] == jenis
        )
        if s:
            return {
                "skill_id": s["skill_id"], "nama_skill": s["nama_skill"],
                "is_new": False, "match_method": "alias",
                "raw": raw_str, "fuzzy_ratio": None,
            }

    # --- exact ---
    s = _match_in_state(
        lambda x: normalize_for_lookup(x["nama_skill"]) == key
        and x["jenis_skill"] == jenis
    )
    if s:
        alias_map[key] = s["nama_skill"]
        return {
            "skill_id": s["skill_id"], "nama_skill": s["nama_skill"],
            "is_new": False, "match_method": "exact",
            "raw": raw_str, "fuzzy_ratio": None,
        }

    # --- fuzzy (hanya dalam jenis yang sama) ---
    candidates = {
        normalize_for_lookup(x["nama_skill"]): x
        for x in skill_state if x["jenis_skill"] == jenis
    }
    best_key, ratio = fuzzy_match(key, list(candidates.keys()))
    if best_key is not None:
        s = candidates[best_key]
        alias_map[key] = s["nama_skill"]
        return {
            "skill_id": s["skill_id"], "nama_skill": s["nama_skill"],
            "is_new": False, "match_method": "fuzzy",
            "raw": raw_str, "fuzzy_ratio": round(ratio, 3),
        }

    # --- baru ---
    new_id = max([s["skill_id"] for s in skill_state] + [0]) + 1
    new_skill = {
        "skill_id": new_id,
        "nama_skill": raw_str,
        "jenis_skill": jenis,
        "status": "approved",
        "dibuat_dari": [raw_str],
    }
    skill_state.append(new_skill)
    alias_map[key] = raw_str

    return {
        "skill_id": new_id, "nama_skill": raw_str,
        "is_new": True, "match_method": "new",
        "raw": raw_str, "fuzzy_ratio": None,
    }


# =========================================================
# RESOLVE: PENCAPAIAN
# =========================================================

def resolve_pencapaian(
    raw_name,
    jenis: str,
    pencapaian_state: list[dict],
    alias_map: dict[str, str],
) -> dict:
    """
    Resolve 1 nama pencapaian → pencapaian_id. Auto-insert jika baru.

    TIDAK pakai fuzzy match — pencapaian (sertifikasi/kompetisi/proyek)
    biasanya unik (mis. "Hackathon 2023" vs "Hackathon 2024" jangan di-merge).
    """
    return _resolve_generic(
        raw_name,
        pencapaian_state,
        name_key="nama_pencapaian",
        id_key="pencapaian_id",
        alias_map=alias_map,
        use_fuzzy=False,
        extra_fields={"jenis": jenis},
    ) | {"_jenis_filter": jenis}


# Catatan: `_resolve_generic` tidak memfilter by `jenis` (karena pencapaian
# tidak pakai fuzzy lintas jenis). Tapi kita ingin memastikan exact/alias
# hanya match dalam `jenis` yang sama. Untuk itu, override di bawah.


def resolve_pencapaian(
    raw_name,
    jenis: str,
    pencapaian_state: list[dict],
    alias_map: dict[str, str],
) -> dict:
    """Resolve 1 nama pencapaian → pencapaian_id. Auto-insert jika baru."""
    if is_placeholder(raw_name):
        return {
            "pencapaian_id": None, "nama_pencapaian": None, "is_new": False,
            "match_method": "empty", "raw": str(raw_name),
        }

    raw_str = str(raw_name).strip()
    key = normalize_for_lookup(raw_str)

    # --- alias ---
    alias_target = alias_map.get(key)
    if alias_target:
        target_key = normalize_for_lookup(alias_target)
        for p in pencapaian_state:
            if normalize_for_lookup(p["nama_pencapaian"]) == target_key and p["jenis"] == jenis:
                return {
                    "pencapaian_id": p["pencapaian_id"], "nama_pencapaian": p["nama_pencapaian"],
                    "is_new": False, "match_method": "alias", "raw": raw_str,
                }

    # --- exact ---
    for p in pencapaian_state:
        if normalize_for_lookup(p["nama_pencapaian"]) == key and p["jenis"] == jenis:
            alias_map[key] = p["nama_pencapaian"]
            return {
                "pencapaian_id": p["pencapaian_id"], "nama_pencapaian": p["nama_pencapaian"],
                "is_new": False, "match_method": "exact", "raw": raw_str,
            }

    # --- baru ---
    new_id = max([p["pencapaian_id"] for p in pencapaian_state] + [0]) + 1
    new_p = {
        "pencapaian_id": new_id,
        "nama_pencapaian": raw_str,
        "jenis": jenis,
        "status": "approved",
        "dibuat_dari": [raw_str],
    }
    pencapaian_state.append(new_p)
    alias_map[key] = raw_str

    return {
        "pencapaian_id": new_id, "nama_pencapaian": raw_str,
        "is_new": True, "match_method": "new", "raw": raw_str,
    }


# =========================================================
# RESOLVE: PRODI
# =========================================================

def resolve_prodi(
    raw_name,
    prodi_state: list[dict],
    alias_map: dict[str, str],
) -> dict:
    """Resolve 1 nama prodi → prodi_id. Auto-insert jika baru."""
    return _resolve_generic(
        raw_name,
        prodi_state,
        name_key="nama_prodi",
        id_key="prodi_id",
        alias_map=alias_map,
        use_fuzzy=True,
    )


# =========================================================
# RESOLVE: BIDANG
# =========================================================

def resolve_bidang(
    raw_name,
    bidang_state: list[dict],
    alias_map: dict[str, str],
) -> dict:
    """Resolve 1 nama bidang pekerjaan → bidang_id. Auto-insert jika baru."""
    return _resolve_generic(
        raw_name,
        bidang_state,
        name_key="nama_bidang",
        id_key="bidang_id",
        alias_map=alias_map,
        use_fuzzy=True,
    )


# =========================================================
# AUDIT: LAPORAN NORMALISASI
# =========================================================

def build_normalization_report(resolutions: list[dict]) -> dict:
    """
    Rangkum hasil resolve untuk dilaporkan ke summary / log.

    Parameter: list hasil resolve_* (skill/pencapaian/prodi/bidang).
    Return:
    {
        "total": int,
        "baru": int,
        "alias": int,
        "exact": int,
        "fuzzy": int,
        "kosong": int,
        "detail_fuzzy": [{raw, name, ratio}, ...],
        "detail_baru": [{raw, name}, ...],
    }
    """
    report = {
        "total": 0, "baru": 0, "alias": 0, "exact": 0, "fuzzy": 0, "kosong": 0,
        "detail_fuzzy": [], "detail_baru": [],
    }
    for r in resolutions:
        report["total"] += 1
        m = r.get("match_method")
        if m == "new":
            report["baru"] += 1
            name = (
                r.get("nama_skill")
                or r.get("nama_pencapaian")
                or r.get("nama_prodi")
                or r.get("nama_bidang")
            )
            report["detail_baru"].append({"raw": r.get("raw"), "name": name})
        elif m == "alias":
            report["alias"] += 1
        elif m == "exact":
            report["exact"] += 1
        elif m == "fuzzy":
            report["fuzzy"] += 1
            name = (
                r.get("nama_skill")
                or r.get("nama_pencapaian")
                or r.get("nama_prodi")
                or r.get("nama_bidang")
            )
            report["detail_fuzzy"].append({
                "raw": r.get("raw"), "name": name, "ratio": r.get("fuzzy_ratio"),
            })
        elif m == "empty":
            report["kosong"] += 1
    return report