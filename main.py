# main.py - Ultimate Bahasa Lo REPL Final
import os, sys, subprocess, time, pickle
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# ----------------------------
# Alias bahasa Indonesia untuk REPL / .blo
# ----------------------------
tulis = print
masukan = input
bulat = int
pecahan = float
panjang = len
daftar = list
kamus = dict
Benar = True
Salah = False
Kosong = None

# ----------------------------
# Global REPL variables
# ----------------------------
variabel = {}
macros = {}
session_file = ".session"
current_folder = "."
prompt_str = "(+)> "
PLUGINS_FOLDER = "./downloads/plugins"
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

# ----------------------------
# Load session
# ----------------------------
if os.path.exists(session_file):
    try:
        with open(session_file, "rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel", {}))
            macros.update(data.get("macros", {}))
        tulis("Session sebelumnya berhasil dimuat.")
    except:
        tulis("Gagal load session, lanjutkan.")

# ----------------------------
# Plugin auto reload
# ----------------------------
for file in os.listdir(PLUGINS_FOLDER):
    if file.endswith(".py"):
        try:
            exec(open(os.path.join(PLUGINS_FOLDER, file)).read(), globals())
        except Exception as e:
            tulis(f"Gagal load plugin {file}: {e}")

# ----------------------------
# Fungsi log
# ----------------------------
log_file = "repl.log"
def log(cmd, output=""):
    with open(log_file, "a") as f:
        f.write(f"CMD> {cmd}\n{output}\n")

# ----------------------------
# File Explorer
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        tulis(f"Folder '{folder}' tidak ada!")
        return
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        size = os.stat(path).st_size
        mtime = time.localtime(os.stat(path).st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            tulis(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size >= 1024 else f"{size}B"
            tulis(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Proses perintah
# ----------------------------
def proses_baris(b):
    global current_folder, prompt_str
    b = b.strip()
    if b == "" or b.startswith("#"):
        return None

    # Bantuan
    if b.lower() == "bantuan":
        tulis("Menu Bantuan:")
        tulis("- Alias Python: tulis, masukan, bulat, pecahan, panjang, daftar, kamus")
        tulis("- REPL commands: ls, cat <file>, cd <folder>, cd .., cd /, keluar_folder")
        tulis("- Linux/Proot-distro: linux")
        tulis("- Plugin: plugin, plugin -m (auto reload)")
        tulis("- File management: pindah <file> <folder>")
        tulis("- Backup: simpan")
        tulis("- Root mode: root -a")
        tulis("- Admin mode: admin")
        return None

    # Admin
    if b.lower() == "admin":
        password = masukan("Masukkan password admin: ").strip()
        if password == "12345":
            tulis("Admin mode aktif! Prompt menjadi [Admin]>")
            prompt_str = "[Admin]> "
            return None
        else:
            tulis("Password salah!")
            return None

    # Root mode
    if b.strip() == "root -a":
        prompt_str = "[Root]> "
        tulis("Prompt REPL sekarang menjadi [Root]>")
        return None

    # File explorer
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
                tulis(f"Folder '{folder}' tidak ditemukan!")
        return None

    if b.strip() == "keluar_folder":
        current_folder = "."
        return None

    if b.startswith("cat "):
        file = os.path.join(current_folder, b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 20 {file}")
            tulis(out)
            log(b, out)
        else:
            tulis(f"File '{file}' tidak ditemukan!")
        return None

    # Jalankan file .blo
    if b.startswith("jalankan "):
        file = b[9:].strip()
        path = os.path.join(current_folder, file)
        if os.path.exists(path):
            try:
                with open(path) as f:
                    kode = f.read()
                    exec(kode, globals(), variabel)
            except Exception as e:
                tulis(f"Error menjalankan {file}: {e}")
        else:
            tulis(f"File '{file}' tidak ditemukan!")
        return None

    # Assignment
    if "=" in b:
        key, val = b.split("=", 1)
        variabel[key.strip()] = eval(val.strip())
        return None

    # print dan input asli
    if b.startswith("print "):
        isi = b[6:].strip()
        out = eval(isi)
        tulis(out)
        log(b, out)
        return None

    if b.startswith("input "):
        isi = b[6:].strip()
        result = masukan(isi)
        log(b, result)
        return result

    # Linux / Proot-distro
    if b.lower() == "linux":
        tulis("Menu Proot-distro:")
        subprocess.run("proot-distro list", shell=True)
        distro = masukan("Pilih distro: ").strip()
        if distro:
            tulis(f"Login ke {distro}...")
            subprocess.run(f"proot-distro login {distro}", shell=True)
        return None

    # Eksekusi command Linux lain
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
        log(b)
    except Exception as e:
        tulis(f"Terjadi kesalahan menjalankan: {b}\n{e}")
    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    tulis("\n=== Ultimate Bahasa Lo REPL ===")
    tulis("Ketik 'keluar' untuk keluar, 'bantuan' untuk bantuan.")
    while True:
        prompt = prompt_str if current_folder == "." else f"{prompt_str}{os.path.basename(current_folder)}> "
        baris = masukan(prompt)
        if baris.lower() in ["keluar", "exit"]:
            with open(session_file, "wb") as f:
                pickle.dump({"variabel": variabel, "macros": macros}, f)
            tulis("Session tersimpan. Bye!")
            break
        proses_baris(baris)

if __name__ == "__main__":
    repl()
