## 📊 Metodologi Analisis

## 1. Perhitungan Tren & Moving AverageUntuk mereduksi noise dari penjualan harian,
   digunakan formula Simple Moving Average dengan jendela waktu 3 hari ($w=3$):$$\text{MA}_{3} = \frac{Y_{t} + Y_{t-1} + Y_{t-2}}{3}$$Logika penentuan durasi beruntun (Consecutive Rise) menggunakan segmentasi blok akumulasi biner.
   Jika tren bernilai True (Naik), indeks akan terus bertambah ($+1$). Jika False (Turun), indeks langsung dipaksa kembali ke angka 0.2.
   
   2. Aturan Asosiasi Keranjang Belanja (Apriori)Algoritma menyaring kombinasi produk di seluruh nomor struk belanja pelanggan menggunakan parameter indikator utama:
* Support:* Mengukur seberapa sering kombinasi produk muncul dalam basis data transaksi.
* Confidence:* Mengukur tingkat kepastian/probabilitas produk B dibeli jika pelanggan membeli produk A.
* Lift Score:* Jika $\text{Lift} > 1$,kedua produk memiliki hubungan asosiasi positif kuat (bukan kebetulan acak) dan sangat valid untuk dijadikan paket promosi (Product Bundling).
