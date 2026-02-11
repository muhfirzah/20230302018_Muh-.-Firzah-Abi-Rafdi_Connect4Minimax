# src/main.py

"""
Entry Point Utama Aplikasi Connect-Four Minimax.

File ini bertanggung jawab untuk:
1. Mengimpor kelas-kelas yang diperlukan dari modul lain (App, Connect4Game, PerformanceAnalyzer).
2. Membuat instance dari setiap kelas.
3. Menjalankan aplikasi dengan memanggil method mainloop() dari instance App.
"""

# Pastikan kita bisa mengimpor dari direktori       
# Ini mungkin diperlukan tergantung pada cara Anda menjalankan skrip
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game_logic import Connect4Game
from src.ui import App
from src.analyzer import PerformanceAnalyzer

def main():
    """
    Fungsi utama untuk menginisialisasi dan menjalankan aplikasi.
    """
    # 1. Buat instance dari logika permainan
    game = Connect4Game()

    # 2. Buat instance dari penganalisis performa
    analyzer = PerformanceAnalyzer()

    # 3. Buat instance dari aplikasi GUI, berikan game dan analyzer
    app = App(game=game, analyzer=analyzer)

    # 4. Jalankan event loop utama Tkinter
    app.mainloop()

if __name__ == "__main__":
    # Blok ini memastikan bahwa fungsi main() hanya akan dipanggil
    # ketika file ini dieksekusi secara langsung oleh interpreter Python.
    print("Menjalankan aplikasi Connect-Four Minimax...")
    main()

