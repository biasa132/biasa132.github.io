# bahasalo_final.py - REPL Final Bahasa Lo + Mirror Repo Linux + Admin + Auto Install Package
import re
import subprocess
import time
import sys

# ----------------------------
# Fungsi progress bar sederhana
# ----------------------------
def progress_bar(task_name, duration=3):
    print(f"{task_name}...", end="")
    sys.stdout.flush()
    for i in range(20):
        print("█", end="")
        sys.stdout.flush()
        time.sleep(duration/20)
    print(" Done!")

# ----------------------------
# Install package jika perlu
# ----------------------------
def install_package(package_name):
    """Install package via apt tanpa crash"""
    try:
        print(f"\nMemeriksa package '{package_name}'...")
        subprocess.run(f"apt install -y {package_name}", shell=True)
        progress_bar(f"Installing {package_name}", 1)
    except Exception as e:
        print(f"Gagal install {package_name}: {e}")

required_packages = ["rsync", "apt-mirror", "git", "wget"]
for pkg in required_packages:
    install_package(pkg)

# ----------------------------
# REPL Bahasa Lo
# ----------------------------
variabel = {}
alias_perintah = {"Echo": "tulis"}
alias_keyword = {"jika": "if", "apabila": "elif", "Maka": ":"}

def evaluasi_ekspresi(ekspresi):
    for var in variabel:
        ekspresi = re.sub(r'\b' + var + r'\b', str(variabel[var]), ekspresi)
    try:
        return eval(ekspresi)
    except Exception:
        return ekspresi.strip('"')

def proses_baris(b):
    b = b.strip()
    if b == "" or b.startswith("#"):
        return None

    # Admin mode
    if b.lower() == "admin":
        password = input("Masukkan password admin: ").strip()
        if password == "rahasia123":  # password contoh
            print("Mode admin aktif! Pilih menu tweak:")
            print("1. Repo GitHub")
            print("2. Repo Linux")
            choice = input("Pilih opsi: ").strip()

            if choice == "1":
                repo_url = input("Masukkan URL GitHub repo: ").strip()
                print(f"Mengupdate/meng-clone repo {repo_url} ...")
                try:
                    subprocess.run(f"git clone {repo_url}", shell=True)
                except Exception as e:
                    print("Gagal update repo GitHub:", e)

            elif choice == "2":
                print("Menu Repo Linux:")
                print("1. Update paket")
                print("2. Mirror repo Linux")
                sub_choice = input("Pilih opsi: ").strip()
                if sub_choice == "1":
                    subprocess.run("apt update && apt upgrade -y", shell=True)
                elif sub_choice == "2":
                    repo_url = input("Masukkan URL repo (misal http://archive.ubuntu.com/ubuntu): ").strip()
                    local_folder = input("Masukkan folder tujuan mirror: ").strip()
                    print(f"Mulai mirror {repo_url} ke {local_folder} ...")
                    try:
                        subprocess.run(f"rsync -av --progress {repo_url} {local_folder}", shell=True)
                        print(f"Mirror selesai di {local_folder}")
                    except Exception as e:
                        print("Gagal mirror repo Linux:", e)
                else:
                    print("Opsi tidak valid")
            else:
                print("Opsi tidak valid")
        else:
            print("Password salah!")
        return None

    # Masuk ke proot-distro
    if b.lower() == "linux":
        print("Masuk ke menu proot-distro...")
        try:
            subprocess.run("proot-distro list", shell=True)
            distro = input("Pilih distro untuk login: ").strip()
            subprocess.run(f"proot-distro login {distro}", shell=True)
        except Exception as e:
            print("Gagal masuk proot-distro:", e)
        return None

    # Ganti alias perintah
    for a in alias_perintah:
        if b.startswith(a + " "):
            b = b.replace(a, alias_perintah[a], 1)

    # Ganti alias keyword
    for k in alias_keyword:
        b = re.sub(r'\b' + k + r'\b', alias_keyword[k], b)

    # Variabel assignment
    if "=" in b and not b.startswith("if") and not b.startswith("elif"):
        key, val = b.split("=", 1)
        key = key.strip()
        val = evaluasi_ekspresi(val.strip())
        variabel[key] = val
        return None

    # tulis perintah
    if b.startswith("tulis "):
        isi = b[6:].strip()
        print(evaluasi_ekspresi(isi))
        return None

    # Semua perintah Linux lainnya
    try:
        subprocess.run(b, shell=True)
    except Exception as e:
        print("Terjadi kesalahan:", e)
    return None

def repl():
    print("\nSelamat datang di Mini Bahasa Lo (REPL Final)")
    print("Ketik 'keluar' untuk keluar.")
    kode_multi = ""
    while True:
        prompt = "(+)> " if kode_multi == "" else "....> "
        baris = input(prompt)
        if baris.lower() in ["keluar", "exit"]:
            print("Bye!")
            break

        kode = proses_baris(baris)
        if kode:
            kode_multi += kode + "\n"

        if kode_multi and not baris.strip().endswith(":"):
            try:
                exec(kode_multi, globals(), variabel)
            except Exception as e:
                print("Error:", e)
            kode_multi = ""

if __name__ == "__main__":
    repl()
