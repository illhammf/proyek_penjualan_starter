# Sistem Manajemen Penjualan Toko

Proyek akhir mata kuliah Bahasa Pemrograman untuk Kelompok 7.

Aplikasi ini merupakan sistem manajemen penjualan toko berbasis desktop yang dibuat menggunakan Python, Tkinter, SQLite, dan konsep Object-Oriented Programming.

## Deskripsi Proyek

Sistem Manajemen Penjualan Toko membantu proses pengelolaan data produk, data pelanggan, transaksi penjualan, pembayaran, stok, dan laporan penjualan.

Aplikasi berjalan sebagai aplikasi desktop. Pengguna dapat menjalankannya langsung melalui Python tanpa server web dan tanpa koneksi internet.

## Fitur Utama

- Mengelola data produk.
- Menambah, mengubah, dan menghapus produk.
- Mengelola harga dan stok produk.
- Mengelola data pelanggan.
- Menambah, mengubah, dan menghapus pelanggan.
- Menyimpan poin pelanggan.
- Membuat transaksi penjualan.
- Menambahkan beberapa produk ke keranjang.
- Menghitung subtotal dan total belanja.
- Memproses pembayaran.
- Menghitung uang kembalian.
- Mengurangi stok secara otomatis setelah transaksi berhasil.
- Menampilkan struk transaksi.
- Menyimpan riwayat transaksi.
- Menampilkan laporan penjualan.
- Menghitung total pendapatan toko.

## Teknologi yang Digunakan

- Python
- Tkinter
- ttk
- SQLite
- Modul standar Python

Proyek ini tidak memerlukan library eksternal.

## Konsep Object-Oriented Programming

Proyek menerapkan konsep utama OOP berikut.

### 1. Class dan Object

Class utama yang digunakan:

- `Person`
- `Kasir`
- `Pelanggan`
- `Produk`
- `Penjualan`
- `Toko`

Setiap class digunakan untuk membuat object sesuai kebutuhan sistem.

### 2. Inheritance

Class `Kasir` dan `Pelanggan` merupakan turunan dari class `Person`.

```python
class Kasir(Person):
    pass


class Pelanggan(Person):
    pass
```

### 3. Encapsulation

Atribut dalam class menggunakan atribut private atau protected. Data diakses dan diubah melalui getter dan setter.

```python
def get_nama(self):
    return self.__nama


def set_nama(self, nama):
    self.__nama = nama
```

### 4. Polymorphism

Method `tampilkan_info()` pada class `Person` dioverride oleh class turunannya.

```python
class Person:
    def tampilkan_info(self):
        return "Informasi Person"


class Kasir(Person):
    def tampilkan_info(self):
        return "Informasi Kasir"
```

### 5. Composition

Class `Penjualan` memiliki object dari class lain, seperti:

- Object `Kasir`
- Object `Pelanggan`
- Object `Produk`

Class `Toko` juga menyimpan kumpulan object produk, kasir, pelanggan, dan penjualan.

### 6. Constructor

Setiap class menggunakan constructor `__init__()` untuk memberikan nilai awal pada object.

## Struktur Folder

```text
proyek_penjualan/
├── data/
│   └── toko.db
├── database.py
├── gui.py
├── main.py
├── models.py
└── README.md
```

Keterangan:

- `main.py` merupakan file utama untuk menjalankan aplikasi.
- `gui.py` berisi tampilan dan interaksi antarmuka Tkinter.
- `models.py` berisi seluruh class OOP.
- `database.py` berisi pengelolaan database SQLite.
- `data/toko.db` menyimpan data produk, pelanggan, dan transaksi.
- `README.md` berisi dokumentasi singkat proyek.

## Persyaratan Sistem

- Python 3.10 atau versi yang lebih baru direkomendasikan.
- Sistem operasi Windows, Linux, atau macOS.
- Tkinter harus tersedia pada instalasi Python.
- SQLite tersedia melalui modul standar Python.

## Cara Menjalankan Program

### 1. Buka folder proyek

Buka folder proyek menggunakan Visual Studio Code.

### 2. Buka terminal

Di Visual Studio Code, pilih menu:

```text
Terminal > New Terminal
```

Pastikan terminal berada di folder proyek.

### 3. Jalankan aplikasi

Gunakan salah satu perintah berikut:

```bash
python main.py
```

Pada Windows, perintah berikut juga dapat digunakan:

```bash
py main.py
```

## Data Kasir Awal

Aplikasi menggunakan data kasir awal berikut:

```text
ID Kasir : KSR001
Nama     : Admin Kasir
Telepon  : 081234567890
Username : admin
Password : admin123
```

Catatan: Pada versi saat ini, data kasir aktif dibuat langsung melalui kode program. Halaman login dapat ditambahkan pada pengembangan berikutnya.

## Cara Menggunakan Aplikasi

### Data Produk

1. Buka tab `Data Produk`.
2. Isi kode produk.
3. Isi nama produk.
4. Isi harga.
5. Isi stok.
6. Tekan tombol `Simpan`.

Untuk mengubah data:

1. Pilih produk pada tabel.
2. Ubah data pada form.
3. Tekan tombol `Ubah`.

Untuk menghapus data:

1. Pilih produk pada tabel.
2. Tekan tombol `Hapus`.
3. Konfirmasi penghapusan.

### Data Pelanggan

1. Buka tab `Data Pelanggan`.
2. Isi ID pelanggan.
3. Isi nama pelanggan.
4. Isi nomor telepon.
5. Isi poin pelanggan.
6. Tekan tombol `Simpan`.

Data pelanggan dapat diubah dan dihapus melalui tombol yang tersedia.

### Transaksi Penjualan

1. Buka tab `Transaksi`.
2. Pilih pelanggan atau gunakan pelanggan umum.
3. Pilih produk.
4. Isi jumlah pembelian.
5. Tekan tombol `Tambah ke Keranjang`.
6. Ulangi langkah tersebut untuk produk lain.
7. Periksa total belanja.
8. Isi jumlah pembayaran.
9. Tekan tombol `Proses Pembayaran`.

Setelah transaksi berhasil:

- Data transaksi disimpan ke database.
- Stok produk berkurang.
- Uang kembalian dihitung.
- Struk transaksi ditampilkan.
- Data laporan diperbarui.

Format pembayaran yang dapat digunakan:

```text
50000
50.000
Rp50.000
```

### Laporan Penjualan

1. Buka tab `Laporan`.
2. Tekan tombol `Muat Ulang` jika diperlukan.
3. Riwayat transaksi akan ditampilkan.
4. Total pendapatan akan dihitung secara otomatis.

## Alur Sistem

```text
Kasir memilih pelanggan
        ↓
Kasir memilih produk
        ↓
Produk ditambahkan ke keranjang
        ↓
Sistem menghitung total
        ↓
Kasir memasukkan pembayaran
        ↓
Sistem memeriksa jumlah pembayaran
        ↓
Transaksi disimpan
        ↓
Stok produk dikurangi
        ↓
Struk dan laporan ditampilkan
```

## Validasi Data

Aplikasi melakukan beberapa validasi:

- Kode produk tidak boleh kosong.
- Nama produk tidak boleh kosong.
- Harga harus berupa angka.
- Harga tidak boleh bernilai negatif.
- Stok harus berupa bilangan bulat.
- ID pelanggan tidak boleh kosong.
- Jumlah pembelian harus lebih dari nol.
- Jumlah pembelian tidak boleh melebihi stok.
- Keranjang tidak boleh kosong saat pembayaran.
- Jumlah pembayaran harus berupa angka.
- Jumlah pembayaran harus mencukupi total belanja.

## Database

Aplikasi menggunakan SQLite.

File database:

```text
data/toko.db
```

Database dibuat secara otomatis ketika program pertama kali dijalankan.

Data yang disimpan meliputi:

- Produk
- Pelanggan
- Penjualan
- Detail penjualan
- Pembayaran
- Uang kembalian

## Pengujian Aplikasi

Lakukan pengujian berikut sebelum presentasi:

1. Tambahkan minimal tiga produk.
2. Tambahkan minimal dua pelanggan.
3. Buat transaksi dengan satu produk.
4. Buat transaksi dengan beberapa produk.
5. Uji pembayaran dengan nominal yang tepat.
6. Uji pembayaran dengan nominal lebih besar.
7. Uji pembayaran yang kurang.
8. Uji jumlah pembelian melebihi stok.
9. Periksa perubahan stok.
10. Periksa data pada laporan.
11. Tutup aplikasi.
12. Jalankan kembali aplikasi.
13. Pastikan data tetap tersimpan.

## Contoh Skenario Pengujian

Data produk:

```text
Kode  : BRG001
Nama  : Beras
Harga : 13000
Stok  : 10
```

Data pelanggan:

```text
ID       : PLG001
Nama     : Ilham Firmansyah
Telepon  : 081234567890
Poin     : 0
```

Transaksi:

```text
Produk       : Beras
Jumlah       : 3
Total        : Rp39.000
Pembayaran   : Rp50.000
Kembalian    : Rp11.000
Sisa Stok    : 7
```

## Troubleshooting

### Program tidak berjalan

Pastikan terminal berada pada folder yang berisi `main.py`.

Gunakan:

```bash
python main.py
```

atau:

```bash
py main.py
```

### ModuleNotFoundError

Pastikan file berikut berada dalam satu folder:

```text
main.py
gui.py
models.py
database.py
```

### Tkinter tidak ditemukan

Pada Windows, instal ulang Python dari situs resmi dan aktifkan komponen Tcl/Tk.

Pada Linux berbasis Debian atau Ubuntu:

```bash
sudo apt install python3-tk
```

### Database terkunci

Tutup program lain yang sedang membuka file `toko.db`, lalu jalankan kembali aplikasi.

### Transaksi tidak masuk ke laporan

Periksa hal berikut:

- Keranjang sudah berisi produk.
- Jumlah pembayaran sudah diisi.
- Pembayaran mencukupi.
- Tidak ada pesan error saat transaksi.
- Tombol `Muat Ulang` pada tab laporan sudah ditekan.

## Batasan Sistem

Versi saat ini memiliki beberapa batasan:

- Belum memiliki halaman login.
- Belum mendukung pencetakan struk ke printer.
- Belum menyediakan ekspor laporan ke PDF atau Excel.
- Belum mendukung banyak akun kasir dari database.
- Belum memiliki fitur diskon.
- Belum memiliki fitur retur barang.
- Belum memiliki grafik laporan.

## Rencana Pengembangan

Fitur berikut dapat ditambahkan:

- Halaman login kasir.
- Manajemen akun kasir.
- Pencarian produk.
- Filter laporan berdasarkan tanggal.
- Cetak struk.
- Ekspor laporan ke PDF.
- Ekspor laporan ke Excel.
- Diskon transaksi.
- Metode pembayaran tunai dan non-tunai.
- Dashboard dengan statistik penjualan.
- Grafik pendapatan.
- Sistem backup database.

## Pembagian Tugas Kelompok

Contoh pembagian tugas:

| Bagian | Tanggung Jawab |
|---|---|
| Analisis kebutuhan | Menentukan fitur dan alur sistem |
| Models OOP | Membuat class dan method |
| Database | Membuat tabel dan query SQLite |
| GUI | Membuat tampilan Tkinter |
| Pengujian | Menguji fitur dan mencatat hasil |
| Dokumentasi | Membuat laporan, manual book, slide, dan poster |

Sesuaikan pembagian tugas dengan jumlah anggota kelompok.

## Deliverables

Berkas yang harus disiapkan:

1. Source code.
2. Laporan proyek dalam format PDF.
3. Manual book.
4. Slide presentasi maksimal 10 slide.
5. Poster.

## Tim Pengembang

Kelompok 7

Anggota:

1. Ilham Firmansyah

Program studi: Teknik Informatika   
Mata kuliah: Bahasa Pemrograman  
Dosen pengampu: Ranny Meilisa, S.Kom., M.Pd.T.  
Tahun: 2026

## Lisensi

Proyek ini dibuat untuk keperluan akademik dan pembelajaran.