# Implementasi Game Connect-Four Berbasis GUI Menggunakan Algoritma Minimax

Proyek ini adalah implementasi dari game klasik Connect-Four untuk dua pemain (Player vs. AI) yang dibuat sebagai tugas Ujian Akhir Semester (UAS) mata kuliah Analisa dan Perancangan Algoritma.

Fokus utama dari proyek ini adalah implementasi **Algoritma Minimax** dari nol untuk memberikan kecerdasan buatan (AI) yang dapat mengambil langkah optimal. Aplikasi ini juga berfungsi sebagai media pembelajaran interaktif untuk memahami cara kerja algoritma dalam teori permainan.

## Fitur Utama

- **GUI Modern**: Antarmuka dibangun menggunakan `customtkinter` dengan tema gelap (dark mode) yang profesional.
- **Papan Permainan Interaktif**: Papan permainan 7x6 digambar menggunakan `tkinter.Canvas`, lengkap dengan efek gravitasi saat bidak dijatuhkan.
- **Player vs. AI**: Mode permainan melawan AI yang menggunakan algoritma Minimax.
- **Implementasi Minimax**:
  - Algoritma Minimax murni yang ditulis dari nol (from scratch).
  - Menggunakan **Depth Limit** (batas kedalaman pencarian) untuk mengontrol kompleksitas.
  - Dilengkapi **Heuristic Evaluation Function** untuk menilai posisi di papan yang belum mencapai kondisi akhir.
- **Analisis Performa Real-time**:
  - GUI menampilkan metrik penting setelah setiap langkah AI:
    - Waktu eksekusi algoritma (dalam milidetik).
    - Jumlah total node yang dievaluasi dalam pohon pencarian Minimax.
    - Kedalaman pencarian (depth) yang digunakan.
  - Terdapat juga notasi kompleksitas waktu teoritis **O(b^d)** sebagai referensi akademis.
- **Struktur Kode Modular**: Proyek dipisahkan ke dalam modul-modul yang jelas: GUI, logika game, algoritma Minimax, dan analisis performa.

## Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python 3
- **GUI Library**: CustomTkinter
- **Lainnya**: Hanya menggunakan library standar Python.

## Struktur Folder

```
Connect4Minimax/
├── src/
│   ├── main.py          # Entry point aplikasi
│   ├── ui.py            # Modul untuk semua komponen GUI
│   ├── game_logic.py    # Modul untuk state dan aturan permainan Connect-Four
│   ├── minimax.py       # Modul implementasi algoritma Minimax dan fungsi evaluasi
│   └── analyzer.py      # Modul untuk melacak dan menghitung metrik performa
│
├── tests/
│   └── test_cases.py    # Unit test untuk logika permainan
│
├── docs/
│   └── analysis_results.txt # Catatan hasil analisis
│
├── README.md            # Dokumentasi ini
└── requirements.txt     # Dependensi proyek
```

## Instalasi

1.  **Clone atau download repositori ini.**

2.  **Buat dan aktifkan virtual environment (opsional namun direkomendasikan).**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Di Windows, gunakan `venv\Scripts\activate`
    ```

3.  **Install dependensi yang dibutuhkan.**
    ```bash
    pip install -r requirements.txt
    ```

## Cara Menjalankan Aplikasi

Pastikan Anda berada di direktori root `Connect4Minimax`. Jalankan aplikasi melalui file `main.py`.

```bash
python src/main.py
```

## Analisis Performa & Laporan

Proyek ini dilengkapi dengan skrip untuk melakukan analisis performa secara otomatis dan menghasilkan grafik untuk laporan.

1.  **Jalankan Skrip Analisis**
    Untuk memulai analisis, jalankan file `report_generator.py` dari direktori root.
    ```bash
    python report_generator.py
    ```
    Skrip akan menguji AI pada berbagai tingkat kedalaman dan ini mungkin memakan waktu beberapa saat.

2.  **Lihat Hasil Grafik**
    Setelah selesai, grafik perbandingan performa akan disimpan di `docs/performance_analysis_graph.png`. Grafik ini sangat berguna untuk disertakan dalam makalah Anda sebagai bukti empiris dari kompleksitas algoritma.
