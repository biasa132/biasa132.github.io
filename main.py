# main.py - Ultimate Bahasa Lo REPL Remastered
import os, sys, time, pickle, subprocess, re
from config import pkg_config as cfg

# ----------------------------
# Global Variables
# ----------------------------
variabel = {}
macros = {}

# Python alias ke bahasa Indonesia
cetak = print
masukkan = input
panjang = len
rentang = range
teks = str
bilangan_bulat = int
bilangan_desimal = float
daftar = list
kamus = dict

alias_perintah = {"Echo":"tulis"}
alias_keyword = {"jika":"if","apabila":"elif","Maka":":"}

log_file = "repl.log"
session_file = ".session"

current_folder = "."  # folder aktif
in_rootfs = False     # sedang di rootfs
prompt_str = "(+)> "

# ----------------------------
# Load session
# ----------------------------
if os.path.exists(session_file):
    try:
        with open(session_file,"rb") as f:
            data = pickle.load(f)
            variabel.update(data.get("variabel",{}))
            macros.update(data.get("macros",{}))
        cetak("Session sebelumnya berhasil dimuat.")
    except:
        cetak("Gagal load session, lanjut.")

# ----------------------------
# Logging
# ----------------------------
def log(cmd, output=""):
    with open(log_file,"a") as f:
        f.write(f"CMD> {cmd}\n{output}\n")

# ----------------------------
# Evaluasi ekspresi
# ----------------------------
def evaluasi_ekspresi(expr):
    alias_dict = {
        "cetak":"print",
        "masukkan":"input",
        "panjang":"len",
        "rentang":"range",
        "teks":"str",
        "bilangan_bulat":"int",
        "bilangan_desimal":"float",
        "daftar":"list",
        "kamus":"dict"
    }
    for k, v in alias_dict.items():
        expr = re.sub(r'\b'+k+r'\b', v, expr)
    for var in variabel:
        expr = re.sub(r'\b'+var+r'\b', str(variabel[var]), expr)
    try:
        return eval(expr)
    except:
        return expr.strip('"')

# ----------------------------
# File Manager
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        cetak(f"Folder '{folder}' tidak ada!")
        return
    entries = os.listdir(folder)
    for entry in entries:
        path = os.path.join(folder, entry)
        stat = os.stat(path)
        size = stat.st_size
        mtime = time.localtime(stat.st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            cetak(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size >= 1024 else f"{size}B"
            cetak(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Proses Baris
# ----------------------------
def proses_baris(b):
    global current_folder, prompt_str, in_rootfs

    b = b.strip()
    if b == "" or b.startswith("#"):
        return None

    # Admin menu
    if b.lower() == "admin":
        password = masukkan("Masukkan password admin: ").strip()
        if password == "rahasia123":
            cetak("Mode admin aktif! Pilih menu tweak:")
            cetak("1. Repo GitHub\n2. Repo Linux / RootFS")
            choice = masukkan("Pilih opsi: ").strip()
            if choice=="1":
                repo = masukkan("Masukkan URL GitHub repo: ").strip()
                out_dir = os.path.join(cfg.DOWNLOADS_FOLDER, repo.split("/")[-1].replace(".git",""))
                cetak(f"Clone/update {repo} ke {out_dir} ...")
                subprocess.run(f"git clone {repo} {out_dir}", shell=True)
            elif choice=="2":
                cetak("RootFS langsung dipakai, fitur tweak tambahan bisa ditambahkan.")
        else:
            cetak("Password salah!")
        return None

    # RootFS login langsung
    if b.lower() == "linux":
        if not os.path.exists(cfg.ROOTFS_FOLDER):
            cetak("RootFS belum ada. Silakan download dan extract rootfs manual dulu.")
            return None
        cetak(cfg.LOADING_MSGS["login_rootfs"])
        in_rootfs = True
        subprocess.run(f"proot -S {cfg.ROOTFS_FOLDER} /bin/bash", shell=True)
        return None

    # Plugin system
    if b.startswith("plugin"):
        plugins_folder = os.path.join(cfg.PACKAGES_FOLDER, "plugins")
        os.makedirs(plugins_folder, exist_ok=True)
        if b.strip() == "plugin -m":
            plugins = [f for f in os.listdir(plugins_folder) if f.endswith(".py")]
            if not plugins:
                cetak("Belum ada plugin.")
            else:
                cetak("Plugin tersedia:")
                for i, p in enumerate(plugins, 1):
                    cetak(f"{i}. {p}")
                choice = masukkan("Pilih plugin untuk aktifkan (nomor): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(plugins):
                    plugin_path = os.path.join(plugins_folder, plugins[int(choice)-1])
                    try:
                        exec(open(plugin_path).read(), globals())
                        cetak("Plugin aktif!")
                    except Exception as e:
                        cetak("Gagal aktifkan plugin:", e)
            return None
        elif b.strip() == "plugin":
            cetak("Menu Plugin:")
            cetak("1. Buat file plugin sendiri")
            cetak("2. Upload dari GitHub")
            choice = masukkan("Pilih opsi: ").strip()
            if choice == "1":
                filename = masukkan("Nama file plugin (.py): ").strip()
                path = os.path.join(plugins_folder, filename)
                with open(path, "w") as f:
                    f.write("# Plugin baru\n")
                cetak(f"Plugin {filename} berhasil dibuat di folder {plugins_folder}")
            elif choice == "2":
                url = masukkan("Masukkan URL GitHub plugin (.py): ").strip()
                out_file = os.path.join(plugins_folder, url.split("/")[-1])
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
                cetak(f"Plugin tersimpan di {out_file}")
            return None

    # Macro execution
    if b in macros:
        subprocess.run(macros[b], shell=True)
        return None

    # Alias perintah & keyword
    for a in alias_perintah:
        if b.startswith(a+" "):
            b = b.replace(a, alias_perintah[a], 1)
    for k in alias_keyword:
        b = re.sub(r'\b'+k+r'\b', alias_keyword[k], b)

    # Assignment
    if "=" in b and not b.startswith("if") and not b.startswith("elif"):
        key,val = b.split("=",1)
        variabel[key.strip()] = evaluasi_ekspresi(val.strip())
        return None

    # tulis
    if b.startswith("tulis "):
        isi = b[6:].strip()
        out = evaluasi_ekspresi(isi)
        cetak(out)
        log(b,out)
        return None

    # CD
    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder == "/":
            current_folder = "."
        else:
            target_path = os.path.join(current_folder, folder)
            if os.path.exists(target_path) and os.path.isdir(target_path):
                current_folder = os.path.abspath(target_path)
            else:
                cetak(f"Folder '{folder}' tidak ditemukan!")
        return None

    if b.strip() == "keluar_folder":
        current_folder = "."
        return None

    # File explorer
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None
    if b.startswith("cat "):
        file = os.path.join(current_folder, b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 10 {file}")
            cetak(out)
            log(b,out)
        else:
            cetak(f"File '{file}' tidak ditemukan!")
        return None

    # Network tools
    if b.startswith("ping "):
        host = b[5:].strip()
        subprocess.run(f"ping -c 4 {host}", shell=True)
        return None
    if b.startswith("curl "):
        url = b[5:].strip()
        filename = url.split("/")[-1]
        out_file = os.path.join(cfg.DOWNLOADS_FOLDER, filename)
        cetak(f"Download {url} ke {out_file} ...")
        subprocess.run(f"curl -o {out_file} {url}", shell=True)
        return None
    if b.startswith("git "):
        repo_url = b[4:].strip()
        repo_name = repo_url.split("/")[-1].replace(".git","")
        out_dir = os.path.join(cfg.DOWNLOADS_FOLDER, repo_name)
        cetak(f"Cloning {repo_url} ke {out_dir} ...")
        subprocess.run(f"git clone {repo_url} {out_dir}", shell=True)
        return None
    if b.startswith("wget "):
        url = b[5:].strip()
        filename = url.split("/")[-1]
        out_file = os.path.join(cfg.DOWNLOADS_FOLDER, filename)
        cetak(f"Download {url} ke {out_file} ...")
        subprocess.run(f"wget -O {out_file} {url}", shell=True)
        return None

    # Jalankan .blo
    if b.startswith("jalankan "):
        file_blo = os.path.join(current_folder, b[8:].strip())
        if os.path.exists(file_blo):
            try:
                with open(file_blo) as f:
                    kode = f.read()
                    exec(kode, globals(), variabel)
            except Exception as e:
                cetak("Error jalankan .blo:", e)
        else:
            cetak(f"File '{file_blo}' tidak ditemukan!")
        return None

    # Semua command lain
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
        log(b)
    except:
        cetak("Terjadi kesalahan menjalankan:", b)
    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    cetak("\n=== Ultimate Bahasa Lo REPL Remastered ===")
    cetak("Ketik 'keluar' untuk keluar.")
    kode_multi=""
    global current_folder, prompt_str
    while True:
        if current_folder == ".":
            prompt = "[Root]> " if prompt_str.startswith("[Root]") else "(+)> "
        else:
            prompt = f"[Root]/{os.path.basename(current_folder)}> " if prompt_str.startswith("[Root]") else f"(+) / {os.path.basename(current_folder)}> "
        baris = masukkan(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            cetak("Session tersimpan. Bye!")
            break

        kode = proses_baris(baris)
        if kode:
            kode_multi += kode+"\n"

        if kode_multi and not baris.strip().endswith(":"):
            try:
                exec(kode_multi, globals(), variabel)
            except Exception as e:
                cetak("Error:", e)
            kode_multi = ""

if __name__=="__main__":
    repl()
