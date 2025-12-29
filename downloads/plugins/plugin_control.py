# Plugin: More Control
# Menambahkan command plugin -c untuk kontrol plugin lebih lanjut

def plugin_control():
    print("=== Plugin Control Menu ===")
    plugins = [f for f in os.listdir(PLUGINS_FOLDER) if f.endswith(".py")]
    if not plugins:
        print("Belum ada plugin.")
        return
    
    # Tampilkan status tiap plugin
    for i, p in enumerate(plugins, 1):
        status = "Aktif" if plugin_status.get(p, True) else "Nonaktif"
        print(f"{i}. {p} [{status}]")
    
    pilihan = input("Pilih plugin (nomor) untuk kontrol: ").strip()
    if pilihan.isdigit() and 1 <= int(pilihan) <= len(plugins):
        p_name = plugins[int(pilihan)-1]
        print(f"Kontrol plugin: {p_name}")
        opsi = input("Opsi (aktif/nonaktif/reload/manual): ").strip().lower()
        
        if opsi == "aktif":
            reload_plugin(p_name)
        elif opsi == "nonaktif":
            plugin_status[p_name] = False
            print(f"Plugin '{p_name}' dinonaktifkan.")
        elif opsi == "reload":
            reload_plugin(p_name)
        elif opsi == "manual":
            # Jalankan plugin satu kali tanpa auto-reload
            try:
                exec(open(os.path.join(PLUGINS_FOLDER, p_name)).read(), globals())
                print(f"Plugin '{p_name}' dijalankan manual!")
            except Exception as e:
                print("Gagal menjalankan plugin manual:", e)
        else:
            print("Opsi tidak valid.")

# Bind ke REPL
macros["plugin -c"] = "plugin_control()"
