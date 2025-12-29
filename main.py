# main.py
import os
import subprocess
import sys
from blo_interpreter import jalankan_blo
from blo_repl import repl_blo
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS
from plugin_loader import auto_reload_all, activate_single_plugin

# ==========================
# Level user
# ==========================
LEVEL_USER = "user"
LEVEL_ROOT = "root"
LEVEL_ADMIN = "admin"
user_level = LEVEL_USER

# ==========================
# Current working directory
# ==========================
cwd = os.getcwd()

# ==========================
# Helper Linux commands
# ==========================
def ls(args):
    path = args[0] if args else cwd
    try:
        for f in os.listdir(path):
            print(f)
    except Exception as e:
        print(f"❌ Error: {e}")

def cd(args):
    global cwd
    path = args[0] if args else os.path.expanduser("~")
    try:
        os.chdir(path)
        cwd = os.getcwd()
    except Exception as e:
        print(f"❌ Error: {e}")

def touch(args):
    for f in args:
        path = os.path.join(cwd, f)
        try:
            open(path, "a").close()
            print(f"✅ File {f} dibuat di {cwd}")
        except Exception as e:
            print(f"❌ Error: {e}")

def rm(args):
    for f in args:
        path = os.path.join(cwd, f)
        try:
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
            print(f"✅ {f} dihapus")
        except Exception as e:
            print(f"❌ Error: {e}")

# ==========================
# Masuk proot-distro
# ==========================
def masuk_linux():
    global user_level
    if user_level not in [LEVEL_ROOT, LEVEL_ADMIN]:
        print("❌ Hanya root/admin yang bisa masuk ke Linux")
        return

    try:
        print("=== Distro Proot-distro terinstall ===")
        result = subprocess.run(["proot-distro", "list"], capture_output=True, text=True)
        print(result.stdout)

        distro = input("Pilih distro untuk login: ").strip()
        if not distro:
            print("❌ Tidak ada distro dipilih")
            return

        print(f"✅ Login ke distro {distro} ...")
        os.environ["PROOT_PACKAGES"] = PACKAGES_FOLDER
        subprocess.run(["proot-distro", "login", distro])
    except FileNotFoundError:
        print("❌ proot-distro tidak ditemukan")
    except Exception as e:
        print(f"❌ Error masuk Linux: {e}")

# ==========================
# Menu bantuan
# ==========================
def bantuan():
    print("""
=== Bantuan Bahasa-lo ===
Command REPL:
- jalankan <file.blo> : jalankan file .blo
- linux              : masuk proot-distro (root/admin)
- cd <folder>        : ganti directory
- ls                 : list file
- touch <file>       : buat file
- rm <file>          : hapus file
- simpan             : backup semua file ke folder ./backup
- plugin -i          : auto reload plugin tertentu
- plugin -a <nama>   : aktifkan plugin manual
- admin              : masuk mode admin (password)
- keluar             : keluar dari REPL
""")

# ==========================
# Backup folder
# ==========================
def simpan():
    try:
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
        for f in os.listdir(cwd):
            src = os.path.join(cwd, f)
            dst = os.path.join(BACKUP_FOLDER, f)
            if os.path.isfile(src):
                import shutil
                shutil.copy(src, dst)
        print(f"✅ Backup selesai ke {BACKUP_FOLDER}")
    except Exception as e:
        print(f"❌ Error backup: {e}")

# ==========================
# Admin login
# ==========================
ADMIN_PASSWORD = "12345"

def masuk_admin():
    global user_level
    pw = input("Masukkan password admin: ")
    if pw == ADMIN_PASSWORD:
        user_level = LEVEL_ADMIN
        print("✅ Anda masuk mode ADMIN")
    else:
        print("❌ Password salah")

# ==========================
# REPL utama
# ==========================
def repl():
    global cwd, user_level
    auto_reload_all()
    print("=== Bahasa-lo REPL FINAL ===")
    while True:
        prompt = "(+)> " if user_level==LEVEL_USER else "[#]> " if user_level==LEVEL_ROOT else "{+}> "
        baris = input(prompt).strip()
        if not baris:
            continue
        cmd, *args = baris.split()

        # exit
        if cmd in ["keluar", "exit"]:
            print("Keluar dari REPL")
            break

        # REPL .blo
        elif cmd == "jalankan":
            if args:
                jalankan_blo(args[0])
            else:
                print("❌ Gunakan: jalankan <file.blo>")

        # Linux command
        elif cmd == "linux":
            masuk_linux()

        elif cmd == "cd":
            cd(args)
        elif cmd == "ls":
            ls(args)
        elif cmd == "touch":
            touch(args)
        elif cmd == "rm":
            rm(args)

        # backup
        elif cmd == "simpan":
            simpan()

        # bantuan
        elif cmd in ["bantuan", "help"]:
            bantuan()

        # plugin
        elif cmd == "plugin":
            if args and args[0]=="-i":
                auto_reload_all()
            elif args and args[0]=="-a" and len(args)>1:
                activate_single_plugin(args[1])
            else:
                print("❌ Plugin command tidak valid")

        # admin
        elif cmd == "admin":
            masuk_admin()

        else:
            print(f"❌ Command {cmd} tidak ditemukan")

# ==========================
# Jalankan REPL
# ==========================
if __name__ == "__main__":
    repl()
