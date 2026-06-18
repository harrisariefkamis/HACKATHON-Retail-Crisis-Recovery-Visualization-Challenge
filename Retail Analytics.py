```markdown
# 📊 Retail Analytics: Consecutive Rise Trend & Market Basket Analysis (Apriori)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Data Mining](https://img.shields.io/badge/Data%20Mining-Apriori-orange.svg)]()
[![Time Series](https://img.shields.io/badge/Time%20Series-Moving%20Average-green.svg)]()

Proyek ini adalah instrumen analitik data ritel komprehensif yang dirancang untuk portofolio profesional. Sistem ini menggabungkan dua metodologi analisis canggih: **Analisis Tren Waktu (Time Series)** untuk mendeteksi momentum kenaikan penjualan produk target secara beruntun, serta **Market Basket Analysis (Data Mining)** menggunakan algoritma Apriori untuk menemukan pola perilaku belanja tersembunyi dari pelanggan.

---

## 🎯 7 Pilar Analisis Utama

Proyek ini mengotomatiskan dan mengeksekusi tujuh tahapan analitik berikut:
1. **Penyaringan Produk Spesifik (`ARAB250gr`)**: Melakukan ekstraksi otomatis dan agregasi harian (*Sum of Total Nilai*) dari data mentah transaksi.
2. **Perhitungan Moving Average (MA-3)**: Menghitung rata-rata bergerak 3 hari guna menghaluskan (*smoothing*) fluktuasi penjualan harian yang ekstrem untuk identifikasi tren yang lebih stabil.
3. **Pemuatan Data Riil (`data_penjualan.csv`)**: Membaca file transaksi komersial dengan pembatas titik koma (`;`) secara efisien.
4. **Identifikasi Tren Naik**: Menentukan arah pergerakan pasar secara matematis jika nilai MA hari ini lebih besar dibanding hari sebelumnya ($MA_{t} > MA_{t-1}$).
5. **Kalkulasi Durasi Kenaikan Berturut-turut (*Consecutive Rise*)**: Algoritma cerdas yang menghitung berapa hari penjualan naik tanpa terputus, dan otomatis mereset kembali ke angka `0` tepat saat tren mulai menurun.
6. **Data Mining & Association Rules (Metode Apriori)**: Mengekstrak metrik kunci *Basket Analysis* berupa **Support** (Popularitas kombinasi), **Confidence** (Kepastian relasi), dan **Lift Score** (Kekuatan dependensi produk).
7. **Ekspor Data & Visualisasi Eksekutif**: Menghasilkan grafik tren modern (*Line Chart*) dan laporan spreadsheet multi-sheet profesional berstandar korporat.

---

## 🛠️ Tech Stack & Pustaka

Proyek ini dibangun sepenuhnya menggunakan ekosistem sains data Python:
* **Pandas** & **NumPy**: Manipulasi matriks, pembersihan data, sinkronisasi tanggal, dan agregasi harian.
* **Mlxtend**: Pemrosesan algoritma data mining frekuensi itemset (Apriori) dan pembentukan aturan asosiasi.
* **Matplotlib**: Pembuatan visualisasi grafik tren garis dan panel informasi *insight*.
* **OpenPyXL**: Mesin penulisan spreadsheet yang dikustomisasi dengan gaya desain eksekutif (*styling formatting*).

---

## 📁 Struktur Repositori

```text
├── data_penjualan.csv                  # Dataset mentah transaksi ritel (CSV; delimiter ';')
├── analisis_consecutive_rise.py        # Skrip utama pemrosesan data (Python Engine)
├── Portfolio_Analisis_Retail_Dashboard.xlsx # Hasil laporan eksekutif terstruktur (Multi-Sheet)
├── dashboard_tren_penjualan.png        # Hasil visualisasi tren grafis siap pakai
└── README.md                           # Dokumentasi portofolio proyek (File ini)
