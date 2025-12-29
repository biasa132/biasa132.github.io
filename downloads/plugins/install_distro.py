# install_distro.py
import os
import subprocess
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, progress_bar, LOADING_MSGS

def install_distro():
    print("=== Plugin: Install Distro (Proot-distro) ===")
    subprocess.run("proot-distro list", shell=True)
    distro = input("Masukkan nama distro yang ingin diinstall: ").strip()
    if not distro:
        print("Distro tidak valid!")
        return
    print(LOADING_MSGS.get("install_pkg","Menginstall package..."))
    progress_bar("Menginstall distro")
    try:
        subprocess.run(f"proot-distro install {distro}", shell=True)
        print(f"Distro '{distro}' berhasil diinstall!")
        # Simpan hasil install ke packages
        pkg_path = os.path.join(PACKAGES_FOLDER, distro)
        os.makedirs(pkg_path, exist_ok=True)
        print(f"File distro '{distro}' tersimpan di {pkg_path}")
    except Exception as e:
        print("Gagal install distro:", e)

# Auto run ketika plugin diaktifkan
if __name__=="__main__":
    install_distro()
