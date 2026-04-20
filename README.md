# ☢️ Simulasi Rekonstruksi Tomografi Interaktif (Metode ART)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/) 
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyek ini adalah simulator interaktif berbasis web untuk mendemonstrasikan **Algebraic Reconstruction Technique (ART)**, sebuah algoritma fundamental yang digunakan dalam tomografi terkomputasi (seperti CT Scan) untuk merekonstruksi citra matriks berdasarkan proyeksi sinar-X.

---

## ✨ Fitur Utama

Simulator ini menawarkan pengalaman belajar yang komprehensif melalui 6 tab interaktif:

* **👁️ Perbandingan Citra Real-time:** Bandingkan hasil rekonstruksi algoritma ART secara *side-by-side* dengan citra asli (*Ground Truth/Phantom*).
* **📊 Sinogram & Data Sensor:** Visualisasi data 'mentah' pembacaan sensor intensitas sinar horizontal (baris) dan vertikal (kolom).
* **🔍 Analisis Error per Pixel:** *Heatmap* divergen yang menyoroti dengan tepat di mana algoritma melakukan "salah tebak" dibandingkan dengan aslinya.
* **📈 Grafik Konvergensi:** Pantau nilai *Root Mean Square Error* (RMSE) yang menurun secara *real-time* untuk membuktikan kestabilan algoritma.
* **🧊 Topologi 3D:** Jelajahi distribusi intensitas piksel citra dalam bentuk permukaan elevasi 3D interaktif.
* **🔢 Kalkulator Langkah Manual:** Fitur edukasi yang membedah rumus matematika ART dan menghitung nilai pembaruan per baris/kolom secara transparan.

---

## 🛠️ Panel Simulasi

Anda memiliki kontrol penuh atas variabel lingkungan tomografi:
* **Resolusi Matriks (n x n):** Ubah ukuran dari 2x2 (untuk perhitungan manual) hingga 20x20 (untuk simulasi citra kompleks).
* **Injeksi Noise (Derau Sensor):** Simulasikan ketidaksempurnaan mesin sinar-X di dunia nyata dengan menambahkan derau acak pada pembacaan sensor.
* **Faktor Relaksasi (λ):** Atur kecepatan pembelajaran algoritma untuk melihat efek *under-relaxation* pada stabilitas konvergensi.
* **Mode Eksekusi:** Jalankan secara *Step-by-step* (1 Iterasi), Cepat (10/50 Iterasi), atau gunakan **Mode Auto-Play** untuk melihat animasi proses rekonstruksi.

---

## 🚀 Cara Menjalankan Secara Lokal

Jika Anda ingin menjalankan atau memodifikasi kode ini di komputer Anda sendiri:
```
1. Clone Repositori
bash
git clone https://github.com/Ghazy-Abiyyu-M/simulasi-tomografi.git
cd simulasi-tomografi
2. Instal DependensiPastikan Anda sudah menginstal Python. Disarankan menggunakan virtual environment.Bashpip install -r requirements.txt
3. Jalankan AplikasiBashstreamlit run tomo.py
```
Aplikasi akan secara otomatis terbuka di browser Anda pada alamat http://localhost:8501.

📖Konsep Dasar Matematis Algoritma ART bekerja secara iteratif untuk menyelesaikan sistem persamaan linear besar ($Ax = b$). Pada setiap langkah iterasi, nilai setiap sel (piksel) diperbarui menggunakan rumus koreksi, di mana selisih antara target pembacaan sensor dan jumlah nilai saat ini didistribusikan secara merata ke seluruh sel yang dilewati oleh sinar tersebut.

