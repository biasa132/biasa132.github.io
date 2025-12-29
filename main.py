# main.py – Ultimate Bahasa Lo REPL Final

import os, sys, subprocess, time, pickle
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# ----------------------------
# Global
# ----------------------------
variabel = {}
macros = {}
session_file = ".session"
current_folder = "."
prompt_str = "(+)> "
LEVEL = "user"  # user/root/admin
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER, "plugins")
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# ----------------------------
# Plugin auto reload
# ----------------------------
AUTO_RELOAD_PLUGINS = ["Explorer_fix.py","Optimasi.py","crash_handle.py"]
LOADED_PLUGINS = set()

def load_plugin(plugin_file):
    path = os.path.join(PLUGINS_FOLDER, plugin_file)
    if os.path.exists(path) and plugin_file not in LOADED_PLUGINS:
        try:
            exec(open(path).read(), globals())
            LOADED_PLUGINS.add(plugin_file)
        except Exception as e:
            print(f"Gagal load plugin {plugin_file}: {e}")

# Load plugin auto reload saat start
for plugin in AUTO_RELOAD_PLUGINS:
    load_plugin(plugin)

# ----------------------------
# Load session
# ----------------------------
if os.path.exists(session_file):
    try:
        with open(session_file,"rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel",{}))
            macros.update(data.get("macros",{}))
        print("Session sebelumnya berhasil dimuat.")
    except:
        print("Gagal load session, lanjut.")

# ----------------------------
# Helper functions
# ----------------------------
def tulis(x): print(x)
def masukan(x): return input(x)
def bulat(x): return int(x)
def pecahan(x): return float(x)
def panjang(x): return len(x)
def daftar(x): return list(x)
def kamus(x): return dict(x)
Benar = True
Salah = False
Kosong = None

# ----------------------------
# File Explorer
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        tulis(f"Folder '{folder}' tidak ada!")
        return
    entries = os.listdir(folder)
    for entry in entries:
        path = os.path.join(folder, entry)
        stat = os.stat(path)
        size = stat.st_size
        mtime = time.localtime(stat.st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            tulis(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size>=1024 else f"{size}B"
            tulis(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Proses baris input
# ----------------------------
def proses_baris(b):
    global prompt_str, current_folder, LEVEL
    b = b.strip()
    if b=="" or b.startswith("#"): return

    # Admin mode
    if b.lower()=="admin":
        password = masukan("Masukkan password admin: ").strip()
        if password=="12345":
            LEVEL="admin"
            prompt_str="[Admin]> "
            tulis("Admin mode aktif!")
        else:
            tulis("Password salah!")
        return

    # Root mode
    if b.lower()=="root":
        LEVEL="root"
        prompt_str="[Root]> "
        tulis("Root mode aktif!")
        return

    if b.lower()=="keluar_root":
        LEVEL="user"
        prompt_str="(+)> "
        tulis("Kembali ke user mode.")
        return

    # File explorer
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return
    if b.startswith("cd "):
        folder = b[3:].strip()
        target = os.path.join(current_folder, folder)
        if os.path.isdir(target):
            current_folder = os.path.abspath(target)
        else:
            tulis(f"Folder '{folder}' tidak ditemukan!")
        return
    if b.strip()=="keluar_folder":
        current_folder="."
        return
    if b.startswith("cat "):
        file = os.path.join(current_folder, b[4:].strip())
        if os.path.exists(file):
            tulis(subprocess.getoutput(f"head -n 10 {file}"))
        else:
            tulis(f"File '{file}' tidak ditemukan!")
        return

    # Backup
    if b.strip()=="simpan":
        backup_folder = BACKUP_FOLDER
        os.makedirs(backup_folder, exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        target = os.path.join(backup_folder, f"backup_{timestamp}")
        os.makedirs(target, exist_ok=True)
        for folder in [DOWNLOADS_FOLDER, PACKAGES_FOLDER, PLUGINS_FOLDER]:
            if os.path.exists(folder):
                subprocess.run(f"rsync -a {folder} {target}/", shell=True)
        if os.path.exists(session_file):
            subprocess.run(f"cp {session_file} {target}/", shell=True)
        tulis(f"Backup selesai di {target}")
        return

    # Plugin manual activation
    if b.startswith("plugin -i"):
        plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
        if not plugins:
            tulis("Belum ada plugin.")
        else:
            for i, p in enumerate(plugins,1): tulis(f"{i}. {p}")
            choice = masukan("Pilih plugin untuk aktifkan (nomor): ").strip()
            if choice.isdigit() and 1<=int(choice)<=len(plugins):
                load_plugin(plugins[int(choice)-1])
                tulis(f"Plugin {plugins[int(choice)-1]} aktif.")
        return

    # Jalankan file .blo
    if b.startswith("jalankan "):
        file = b[9:].strip()
        path = os.path.join(current_folder, file)
        if os.path.exists(path):
            try: exec(open(path).read(), globals())
            except Exception as e: tulis(f"Gagal jalankan {file}: {e}")
        else: tulis(f"File {file} tidak ditemukan!")
        return

    # Bantuan
    if b.lower()=="bantuan":
        tulis("Command dasar:")
        tulis("ls, cd <folder>, keluar_folder, cat <file>")
        tulis("simpan (backup), plugin -i (aktifkan plugin manual)")
        tulis("jalankan <file.blo>, admin, root, keluar_root")
        tulis("Keluar REPL: keluar/exit")
        return

    # Semua perintah lain dijalankan sebagai shell
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
    except:
        tulis("Terjadi kesalahan menjalankan perintah.")

# ----------------------------
# REPL
# ----------------------------
def repl():
    tulis("\n=== Ultimate Bahasa Lo REPL ===")
    tulis("Ketik 'bantuan' untuk melihat command.")
    kode_multi=""
    global current_folder
    while True:
        if current_folder==".":
            prompt = prompt_str
        else:
            prompt = f"{prompt_str}{os.path.basename(current_folder)}> "
        baris = masukan(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            tulis("Session tersimpan. Bye!")
            break
        proses_baris(baris)

if __name__=="__main__":
    repl()
