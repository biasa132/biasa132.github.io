# main.py – Ultimate Bahasa Lo REPL Final
import os, sys, time, pickle, subprocess

# ----------------------------
# Import config
# ----------------------------
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS, PROGRESS_SPEED

# ----------------------------
# Variabel global
# ----------------------------
variabel = {}
macros = {}
alias_perintah = {"Echo":"tulis"}
alias_keyword = {"jika":"if","apabila":"elif","Maka":":"}
log_file = "repl.log"
session_file = ".session"
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER,"plugins")
os.makedirs(PLUGINS_FOLDER, exist_ok=True)

current_folder = "."
prompt_str = "(+)> "
user_level = "user"  # user, root, admin

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
# Log
# ----------------------------
def log(cmd, output=""):
    with open(log_file,"a") as f:
        f.write(f"CMD> {cmd}\n{output}\n")

# ----------------------------
# Evaluasi ekspresi
# ----------------------------
def evaluasi_ekspresi(expr):
    for var in variabel:
        expr = expr.replace(var,str(variabel[var]))
    try:
        return eval(expr)
    except:
        return expr.strip('"')

# ----------------------------
# File Explorer
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        print(f"Folder '{folder}' tidak ada!")
        return
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        size = os.stat(path).st_size
        mtime = time.localtime(os.stat(path).st_mtime)
        mtime_str = time.strftime("%b %d %H:%M", mtime)
        if os.path.isdir(path):
            print(f"drwxr-xr-x       {mtime_str} {entry}")
        else:
            size_str = f"{size/1024:.1f}K" if size >=1024 else f"{size}B"
            print(f"-rw-r--r-- {size_str:>6} {mtime_str} {entry}")

# ----------------------------
# Proses perintah
# ----------------------------
def proses_baris(b):
    global current_folder, prompt_str, user_level
    b = b.strip()
    if b=="" or b.startswith("#"):
        return None

    # Admin mode
    if b.lower()=="admin":
        pwd = input("Masukkan password admin: ").strip()
        if pwd=="12345":
            user_level="admin"
            prompt_str="[Admin]> "
            print("Mode admin aktif!")
        else:
            print("Password salah!")
        return None

    # Keluar root/admin
    if b.lower() in ["keluar_root","keluar_admin"]:
        user_level="user"
        prompt_str="(+)> "
        print("Kembali ke mode user.")
        return None

    # Linux/proot-distro
    if b.lower()=="linux":
        if user_level=="user":
            print("Linux hanya untuk root/admin.")
            return None
        result = subprocess.getoutput("proot-distro list")
        print("Distro tersedia:")
        for line in result.splitlines():
            line = line.strip()
            if line.startswith("*"):
                print(f"{line[1:].strip()} (diinstal)")
            else:
                print(line)
        distro = input("Pilih distro: ").strip()
        if distro:
            subprocess.run(f"proot-distro login {distro}", shell=True)
        return None

    # Plugin system
    if b.startswith("plugin"):
        parts = b.split()
        if len(parts)==1:
            # Menu plugin
            plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
            if not plugins:
                print("Belum ada plugin.")
            else:
                print("Plugin tersedia:")
                for i,p in enumerate(plugins,1):
                    print(f"{i}. {p}")
            return None
        elif parts[1]=="-m":
            # Aktifkan plugin manual
            plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
            for i,p in enumerate(plugins,1):
                print(f"{i}. {p}")
            choice = input("Pilih plugin (nomor): ").strip()
            if choice.isdigit() and 1<=int(choice)<=len(plugins):
                try:
                    exec(open(os.path.join(PLUGINS_FOLDER,plugins[int(choice)-1])).read(), globals())
                    print(f"Plugin {plugins[int(choice)-1]} aktif!")
                except Exception as e:
                    print("Gagal aktifkan plugin:", e)
            return None

    # Jalankan file .blo
    if b.startswith("jalankan "):
        file = os.path.join(current_folder,b[8:].strip())
        if os.path.exists(file):
            try:
                exec(open(file).read(), globals())
            except Exception as e:
                print("Error menjalankan file:", e)
        else:
            print("File tidak ditemukan!")
        return None

    # Assignment
    if "=" in b:
        key,val = b.split("=",1)
        variabel[key.strip()]=evaluasi_ekspresi(val.strip())
        return None

    # Echo / tulis
    for a in alias_perintah:
        if b.startswith(a+" "):
            b=b.replace(a,alias_perintah[a],1)
    if b.startswith("tulis "):
        isi = b[6:].strip()
        out = evaluasi_ekspresi(isi)
        print(out)
        log(b,out)
        return None

    # File Explorer commands
    if b.startswith("ls"):
        folder = b[3:].strip() or current_folder
        list_files(folder)
        return None
    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder=="..":
            current_folder=os.path.dirname(current_folder)
        else:
            target = os.path.join(current_folder,folder)
            if os.path.exists(target) and os.path.isdir(target):
                current_folder=os.path.abspath(target)
            else:
                print("Folder tidak ditemukan!")
        return None
    if b.strip()=="keluar_folder":
        current_folder="."
        return None
    if b.startswith("cat "):
        file = os.path.join(current_folder,b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 10 {file}")
            print(out)
        else:
            print("File tidak ditemukan!")
        return None

    # Backup
    if b.strip()=="simpan":
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        target = os.path.join(BACKUP_FOLDER,f"backup_{timestamp}")
        os.makedirs(target, exist_ok=True)
        for folder in [DOWNLOADS_FOLDER, PACKAGES_FOLDER]:
            if os.path.exists(folder):
                subprocess.run(f"cp -r {folder} {target}/", shell=True)
        if os.path.exists(session_file):
            subprocess.run(f"cp {session_file} {target}/", shell=True)
        print(f"Backup selesai di {target}")
        return None

    # Bantuan
    if b.lower()=="bantuan":
        print("=== Menu Bantuan Bahasa Lo ===")
        print("Mode user/root/admin: user/root/admin")
        print("File Explorer: ls, cd <folder>, cat <file>, keluar_folder")
        print("Admin: admin, keluar_admin")
        print("Root: keluar_root, linux")
        print("Plugin: plugin, plugin -m")
        print("Backup: simpan")
        print("Jalankan file .blo: jalankan <file>.blo")
        return None

    # Eksekusi perintah shell
    try:
        if user_level!="user":
            subprocess.run(b,shell=True)
        else:
            print("Perintah shell hanya untuk root/admin.")
    except:
        print("Terjadi kesalahan menjalankan perintah.")
    return None

# ----------------------------
# REPL
# ----------------------------
def repl():
    print("\n=== Ultimate Bahasa Lo REPL Final ===")
    print("Ketik 'keluar' untuk keluar.")
    kode_multi=""
    global current_folder, prompt_str
    while True:
        if current_folder==".":
            prompt=prompt_str
        else:
            prompt=f"(+) / {os.path.basename(current_folder)}> " if prompt_str=="(+)> " else f"{prompt_str}{os.path.basename(current_folder)}> "
        baris=input(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        kode=proses_baris(baris)
        if kode:
            kode_multi+=kode+"\n"
        if kode_multi and not baris.strip().endswith(":"):
            try:
                exec(kode_multi, globals(), variabel)
            except Exception as e:
                print("Error:",e)
            kode_multi=""

if __name__=="__main__":
    repl()
