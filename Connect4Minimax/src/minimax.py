# src/minimax.py

"""
Modul ini berisi implementasi dari algoritma Minimax dan fungsi-fungsi
terkait yang digunakan oleh AI untuk menentukan langkah terbaik.

Struktur Algoritma:
1.  get_best_move: Fungsi utama yang dipanggil untuk memulai proses pencarian.
    Fungsi ini akan menguji setiap kolom yang valid, menjalankan minimax
    untuk setiap pilihan, dan memilih kolom yang menghasilkan skor terbaik.
    Di sini juga kita mengukur performa (waktu, jumlah node).

2.  minimax: Fungsi rekursif inti. Berdasarkan apakah giliran 'maximizer' (AI)
    atau 'minimizer' (Player), fungsi ini akan memilih langkah yang memaksimalkan
    atau meminimalkan skor evaluasi.

3.  score_position: Fungsi evaluasi heuristik. Fungsi ini memberikan skor
    numerik pada keadaan papan saat ini. Skor ini mengestimasi seberapa
    menguntungkan posisi tersebut untuk AI.

4.  evaluate_window: Fungsi pembantu untuk 'score_position'. Ia akan menganalisis
    sebuah segmen dari 4 slot (horizontal, vertikal, atau diagonal) dan
    memberikan skor berdasarkan jumlah bidak AI, Player, dan slot kosong di dalamnya.
"""

import numpy as np
import random
import time
from math import inf
import psutil
import os

# Impor dari modul lain dalam proyek
from .game_logic import Connect4Game, PLAYER_PIECE, AI_PIECE, ROW_COUNT, COLUMN_COUNT

# --- Bobot untuk Fungsi Evaluasi Heuristik ---
# Bobot ini sangat krusial dan bisa di-tweak untuk mengubah "kepribadian" AI.
# Skor diberikan jika AI memiliki N bidak dalam satu baris (sisanya kosong).
SCORE_MAP = {
    '4_ai': 1000000, # Kemenangan pasti, skor sangat tinggi
    '3_ai': 50,
    '2_ai': 5,
    '3_player': -80, # Lawan akan menang, harus segera diblok. Skor negatif tinggi.
    '2_player': -10
}

# Kedalaman pencarian default untuk Minimax.
# Angka yang lebih tinggi membuat AI lebih "pintar" tapi jauh lebih lambat.
# Depth 4 atau 5 adalah titik awal yang baik.
DEFAULT_DEPTH = 4

# Variabel global sementara untuk menghitung node selama satu pemanggilan
nodes_evaluated_counter = 0

def evaluate_window(window, piece):
    """
    Fungsi pembantu yang mengevaluasi sebuah 'window' (list 4 elemen)
    dan memberikan skor berdasarkan isinya.
    """
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # Hitung jumlah bidak masing-masing pemain di dalam window
    ai_count = window.count(piece)
    player_count = window.count(opponent_piece)
    empty_count = window.count(0)

    # Prioritas 1: AI menang
    if ai_count == 4:
        score += SCORE_MAP['4_ai']
    # Prioritas 2: AI hampir menang (3 bidak)
    elif ai_count == 3 and empty_count == 1:
        score += SCORE_MAP['3_ai']
    # Prioritas 3: AI punya potensi (2 bidak)
    elif ai_count == 2 and empty_count == 2:
        score += SCORE_MAP['2_ai']
    
    # Prioritas 4: Blokir lawan yang akan menang
    if player_count == 3 and empty_count == 1:
        score += SCORE_MAP['3_player']
    # Prioritas 5: Blokir potensi lawan
    elif player_count == 2 and empty_count == 2:
        score += SCORE_MAP['2_player']

    return score

def score_position(board, piece):
    """
    Fungsi evaluasi heuristik utama.
    Memberikan skor keseluruhan untuk posisi papan saat ini.
    Skor positif menguntungkan AI, skor negatif menguntungkan Player.
    """
    score = 0
    
    # Skor Berdasarkan Posisi Tengah
    # Bidak di kolom tengah lebih berharga karena membuka lebih banyak peluang.
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Skor Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Skor Vertikal
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Skor Diagonal (positif /)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Skor Diagonal (negatif \)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
            
    return score

def is_terminal_node(game):
    """
    Mengecek apakah state permainan saat ini adalah terminal (akhir).
    Kondisi terminal: ada pemenang, atau papan penuh (seri).
    """
    return game.winning_move(PLAYER_PIECE) is not None or \
           game.winning_move(AI_PIECE) is not None or \
           game.is_board_full()

def minimax_alpha_beta(game, depth, alpha, beta, maximizing_player):
    """
    Implementasi algoritma Minimax dengan optimisasi Alpha-Beta Pruning.
    """
    global nodes_evaluated_counter
    nodes_evaluated_counter += 1

    valid_locations = game.get_valid_locations()
    is_terminal = is_terminal_node(game)

    # Base case: kedalaman tercapai atau permainan berakhir
    if depth == 0 or is_terminal:
        if is_terminal:
            if game.winning_move(AI_PIECE) is not None:
                return (None, SCORE_MAP['4_ai']) # AI menang
            elif game.winning_move(PLAYER_PIECE) is not None:
                return (None, -SCORE_MAP['4_ai']) # Player menang
            else: # Game seri
                return (None, 0)
        else: # Kedalaman 0, gunakan heuristik
            return (None, score_position(game.board, AI_PIECE))

    # Langkah rekursif untuk Maximizing Player (AI)
    if maximizing_player:
        value = -inf
        best_col = random.choice(valid_locations) # Pilih langkah acak sebagai default
        for col in valid_locations:
            temp_game = Connect4Game()
            temp_game.board = np.copy(game.board)
            row = temp_game.get_next_open_row(col)
            temp_game.drop_piece(row, col, AI_PIECE)
            
            new_score = minimax_alpha_beta(temp_game, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break # Pruning
        return best_col, value

    # Langkah rekursif untuk Minimizing Player (Player)
    else: # Minimizing player
        value = inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_game = Connect4Game()
            temp_game.board = np.copy(game.board)
            row = temp_game.get_next_open_row(col)
            temp_game.drop_piece(row, col, PLAYER_PIECE)

            new_score = minimax_alpha_beta(temp_game, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break # Pruning
        return best_col, value


def get_best_move(game, analyzer, depth=DEFAULT_DEPTH):
    """
    Fungsi utama untuk mendapatkan langkah terbaik dari AI.
    Ini adalah jembatan antara UI dan algoritma Minimax dengan Alpha-Beta Pruning.
    """
    global nodes_evaluated_counter
    nodes_evaluated_counter = 0 # Reset counter setiap kali AI berpikir
    
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    
    start_time = time.time()
    
    # Panggil minimax dengan alpha-beta pruning
    col, minimax_score = minimax_alpha_beta(game, depth, -inf, inf, True)
    
    end_time = time.time()
    
    mem_after = process.memory_info().rss
    peak_memory_mb = (mem_after - mem_before) / (1024 * 1024)

    execution_time_ms = (end_time - start_time) * 1000
    
    # Simpan metrik performa menggunakan analyzer
    analyzer.set_metrics(execution_time_ms, nodes_evaluated_counter, depth, peak_memory_mb)
    
    print(f"[AI] Memilih kolom {col} dengan skor: {minimax_score}")
    print(f"[AI] Analisis selesai dalam {execution_time_ms:.2f} ms, {nodes_evaluated_counter} node dievaluasi, memori puncak: {peak_memory_mb:.2f} MB (Depth: {depth}).")
    
    return col
