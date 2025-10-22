# 🗺️ TSP Heuristic Optimizer

Aplikasi web interaktif untuk menyelesaikan Traveling Salesman Problem (TSP) menggunakan berbagai metode heuristik konstruksi dan optimasi 3-Opt.

## 📋 Fitur

- ✅ **Generate Data Random**: Buat data kota secara otomatis
- ✅ **Upload CSV**: Import data kota dari file CSV
- ✅ **5 Metode Heuristik Konstruksi**:
  - Nearest Neighbor (NN)
  - Nearest Insertion (NI)
  - Farthest Insertion (FI)
  - Cheapest Insertion (CI)
  - Arbitrary Insertion (AI)
- ✅ **3-Opt Optimization**: Perbaikan rute dengan algoritma 3-Opt
- ✅ **Visualisasi Interaktif**: Lihat rute TSP secara visual
- ✅ **Tabel Perbandingan**: Bandingkan performa setiap metode
- ✅ **Riwayat Hasil**: Simpan dan lihat hasil eksperimen sebelumnya
- ✅ **Download Template CSV**: Template format input data

## 📁 Struktur File

```
tsp-optimizer/
│
├── app.py                 # Aplikasi utama Streamlit
├── tsp_solver.py          # Modul algoritma TSP
├── requirements.txt       # Dependencies Python
├── README.md              # Dokumentasi
└── .streamlit/            # (opsional) Konfigurasi Streamlit
    └── config.toml
```

## 🚀 Cara Menjalankan Lokal

### 1. Clone atau Download Repository

```bash
# Buat folder project
mkdir tsp-optimizer
cd tsp-optimizer
```

### 2. Buat File-File yang Diperlukan

Buat 3 file utama:
- `app.py` (copy dari artifact pertama)
- `tsp_solver.py` (copy dari artifact kedua)
- `requirements.txt` (copy dari artifact ketiga)

### 3. Install Dependencies

```bash
# Buat virtual environment (opsional tapi direkomendasikan)
python -m venv venv

# Aktifkan virtual environment
# Untuk Windows:
venv\Scripts\activate
# Untuk Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## 🌐 Deploy ke Streamlit Cloud

### Persiapan

1. **Buat akun GitHub** (jika belum punya): https://github.com
2. **Buat akun Streamlit Cloud**: https://streamlit.io/cloud

### Langkah Deployment

#### Opsi 1: Deploy dari GitHub (Recommended)

1. **Upload ke GitHub**:
   ```bash
   # Inisialisasi git repository
   git init
   
   # Tambahkan semua file
   git add .
   
   # Commit
   git commit -m "Initial commit - TSP Optimizer"
   
   # Buat repository di GitHub, lalu:
   git remote add origin https://github.com/USERNAME/tsp-optimizer.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy di Streamlit Cloud**:
   - Login ke https://share.streamlit.io
   - Klik "New app"
   - Pilih repository GitHub Anda
   - Main file path: `app.py`
   - Klik "Deploy"

#### Opsi 2: Deploy Langsung

1. Login ke Streamlit Cloud
2. Klik "New app" → "Paste GitHub URL"
3. Masukkan URL repository
4. Atur:
   - **Branch**: main
   - **Main file path**: app.py
5. Klik "Deploy"

### Troubleshooting Deployment

Jika ada error saat deployment:

1. **Module not found error**:
   - Pastikan semua module ada di `requirements.txt`
   - Cek versi Python yang kompatibel

2. **Import error**:
   - Pastikan `tsp_solver.py` ada di folder yang sama dengan `app.py`

3. **Memory error**:
   - Batasi jumlah kota maksimal (misalnya 30 kota)
   - Matikan opsi yang tidak diperlukan

## 📊 Format CSV Input

File CSV harus memiliki 3 kolom: `city_id`, `x`, `y`

### Contoh Format CSV:

```csv
city_id,x,y
1,100,200
2,300,400
3,500,100
4,700,500
5,900,300
```

### Download Template

Aplikasi menyediakan tombol **"Download Template CSV"** di sidebar untuk mengunduh template yang sudah sesuai format.

## 🎯 Cara Penggunaan

### 1. Input Data

**Opsi A: Generate Random**
- Pilih "Generate Random" di sidebar
- Atur jumlah kota (5-50)
- Atur koordinat maksimal X dan Y
- Klik "Generate Cities"

**Opsi B: Upload CSV**
- Pilih "Upload CSV" di sidebar
- Download template jika perlu
- Upload file CSV Anda
- Data akan divalidasi otomatis

### 2. Pilih Metode Heuristik

Centang metode yang ingin dijalankan:
- ✅ Nearest Neighbor (NN) - Cepat, hasil lumayan
- ✅ Nearest Insertion (NI) - Hasil lebih baik dari NN
- ✅ Farthest Insertion (FI) - Bagus untuk distribusi merata
- ✅ Cheapest Insertion (CI) - Sering memberikan hasil terbaik
- ✅ Arbitrary Insertion (AI) - Random, perlu multiple runs

### 3. Aktifkan 3-Opt (Opsional)

Centang "Gunakan 3-Opt Optimization" untuk memperbaiki hasil konstruksi.

⚠️ **Note**: 3-Opt membutuhkan waktu lebih lama, terutama untuk jumlah kota > 30.

### 4. Run Optimization

Klik tombol **"▶️ Run Optimization"**

Aplikasi akan:
1. Menjalankan setiap metode konstruksi
2. Mengaplikasikan 3-Opt (jika diaktifkan)
3. Menampilkan hasil dalam tabel
4. Visualisasi rute terbaik
5. Chart perbandingan

### 5. Analisis Hasil

- **Tabel Hasil**: Lihat performa setiap metode
- **Visualisasi Rute**: Rute terbaik ditampilkan dengan garis dan marker
- **Chart Perbandingan**: Bandingkan jarak sebelum dan sesudah 3-Opt
- **Riwayat**: Lihat hasil eksperimen sebelumnya

## 📈 Interpretasi Hasil

### Kolom Tabel Hasil:

- **Method**: Nama metode heuristik
- **Initial Distance**: Jarak total sebelum 3-Opt
- **Final Distance**: Jarak total setelah 3-Opt
- **Improvement (%)**: Persentase perbaikan dari 3-Opt
- **Construction Time**: Waktu eksekusi konstruksi awal
- **3-Opt Time**: Waktu eksekusi 3-Opt
- **Total Time**: Total waktu komputasi

### Tips Memilih Metode:

1. **Untuk kecepatan**: Gunakan Nearest Neighbor tanpa 3-Opt
2. **Untuk kualitas**: Gunakan Cheapest Insertion + 3-Opt
3. **Untuk eksperimen**: Coba semua metode dan bandingkan

## ⚙️ Konfigurasi Lanjutan (Opsional)

Buat folder `.streamlit` dan file `config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 10
```

## 🔧 Optimasi Performa

### Untuk Dataset Besar (>30 kota):

1. **Batasi metode**: Pilih hanya 1-2 metode terbaik
2. **Matikan 3-Opt**: Atau gunakan untuk metode terbaik saja
3. **Reduce AI runs**: Kurangi jumlah runs untuk Arbitrary Insertion

### Memory Management:

- Streamlit Cloud: 1GB RAM limit
- Local: Tergantung spesifikasi komputer
- Rekomendasi: Maksimal 50 kota untuk deployment cloud

## 📚 Algoritma yang Digunakan

### Konstruksi Heuristics:

1. **Nearest Neighbor (NN)**: Greedy - pilih kota terdekat
2. **Nearest Insertion (NI)**: Insert kota terdekat ke tour
3. **Farthest Insertion (FI)**: Insert kota terjauh ke tour
4. **Cheapest Insertion (CI)**: Insert kota dengan biaya minimal
5. **Arbitrary Insertion (AI)**: Insert kota secara random

### Improvement Heuristic:

**3-Opt**: Mencoba 7 kemungkinan reconnection untuk setiap 3 edge break, menggunakan first-improvement strategy.

## 🐛 Known Issues & Limitations

1. **3-Opt lambat untuk >40 kota**: Kompleksitas O(n³)
2. **Browser memory**: Visualisasi berat untuk banyak kota
3. **Random seed**: Arbitrary Insertion bisa berbeda setiap run

## 📞 Support

Jika ada pertanyaan atau issue:
1. Check dokumentasi di atas
2. Lihat contoh CSV template
3. Mulai dengan dataset kecil (10-15 kota) untuk testing

## 📄 License

Free to use untuk keperluan pendidikan dan penelitian.

## 🎓 Credits

Implementasi berdasarkan:
- TSP Construction Heuristics (Rosenkrantz et al.)
- 3-Opt Local Search (Lin & Kernighan)

---

**Happy Optimizing! 🚀**
