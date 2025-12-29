import os, subprocess, sys, time

from config.pkg_config import (
    DOWNLOADS_FOLDER,
    PACKAGES_FOLDER,
    ADMIN_FOLDER,
    BACKUP_FOLDER,
    PLUGINS_FOLDER,
    progress_bar
)

# =============================
# Alias Python Bahasa Indonesia
# =============================
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

# =============================
# Status sistem
# =============================
LEVEL = "user"   # user | admin | root
FOLDER_AKTIF = os.getcwd()

# =============================
# Plugin loader (auto reload)
# =============================
def muat_plugin():
    untuk file in os.listdir(PLUGINS_FOLDER):
        jika file.endswith(".py"):
            coba:
                exec(open(os.path.join(PLUGINS_FOLDER, file)).read(), globals())
            kecuali Exception sebagai e:
                tulis(f"[Plugin error] {file} -> {e}")

# =============================
# Prompt
# =============================
def prompt():
    jika LEVEL == "user":
        return "(+)> "
    jika LEVEL == "admin":
        return "[ADMIN]> "
    jika LEVEL == "root":
        return "[ROOT]> "

# =============================
# Menu bantuan
# =============================
def bantuan():
    tulis("""
Perintah dasar:
  bantuan          → tampilkan bantuan
  linux            → masuk proot-distro
  ls               → lihat isi folder
  cd <folder>      → masuk folder
  admin            → masuk admin mode
  root             → masuk root mode
  keluar           → keluar REPL

Alias Python:
  tulis() masukan() bulat() pecahan()
  Benar Salah Kosong
""")

# =============================
# Admin mode
# =============================
def masuk_admin():
    global LEVEL
    sandi = masukan("Password admin: ")
    jika sandi == "12345":
        LEVEL = "admin"
        tulis("Admin mode aktif")
    lainnya:
        tulis("Password salah")

# =============================
# Root mode
# =============================
def masuk_root():
    global LEVEL
    LEVEL = "root"
    tulis("Root mode aktif")

# =============================
# Linux (proot-distro)
# =============================
def linux_menu():
    hasil = subprocess.getoutput("proot-distro list")
    data = {}

    tulis("\nDistro tersedia:")
    untuk baris in hasil.splitlines():
        jika baris.startswith("*"):
            nama = baris[1:].strip()
            tulis(f"- {nama} (diinstal)")
            data[nama] = Benar
        elif baris.strip():
            tulis(f"- {baris.strip()}")
            data[baris.strip()] = Salah

    pilih = masukan("Pilih distro: ").strip()
    jika pilih == "":
        kembalikan

    jika data.get(pilih) == Salah:
        progress_bar("Menginstall distro")
        subprocess.run(f"proot-distro install {pilih}", shell=True)

    tulis("Login ke distro...")
    subprocess.run(f"proot-distro login {pilih}", shell=True)

# =============================
# File explorer
# =============================
def ls():
    untuk f in os.listdir("."):
        tulis(f)

def cd(folder):
    global FOLDER_AKTIF
    coba:
        os.chdir(folder)
        FOLDER_AKTIF = os.getcwd()
    kecuali:
        tulis("Folder tidak ditemukan")

# =============================
# REPL
# =============================
def repl():
    muat_plugin()
    tulis("\n=== Ultimate Bahasa-Lo REPL ===")
    bantuan()

    selama Benar:
        perintah = masukan(prompt()).strip()

        jika perintah == "":
            lanjutkan
        jika perintah == "keluar":
            break
        jika perintah == "bantuan":
            bantuan()
        elif perintah == "linux":
            linux_menu()
        elif perintah == "ls":
            ls()
        elif perintah.startswith("cd "):
            cd(perintah[3:])
        elif perintah == "admin":
            masuk_admin()
        elif perintah == "root":
            masuk_root()
        lainnya:
            subprocess.run(perintah, shell=True)

# =============================
# Start
# =============================
jika __name__ == "__main__":
    repl()
