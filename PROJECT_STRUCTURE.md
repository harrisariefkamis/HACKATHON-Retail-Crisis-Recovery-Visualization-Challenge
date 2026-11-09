# Struktur Proyek Analisis Retail

Dokumen ini merangkum komponen repository yang relevan untuk analisis hackathon DQLab Retail Crisis and Recovery.

## Struktur saat ini

```text
.
├── data_penjualan.csv                 # Data transaksi yang tersedia di repository
├── solusi_retail.py                   # Analisis tren, Apriori, ekspor Excel, dan visualisasi
├── solusi_retail.ipynb                 # Notebook analisis
├── Examp:Projet hackathon.ipynb        # Notebook contoh/eksperimen
├── Method Analisis.md                  # Ringkasan metodologi
├── Consecutive Rise Analysis.tx        # Catatan analisis tren beruntun
├── rising_star_index.png               # Visualisasi indeks
├── rising_star_actual.png              # Visualisasi nilai aktual
├── README.md                           # Dokumentasi repository
└── [file konfigurasi dan aplikasi web]  # package.json, server.ts, index.html, dan file terkait
```

## Alur analisis yang dituju

1. Membaca data transaksi dan memvalidasi kolom serta formatnya.
2. Mengagregasikan `total_nilai` per tanggal dan produk.
3. Membuat deret tanggal harian lengkap per produk dan menghitung moving average 3 hari.
4. Mendeteksi sesi kenaikan MA dan memilih produk dengan sekurangnya 12 kenaikan harian berturut-turut.
5. Menghitung pertumbuhan dari MA sebelum sesi sampai MA terakhir dalam sesi.
6. Membentuk keranjang produk per `nomor_struk`, menjalankan Apriori, lalu menyaring association rules yang melibatkan Rising Star dan memiliki lift minimal 2.
7. Menghasilkan Excel dengan sheet `Rising Star` dan `Potential Packaging`, serta grafik indeks dan nilai penjualan aktual.

## Temuan dan isu yang perlu ditangani

- Soal mengharapkan input `sales_transaction.csv`, sedangkan repository menyediakan `data_penjualan.csv` dan script `solusi_retail.py` membaca `data_penjualan.xlsx` (sheet `Transaksi`). Samakan file input, format, delimiter, dan nama kolom sebelum menjalankan script.
- Soal meminta output `retail_insight.xlsx`, sedangkan script saat ini menggunakan `retail-insight.xlsx`. Samakan nama output.
- Rolling MA pada script perlu dihitung pada kalender harian lengkap. Tanpa tanggal yang tidak memiliki transaksi, rolling tiga baris belum tentu mewakili tiga hari kalender.
- Growth sesi tren sebaiknya membandingkan MA terakhir sesi dengan MA tepat sebelum kenaikan pertama, agar semua kenaikan dalam sesi tercakup.
- Dokumentasi menyebut beberapa nama file yang tidak konsisten dengan file aktual. Perbarui dokumentasi saat input dan output final telah ditetapkan.
- Soal menyebut satu tab tetapi juga meminta dua bagian bernama `Rising Star` dan `Potential Packaging`; konfirmasikan interpretasi format workbook. Implementasi saat ini membuat dua sheet.

> Catatan: tanpa dataset hackathon yang dipastikan benar dan eksekusi script yang telah diperbaiki, SKU Rising Star dan rekomendasi packaging aktual belum dapat disimpulkan dari struktur repository saja.
