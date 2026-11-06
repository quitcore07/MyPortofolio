"""
Game Hoki - Angka Meloncat-loncat
=================================
Game keberuntungan berbasis terminal: komputer mengacak angka 1-100,
dan setiap angka bisa memberi hadiah (atau "angka kematian").

Fitur:
  - Data hadiah terpisah dari logika (mudah ditambah/diubah)
  - Animasi mengacak di terminal
  - Bisa main berulang tanpa menjalankan ulang program
  - Koleksi harta: hadiah yang sudah didapat tersimpan selama sesi
  - Statistik permainan (total putar, jackpot, zonk, win rate)
  - Tersimpan ke file JSON, jadi progres tidak hilang saat program ditutup

Cara menjalankan:
    python game_hoki.py
"""

from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

# --------------------------------------------------------------------------
# Konfigurasi
# --------------------------------------------------------------------------
MIN_ANGKA = 1
MAX_ANGKA = 100
ANGKA_JACKPOT = 67
LEBAR = 56
SAVE_FILE = Path("hoki_save.json")


@dataclass(frozen=True)
class Hadiah:
    """Satu hadiah yang bisa didapat dari angka tertentu."""
    emoji: str
    nama: str
    deskripsi: str


# Angka -> hadiah. Tambah baris baru di sini untuk menambah hadiah.
HADIAH: dict[int, Hadiah] = {
    5:  Hadiah("💎", "PETI HARTA KARUN", "Penuh emas murni dan permata berkilauan!"),
    49: Hadiah("⚔️", "PEDANG RAJA SAKTI", "Tajamnya menembus awan, tak ada lawan yang berani!"),
    83: Hadiah("👑", "MAHKOTA DEWA", "Bersinar cahaya surga, pemiliknya disegani semua!"),
    17: Hadiah("🛡️", "PERISAI TAK TERKALAHKAN", "Melindungimu dari segala serangan dan bahaya!"),
    92: Hadiah("🔐", "KUNCI SEGALA RAHASIA", "Membuka pintu harta karun yang tersembunyi ribuan tahun!"),
    31: Hadiah("🏰", "ISTANA DI ATAS AWAN", "Tempat tinggalmu megah dikelilingi awan putih!"),
    74: Hadiah("🐴", "KUDA BERSAYAP", "Terbang melintasi gunung dan samudra dalam sekejap!"),
    28: Hadiah("🕯️", "LAMPU AJAIB", "Cahayanya menerangi jalan gelap sekalipun!"),
    61: Hadiah("📜", "PETA NERAKA & SURGA", "Menunjukkan jalan menuju kebahagiaan abadi!"),
    14: Hadiah("🔮", "BOLA KRISTAL", "Mampu melihat masa depan dan segala yang tersembunyi!"),
    88: Hadiah("🪶", "BULU BURUNG SUCI", "Membuatmu ringan, terbang tinggi menembus langit!"),
    53: Hadiah("💍", "CINCIN KEKUATAN", "Memilikinya membuatmu kuat sepuluh kali lipat!"),
    39: Hadiah("📖", "KITAB HIKMAT", "Berisi segala ilmu pengetahuan langka dunia!"),
    71: Hadiah("🗝️", "KUNCI GERBANG DUNIA", "Bisa bepergian ke mana saja seketika!"),
    22: Hadiah("🌿", "RAMUAN HIDUP ABADI", "Menyembuhkan luka, membuat tubuh tetap muda!"),
    95: Hadiah("⭐", "BATU BINTANG UTAMA", "Memancarkan cahaya keberuntungan setiap saat!"),
    44: Hadiah("🗺️", "KOMPAS HATI", "Selalu menunjuk ke arah kebahagiaan sejati!"),
    79: Hadiah("👘", "JUBAH TAK TERLIHAT", "Memakainya membuatmu tak terlihat oleh siapa pun!"),
    11: Hadiah("🌊", "MUTIARA KERAJAAN LAUT", "Permata terindah dari dasar samudra terdalam!"),
}

JACKPOT_ITEMS = [
    ("💎", "Harta Karun Terbesar"), ("⚔️", "Pedang Raja Agung"),
    ("👑", "Mahkota Permata"),      ("🛡️", "Perisai Tak Terkalahkan"),
    ("🔐", "Kunci Segala Harta"),   ("🏰", "Istana Emas"),
    ("🐴", "Kuda Perkasa"),         ("🕯️", "Lampu Keabadian"),
    ("🌊", "Samudra Kekayaan"),     ("⭐", "Bintang Keberuntungan"),
]


# --------------------------------------------------------------------------
# State permainan
# --------------------------------------------------------------------------
@dataclass
class Statistik:
    total_putar: int = 0
    jackpot: int = 0
    hadiah_biasa: int = 0
    zonk: int = 0
    koleksi: list[int] = field(default_factory=list)  # angka hadiah unik yang didapat

    @property
    def win_rate(self) -> float:
        if self.total_putar == 0:
            return 0.0
        menang = self.jackpot + self.hadiah_biasa
        return menang / self.total_putar * 100

    def simpan(self, path: Path = SAVE_FILE) -> None:
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @classmethod
    def muat(cls, path: Path = SAVE_FILE) -> "Statistik":
        if not path.exists():
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return cls(**data)
        except (json.JSONDecodeError, TypeError):
            return cls()  # file rusak -> mulai baru


# --------------------------------------------------------------------------
# Tampilan
# --------------------------------------------------------------------------
def garis(char: str = "=") -> None:
    print(char * LEBAR)


def judul() -> None:
    garis()
    print("🍀  GAME HOKI — ANGKA MELONCAT-LONCAT  🍀".center(LEBAR))
    garis()
    peluang_hadiah = (len(HADIAH) + 1) / (MAX_ANGKA - MIN_ANGKA + 1) * 100
    print(f"\n🎯 Angka {ANGKA_JACKPOT} = JACKPOT! SEGALA HARTA & KEKUASAAN!")
    print(f"🎁 {len(HADIAH)} angka lain memberi harta langka.")
    print("💀 Angka lainnya = ANGKA KEMATIAN!")
    print(f"📈 Peluang dapat sesuatu: {peluang_hadiah:.0f}%")


def animasi_acak(durasi: float = 1.2) -> None:
    """Animasi angka berputar sebelum hasil keluar."""
    langkah = int(durasi / 0.06)
    for _ in range(langkah):
        print(f"\r🔄  {random.randint(MIN_ANGKA, MAX_ANGKA):>3}  🔄", end="", flush=True)
        time.sleep(0.06)
    print("\r" + " " * 20 + "\r", end="")


def tampil_angka(angka: int) -> None:
    print("\n" + "✨" * (LEBAR // 2))
    print(f"🎲 Angka yang keluar: {angka}")
    print("✨" * (LEBAR // 2))


def tampil_jackpot() -> None:
    print("\n🏆🏆🏆  JACKPOT!!! ANGKA 67 DITEMUKAN!!! 🏆🏆🏆")
    print("👑 KAMU MEMENANGKAN SEGALANYA:")
    for i in range(0, len(JACKPOT_ITEMS), 2):
        kiri = JACKPOT_ITEMS[i]
        kanan = JACKPOT_ITEMS[i + 1]
        print(f"   {kiri[0]} {kiri[1]:<24}{kanan[0]} {kanan[1]}")
    print("\n💪 Kamu adalah PENGUASA SEGALA HARTA!")


def tampil_hadiah(angka: int, hadiah: Hadiah, baru: bool) -> None:
    print(f"\n{hadiah.emoji} Kamu mendapatkan {hadiah.nama} {hadiah.emoji}")
    print(hadiah.deskripsi)
    if baru:
        print("🆕 Koleksi baru!")
    else:
        print("🔁 Sudah ada di koleksimu.")


def tampil_zonk(angka: int) -> None:
    print("\n💀💀💀  ANGKA KEMATIAN!!!  💀💀💀")
    print(f"Angka {angka} bukan angka keberuntungan...")
    print("Kehampaan menyelimutimu. Tidak ada harta, hanya kesunyian abadi. 💀")


def tampil_statistik(s: Statistik) -> None:
    print()
    garis("-")
    print("📊 STATISTIK".center(LEBAR))
    garis("-")
    print(f"  Total putaran   : {s.total_putar}")
    print(f"  Jackpot (67)    : {s.jackpot}")
    print(f"  Hadiah biasa    : {s.hadiah_biasa}")
    print(f"  Angka kematian  : {s.zonk}")
    print(f"  Win rate        : {s.win_rate:.1f}%")
    print(f"  Koleksi         : {len(s.koleksi)}/{len(HADIAH)} hadiah unik")
    garis("-")


def tampil_koleksi(s: Statistik) -> None:
    print("\n🎒 KOLEKSI HARTAMU")
    garis("-")
    for angka, hadiah in sorted(HADIAH.items()):
        if angka in s.koleksi:
            print(f"  ✅ {hadiah.emoji} {hadiah.nama} (angka {angka})")
        else:
            print("  ❔ ??? (belum ditemukan)")
    garis("-")


# --------------------------------------------------------------------------
# Logika permainan
# --------------------------------------------------------------------------
def putar(s: Statistik) -> int:
    """Satu putaran: acak angka, perbarui statistik, tampilkan hasil."""
    print("\nSedang mengacak...")
    animasi_acak()
    angka = random.randint(MIN_ANGKA, MAX_ANGKA)
    s.total_putar += 1
    tampil_angka(angka)

    if angka == ANGKA_JACKPOT:
        s.jackpot += 1
        tampil_jackpot()
    elif angka in HADIAH:
        s.hadiah_biasa += 1
        baru = angka not in s.koleksi
        if baru:
            s.koleksi.append(angka)
        tampil_hadiah(angka, HADIAH[angka], baru)
    else:
        s.zonk += 1
        tampil_zonk(angka)
    return angka


def main() -> None:
    stat = Statistik.muat()
    judul()

    while True:
        print("\n[Enter] Putar   [s] Statistik   [k] Koleksi   [q] Keluar")
        pilihan = input("> ").strip().lower()

        if pilihan == "":
            putar(stat)
            stat.simpan()
        elif pilihan == "s":
            tampil_statistik(stat)
        elif pilihan == "k":
            tampil_koleksi(stat)
        elif pilihan == "q":
            break
        else:
            print("Pilihan tidak dikenal.")

    tampil_statistik(stat)
    print("Terima kasih sudah bermain! 🍀")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSampai jumpa! 👋")