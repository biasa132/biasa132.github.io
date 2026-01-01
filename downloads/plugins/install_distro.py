# install_distro.py
# Plugin install & kelola proot-distro untuk Bahasa-lo

import os
import subprocess

def _jalankan(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print("❌ Gagal menjalankan perintah:", cmd)
        print(e)

def cek_proot_distro():
    print("🔍 Mengecek proot-distro...")
    hasil = subprocess.getoutput("which proot-distro")
    if hasil.strip() == "":
        print("⚠️ proot-distro belum terpasang")
        print("📥 Menginstall proot-distro...")
        _jalankan("pkg install proot-distro -y")
    else:
        print("✅ proot-distro sudah terpasang")

def daftar_distro():
    print("\n📜 Daftar distro tersedia:")
    _jalankan("proot-distro list")

def daftar_distro_terpasang():
    print("\n📦 Distro terinstall:")
    _jalankan("proot-distro list --installed")

def install_distro():
    nama = input("\n🧩 Masukkan nama distro (contoh: ubuntu): ").strip()
    if not nama:
        print("❌ Nama distro kosong")
        return
    print(f"📥 Menginstall distro: {nama}")
    _jalankan(f"proot-distro install {nama}")

def masuk_distro():
    nama = input("\n🚀 Masuk ke distro: ").strip()
    if not nama:
        print("❌ Nama distro kosong")
        return

    # pastikan folder packages
    os.makedirs("./downloads/packages", exist_ok=True)

    print(f"🔑 Login ke {nama}")
    print("📦 Semua download diarahkan ke ./downloads/packages")
    os.system(
        f'PROOT_TMP_DIR=./downloads/packages proot-distro login {nama}'
    )

def menu_install_distro():
    while True:
        print("""
=== Plugin Install Distro (proot-distro) ===
1. Cek / Install proot-distro
2. Lihat daftar distro tersedia
3. Lihat distro terpasang
4. Install distro
5. Masuk ke distro
6. Keluar
""")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            cek_proot_distro()
        elif pilih == "2":
            daftar_distro()
        elif pilih == "3":
            daftar_distro_terpasang()
        elif pilih == "4":
            install_distro()
        elif pilih == "5":
            masuk_distro()
        elif pilih == "6":
            print("Keluar dari plugin install distro")
            break
        else:
            print("❌ Pilihan tidak valid")

# AUTO EKSEKUSI (sesuai sistem plugin Bahasa-lo)
menu_install_distro()
