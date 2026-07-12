from __future__ import annotations

import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from database import Database
from models import Kasir, Pelanggan, Penjualan, Produk, Toko


class AplikasiPenjualan(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sistem Manajemen Penjualan Toko - Kelompok 7")
        self.geometry("1100x700")
        self.minsize(950, 620)

        self.database = Database()
        self.toko = Toko("Toko Kelompok 7")
        self.kasir_aktif = Kasir("KSR001", "Admin Kasir", "081234567890", "admin", "admin123")
        self.toko.tambah_kasir(self.kasir_aktif)

        self.produk_cache: dict[str, Produk] = {}
        self.pelanggan_cache: dict[str, Pelanggan] = {}
        self.penjualan_aktif = self._buat_penjualan_baru()

        self._atur_tampilan()
        self._buat_notebook()
        self.muat_produk()
        self.muat_pelanggan()
        self.muat_laporan()

    def _atur_tampilan(self) -> None:
        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        warna_latar = "#EAF2F8"
        warna_putih = "#FFFFFF"
        warna_biru = "#1565C0"
        warna_biru_tua = "#0D47A1"
        warna_biru_muda = "#BBDEFB"
        warna_teks = "#1F2937"

        self.configure(bg=warna_latar)

        style.configure(
            ".",
            font=("Segoe UI", 10),
        )

        style.configure(
            "TFrame",
            background=warna_latar,
        )

        style.configure(
            "TLabel",
            background=warna_latar,
            foreground=warna_teks,
        )

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold"),
            background=warna_latar,
            foreground=warna_biru_tua,
        )

        style.configure(
            "Total.TLabel",
            font=("Segoe UI", 18, "bold"),
            background=warna_latar,
            foreground=warna_biru_tua,
        )

        style.configure(
            "TLabelframe",
            background=warna_latar,
            bordercolor="#90CAF9",
            borderwidth=1,
            relief="solid",
        )

        style.configure(
            "TLabelframe.Label",
            background=warna_latar,
            foreground=warna_biru_tua,
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            background=warna_biru,
            foreground=warna_putih,
            borderwidth=0,
        )

        style.map(
            "TButton",
            background=[
                ("active", "#1976D2"),
                ("pressed", warna_biru_tua),
                ("disabled", "#B0BEC5"),
            ],
            foreground=[
                ("disabled", "#ECEFF1"),
            ],
        )

        style.configure(
            "Danger.TButton",
            background="#D32F2F",
            foreground=warna_putih,
        )

        style.map(
            "Danger.TButton",
            background=[
                ("active", "#B71C1C"),
                ("pressed", "#8E0000"),
            ],
        )

        style.configure(
            "TNotebook",
            background=warna_latar,
            borderwidth=0,
        )

        style.configure(
            "TNotebook.Tab",
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
            background=warna_biru_muda,
            foreground=warna_biru_tua,
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", warna_biru),
                ("active", "#90CAF9"),
            ],
            foreground=[
                ("selected", warna_putih),
            ],
        )

        style.configure(
            "Treeview",
            rowheight=30,
            background=warna_putih,
            fieldbackground=warna_putih,
            foreground=warna_teks,
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=warna_biru,
            foreground=warna_putih,
            relief="flat",
            padding=8,
        )

        style.map(
            "Treeview.Heading",
            background=[
                ("active", "#1976D2"),
            ],
        )

    def _buat_notebook(self) -> None:
        judul = ttk.Label(
            self,
            text="Sistem Manajemen Penjualan Toko",
            style="Title.TLabel",
        )
        judul.pack(pady=(12, 4))

        info = ttk.Label(self, text=self.kasir_aktif.tampilkan_info())
        info.pack(pady=(0, 8))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=10)

        self.tab_produk = ttk.Frame(notebook)
        self.tab_pelanggan = ttk.Frame(notebook)
        self.tab_transaksi = ttk.Frame(notebook)
        self.tab_laporan = ttk.Frame(notebook)

        notebook.add(self.tab_produk, text="Data Produk")
        notebook.add(self.tab_pelanggan, text="Data Pelanggan")
        notebook.add(self.tab_transaksi, text="Transaksi")
        notebook.add(self.tab_laporan, text="Laporan")

        self._buat_tab_produk()
        self._buat_tab_pelanggan()
        self._buat_tab_transaksi()
        self._buat_tab_laporan()

    def _buat_tab_produk(self) -> None:
        form = ttk.LabelFrame(self.tab_produk, text="Form Produk")
        form.pack(fill="x", padx=10, pady=10)

        self.var_kode_produk = tk.StringVar()
        self.var_nama_produk = tk.StringVar()
        self.var_harga_produk = tk.StringVar()
        self.var_stok_produk = tk.StringVar()

        labels = ["Kode", "Nama", "Harga", "Stok"]
        vars_ = [
            self.var_kode_produk,
            self.var_nama_produk,
            self.var_harga_produk,
            self.var_stok_produk,
        ]
        for index, (label, variable) in enumerate(zip(labels, vars_)):
            ttk.Label(form, text=label).grid(row=0, column=index, padx=6, pady=(8, 2), sticky="w")
            ttk.Entry(form, textvariable=variable, width=24).grid(
                row=1, column=index, padx=6, pady=(0, 8), sticky="ew"
            )
            form.columnconfigure(index, weight=1)

        tombol = ttk.Frame(self.tab_produk)
        tombol.pack(fill="x", padx=10, pady=(0, 8))
        ttk.Button(tombol, text="Simpan", command=self.simpan_produk).pack(side="left", padx=3)
        ttk.Button(tombol, text="Ubah", command=self.ubah_produk).pack(side="left", padx=3)
        ttk.Button(tombol, text="Hapus", command=self.hapus_produk).pack(side="left", padx=3)
        ttk.Button(tombol, text="Reset", command=self.reset_form_produk).pack(side="left", padx=3)

        self.tree_produk = ttk.Treeview(
            self.tab_produk,
            columns=("kode", "nama", "harga", "stok"),
            show="headings",
        )
        for kolom, judul in zip(
            ("kode", "nama", "harga", "stok"),
            ("Kode", "Nama Produk", "Harga", "Stok"),
        ):
            self.tree_produk.heading(kolom, text=judul)
        self.tree_produk.column("kode", width=130, anchor="center")
        self.tree_produk.column("nama", width=360)
        self.tree_produk.column("harga", width=180, anchor="e")
        self.tree_produk.column("stok", width=100, anchor="center")
        self.tree_produk.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.tree_produk.bind("<<TreeviewSelect>>", self.pilih_produk)

    def _buat_tab_pelanggan(self) -> None:
        form = ttk.LabelFrame(self.tab_pelanggan, text="Form Pelanggan")
        form.pack(fill="x", padx=10, pady=10)

        self.var_id_pelanggan = tk.StringVar()
        self.var_nama_pelanggan = tk.StringVar()
        self.var_telepon_pelanggan = tk.StringVar()
        self.var_poin_pelanggan = tk.StringVar(value="0")

        labels = ["ID Pelanggan", "Nama", "Telepon", "Poin"]
        vars_ = [
            self.var_id_pelanggan,
            self.var_nama_pelanggan,
            self.var_telepon_pelanggan,
            self.var_poin_pelanggan,
        ]
        for index, (label, variable) in enumerate(zip(labels, vars_)):
            ttk.Label(form, text=label).grid(row=0, column=index, padx=6, pady=(8, 2), sticky="w")
            ttk.Entry(form, textvariable=variable, width=24).grid(
                row=1, column=index, padx=6, pady=(0, 8), sticky="ew"
            )
            form.columnconfigure(index, weight=1)

        tombol = ttk.Frame(self.tab_pelanggan)
        tombol.pack(fill="x", padx=10, pady=(0, 8))
        ttk.Button(tombol, text="Simpan", command=self.simpan_pelanggan).pack(side="left", padx=3)
        ttk.Button(tombol, text="Ubah", command=self.ubah_pelanggan).pack(side="left", padx=3)
        ttk.Button(tombol, text="Hapus", command=self.hapus_pelanggan).pack(side="left", padx=3)
        ttk.Button(tombol, text="Reset", command=self.reset_form_pelanggan).pack(side="left", padx=3)

        self.tree_pelanggan = ttk.Treeview(
            self.tab_pelanggan,
            columns=("id", "nama", "telepon", "poin"),
            show="headings",
        )
        for kolom, judul in zip(
            ("id", "nama", "telepon", "poin"),
            ("ID", "Nama Pelanggan", "Telepon", "Poin"),
        ):
            self.tree_pelanggan.heading(kolom, text=judul)
        self.tree_pelanggan.column("id", width=130, anchor="center")
        self.tree_pelanggan.column("nama", width=330)
        self.tree_pelanggan.column("telepon", width=220)
        self.tree_pelanggan.column("poin", width=100, anchor="center")
        self.tree_pelanggan.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.tree_pelanggan.bind("<<TreeviewSelect>>", self.pilih_pelanggan)

    def _buat_tab_transaksi(self) -> None:
        # Mengatur layout utama tab transaksi.
        self.tab_transaksi.columnconfigure(0, weight=1)
        self.tab_transaksi.rowconfigure(1, weight=1)

        # =========================
        # FORM INPUT TRANSAKSI
        # =========================
        kontrol = ttk.LabelFrame(
            self.tab_transaksi,
            text="Input Transaksi",
            padding=10,
        )
        kontrol.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10, 5),
        )

        kontrol.columnconfigure(0, weight=1)
        kontrol.columnconfigure(1, weight=2)
        kontrol.columnconfigure(2, weight=0)
        kontrol.columnconfigure(3, weight=0)

        self.var_pelanggan_transaksi = tk.StringVar(value="Umum")
        self.var_produk_transaksi = tk.StringVar()
        self.var_jumlah_transaksi = tk.StringVar(value="1")

        ttk.Label(
            kontrol,
            text="Pelanggan",
        ).grid(
            row=0,
            column=0,
            padx=6,
            pady=(2, 4),
            sticky="w",
        )

        self.combo_pelanggan = ttk.Combobox(
            kontrol,
            textvariable=self.var_pelanggan_transaksi,
            state="readonly",
            width=30,
        )
        self.combo_pelanggan.grid(
            row=1,
            column=0,
            padx=6,
            pady=(0, 4),
            sticky="ew",
        )

        ttk.Label(
            kontrol,
            text="Produk",
        ).grid(
            row=0,
            column=1,
            padx=6,
            pady=(2, 4),
            sticky="w",
        )

        self.combo_produk = ttk.Combobox(
            kontrol,
            textvariable=self.var_produk_transaksi,
            state="readonly",
            width=40,
        )
        self.combo_produk.grid(
            row=1,
            column=1,
            padx=6,
            pady=(0, 4),
            sticky="ew",
        )

        ttk.Label(
            kontrol,
            text="Jumlah",
        ).grid(
            row=0,
            column=2,
            padx=6,
            pady=(2, 4),
            sticky="w",
        )

        self.entry_jumlah_transaksi = ttk.Entry(
            kontrol,
            textvariable=self.var_jumlah_transaksi,
            width=10,
        )
        self.entry_jumlah_transaksi.grid(
            row=1,
            column=2,
            padx=6,
            pady=(0, 4),
            sticky="ew",
        )

        ttk.Button(
            kontrol,
            text="Tambah ke Keranjang",
            command=self.tambah_ke_keranjang,
        ).grid(
            row=1,
            column=3,
            padx=6,
            pady=(0, 4),
            sticky="ew",
        )

        # =========================
        # TABEL KERANJANG
        # =========================
        area_tabel = ttk.Frame(self.tab_transaksi)
        area_tabel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5,
        )

        area_tabel.columnconfigure(0, weight=1)
        area_tabel.rowconfigure(0, weight=1)

        self.tree_keranjang = ttk.Treeview(
            area_tabel,
            columns=("kode", "nama", "harga", "jumlah", "subtotal"),
            show="headings",
        )

        kolom_keranjang = (
            ("kode", "Kode"),
            ("nama", "Produk"),
            ("harga", "Harga"),
            ("jumlah", "Jumlah"),
            ("subtotal", "Subtotal"),
        )

        for kolom, judul in kolom_keranjang:
            self.tree_keranjang.heading(kolom, text=judul)

        self.tree_keranjang.column(
            "kode",
            width=110,
            minwidth=90,
            anchor="center",
        )
        self.tree_keranjang.column(
            "nama",
            width=280,
            minwidth=180,
        )
        self.tree_keranjang.column(
            "harga",
            width=150,
            minwidth=110,
            anchor="e",
        )
        self.tree_keranjang.column(
            "jumlah",
            width=90,
            minwidth=70,
            anchor="center",
        )
        self.tree_keranjang.column(
            "subtotal",
            width=170,
            minwidth=120,
            anchor="e",
        )

        scrollbar_keranjang = ttk.Scrollbar(
            area_tabel,
            orient="vertical",
            command=self.tree_keranjang.yview,
        )

        self.tree_keranjang.configure(
            yscrollcommand=scrollbar_keranjang.set
        )

        self.tree_keranjang.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scrollbar_keranjang.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        # =========================
        # TOMBOL DAN TOTAL
        # =========================
        bawah = ttk.Frame(self.tab_transaksi)
        bawah.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=5,
        )

        ttk.Button(
            bawah,
            text="Hapus Item",
            style="Danger.TButton",
            command=self.hapus_item_keranjang,
        ).pack(
            side="left",
            padx=(0, 6),
        )

        ttk.Button(
            bawah,
            text="Batalkan Transaksi",
            style="Danger.TButton",
            command=self.reset_transaksi,
        ).pack(
            side="left",
            padx=6,
        )

        self.var_total = tk.StringVar(value="Total: Rp0")

        ttk.Label(
            bawah,
            textvariable=self.var_total,
            style="Total.TLabel",
        ).pack(
            side="right",
            padx=8,
        )

        # =========================
        # PEMBAYARAN
        # =========================
        bayar_frame = ttk.LabelFrame(
            self.tab_transaksi,
            text="Pembayaran",
            padding=10,
        )
        bayar_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 10),
        )

        bayar_frame.columnconfigure(1, weight=1)

        self.var_bayar = tk.StringVar()

        ttk.Label(
            bayar_frame,
            text="Jumlah Bayar",
        ).grid(
            row=0,
            column=0,
            padx=(4, 8),
            pady=4,
            sticky="w",
        )

        self.entry_bayar = ttk.Entry(
            bayar_frame,
            textvariable=self.var_bayar,
            font=("Segoe UI", 12),
        )
        self.entry_bayar.grid(
            row=0,
            column=1,
            padx=4,
            pady=4,
            sticky="ew",
        )

        ttk.Button(
            bayar_frame,
            text="Proses Pembayaran",
            command=self.proses_pembayaran,
        ).grid(
            row=0,
            column=2,
            padx=(10, 4),
            pady=4,
            sticky="ew",
        )

        # Tekan Enter untuk memproses pembayaran.
        self.entry_bayar.bind(
            "<Return>",
            lambda _event: self.proses_pembayaran(),
        )

    def _buat_tab_laporan(self) -> None:
        atas = ttk.Frame(self.tab_laporan)
        atas.pack(fill="x", padx=10, pady=10)
        ttk.Button(atas, text="Muat Ulang", command=self.muat_laporan).pack(side="left")
        self.var_ringkasan_laporan = tk.StringVar(value="Total pendapatan: Rp0")
        ttk.Label(atas, textvariable=self.var_ringkasan_laporan, style="Total.TLabel").pack(side="right")

        self.tree_laporan = ttk.Treeview(
            self.tab_laporan,
            columns=("kode", "tanggal", "kasir", "pelanggan", "total", "bayar", "kembalian"),
            show="headings",
        )
        headings = (
            "Kode Transaksi",
            "Tanggal",
            "Kasir",
            "Pelanggan",
            "Total",
            "Bayar",
            "Kembalian",
        )
        for kolom, judul in zip(self.tree_laporan["columns"], headings):
            self.tree_laporan.heading(kolom, text=judul)
        self.tree_laporan.column("kode", width=170)
        self.tree_laporan.column("tanggal", width=155)
        self.tree_laporan.column("kasir", width=140)
        self.tree_laporan.column("pelanggan", width=150)
        self.tree_laporan.column("total", width=120, anchor="e")
        self.tree_laporan.column("bayar", width=120, anchor="e")
        self.tree_laporan.column("kembalian", width=120, anchor="e")
        self.tree_laporan.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _buat_penjualan_baru(self) -> Penjualan:
        kode = datetime.now().strftime("TRX%Y%m%d%H%M%S%f")
        return Penjualan(kode, self.kasir_aktif)

    @staticmethod
    def _rupiah(nilai: float) -> str:
        return f"Rp{nilai:,.0f}".replace(",", ".")
    
    @staticmethod
    def _parse_nominal(teks: str) -> float:
        nominal = teks.strip().lower()

        if not nominal:
            raise ValueError("Jumlah pembayaran belum diisi.")

        nominal = nominal.replace("rp", "")
        nominal = nominal.replace(" ", "")
        nominal = nominal.replace(".", "")
        nominal = nominal.replace(",", ".")

        try:
            nilai = float(nominal)
        except ValueError as error:
            raise ValueError(
                "Jumlah pembayaran harus berupa angka."
            ) from error

        if nilai <= 0:
            raise ValueError(
                "Jumlah pembayaran harus lebih dari nol."
            )

        return nilai

    def muat_produk(self) -> None:
        self.produk_cache.clear()
        for item in self.tree_produk.get_children():
            self.tree_produk.delete(item)

        produk_list = self.database.ambil_semua_produk()
        for produk in produk_list:
            self.produk_cache[produk.get_kode()] = produk
            self.tree_produk.insert(
                "",
                "end",
                values=(
                    produk.get_kode(),
                    produk.get_nama(),
                    self._rupiah(produk.get_harga()),
                    produk.get_stok(),
                ),
            )

        self.combo_produk["values"] = [
            f"{produk.get_kode()} | {produk.get_nama()} | stok {produk.get_stok()}"
            for produk in produk_list
        ]
        self.var_produk_transaksi.set("")

    def simpan_produk(self) -> None:
        try:
            produk = Produk(
                self.var_kode_produk.get().strip(),
                self.var_nama_produk.get().strip(),
                float(self.var_harga_produk.get()),
                int(self.var_stok_produk.get()),
            )
            self.database.tambah_produk(produk)
            messagebox.showinfo("Berhasil", "Produk berhasil disimpan.")
            self.reset_form_produk()
            self.muat_produk()
        except (ValueError, sqlite3.IntegrityError) as error:
            messagebox.showerror("Gagal", str(error))

    def pilih_produk(self, _event=None) -> None:
        selection = self.tree_produk.selection()
        if not selection:
            return
        kode, nama, harga, stok = self.tree_produk.item(selection[0], "values")
        self.var_kode_produk.set(kode)
        self.var_nama_produk.set(nama)
        self.var_harga_produk.set(str(self.produk_cache[kode].get_harga()))
        self.var_stok_produk.set(stok)

    def ubah_produk(self) -> None:
        try:
            produk = Produk(
                self.var_kode_produk.get().strip(),
                self.var_nama_produk.get().strip(),
                float(self.var_harga_produk.get()),
                int(self.var_stok_produk.get()),
            )
            self.database.ubah_produk(produk)
            messagebox.showinfo("Berhasil", "Produk berhasil diubah.")
            self.reset_form_produk()
            self.muat_produk()
        except ValueError as error:
            messagebox.showerror("Gagal", str(error))

    def hapus_produk(self) -> None:
        kode = self.var_kode_produk.get().strip()
        if not kode:
            messagebox.showwarning("Peringatan", "Pilih produk yang akan dihapus.")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus produk {kode}?"):
            self.database.hapus_produk(kode)
            self.reset_form_produk()
            self.muat_produk()

    def reset_form_produk(self) -> None:
        self.var_kode_produk.set("")
        self.var_nama_produk.set("")
        self.var_harga_produk.set("")
        self.var_stok_produk.set("")

    def muat_pelanggan(self) -> None:
        self.pelanggan_cache.clear()
        for item in self.tree_pelanggan.get_children():
            self.tree_pelanggan.delete(item)

        pelanggan_list = self.database.ambil_semua_pelanggan()
        for pelanggan in pelanggan_list:
            self.pelanggan_cache[pelanggan.get_id_person()] = pelanggan
            self.tree_pelanggan.insert(
                "",
                "end",
                values=(
                    pelanggan.get_id_person(),
                    pelanggan.get_nama(),
                    pelanggan.get_telepon(),
                    pelanggan.get_poin(),
                ),
            )

        self.combo_pelanggan["values"] = ["Umum"] + [
            f"{pelanggan.get_id_person()} | {pelanggan.get_nama()}"
            for pelanggan in pelanggan_list
        ]
        if self.var_pelanggan_transaksi.get() not in self.combo_pelanggan["values"]:
            self.var_pelanggan_transaksi.set("Umum")

    def simpan_pelanggan(self) -> None:
        try:
            pelanggan = Pelanggan(
                self.var_id_pelanggan.get().strip(),
                self.var_nama_pelanggan.get().strip(),
                self.var_telepon_pelanggan.get().strip(),
                int(self.var_poin_pelanggan.get() or 0),
            )
            self.database.tambah_pelanggan(pelanggan)
            messagebox.showinfo("Berhasil", "Pelanggan berhasil disimpan.")
            self.reset_form_pelanggan()
            self.muat_pelanggan()
        except (ValueError, sqlite3.IntegrityError) as error:
            messagebox.showerror("Gagal", str(error))

    def pilih_pelanggan(self, _event=None) -> None:
        selection = self.tree_pelanggan.selection()
        if not selection:
            return
        id_person, nama, telepon, poin = self.tree_pelanggan.item(selection[0], "values")
        self.var_id_pelanggan.set(id_person)
        self.var_nama_pelanggan.set(nama)
        self.var_telepon_pelanggan.set(telepon)
        self.var_poin_pelanggan.set(poin)

    def ubah_pelanggan(self) -> None:
        try:
            pelanggan = Pelanggan(
                self.var_id_pelanggan.get().strip(),
                self.var_nama_pelanggan.get().strip(),
                self.var_telepon_pelanggan.get().strip(),
                int(self.var_poin_pelanggan.get() or 0),
            )
            self.database.ubah_pelanggan(pelanggan)
            messagebox.showinfo("Berhasil", "Pelanggan berhasil diubah.")
            self.reset_form_pelanggan()
            self.muat_pelanggan()
        except ValueError as error:
            messagebox.showerror("Gagal", str(error))

    def hapus_pelanggan(self) -> None:
        id_person = self.var_id_pelanggan.get().strip()
        if not id_person:
            messagebox.showwarning("Peringatan", "Pilih pelanggan yang akan dihapus.")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus pelanggan {id_person}?"):
            self.database.hapus_pelanggan(id_person)
            self.reset_form_pelanggan()
            self.muat_pelanggan()

    def reset_form_pelanggan(self) -> None:
        self.var_id_pelanggan.set("")
        self.var_nama_pelanggan.set("")
        self.var_telepon_pelanggan.set("")
        self.var_poin_pelanggan.set("0")

    def tambah_ke_keranjang(self) -> None:
        try:
            pilihan = self.var_produk_transaksi.get()
            if not pilihan:
                raise ValueError("Pilih produk terlebih dahulu.")
            kode_produk = pilihan.split(" | ", 1)[0]
            jumlah = int(self.var_jumlah_transaksi.get())
            produk = self.produk_cache[kode_produk]
            self.penjualan_aktif.tambah_item(produk, jumlah)
            self.tampilkan_keranjang()
            self.var_jumlah_transaksi.set("1")
        except (ValueError, KeyError) as error:
            messagebox.showerror("Gagal", str(error))

    def tampilkan_keranjang(self) -> None:
        for item in self.tree_keranjang.get_children():
            self.tree_keranjang.delete(item)
        for item in self.penjualan_aktif.get_daftar_item():
            produk = item["produk"]
            self.tree_keranjang.insert(
                "",
                "end",
                values=(
                    produk.get_kode(),
                    produk.get_nama(),
                    self._rupiah(produk.get_harga()),
                    item["jumlah"],
                    self._rupiah(item["subtotal"]),
                ),
            )
        self.var_total.set(f"Total: {self._rupiah(self.penjualan_aktif.hitung_total())}")

    def hapus_item_keranjang(self) -> None:
        selection = self.tree_keranjang.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih item pada keranjang.")
            return
        kode_produk = self.tree_keranjang.item(selection[0], "values")[0]
        self.penjualan_aktif.hapus_item(kode_produk)
        self.tampilkan_keranjang()

    def _pelanggan_terpilih(self) -> Pelanggan | None:
        pilihan = self.var_pelanggan_transaksi.get()
        if not pilihan or pilihan == "Umum":
            return None
        id_person = pilihan.split(" | ", 1)[0]
        return self.pelanggan_cache.get(id_person)

    def proses_pembayaran(self) -> None:
        try:
            pelanggan = self._pelanggan_terpilih()
            self.penjualan_aktif.set_pelanggan(pelanggan)
            jumlah_bayar = float(self.var_bayar.get())
            kembalian = self.database.simpan_penjualan(self.penjualan_aktif, jumlah_bayar)
            self.toko.simpan_penjualan(self.penjualan_aktif)

            struk = self.penjualan_aktif.cetak_struk()
            messagebox.showinfo(
                "Transaksi Berhasil",
                f"{struk}\nBayar: {self._rupiah(jumlah_bayar)}\nKembalian: {self._rupiah(kembalian)}",
            )
            self.reset_transaksi()
            self.muat_produk()
            self.muat_pelanggan()
            self.muat_laporan()
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror("Transaksi Gagal", str(error))

    def reset_transaksi(self) -> None:
        self.penjualan_aktif = self._buat_penjualan_baru()
        self.var_pelanggan_transaksi.set("Umum")
        self.var_produk_transaksi.set("")
        self.var_jumlah_transaksi.set("1")
        self.var_bayar.set("")
        self.tampilkan_keranjang()

    def muat_laporan(self) -> None:
        for item in self.tree_laporan.get_children():
            self.tree_laporan.delete(item)

        total_pendapatan = 0.0
        for row in self.database.ambil_laporan_penjualan():
            total_pendapatan += row["total"]
            tanggal = row["tanggal"].replace("T", " ")
            self.tree_laporan.insert(
                "",
                "end",
                values=(
                    row["kode_penjualan"],
                    tanggal,
                    row["nama_kasir"],
                    row["nama_pelanggan"],
                    self._rupiah(row["total"]),
                    self._rupiah(row["bayar"]),
                    self._rupiah(row["kembalian"]),
                ),
            )
        self.var_ringkasan_laporan.set(
            f"Total pendapatan: {self._rupiah(total_pendapatan)}"
        )
