# download_manager.py
# ==========================
# Plugin Bahasa-lo: download manager
# Semua hasil download di luar proot-distro masuk ke ./downloads
# ==========================

import os
import subprocess
from config.pkg_config import DOWNLOADS_FOLDER

def download_file(url, method="wget"):
    """
    method: wget / curl / git
    """
    os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
    filename = url.split("/")[-1]
    path = os.path.join(DOWNLOADS_FOLDER, filename)

    try:
        if method.lower() == "wget":
            subprocess.run(["wget", url, "-O", path])
        elif method.lower() == "curl":
            subprocess.run(["curl", "-L", url, "-o", path])
        elif method.lower() == "git":
            subprocess.run(["git", "clone", url, path])
        else:
            print(f"❌ Method {method} tidak dikenali")
            return
        print(f"✅ Download selesai: {path}")
    except Exception as e:
        print(f"❌ Error saat download: {e}")

# ==========================
# Fungsi untuk REPL/plugin
# ==========================
def jalankan(args):
    if not args:
        print("❌ Gunakan: download <url> [wget/curl/git]")
        return
    url = args[0]
    method = args[1] if len(args) > 1 else "wget"
    download_file(url, method)
