"""
Skrip untuk Analisis Performa dan Pembuatan Laporan Grafik.

Skrip ini dijalankan secara terpisah dari aplikasi utama (GUI). Tujuannya adalah
untuk secara sistematis menguji performa algoritma Minimax pada berbagai
tingkat kedalaman pencarian (depth) dan memvisualisasikan hasilnya.

Proses yang dilakukan:
1. Menjalankan algoritma `get_best_move` untuk setiap depth yang ditentukan.
2. Mengumpulkan data metrik: waktu eksekusi dan jumlah node yang dievaluasi.
3. Menggunakan `matplotlib` untuk membuat dua plot:
   - Depth vs. Waktu Eksekusi (ms)
   - Depth vs. Jumlah Node
4. Menyimpan grafik yang dihasilkan sebagai file gambar di dalam folder `docs/`.

Grafik ini dapat langsung dimasukkan ke dalam makalah sebagai bukti empiris
dari kompleksitas waktu O(b^d) dari algoritma Minimax.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Menambahkan direktori root proyek ke path agar bisa mengimpor 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.game_logic import Connect4Game, PLAYER_PIECE
from src.minimax import get_best_move
from src.analyzer import PerformanceAnalyzer

def run_performance_analysis(depths_to_test):
    """
    Menjalankan Minimax untuk setiap depth dan mengumpulkan data performa.
    """
    print(f"Memulai analisis performa untuk depths: {depths_to_test}...")
    
    execution_times = []
    evaluated_nodes = []
    analyzer = PerformanceAnalyzer()

    for depth in depths_to_test:
        print(f"  Menguji depth = {depth}...")
        
        # Buat state papan permainan awal yang konsisten untuk setiap pengujian
        # (misalnya, papan dengan beberapa bidak di tengah)
        game = Connect4Game()
        game.board[0][3] = PLAYER_PIECE
        game.board[0][2] = PLAYER_PIECE
        game.board[1][3] = PLAYER_PIECE
        
        # Panggil fungsi utama AI untuk mendapatkan langkah terbaik
        get_best_move(game, analyzer, depth=depth)
        
        # Simpan hasil analisis
        execution_times.append(analyzer.execution_time_ms)
        evaluated_nodes.append(analyzer.nodes_evaluated)

    print("Analisis selesai.")
    return execution_times, evaluated_nodes

def create_performance_graphs(depths, times, nodes):
    """
    Membuat dan menyimpan grafik perbandingan performa.
    """
    print("Membuat grafik performa...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    fig.suptitle('Analisis Performa Algoritma Minimax', fontsize=16)

    # Plot 1: Waktu Eksekusi vs. Depth
    ax1.plot(depths, times, 'o-', color='b', label='Waktu Eksekusi')
    ax1.set_title('Waktu Eksekusi vs. Kedalaman Pencarian')
    ax1.set_xlabel('Depth')
    ax1.set_ylabel('Waktu Eksekusi (ms)')
    ax1.set_xticks(depths)
    ax1.grid(True)
    ax1.legend()

    # Plot 2: Node Dievaluasi vs. Depth
    ax2.plot(depths, nodes, 's-', color='r', label='Node Dievaluasi')
    ax2.set_title('Jumlah Node Dievaluasi vs. Kedalaman Pencarian')
    ax2.set_xlabel('Depth')
    ax2.set_ylabel('Jumlah Node')
    ax2.set_xticks(depths)
    ax2.grid(True)
    ax2.legend()
    # Menggunakan skala logaritmik untuk visualisasi pertumbuhan eksponensial
    ax2.set_yscale('log')

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    # Simpan grafik ke file
    output_path = os.path.join(os.path.dirname(__file__), 'docs', 'performance_analysis_graph.png')
    plt.savefig(output_path)
    
    print(f"Grafik telah disimpan di: {output_path}")
    
    # Tampilkan grafik
    plt.show()


if __name__ == '__main__':
    # Tentukan kedalaman yang ingin diuji.
    # Hati-hati, depth 5 atau lebih bisa memakan waktu sangat lama.
    test_depths = [1, 2, 3, 4] 
    
    times, nodes = run_performance_analysis(test_depths)
    create_performance_graphs(test_depths, times, nodes)
