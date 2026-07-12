from __future__ import annotations

from datetime import datetime
from typing import Optional


class Person:
    def __init__(self, id_person: str, nama: str, telepon: str) -> None:
        self._id_person = id_person
        self.__nama = nama
        self.__telepon = telepon

    def get_id_person(self) -> str:
        return self._id_person

    def set_id_person(self, id_person: str) -> None:
        if not id_person.strip():
            raise ValueError("ID person tidak boleh kosong.")
        self._id_person = id_person.strip()

    def get_nama(self) -> str:
        return self.__nama

    def set_nama(self, nama: str) -> None:
        if not nama.strip():
            raise ValueError("Nama tidak boleh kosong.")
        self.__nama = nama.strip()

    def get_telepon(self) -> str:
        return self.__telepon

    def set_telepon(self, telepon: str) -> None:
        self.__telepon = telepon.strip()

    def tampilkan_info(self) -> str:
        return f"ID: {self._id_person} | Nama: {self.__nama} | Telepon: {self.__telepon}"


class Kasir(Person):
    def __init__(self, id_person: str, nama: str, telepon: str, username: str, password: str) -> None:
        super().__init__(id_person, nama, telepon)
        self.__username = username
        self.__password = password

    def get_username(self) -> str:
        return self.__username

    def set_username(self, username: str) -> None:
        if not username.strip():
            raise ValueError("Username tidak boleh kosong.")
        self.__username = username.strip()

    def login(self, username: str, password: str) -> bool:
        return self.__username == username and self.__password == password

    def proses_penjualan(self, penjualan: "Penjualan", jumlah_bayar: float) -> float:
        return penjualan.proses_pembayaran(jumlah_bayar)

    def tampilkan_info(self) -> str:
        return f"Kasir | {super().tampilkan_info()} | Username: {self.__username}"


class Pelanggan(Person):
    def __init__(self, id_person: str, nama: str, telepon: str, poin: int = 0) -> None:
        super().__init__(id_person, nama, telepon)
        self.__poin = poin

    def get_poin(self) -> int:
        return self.__poin

    def set_poin(self, poin: int) -> None:
        if poin < 0:
            raise ValueError("Poin tidak boleh negatif.")
        self.__poin = poin

    def tambah_poin(self, poin: int) -> None:
        if poin > 0:
            self.__poin += poin

    def gunakan_poin(self, poin: int) -> None:
        if poin <= 0:
            raise ValueError("Poin yang digunakan harus lebih dari nol.")
        if poin > self.__poin:
            raise ValueError("Poin pelanggan tidak mencukupi.")
        self.__poin -= poin

    def tampilkan_info(self) -> str:
        return f"Pelanggan | {super().tampilkan_info()} | Poin: {self.__poin}"


class Produk:
    def __init__(self, kode: str, nama: str, harga: float, stok: int) -> None:
        self.__kode = kode
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok
        self._validasi()

    def _validasi(self) -> None:
        if not self.__kode.strip() or not self.__nama.strip():
            raise ValueError("Kode dan nama produk tidak boleh kosong.")
        if self.__harga < 0 or self.__stok < 0:
            raise ValueError("Harga dan stok tidak boleh negatif.")

    def get_kode(self) -> str:
        return self.__kode

    def get_nama(self) -> str:
        return self.__nama

    def set_nama(self, nama: str) -> None:
        if not nama.strip():
            raise ValueError("Nama produk tidak boleh kosong.")
        self.__nama = nama.strip()

    def get_harga(self) -> float:
        return self.__harga

    def set_harga(self, harga: float) -> None:
        if harga < 0:
            raise ValueError("Harga tidak boleh negatif.")
        self.__harga = harga

    def get_stok(self) -> int:
        return self.__stok

    def set_stok(self, stok: int) -> None:
        if stok < 0:
            raise ValueError("Stok tidak boleh negatif.")
        self.__stok = stok

    def tambah_stok(self, jumlah: int) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah stok harus lebih dari nol.")
        self.__stok += jumlah

    def kurangi_stok(self, jumlah: int) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah pembelian harus lebih dari nol.")
        if jumlah > self.__stok:
            raise ValueError(f"Stok {self.__nama} tidak mencukupi.")
        self.__stok -= jumlah

    def tampilkan_produk(self) -> str:
        return f"{self.__kode} - {self.__nama} | Rp{self.__harga:,.0f} | Stok: {self.__stok}"


class Penjualan:
    def __init__(
        self,
        kode_penjualan: str,
        kasir: Kasir,
        pelanggan: Optional[Pelanggan] = None,
        tanggal: Optional[datetime] = None,
    ) -> None:
        self.__kode_penjualan = kode_penjualan
        self.__kasir = kasir
        self.__pelanggan = pelanggan
        self.__tanggal = tanggal or datetime.now()
        self.__daftar_item: list[dict] = []

    def get_kode_penjualan(self) -> str:
        return self.__kode_penjualan

    def get_kasir(self) -> Kasir:
        return self.__kasir

    def get_pelanggan(self) -> Optional[Pelanggan]:
        return self.__pelanggan

    def set_pelanggan(self, pelanggan: Optional[Pelanggan]) -> None:
        self.__pelanggan = pelanggan

    def get_tanggal(self) -> datetime:
        return self.__tanggal

    def get_daftar_item(self) -> list[dict]:
        return list(self.__daftar_item)

    def tambah_item(self, produk: Produk, jumlah: int) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah pembelian harus lebih dari nol.")
        if jumlah > produk.get_stok():
            raise ValueError(f"Stok {produk.get_nama()} tidak mencukupi.")

        for item in self.__daftar_item:
            if item["produk"].get_kode() == produk.get_kode():
                jumlah_baru = item["jumlah"] + jumlah
                if jumlah_baru > produk.get_stok():
                    raise ValueError(f"Stok {produk.get_nama()} tidak mencukupi.")
                item["jumlah"] = jumlah_baru
                item["subtotal"] = jumlah_baru * produk.get_harga()
                return

        self.__daftar_item.append(
            {
                "produk": produk,
                "jumlah": jumlah,
                "subtotal": produk.get_harga() * jumlah,
            }
        )

    def hapus_item(self, kode_produk: str) -> None:
        self.__daftar_item = [
            item for item in self.__daftar_item if item["produk"].get_kode() != kode_produk
        ]

    def hitung_total(self) -> float:
        return sum(item["subtotal"] for item in self.__daftar_item)

    def hitung_kembalian(self, jumlah_bayar: float) -> float:
        return jumlah_bayar - self.hitung_total()

    def proses_pembayaran(self, jumlah_bayar: float) -> float:
        if not self.__daftar_item:
            raise ValueError("Keranjang transaksi masih kosong.")
        if jumlah_bayar < self.hitung_total():
            raise ValueError("Jumlah pembayaran kurang.")
        return self.hitung_kembalian(jumlah_bayar)

    def cetak_struk(self) -> str:
        pelanggan = self.__pelanggan.get_nama() if self.__pelanggan else "Umum"
        baris = [
            "TOKO KELOMPOK 7",
            f"Kode: {self.__kode_penjualan}",
            f"Tanggal: {self.__tanggal:%d-%m-%Y %H:%M:%S}",
            f"Kasir: {self.__kasir.get_nama()}",
            f"Pelanggan: {pelanggan}",
            "-" * 42,
        ]
        for item in self.__daftar_item:
            produk = item["produk"]
            baris.append(
                f"{produk.get_nama()} x{item['jumlah']} = Rp{item['subtotal']:,.0f}"
            )
        baris.extend(["-" * 42, f"TOTAL: Rp{self.hitung_total():,.0f}"])
        return "\n".join(baris)


class Toko:
    def __init__(self, nama_toko: str) -> None:
        self.__nama_toko = nama_toko
        self.__daftar_produk: list[Produk] = []
        self.__daftar_kasir: list[Kasir] = []
        self.__daftar_pelanggan: list[Pelanggan] = []
        self.__daftar_penjualan: list[Penjualan] = []

    def get_nama_toko(self) -> str:
        return self.__nama_toko

    def tambah_produk(self, produk: Produk) -> None:
        if self.cari_produk(produk.get_kode()) is not None:
            raise ValueError("Kode produk sudah digunakan.")
        self.__daftar_produk.append(produk)

    def hapus_produk(self, kode_produk: str) -> None:
        self.__daftar_produk = [
            produk for produk in self.__daftar_produk if produk.get_kode() != kode_produk
        ]

    def cari_produk(self, kode_produk: str) -> Optional[Produk]:
        return next(
            (produk for produk in self.__daftar_produk if produk.get_kode() == kode_produk),
            None,
        )

    def tambah_kasir(self, kasir: Kasir) -> None:
        self.__daftar_kasir.append(kasir)

    def tambah_pelanggan(self, pelanggan: Pelanggan) -> None:
        self.__daftar_pelanggan.append(pelanggan)

    def simpan_penjualan(self, penjualan: Penjualan) -> None:
        self.__daftar_penjualan.append(penjualan)

    def get_daftar_produk(self) -> list[Produk]:
        return list(self.__daftar_produk)

    def get_daftar_pelanggan(self) -> list[Pelanggan]:
        return list(self.__daftar_pelanggan)

    def get_daftar_penjualan(self) -> list[Penjualan]:
        return list(self.__daftar_penjualan)

    def hitung_total_penjualan(self) -> float:
        return sum(penjualan.hitung_total() for penjualan in self.__daftar_penjualan)
