# main.py – Ultimate Bahasa Lo REPL Final v7
import os, sys, time, subprocess, pickle, re
from config import pkg_config as cfg

# ----------------------------
# Setup global
# ----------------------------
variabel = {}
macros = {}
alias_perintah = {"Echo":"tulis"}
alias_keyword = {"jika":"if","apabila":"elif","Maka":":"}
session_file = ".session"
prompt_str = "(+)> "
current_folder = "."

# ----------------------------
# Load session sebelumnya
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
# Logging
# ----------------------------
def log(cmd, output=""):
    with open("repl.log","a") as f:
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
# File manager Linux vibes
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
            print(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size >= 1024 else f"{size}B"
            print(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Ganti 'print' jadi 'tulis' di Python
# ----------------------------
def tulis(isi):
    out = evaluasi_ekspresi(isi)
    print(out)
    log("tulis "+isi,str(out))

# ----------------------------
# Input
# ----------------------------
def masukkan(prompt="> "):
    return input(prompt)

# ----------------------------
# Proses perintah
# ----------------------------
def proses_baris(b):
    b = b.strip()
    if b=="" or b.startswith("#"):
        return None

    global prompt_str, current_folder

    # Admin mode
    if b.lower()=="admin":
        password = masukkan("Masukkan password admin: ").strip()
        if password=="rahasia123":
            tulis("Mode admin aktif! Pilih menu tweak:")
            tulis("1. Repo GitHub\n2. Repo Linux")
            choice = masukkan("Pilih opsi: ").strip()
            if choice=="1":
                repo = masukkan("Masukkan URL GitHub repo: ").strip()
                out_dir = os.path.join(cfg.DOWNLOADS_FOLDER, repo.split("/")[-1].replace(".git",""))
                tulis(f"Clone/update {repo} ke {out_dir} ...")
                subprocess.run(f"git clone {repo} {out_dir}", shell=True)
            elif choice=="2":
                tulis("1. Update paket\n2. Mirror repo Linux")
                sub = masukkan("Pilih opsi: ").strip()
                if sub=="1":
                    subprocess.run("apt update && apt upgrade -y", shell=True)
                elif sub=="2":
                    repo_url = masukkan("Masukkan URL repo: ").strip()
                    folder = masukkan("Folder tujuan mirror: ").strip()
                    subprocess.run(f"rsync -av --progress {repo_url} {folder}", shell=True)
                    tulis(f"Mirror selesai di {folder}")
        else:
            tulis("Password salah!")
        return None

    # Plugin system
    if b.startswith("plugin"):
        plugins_folder = os.path.join(cfg.DOWNLOADS_FOLDER,"plugins")
        os.makedirs(plugins_folder, exist_ok=True)
        if b.strip()=="plugin -m":
            plugins = [f for f in os.listdir(plugins_folder) if f.endswith(".py")]
            if not plugins:
                tulis("Belum ada plugin.")
            else:
                tulis("Plugin tersedia:")
                for i,p in enumerate(plugins,1):
                    tulis(f"{i}. {p}")
                choice = masukkan("Pilih plugin untuk aktifkan (nomor): ").strip()
                if choice.isdigit() and 1<=int(choice)<=len(plugins):
                    plugin_path = os.path.join(plugins_folder,plugins[int(choice)-1])
                    tulis(f"Mengaktifkan plugin {plugins[int(choice)-1]} ...")
                    try:
                        exec(open(plugin_path).read(), globals())
                        tulis("Plugin aktif!")
                    except Exception as e:
                        tulis(f"Gagal aktifkan plugin: {e}")
        elif b.strip()=="plugin":
            tulis("Menu Plugin:\n1. Buat file plugin sendiri\n2. Upload dari GitHub")
            choice = masukkan("Pilih opsi: ").strip()
            if choice=="1":
                filename = masukkan("Nama file plugin (.py): ").strip()
                path = os.path.join(plugins_folder, filename)
                with open(path,"w") as f:
                    f.write("# Plugin baru\n")
                tulis(f"Plugin {filename} berhasil dibuat di folder {plugins_folder}")
            elif choice=="2":
                url = masukkan("Masukkan URL GitHub plugin (.py): ").strip()
                out_file = os.path.join(plugins_folder, url.split("/")[-1])
                tulis(f"Download dari {url} ke {out_file} ...")
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
                tulis(f"Plugin tersimpan di {out_file}")
        return None

    # Jalankan file .blo
    if b.startswith("jalankan "):
        file = os.path.join(current_folder,b[8:].strip())
        if os.path.exists(file):
            tulis(f"Menjalankan {file} ...")
            with open(file,"r") as f:
                kode = f.read()
                try:
                    exec(kode, globals(), variabel)
                except Exception as e:
                    tulis(f"Error: {e}")
        else:
            tulis(f"File '{file}' tidak ditemukan!")
        return None

    # File explorer
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None
    if b.startswith("cat "):
        file = os.path.join(current_folder,b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 10 {file}")
            tulis(out)
            log(b,out)
        else:
            tulis(f"File '{file}' tidak ditemukan!")
        return None
    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder=="/":
            current_folder="."
        else:
            target_path = os.path.join(current_folder, folder)
            if os.path.exists(target_path) and os.path.isdir(target_path):
                current_folder = os.path.abspath(target_path)
            else:
                tulis(f"Folder '{folder}' tidak ditemukan!")
        return None
    if b.strip()=="keluar_folder":
        current_folder="."
        return None

    # Root mode
    if b.strip()=="root -a":
        prompt_str="[Root]> "
        tulis("Prompt REPL sekarang menjadi [Root]>")
        return None

    # Backup
    if b.strip()=="simpan":
        os.makedirs(cfg.BACKUP_FOLDER, exist_ok=True)
        ts = time.strftime("%Y%m%d-%H%M%S")
        target = os.path.join(cfg.BACKUP_FOLDER,f"backup_{ts}")
        os.makedirs(target, exist_ok=True)
        for folder in [cfg.DOWNLOADS_FOLDER, cfg.PACKAGES_FOLDER]:
            if os.path.exists(folder):
                subprocess.run(f"rsync -a {folder} {target}/", shell=True)
        if os.path.exists(session_file):
            subprocess.run(f"cp {session_file} {target}/", shell=True)
        tulis(f"Backup selesai! Tersimpan di {target}")
        return None

    # Proot-distro login
    if b.lower()=="linux":
        tulis("Memeriksa proot-distro...")
        result = subprocess.getoutput("proot-distro list")
        lines = result.splitlines()
        distro_status={}
        tulis("Distro tersedia:")
        for line in lines:
            line=line.strip()
            if line.startswith("*"):
                name=line[1:].strip()
                tulis(f"{name} (diinstal)")
                distro_status[name]=True
            elif line:
                tulis(line)
                distro_status[line]=False
        distro=masukkan("Pilih distro: ").strip()
        if distro:
            if not distro_status.get(distro,False):
                tulis(f"Distro {distro} belum diinstall. Menginstall sekarang...")
                subprocess.run(f"proot-distro install {distro}", shell=True)
                tulis(f"{distro} selesai diinstall!")
            tulis(f"Login ke {distro} ...")
            subprocess.run(f"proot-distro login {distro} --bind ./packages:/usr/local/packages", shell=True)
        return None

    # Assignment
    if "=" in b and not b.startswith("if") and not b.startswith("elif"):
        key,val=b.split("=",1)
        variabel[key.strip()]=evaluasi_ekspresi(val.strip())
        return None

    # Tulisan
    for a in alias_perintah:
        if b.startswith(a+" "):
            b=b.replace(a,alias_perintah[a],1)
    for k in alias_keyword:
        b=re.sub(r'\b'+k+r'\b', alias_keyword[k], b)

    # Semua command Linux lain
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
        log(b)
    except:
        tulis("Terjadi kesalahan menjalankan:",b)
    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    tulis("\n=== Ultimate Bahasa Lo REPL Final v7 ===")
    tulis("Ketik 'keluar' untuk keluar.")
    global current_folder, prompt_str
    kode_multi=""
    while True:
        if current_folder==".":
            prompt="[Root]> " if prompt_str.startswith("[Root]") else "(+)> "
        else:
            prompt=f"[Root]/{os.path.basename(current_folder)}> " if prompt_str.startswith("[Root]") else f"(+) / {os.path.basename(current_folder)}> "
        baris=masukkan(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            tulis("Session tersimpan. Bye!")
            break

        kode=proses_baris(baris)
        if kode:
            kode_multi+=kode+"\n"

        if kode_multi and not baris.strip().endswith(":"):
            try:
                exec(kode_multi, globals(), variabel)
            except Exception as e:
                tulis("Error:",e)
            kode_multi=""

if __name__=="__main__":
    repl()
