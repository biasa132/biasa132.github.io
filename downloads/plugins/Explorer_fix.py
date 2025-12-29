# file_explorer_fix.py
# Plugin untuk memperbaiki File Explorer di Bahasa-lo REPL
# Autor: Auto Generated
# ----------------------------

import os

def safe_list_files(folder=None):
    """Menampilkan daftar file/folder dengan pengecekan aman"""
    folder = folder or os.getcwd()
    if not os.path.exists(folder):
        print(f"Folder '{folder}' tidak ada!")
        return
    try:
        entries = os.listdir(folder)
    except PermissionError:
        print(f"Permission denied: tidak bisa mengakses {folder}")
        return
    for entry in entries:
        path = os.path.join(folder, entry)
        if os.path.isdir(path):
            print(f"drwxr-xr-x {entry}")
        else:
            try:
                size = os.stat(path).st_size
            except Exception:
                size = 0
            print(f"-rw-r--r-- {size} {entry}")

def safe_cd(target, current_folder):
    """CD aman, menangani .. dan folder yang tidak ada"""
    if target=="..":
        new_folder = os.path.dirname(current_folder)
    elif target=="/":
        new_folder = os.getcwd()  # tetap di REPL root folder
    else:
        new_folder = os.path.join(current_folder, target)
    if os.path.exists(new_folder) and os.path.isdir(new_folder):
        return os.path.abspath(new_folder)
    else:
        print(f"Folder '{target}' tidak ditemukan!")
        return current_folder

def safe_pwd(current_folder):
    """Menampilkan folder saat ini dengan aman"""
    print(current_folder)

# ----------------------------
# Override REPL functions
# ----------------------------
try:
    globals()['list_files'] = safe_list_files
    globals()['cd'] = safe_cd
    globals()['pwd'] = safe_pwd
    print("Plugin File Explorer loaded: CD, LS, PWD aman.")
except Exception as e:
    print("Gagal load plugin File Explorer:", e)
