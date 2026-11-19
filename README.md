# Ringkasan Berita Dunia — Kamis, 19 November 2026

[![Kompetisi news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Peringkat](https://make.fun/badge/news-image-20261119/swaetczher/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Hadiah](https://make.fun/badge/news-image-20261119/swaetczher/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

Program Python yang menulis satu gambar ringkasan berita dunia hari Kamis,
19 November 2026 ke `/output/entry.png`, dibuat untuk kompetisi
[news-image-20261119 di make.fun](https://make.fun/bounty/news-image-20261119).

## Cara jalan

```sh
python3 main.py
```

Program tidak butuh jaringan dan tidak butuh dependensi di luar pustaka
standar Python: ia menyalin gambar 1024×1024 piksel yang sudah dirender dan
disimpan di repo sebagai `entry.png` (maks 1 MiB), lalu memverifikasi ukuran
dan sha256-nya. Dua kali jalan menghasilkan byte yang sama.

## Isi gambar

Satu halaman bergaya koran: judul + tanggal, berita utama hari itu, dan
beberapa berita lain dari berbagai kawasan dan bidang — masing-masing dengan
judul singkat dan satu-dua baris isi — tersusun rapi dan terbaca pada lebar
~300 piksel.

## File

- `main.py` — entrypoint: menyalin dan memverifikasi `entry.png` (stdlib-only)
- `render.py` — mesin gambar yang menghasilkan `entry.png` saat build
- `layout.py` — konstanta layout + helper teks
- `news_data.py` — data berita 19 November 2026 yang diringkas
