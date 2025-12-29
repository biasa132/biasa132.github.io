# main.py - Bahasa-lo REPL Final
import os
import sys
import shutil
import importlib.util
from blo_interpreter import jalankan_blo
from config.pkg_config import DOWNLOADS_FOLDER, PACKAGES_FOLDER, ADMIN_FOLDER, BACKUP_FOLDER, progress_bar, LOADING_MSGS

# ----------------------------
# Plugins
# ----------------------------
PLUGINS_FOLDER = os.path.join(DOWNLOADS_FOLDER, "plugins")
AUTO_PLUGINS = ["Explorer_fix", "Optimasi", "crash_handle"]
loaded_plugins = {}

def load_plugin(nama_plugin):
    path_plugin = os.path.join(PLUGINS_FOLDER, f"{nama_plugin}.py")
    if not os.path.isfile(path_plugin):
        print(f"❌ Plugin {nama_plugin} tidak ditemukan di {PLUGINS_FOLDER}")
        return None
    spec = importlib.util.spec_from_file_location(nama_plugin, path_plugin)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    return plugin

# Load & auto reload plugin tertentu
for p in AUTO_PLUGINS:
    plugin_obj = load_plugin(p)
    if plugin_obj:
        loaded_plugins[p] = plugin_obj

# ----------------------------
# Path sekarang
# ----------------------------
current_path = os.getcwd()

# ----------------------------
# REPL Prompt level
# ----------------------------
LEVELS = {"user": "(+)> ", "root": "[#]> ", "admin": "{+}> "}
user_level = "user"

# ----------------------------
# Fungsi bantu Linux command
# ----------------------------
def cmd_cd(path):
    global current_path
    try:
        target = os.path.abspath(os.path.join(current_path, path))
        if os.path.isdir(target):
            current_path = target
        else:
            print(f"❌ Folder tidak ditemukan: {path}")
    except Exception as e:
        print(f"❌ Error cd: {e}")

def cmd_ls():
    try:
        print("\n".join(os.listdir(current_path)))
    except Exception as e:
        print(f"❌ Error ls: {e}")

def cmd_mkdir(name):
    try:
        os.makedirs(os.path.join(current_path, name), exist_ok=True)
    except Exception as e:
        print(f"❌ Error mkdir: {e}")

def cmd_touch(name):
    try:
        open(os.path.join(current_path, name), "a").close()
    except Exception as e:
        print(f"❌ Error touch: {e}")

def masuk_linux():
    if user_level not in ["root", "admin"]:
        print("❌ Hanya root/admin bisa masuk Linux")
        return
    # TODO: list proot-distro, pilih distro, login
    print("🖥️ Masuk Linux (proot-distro) - sementara demo")

# ----------------------------
# Fungsi jalankan .blo
# ----------------------------
def cmd_jalankan(file_name):
    path = os.path.join(current_path, file_name)
    if not os.path.isfile(path):
        print(f"❌ File tidak ditemukan: {file_name}")
        return
    jalankan_blo(path)

# ----------------------------
# Admin menu
# ----------------------------
def admin_menu():
    global user_level
    pwd = input("Masukkan password admin: ")
    if pwd != "12345":
        print("❌ Password salah")
        return
    user_level = "admin"
    print("✅ Admin mode aktif")
    while True:
        cmd = input(LEVELS[user_level])
        if cmd in ["keluar", "exit"]:
            user_level = "user"
            print("🔹 Kembali ke mode user")
            break
        elif cmd.startswith("plugin -i "):
            plugin_name = cmd.split(" ")[-1]
            pl = load_plugin(plugin_name)
            if pl:
                loaded_plugins[plugin_name] = pl
                print(f"✅ Plugin {plugin_name} aktif")
        else:
            print(f"❌ Perintah admin belum terimplementasi: {cmd}")

# ----------------------------
# Menu bantuan
# ----------------------------
def menu_bantuan():
    print("""
=== Bantuan Bahasa-lo ===
Command REPL:
  cd <folder>       : pindah folder
  ls                : list file/folder
  mkdir <folder>    : buat folder
  touch <file>      : buat file kosong
  jalankan <file>   : jalankan file .blo
  linux             : masuk Linux (root/admin)
  admin             : masuk mode admin
  simpan <file>     : backup file
  keluar            : keluar REPL
""")

# ----------------------------
# REPL
# ----------------------------
def repl():
    global current_path
    print("=== Bahasa-lo REPL FINAL ===")
    while True:
        try:
            # Auto reload plugin tertentu
            for p in AUTO_PLUGINS:
                if loaded_plugins.get(p):
                    importlib.reload(loaded_plugins[p])

            cmd_input = input(LEVELS[user_level])
            if not cmd_input.strip():
                continue
            parts = cmd_input.strip().split()
            cmd = parts[0]
            args = parts[1:]

            if cmd == "cd" and args:
                cmd_cd(args[0])
            elif cmd == "ls":
                cmd_ls()
            elif cmd == "mkdir" and args:
                cmd_mkdir(args[0])
            elif cmd == "touch" and args:
                cmd_touch(args[0])
            elif cmd == "jalankan" and args:
                cmd_jalankan(args[0])
            elif cmd == "linux":
                masuk_linux()
            elif cmd == "admin":
                admin_menu()
            elif cmd == "bantuan":
                menu_bantuan()
            elif cmd in ["keluar", "exit"]:
                print("👋 Keluar dari REPL")
                break
            else:
                print(f"❌ Perintah tidak dikenal: {cmd_input}")
        except KeyboardInterrupt:
            print("\n🔹 Tekan 'keluar' untuk keluar REPL")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    repl()
