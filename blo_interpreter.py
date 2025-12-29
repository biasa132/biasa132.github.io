# blo_interpreter.py
# Interpreter Bahasa-lo (.blo)

import re

# ==========================
# Kamus Bahasa Indonesia → Python
# ==========================
KAMUS = {
    r'\btulis\b': 'print',
    r'\bmasukan\b': 'input',
    r'\bbulat\b': 'int',
    r'\bpecahan\b': 'float',
    r'\bpanjang\b': 'len',
    r'\bdaftar\b': 'list',
    r'\bkamus\b': 'dict',

    r'\bjika\b': 'if',
    r'\bapabila\b': 'elif',
    r'\blainnya\b': 'else',
    r'\buntuk\b': 'for',
    r'\bfungsi\b': 'def',
    r'\bkembalikan\b': 'return',

    r'\bBenar\b': 'True',
    r'\bSalah\b': 'False',
    r'\bKosong\b': 'None',
}

# ==========================
# Translate kode .blo → Python
# ==========================
def translate_blo(kode_blo: str) -> str:
    kode_python = kode_blo

    # ganti keyword
    for pola, pengganti in KAMUS.items():
        kode_python = re.sub(pola, pengganti, kode_python)

    # otomatis tambahin () ke print jika lupa
    kode_python = re.sub(
        r'print\s+"([^"]+)"',
        r'print("\1")',
        kode_python
    )

    return kode_python


# ==========================
# Jalankan file .blo
# ==========================
def jalankan_blo(path: str, debug=False):
    with open(path, "r") as f:
        kode_blo = f.read()

    kode_python = translate_blo(kode_blo)

    if debug:
        print("=== HASIL TRANSLATE ===")
        print(kode_python)
        print("=======================")

    try:
        exec(kode_python, {})
    except Exception as e:
        print("❌ Error saat menjalankan .blo")
        print(e)
