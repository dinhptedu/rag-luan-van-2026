import os

# ═══ NGƯỜI DÙNG VÀ PHÂN QUYỀN ═══════════════════════
# Thêm/sửa user tại đây. Password nên đổi trước khi demo.
USERS = {
    "admin":  {"password": "Admin@2026", "role": "admin",  "groups": ["all"]},
    "guest1": {"password": "Guest1@2026","role": "guest",  "groups": ["Lao dong & BHXH"]},
    "guest2": {"password": "Guest2@2026","role": "guest",  "groups": ["Ngan hang & Tin dung"]},
}

ROLE_MENUS = {
    "admin": ["download", "chunking", "qa", "report"],
    "guest": ["qa"],
}

# ═══ NHÓM TÀI LIỆU ═══════════════════════════════════
# Thêm nhóm mới bằng cách copy 1 block và sửa lại
DOCUMENT_GROUPS = {
    "Ngan hang & Tin dung": {
        "keywords": ["ngan hang", "tin dung", "lai suat"],
        "vbpl_id_range": (160000, 173000),
        "target_docs": 400,
        "icon": "ngan_hang",
    },
    "Lao dong & BHXH": {
        "keywords": ["lao dong", "bao hiem xa hoi", "tien luong"],
        "vbpl_id_range": (154000, 169000),
        "target_docs": 400,
        "icon": "lao_dong",
    },
    "Doanh nghiep & Dau tu": {
        "keywords": ["doanh nghiep", "dau tu", "thue"],
        "vbpl_id_range": (149000, 164000),
        "target_docs": 300,
        "icon": "doanh_nghiep",
    },
}

# ═══ CHUNKING ═════════════════════════════════════════
CHUNKING_OPTIONS = {
    "Fixed-size (baseline)": {"strategy":"fixed","size":500,"overlap":100},
    "Sentence-based":        {"strategy":"sentence","max_size":500},
    "Structure-aware":       {"strategy":"structure","max_size":800},
    "Hierarchical":          {"strategy":"hierarchical","parent":800,"child":200},
}

# ═══ EMBEDDING MODELS ════════════════════════════════
EMBEDDING_MODELS = {
    "multilingual-e5-base":  "intfloat/multilingual-e5-base",
    "PhoBERT-base":          "vinai/phobert-base-v2",
    "MiniLM-multilingual":   "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
}

# ═══ PATHS ════════════════════════════════════════════
BASE_DIR   = './data'
DOCX_DIR   = f'{BASE_DIR}/docx'
VECTOR_DIR = f'{BASE_DIR}/vectordb'
RESULT_DIR = f'{BASE_DIR}/results'

# ═══ LLM & ĐÁNH GIÁ ══════════════════════════════════
LLM_MODEL      = 'gemini-2.0-flash'
GEMINI_API_KEY = os.environ.get('AIzaSyC7mNnB99Ptiv5ABdQsdIeswmVehbBUTLE', '')
TOP_K          = 4
N_EVAL_RUNS    = 5
