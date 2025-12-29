# Ultimate REPL v13 – Full Bahasa Indonesia
import os, sys, re, time, pickle, subprocess

# ----------------------------
# Progress bar sederhana
# ----------------------------
def progress_bar(tugas, durasi=1):
    print(f"{tugas}...", end="")
    sys.stdout.flush()
    for _ in range(20):
        print("█", end="")
        sys.stdout.flush()
        time.sleep(durasi/20)
    print(" Selesai!")

# ----------------------------
# Setup global
# ----------------------------
variabel = {}
alias_perintah = {"Echo":"tulis"}
alias_keyword = {
    "jika":"if", "apabila":"elif", "Maka":":",
    "selesai":"pass", "ulang":"for", "selama":"while",
    "fungsi":"def", "kembalikan":"return", "coba":"try",
    "kecuali":"except", "impor":"import", "dari":"from",
    "sebagai":"as", "kelas":"class", "dengan":"with",
    "lambda":"lambda", "hentikan":"break", "lanjut":"continue",
    "global":"global", "nonlokal":"nonlocal"
}
macros = {}
log_file = "repl.log"
session_file = ".session"
downloads_folder = "./downloads"
plugins_folder = os.path.join(downloads_folder,"plugins")
os.makedirs(downloads_folder, exist_ok=True)
os.makedirs(plugins_folder, exist_ok=True)
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
# Log function
# ----------------------------
def log(cmd, output=""):
    with open(log_file,"a") as f:
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
# File manager versi Linux vibes
# ----------------------------
def list_files(folder=None):
    folder = folder or current_folder
    if not os.path.exists(folder):
        print(f"Folder '{folder}' tidak ada!")
        return
    for entry in os.listdir(folder):
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
# Proses baris REPL
# ----------------------------
def proses_baris(b):
    b = b.strip()
    if b=="" or b.startswith("#"):
        return None

    global current_folder, prompt_str

    # Admin mode
    if b.lower() == "admin":
        password = input("Masukkan password admin: ").strip()
        if password=="rahasia123":
            print("Mode admin aktif! Pilih menu tweak:")
            print("1. Repo GitHub\n2. Repo Linux")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                repo = input("Masukkan URL GitHub repo: ").strip()
                out_dir = os.path.join(downloads_folder, repo.split("/")[-1].replace(".git",""))
                print(f"Clone/update {repo} ke {out_dir} ...")
                subprocess.run(f"git clone {repo} {out_dir}", shell=True)
            elif choice=="2":
                print("1. Update paket\n2. Mirror repo Linux")
                sub = input("Pilih opsi: ").strip()
                if sub=="1":
                    subprocess.run("apt update && apt upgrade -y", shell=True)
                elif sub=="2":
                    repo_url = input("Masukkan URL repo: ").strip()
                    folder = input("Folder tujuan mirror: ").strip()
                    subprocess.run(f"rsync -av --progress {repo_url} {folder}", shell=True)
                    print(f"Mirror selesai di {folder}")
        else:
            print("Password salah!")
        return None

    # Plugin system
    if b.startswith("plugin"):
        if b.strip() == "plugin -m":
            plugins = [f for f in os.listdir(plugins_folder) if f.endswith(".py")]
            if not plugins:
                print("Belum ada plugin.")
            else:
                print("Plugin tersedia:")
                for i,p in enumerate(plugins,1):
                    print(f"{i}. {p}")
                choice = input("Pilih plugin (nomor): ").strip()
                if choice.isdigit() and 1<=int(choice)<=len(plugins):
                    plugin_path = os.path.join(plugins_folder, plugins[int(choice)-1])
                    print(f"Mengaktifkan plugin {plugins[int(choice)-1]} ...")
                    try:
                        exec(open(plugin_path).read(), globals())
                        print("Plugin aktif!")
                    except Exception as e:
                        print("Gagal aktifkan plugin:", e)
        elif b.strip() == "plugin":
            print("Menu Plugin:")
            print("1. Buat file plugin sendiri")
            print("2. Upload dari GitHub")
            choice = input("Pilih opsi: ").strip()
            if choice=="1":
                filename = input("Nama file plugin (.py): ").strip()
                path = os.path.join(plugins_folder, filename)
                with open(path,"w") as f:
                    f.write("# Plugin baru\n")
                print(f"Plugin {filename} berhasil dibuat di {plugins_folder}")
            elif choice=="2":
                url = input("Masukkan URL GitHub plugin (.py): ").strip()
                out_file = os.path.join(plugins_folder, url.split("/")[-1])
                print(f"Download dari {url} ke {out_file} ...")
                subprocess.run(f"wget -O {out_file} {url}", shell=True)
                print(f"Plugin tersimpan di {out_file}")
        return None

    # Ganti alias perintah & keyword bahasa Indonesia
    for a in alias_perintah:
        if b.startswith(a+" "):
            b = b.replace(a,alias_perintah[a],1)
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
        print(evaluasi_ekspresi(isi))
        return None

    # CD
    if b.startswith("cd "):
        folder = b[3:].strip()
        if folder=="..":
            current_folder = os.path.dirname(current_folder)
        else:
            target = os.path.join(current_folder, folder)
            if os.path.isdir(target):
                current_folder = os.path.abspath(target)
            else:
                print(f"Folder '{folder}' tidak ada!")
        return None

    # Shortcut keluar folder
    if b.strip() == "keluar_folder":
        current_folder = "."
        return None

    # ls
    if b.startswith("ls"):
        list_files(current_folder)
        return None

    # cat
    if b.startswith("cat "):
        file = os.path.join(current_folder, b[4:].strip())
        if os.path.exists(file):
            out = subprocess.getoutput(f"head -n 10 {file}")
            print(out)
        else:
            print(f"File '{file}' tidak ada!")
        return None

    # jalankan file .blo
    if b.startswith("jalankan "):
        fname = os.path.join(current_folder, b[8:].strip())
        if os.path.exists(fname):
            with open(fname,"r") as f:
                kode = f.read()
            try:
                for a in alias_perintah:
                    kode = kode.replace(a,alias_perintah[a])
                for k in alias_keyword:
                    kode = re.sub(r'\b'+k+r'\b',alias_keyword[k],kode)
                exec(kode, globals(), variabel)
            except Exception as e:
                print("Error menjalankan file:", e)
        else:
            print(f"File {fname} tidak ada!")
        return None

    # Backup
    if b.strip()=="simpan":
        backup_folder = "./backup"
        os.makedirs(backup_folder, exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        target = os.path.join(backup_folder, f"backup_{timestamp}")
        os.makedirs(target, exist_ok=True)
        for folder in [downloads_folder, plugins_folder]:
            if os.path.exists(folder):
                subprocess.run(f"rsync -a {folder} {target}/", shell=True)
        if os.path.exists(session_file):
            subprocess.run(f"cp {session_file} {target}/", shell=True)
        print(f"Backup selesai! Tersimpan di {target}")
        return None

    # Root mode
    if b.strip()=="root -a":
        prompt_str = "[Root]> "
        print("Prompt REPL sekarang menjadi [Root]>")
        return None

    # Bantuan
    if b.lower()=="bantuan":
        print("Alias perintah:", alias_perintah)
        print("Keyword:", alias_keyword)
        print("Macros:", list(macros.keys()))
        print("Admin menu: admin")
        print("File/Network: ls, cat")
        print("Plugin: plugin, plugin -m")
        print("File management: pindah <nama_file> <folder_tujuan>")
        print("Backup: simpan")
        print("Root mode: root -a")
        print("Change folder: cd <folder>, cd .., cd /, keluar_folder")
        print("Jalankan file: jalankan <file.blo>")
        return None

    # Semua command Linux lain
    try:
        subprocess.run(b, shell=True, cwd=current_folder)
    except:
        print("Terjadi kesalahan menjalankan:", b)
    return None

# ----------------------------
# REPL loop
# ----------------------------
def repl():
    global current_folder, prompt_str
    print("\n=== Ultimate Bahasa Lo REPL v13 ===")
    print("Ketik 'keluar' untuk keluar")
    while True:
        if current_folder==".":
            prompt = "[Root]> " if prompt_str.startswith("[Root]") else "(+)> "
        else:
            prompt = f"[Root]/{os.path.basename(current_folder)}> " if prompt_str.startswith("[Root]") else f"(+) / {os.path.basename(current_folder)}> "
        baris = input(prompt)
        if baris.lower() in ["keluar","exit"]:
            with open(session_file,"wb") as f:
                pickle.dump({"variabel":variabel,"macros":macros},f)
            print("Session tersimpan. Bye!")
            break
        proses_baris(baris)

if __name__=="__main__":
    repl()
