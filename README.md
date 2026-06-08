# HACKATHON-Retail-Crisis-Recovery-Visualization-Challenge

DASHBOARD PLANT:https://retail-growth-association-panel-142260617876.asia-southeast1.run.app

---
Retail Crisis & Recovery-Visualization Challenge with Python
---

Generate Library Python 
- Pandas
- Numpy
- Matplotlin
- Seaborn
---

Data Understanding
1. Data Cleansing
2. Data Processing
3. Data Analysis
5. Data Visualization
6. Decision Making


├── README.md                  <- Dokumentasi lengkap, latar belakang bisnis, & cara menjalankan code
├── solusi_retail.py           <- Source code python utama Anda
├── retail-insight.xlsx        <- Output file Excel hasil generator openpyxl
├── rising_star_index.png      <- Grafik visualisasi indeks pertumbuhan
└── rising_star_actual.png     <- Grafik visualisasi nominal penjualan asli

DATA_PENJUALAN  <- Type Data
nomor_struk	    <- String
tgl_transaksi	  <- Datetime
 kode_produk	    <- String
nama_produk	    <- String
jumlah_terjual	<- Integer
harga	          <- integer
total_nilai	    <- integer


# 📊 End-to-End Retail Data Pipeline: Time-Series Trend Detection & Market Basket Analysis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org)
[![Licence](https://img.shields.io/badge/licence-MIT-green.svg)](LICENSE)

Anomali data harian dan fluktuasi pasar sering kali menyamarkan tren produk potensial yang sesungguhnya. Proyek ini membangun sebuah *End-to-End Data Pipeline* otomatis menggunakan Python untuk mengolah data *time-series* penjualan retail yang kompleks dan *noisy*. Sistem ini secara cerdas mengintegrasikan dua mesin analisis bisnis: **Trend Tracking (Moving Average)** untuk mendeteksi performa *Rising Star*, dan **Market Basket Analysis (Algoritma Apriori)** untuk merumuskan strategi paket produk (*product bundling*) berbasis keterikatan statistik yang kuat.

---

## 🎯 Masalah Bisnis & Dampak (Business Case)
* **Tantangan Data Mentah:** Log transaksi berskala besar sangat rentan terhadap data pencilan (*outliers*) akibat promosi sesaat, hari libur, atau kendala stok harian. Fluktuasi jangka pendek (*noise*) ini menyulitkan manajemen dalam mengidentifikasi pertumbuhan organik jangka panjang.
* **Kehilangan Peluang Penjualan:** Manajemen sering kali terlambat menyadari produk baru yang sedang populer (*Rising Star*), serta gagal mengoptimalkan penjualan silang (*cross-selling*) karena penyusunan paket produk (*bundling*) masih mengandalkan intuisi manual, bukan pembuktian empiris.
* **Solusi Proyek:** Pipeline ini mengeliminasi *noise* data melalui teknik *smoothing* berbasis waktu, menyaring produk dengan tren positif konsisten minimal 12 hari berturut-turut, dan secara otomatis merekomendasikan paket produk terbaik yang wajib melibatkan produk tren tersebut.

---

## 🛠️ Tech Stack & Library Python
Proyek ini mengutamakan efisiensi pemrosesan data menggunakan kombinasi pustaka berkinerja tinggi:
* **Pandas & NumPy:** Ingesti data, agregasi matriks multi-level, penanganan runtun waktu (*datetime*), kalkulasi jendela bergerak (*rolling window*), dan transformasi logika kondisional.
* **MLxtend (Apriori & Association Rules):** Ekstraksi pola keterkaitan item (*frequent itemsets*) dan kalkulasi parameter asosiasi (*Support, Confidence, Lift*).
* **Openpyxl:** Pembuatan *automated spreadsheet reporting* dari Python langsung ke format Excel korporat siap pakai.
* **Matplotlib:** Mesin visualisasi data untuk menghasilkan grafik multi-axis beresolusi tinggi (DPI 100) dengan kustomisasi palet warna berbasis peringkat.

---

## 🧬 Arsitektur & Framework Data Pipeline
Alur kerja pemrosesan data dirancang secara linear mengacu pada *Data Analytics Lifecycle Framework*:

```mermaid
graph TD
    A[Data Mentah: Excel] --> B[1. Data Cleansing & Agregasi Harian]
    B --> C[2. Data Processing: 3-Day Moving Average]
    C --> D[3. Normalisasi: Indeks Base-100]
    D --> E[4. Dual-Engine Analysis]
    E --> E1[Engine A: Sesi Tren Naik >= 12 Hari]
    E --> E2[Engine B: Matriks Asosiasi Apriori]
    E1 --> F[Cross-Filter Validation: Lift >= 2]
    E2 --> F
    F --> G[5. Visualisasi & Automated Export]
    G --> G1[Laporan: retail-insight.xlsx]
    G --> G2[Grafik Tren: PNG Plots]
