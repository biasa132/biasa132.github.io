# Bahasa-Lo REPL FINAL v5

Ultimate REPL interaktif dengan sintaks **Bahasa Indonesia**. Semua command Python diubah agar ramah pemula.

---

## Fitur Utama

- Prompt interaktif:
  - `(+)>` → user
  - `[Root]>` → root
- **Bahasa Indonesia alias Python**:
  - `print` → `tulis`
  - `input` → `masukan`
  - `int` → `bulat`
  - `float` → `pecahan`
  - `len` → `panjang`
  - `list` → `daftar`
  - `dict` → `kamus`
  - `for` → `untuk`
  - `if` → `jika`
  - `elif` → `apabila`
  - `else` → `lainnya`
  - `def` → `fungsi`
  - `return` → `kembalikan`
  - `True/False/None` → `Benar/Salah/Kosong`
- **Admin Menu**: `admin` → tweak GitHub atau repo Linux
- **Proot-distro**: `linux` → list, install, login distro Linux
- **Plugin system**: `plugin`, `plugin -m`
- **File Explorer**: `ls`, `cat <file>`, `cd <folder>`, `keluar_folder`, `pindah <file> <folder>`
- **Downloads** otomatis ke folder `downloads/`
- **Backup**: `simpan` → backup `downloads`, `plugins`, `.session`
- **Root mode**: `root -a` → ubah prompt menjadi `[Root]>`
- **Jalankan file .blo**: `jalankan <nama_file>.blo`

---

## Catatan
Semua file yang di-download (git, wget, curl) masuk ke folder downloads/
Plugins tersimpan di downloads/plugins/
Backup tersimpan di backup/ dengan timestamp
Password admin default: rahasia123

## Contoh Kode

```Script
tulis "Halo dunia!"
x = 5
jika x > 3 Maka:
    tulis "x lebih dari 3"

fungsi halo():
    tulis "Halo semua!"
halo()
# Loop & input
nama = masukan("Masukkan nama: ")
untuk i dalam jangkauan(3):
    tulis "Halo " + nama + " ke-" + str(i+1)```
