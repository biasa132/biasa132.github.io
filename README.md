## Bahasa Lo - Ultimate REPL
Bahasa Lo adalah environment interaktif (REPL) berbasis Python yang dilengkapi dengan:
Interpreter file .blo
File Explorer ala Linux (ls, cd, cat)
Plugin system dengan auto-reload untuk plugin tertentu
Level akses: User, Admin
Integrasi proot-distro Linux (login langsung ke distro)
Sistem backup, download, dan manajemen package
Fitur Utama

# 0.Installation
``apt install python``

``git clone https://github.com/m29752885-glitch/Bahasa-lo.git cd Bahasa-lo``

``pip install -r requirements.txt``

``python main.py``
# 1.REPL Interaktif
Menjalankan perintah Python asli tanpa error.
Bisa menyimpan session dan variabel.
Interpreter .blo
Jalankan file .blo dengan command jalankan namafile.blo.
File Explorer Linux
ls : menampilkan isi folder saat ini
cd nama_folder : pindah folder
keluar_folder : kembali ke folder utama
cat nama_file : menampilkan isi file
Plugin System
Plugin tertentu akan auto-reload saat REPL dijalankan.
Plugin bisa diaktifkan manual via plugin -m.
Plugin tertentu bisa diaktifkan manual satu per satu.
# 2.Level Akses
User : akses terbatas, hanya folder tertentu (downloads).
Admin : akses penuh, bisa mengatur file system, plugin, repo, backup.
Proot-distro Linux
Command linux menampilkan distro yang tersedia.
Bisa login ke distro, install jika belum tersedia.
# 3.Backup & Download
Folder downloads untuk file luar rootfs
Folder packages untuk package dan hasil download
Folder backup untuk menyimpan backup penting
# 4.Command Dasar
Python Dasar
tulis <ekspresi> : mencetak output
<variabel> = <nilai> : assignment
jalankan <file.blo> : menjalankan file .blo
# 5.File Explorer
ls : list isi folder
cd <folder> : pindah folder
keluar_folder : kembali ke folder utama
cat <file> : baca isi file
# 6.Plugin
plugin -m : aktifkan plugin secara manual
plugin -i : reload plugin auto-reload
Admin Mode
Ketik admin, masukkan password 12345
Bisa mengakses semua folder dan file
Bisa menambahkan plugin, mengatur package, dan backup
# 7.Linux / proot-distro
Ketik linux untuk melihat distro yang tersedia
Pilih distro untuk login atau install jika belum ada
# 8.REPL Lain
Semua perintah shell Linux bisa dijalankan langsung (misal wget, curl, ping)
Exit session: keluar atau exit
# Catatan:
Folder penting:
downloads : file luar rootfs
packages : hasil install plugin / package
admin : file konfigurasi admin
backup : simpan file backup

Update?
# No aku lelah bikin script ini
