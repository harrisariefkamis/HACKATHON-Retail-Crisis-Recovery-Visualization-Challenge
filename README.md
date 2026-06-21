# 📊 Retail Data Analytics: Consecutive Rise Trend & Market Basket Analysis (Apriori)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Data Mining](https://img.shields.io/badge/Data%20Mining-Apriori-orange.svg)]()
[![Time Series](https://img.shields.io/badge/Time%20Series-Moving%20Average-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-informational.svg)]()

<p align="center">
  <img src="workflow hackathon python.png"alt="Dashboard Portofolio Analyst Retail" width="500%">
</p>

<p align="center">
  <img src="[https://portfolio-analisis-retail-dashboard-142260617876.asia-southeast1.run.app/]"alt="Dashboard Portofolio Analyst Retail" width="50%">
</p>

Infrastruktur End to End Project ini memadukan **Analisis Tren Waktu (Time Series)** menggunakan metode rata-rata bergerak untuk mendeteksi momentum kenaikan penjualan produk target secara beruntun, serta **Market Basket Analysis (Data Mining)** dengan algoritma Apriori untuk mengidentifikasi perilaku belanja silang (*cross-selling*) pelanggan.

---

## 🎯 7 Pilar Analisis Utama

Framework data analsisis ini saya bangun dengan pendekatan Data Understanding,Problem Solving dan Decision Making untuk memnbangun sistem otomatisasi yang dirancang dengan mengeksekusi runtunan logika analitik berikut:
1. **Penyaringan & Agregasi**: Melakukan ekstraksi otomatis pada produk target (`ARAB250gr`) dan mengagregasikan nilai omzet harian (*Sum of Total Nilai*).
2. **Kalkulasi Moving Average (MA)**: Menghitung rata-rata bergerak 3 hari untuk mereduksi *noise* fluktuasi harian yang tidak beraturan.
3. **Pemuatan Data Fleksibel**: Membaca file data terstruktur (`data_penjualan.csv`) dengan pembatas titik koma (`;`) serta menangani variasi format tanggal.
4. **Identifikasi Tren**: Menilai arah pergerakan pasar secara harian untuk mendeteksi momentum pertumbuhan positif.
5. **Kalkulasi Durasi Beruntun (*Consecutive Rise*)**: Algoritma cerdas yang menghitung berapa hari penjualan naik tanpa terputus, dan otomatis mereset kembali ke angka `0` tepat saat tren mulai menurun.
6. **Data Mining Aturan Asosiasi (Apriori)**: Mengekstrak metrik keterikatan antarproduk melalui nilai *Support*, *Confidence*, dan *Lift Score*.
7. **Ekspor Data & Visualisasi Eksekutif**: Menghasilkan grafik tren interaktif (*Line Chart*) dan laporan spreadsheet *multi-sheet* formal berstandar korporat.

---

## 🛠️ Tech Stack & Dependensi

Proyek ini dibangun sepenuhnya menggunakan ekosistem sains data Python:
* **Pandas & NumPy**: Manipulasi matriks data, sinkronisasi format waktu, dan agregasi harian.
* **Mlxtend**: Pemrosesan algoritma data mining frekuensi itemset (Apriori) dan pembentukan aturan asosiasi.
* **Matplotlib**: Pembuatan grafik visualisasi visual tren garis dan panel informasi *insight*.
* **OpenPyXL**: Mesin penulisan spreadsheet yang dikustomisasi dengan gaya desain eksekutif (*corporate formatting style*).

---

## 📁 Struktur Repositori

```text
├── data_penjualan.csv                      # Dataset mentah transaksi ritel (CSV; delimiter ';')
├── analisis_consecutive_rise_apriori.py    # Skrip utama pemrosesan data (Python Engine)
├── Portfolio_Analisis_Retail_Dashboard.xlsx # Hasil laporan eksekutif terstruktur (Multi-Sheet)
├── dashboard_tren_penjualan.png            # Hasil visualisasi tren grafis siap pakai
└── README.md                               # Dokumentasi portofolio proyek (File ini)

```

---

## 📊 Metodologi & Formulasi Matematis

### 1. Simple Moving Average 3-Hari (SMA-3)

Untuk menghaluskan volatilitas fluktuasi harian, nilai rata-rata dihitung berdasarkan jendela bergerak 3 hari ($w=3$) menggunakan formula:

$$\text{MA}_{3} = \frac{Y_{t} + Y_{t-1} + Y_{t-2}}{3}$$

Di mana $Y_{t}$ merupakan total nilai penjualan aktual pada hari ke-$t$. Tren didefinisikan sebagai **Naik** jika nilai $\text{MA}_{t} > \text{MA}_{t-1}$.

### 2. Aturan Asosiasi (Market Basket Analysis)

Algoritma Apriori bekerja dengan mengukur kekuatan kombinasi produk menggunakan tiga metrik evaluasi utama:

* **Support**: Mengukur tingkat popularitas atau seberapa sering kombinasi produk muncul dalam basis data transaksi.

$$\text{Support}(A \implies B) = P(A \cap B)$$


* **Confidence**: Mengukur tingkat kepastian/probabilitas produk B dibeli jika pelanggan membeli produk A.

$$\text{Confidence}(A \implies B) = \frac{P(A \cap B)}{P(A)}$$


* **Lift Score**: Mengukur kekuatan ketergantungan antarproduk. Nilai $\text{Lift} > 1$ membuktikan adanya hubungan asosiasi positif yang kuat (bukan kebetulan acak).

$$\text{Lift}(A \implies B) = \frac{P(A \cap B)}{P(A) \times P(B)}$$



---

## 🚀 Cara Menjalankan Proyek

### 1. Kloning Repositori

```bash
git clone [https://github.com/harrisariefkamis/HACKATHON-Retail-Crisis-Recovery-Visualization-Challenge.git](https://github.com/harrisariefkamis/HACKATHON-Retail-Crisis-Recovery-Visualization-Challenge.git)
cd nama-repositori

```

### 2. Instalasi Pustaka Dependensi

Pastikan Anda telah menginstal seluruh library yang dibutuhkan dengan menjalankan perintah berikut di terminal:

```bash
pip install pandas numpy mlxtend matplotlib openpyxl

```

### 3. Eksekusi Program

Pastikan file data transaksi Anda berada di folder yang sama dengan nama `data_penjualan.csv`, lalu jalankan program:

```bash
python analisis_consecutive_rise_apriori.py

```

---

## 📈 Output Proyek & Wawasan Bisnis

### 🟢 1. Dashboard Tren Komersial (`dashboard_tren_penjualan.png`)

Menampilkan visualisasi komparatif yang tajam antara fluktuasi riil harian (*grey dashed line*) dengan garis tren halus *Moving Average* (*orange solid line*). Grafik dilengkapi dengan **Insight Box** dinamis yang mendeteksi rekor durasi kenaikan beruntun terlama beserta tanggal puncaknya secara otomatis untuk kebutuhan presentasi bisnis.

### 🟢 2. Spreadsheet Laporan Korporat (`Portfolio_Analisis_Retail_Dashboard.xlsx`)

File Excel yang dihasilkan dikustomisasi menggunakan standar analitik profesional:

* **Sheet "Analisis Tren Harian"**: Menyajikan riwayat penjualan, nilai MA-3, status tren, dan durasi kenaikan beruntun harian untuk produk `ARAB250gr`.
* **Sheet "Market Basket Analysis"**: Menampilkan tabel strategi komersial berisi aturan kombinasi produk pendamping, jumlah invoice yang terdampak, lengkap dengan kolom nilai *Support*, *Confidence*, dan *Lift Score* yang telah diurutkan berdasarkan kekuatan relasi tertinggi.
* **Spesifikasi Tampilan**: Memiliki pembekuan baris judul (*Freeze Panes*) agar mudah dibaca saat di-scroll, warna latar header *Navy Blue* formal, border tipis abu-abu, dan lebar kolom otomatis dinamis (*Auto-fit dimensions*) untuk mencegah eror karakter tanda pagar (`###`).

---

## 👨‍💻 Kontak & Kolaborasi

📧 **Email:** [harisariefkamis16@gmail.com](https://www.google.com/search?q=mailto%harisariefkamis16@gmail.com)

🔗 **LinkedIn:** [linkedin.com/in/harisariefkamis](https://www.google.com/search?q=https://linkedin.com/in/harisariefkamis)

💼 **Portfolio:** [github.com/harrisariefkamis](https://www.google.com/search?q=https://github.com/harrisariefkamis)

```

```
