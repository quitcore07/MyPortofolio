# 🎲 Roll & Loot

> **Project coding Python: game loot berbasis terminal.**
> Dimainkan langsung lewat terminal (command line), tanpa tampilan grafis.

## 📖 Tentang

**Roll & Loot** adalah game sederhana buatan saya dengan Python untuk melatih logika pemrograman. Setiap putaran, komputer mengacak satu angka dari 1 sampai 100:

- 🏆 **Angka 67**: jackpot, dapat semua harta
- 🎁 **19 angka tertentu**: dapat harta langka (Pedang Raja Sakti, Mahkota Dewa, Kuda Bersayap, dan lainnya)
- 💀 **Angka lainnya**: angka kematian, tidak dapat apa-apa

Tujuannya: kumpulkan semua harta dan temukan angka 67.

## ✨ Fitur

Animasi pengacakan · Koleksi harta · Statistik permainan (total putaran, jackpot, win rate) · Progres tersimpan otomatis ke file JSON

## 🚀 Cara Main

**Kebutuhan:** [Python 3.8+](https://www.python.org/downloads/) dan terminal (Command Prompt, PowerShell, atau Terminal). Tidak perlu instal library tambahan.

1. Unduh file `roll_loot.py` atau clone repo ini:
   ```bash
   git clone https://github.com/quitcore07/roll-loot.git
   cd roll-loot
   ```
2. Jalankan di terminal:
   ```bash
   python roll_loot.py
   ```
   (Di macOS/Linux: `python3 roll_loot.py`)
3. Mainkan dengan tombol berikut:

| Tombol  | Fungsi                   |
| ------- | ------------------------ |
| `Enter` | Putar angka              |
| `s`     | Lihat statistik          |
| `k`     | Lihat koleksi harta      |
| `q`     | Keluar                   |

💡 Progres tersimpan di `hoki_save.json`. Hapus file itu untuk mengulang dari nol. Di Windows, gunakan **Windows Terminal** agar emoji tampil dengan benar.

## 🛠️ Teknologi

Python 3.8+ (hanya library bawaan: `random`, `json`, `time`, `dataclasses`, `pathlib`)
