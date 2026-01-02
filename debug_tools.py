# debug_tools.py
DEBUG_MODE = True  # True = aktifkan debug, False = nonaktifkan

def debug_log(msg):
    """Cetak pesan debug jika DEBUG_MODE True"""
    if DEBUG_MODE:
        print(f"[DEBUG] {msg}")

def cetak(msg):
    """Cetak biasa"""
    print(msg)
  
