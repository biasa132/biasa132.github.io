# main.py - Ultimate Bahasa-Lo REPL v7
import os, sys, time, re, pickle, subprocess
from config.pkg_config import *

# ----------------------------
# Global
# ----------------------------
variabel = {}
macros = {}
prompt_str = "(+)> "
current_folder = "."
MODE_ADMIN = False
MODE_ROOT = False
session_file = ".session"

# ----------------------------
# Load session sebelumnya
# ----------------------------
if os.path.exists(session_file):
    try:
        with open(session_file, "rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel", {}))
            macros.update(data.get("macros", {}))
        print("Session sebelumnya berhasil dimuat.")
    except:
        print("Gagal load session, lanjut.")

# ----------------------------
# Log
# ----------------------------
log_file = "repl.log"
def log(cmd, output=""):
    with open(log_file,"a") as f:
        f.write(f"CMD> {cmd}\n{output}\n")

# ----------------------------
# Evaluasi ekspresi
# ----------------------------
def evaluasi_ekspresi(expr):
    for var in variabel:
        expr = re.sub(r'\b'+var+r'\b', str(variabel[var]), expr)
    try:
        return eval(expr)
    except:
        return expr.strip('"')

# ----------------------------
# File Explorer Linux vibes
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        print(f"Folder '{folder}' tidak ada!")
        return
    entries = os.listdir(folder)
    for entry in entries:
        path = os.path.join(folder, entry)
        stat = os.stat(path)
        size = stat.st_size
        mtime = time.localtime(stat.st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            print(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size >= 1024 else f"{size}B"
            print(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Admin menu
# ----------------------------
def menu_admin():
    global MODE_ADMIN
    password = input("Masukkan password admin: ").strip()
    if password == "12345":
        MODE_ADMIN = True
        print("[ADMIN]> Mode aktif!")
        print("1. Kelola repo")
        print("2. Kelola filesystem")
        print("3. Kelola plugin")
        choice = input("Pilih menu: ").strip()
        # tambahan fungsi sesuai menu nanti
    else:
        print("Password salah!")

# ----------------------------
# Proses baris
# ----------------------------
def proses_baris(b):
    global prompt_str, current_folder, MODE_ADMIN, MODE_ROOT

    b = b.strip()
    if b == "" or b.startswith("#"):
        return None

    # Admin
    if b.lower() == "admin":
        menu_admin()
        return None

    # Root
    if b.strip() == "root -a":
        MODE_ROOT = True
        prompt_str = "[Root]> "
        print("Prompt REPL sekarang menjadi [Root]>")
        return None

    # File Explorer
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None

    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder == "/":
            current_folder = "."
        else:
            target_path = os.path.join(current_folder, folder)
            if os.path.exists(target_path) and os.path.isdir(target_path):
                current_folder = os.path.abspath(target_path)
            else:
                print(f"Folder '{folder}' tidak ditemukan!")
        return None

    if b.strip() == "keluar_folder":
        current_folder = "."
        return None

    if b.startswith("cat "):
        file = os.path.join(current_folder, b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 10 {file}")
            print(out)
            log(b,out)
        else:
            print(f"File '{file}' tidak ditemukan!")
        return None

    # Jalankan .blo
    if b.startswith("jalankan "):
        nama_file = os.path.join(current_folder, b[8:].strip())
        if os.path.exists(nama_file):
            try:
                with open(nama_file) as f:
                    kode = f.read()
                exec(kode, globals(), variabel)
            except Exception as e:
                print("Error:", e)
        else:
            print(f"File '{nama_file}' tidak ditemukan!")
        return None

    # Macro execution
    if b in macros:
        subprocess.run(macros[b], shell=True)
        return None

    # Assignment
    if "=" in b and not b.startswith("jika") and not b.startswith("apabila"):
        key,val = b.split("=",1)
        variabel[key.strip()] = evaluasi_ekspresi(val.strip())
        return None

    # Tulis
    if b.startswith("tulis "):
        isi = b[6:].strip()
        out = evaluasi_ekspresi(isi)
        print(out)
        log(b,out)
        return None

    # Semua command Linux lain
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
        log(b)
    except:
        print("Terjadi kesalahan menjalankan:", b)
    return None

# ----------------------------
# Bantuan
# ----------------------------
def menu_bantuan():
    print("Alias perintah: tulis")
    print("Keyword: jika, apabila, Maka")
    print("Macros: <nama_macro>")
    print("Admin menu: admin")
    print("Root mode: root -a")
    print("File/Network: ls, cd, cat, ping, curl, wget, git")
    print("Plugin: plugin, plugin -m")
    print("File management: pindah <file> <folder>, keluar_folder")
    print("Backup: simpan")
    print("Roles: User, Root, Admin")

# ----------------------------
# REPL
# ----------------------------
def repl():
    print("\n=== Ultimate Bahasa-Lo REPL v7 ===")
    print("Ketik 'keluar' untuk keluar, 'bantuan' untuk help.")
    global current_folder, prompt_str

    while True:
        if current_folder == ".":
            prompt = prompt_str
        else:
            prompt = f"{prompt_str[:-1]} / {os.path.basename(current_folder)}> "
        baris = input(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        if baris.lower() == "bantuan":
            menu_bantuan()
            continue
        proses_baris(baris)

if __name__=="__main__":
    repl()
