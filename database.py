from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from models import Pelanggan, Penjualan, Produk


class Database:
    def __init__(self, db_path: str = "data/toko.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.inisialisasi_database()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def inisialisasi_database(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS produk (
                    kode TEXT PRIMARY KEY,
                    nama TEXT NOT NULL,
                    harga REAL NOT NULL CHECK(harga >= 0),
                    stok INTEGER NOT NULL CHECK(stok >= 0)
                );

                CREATE TABLE IF NOT EXISTS pelanggan (
                    id_person TEXT PRIMARY KEY,
                    nama TEXT NOT NULL,
                    telepon TEXT NOT NULL,
                    poin INTEGER NOT NULL DEFAULT 0 CHECK(poin >= 0)
                );

                CREATE TABLE IF NOT EXISTS penjualan (
                    kode_penjualan TEXT PRIMARY KEY,
                    tanggal TEXT NOT NULL,
                    id_kasir TEXT NOT NULL,
                    nama_kasir TEXT NOT NULL,
                    id_pelanggan TEXT,
                    nama_pelanggan TEXT,
                    total REAL NOT NULL,
                    bayar REAL NOT NULL,
                    kembalian REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS detail_penjualan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kode_penjualan TEXT NOT NULL,
                    kode_produk TEXT NOT NULL,
                    nama_produk TEXT NOT NULL,
                    harga REAL NOT NULL,
                    jumlah INTEGER NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY(kode_penjualan) REFERENCES penjualan(kode_penjualan)
                );
                """
            )

    def tambah_produk(self, produk: Produk) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO produk(kode, nama, harga, stok) VALUES (?, ?, ?, ?)",
                (
                    produk.get_kode(),
                    produk.get_nama(),
                    produk.get_harga(),
                    produk.get_stok(),
                ),
            )

    def ubah_produk(self, produk: Produk) -> None:
        with self._connect() as conn:
            cursor = conn.execute(
                "UPDATE produk SET nama = ?, harga = ?, stok = ? WHERE kode = ?",
                (
                    produk.get_nama(),
                    produk.get_harga(),
                    produk.get_stok(),
                    produk.get_kode(),
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError("Produk tidak ditemukan.")

    def hapus_produk(self, kode_produk: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM produk WHERE kode = ?", (kode_produk,))

    def ambil_semua_produk(self) -> list[Produk]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM produk ORDER BY nama").fetchall()
        return [Produk(row["kode"], row["nama"], row["harga"], row["stok"]) for row in rows]

    def cari_produk(self, kode_produk: str) -> Optional[Produk]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM produk WHERE kode = ?", (kode_produk,)
            ).fetchone()
        if row is None:
            return None
        return Produk(row["kode"], row["nama"], row["harga"], row["stok"])

    def tambah_pelanggan(self, pelanggan: Pelanggan) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO pelanggan(id_person, nama, telepon, poin) VALUES (?, ?, ?, ?)",
                (
                    pelanggan.get_id_person(),
                    pelanggan.get_nama(),
                    pelanggan.get_telepon(),
                    pelanggan.get_poin(),
                ),
            )

    def ubah_pelanggan(self, pelanggan: Pelanggan) -> None:
        with self._connect() as conn:
            cursor = conn.execute(
                "UPDATE pelanggan SET nama = ?, telepon = ?, poin = ? WHERE id_person = ?",
                (
                    pelanggan.get_nama(),
                    pelanggan.get_telepon(),
                    pelanggan.get_poin(),
                    pelanggan.get_id_person(),
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError("Pelanggan tidak ditemukan.")

    def hapus_pelanggan(self, id_person: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM pelanggan WHERE id_person = ?", (id_person,))

    def ambil_semua_pelanggan(self) -> list[Pelanggan]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM pelanggan ORDER BY nama").fetchall()
        return [
            Pelanggan(row["id_person"], row["nama"], row["telepon"], row["poin"])
            for row in rows
        ]

    def simpan_penjualan(self, penjualan: Penjualan, jumlah_bayar: float) -> float:
        total = penjualan.hitung_total()
        kembalian = penjualan.proses_pembayaran(jumlah_bayar)
        pelanggan = penjualan.get_pelanggan()
        kasir = penjualan.get_kasir()

        with self._connect() as conn:
            try:
                conn.execute("BEGIN")
                conn.execute(
                    """
                    INSERT INTO penjualan(
                        kode_penjualan, tanggal, id_kasir, nama_kasir,
                        id_pelanggan, nama_pelanggan, total, bayar, kembalian
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        penjualan.get_kode_penjualan(),
                        penjualan.get_tanggal().isoformat(timespec="seconds"),
                        kasir.get_id_person(),
                        kasir.get_nama(),
                        pelanggan.get_id_person() if pelanggan else None,
                        pelanggan.get_nama() if pelanggan else "Umum",
                        total,
                        jumlah_bayar,
                        kembalian,
                    ),
                )

                for item in penjualan.get_daftar_item():
                    produk = item["produk"]
                    jumlah = item["jumlah"]
                    cursor = conn.execute(
                        """
                        UPDATE produk
                        SET stok = stok - ?
                        WHERE kode = ? AND stok >= ?
                        """,
                        (jumlah, produk.get_kode(), jumlah),
                    )
                    if cursor.rowcount == 0:
                        raise ValueError(
                            f"Stok {produk.get_nama()} berubah atau tidak mencukupi."
                        )

                    conn.execute(
                        """
                        INSERT INTO detail_penjualan(
                            kode_penjualan, kode_produk, nama_produk,
                            harga, jumlah, subtotal
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            penjualan.get_kode_penjualan(),
                            produk.get_kode(),
                            produk.get_nama(),
                            produk.get_harga(),
                            jumlah,
                            item["subtotal"],
                        ),
                    )

                if pelanggan:
                    tambahan_poin = int(total // 10000)
                    conn.execute(
                        "UPDATE pelanggan SET poin = poin + ? WHERE id_person = ?",
                        (tambahan_poin, pelanggan.get_id_person()),
                    )

                conn.commit()
            except Exception:
                conn.rollback()
                raise

        return kembalian

    def ambil_laporan_penjualan(self) -> list[sqlite3.Row]:
        with self._connect() as conn:
            return conn.execute(
                """
                SELECT kode_penjualan, tanggal, nama_kasir, nama_pelanggan,
                       total, bayar, kembalian
                FROM penjualan
                ORDER BY tanggal DESC
                """
            ).fetchall()
