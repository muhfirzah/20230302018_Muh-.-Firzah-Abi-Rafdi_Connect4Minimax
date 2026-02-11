"""
Unit tests untuk modul minimax.py.

Tujuan dari file ini adalah untuk memverifikasi "kecerdasan" dari AI, yaitu
kemampuannya untuk membuat keputusan strategis yang benar dalam situasi kritis.
Pengujian ini berfokus pada dua skenario paling penting:

1.  Apakah AI dapat melihat dan mengambil langkah kemenangan? (Best Case)
2.  Apakah AI dapat melihat dan memblokir langkah kemenangan lawan? (Worst Case)

Pengujian ini melengkapi `test_cases.py` yang hanya menguji aturan dasar
permainan. Dengan adanya tes ini, kita dapat lebih yakin bahwa implementasi
algoritma Minimax berfungsi sesuai harapan.
"""
import unittest
import numpy as np
import sys
import os

# Menambahkan direktori root proyek ke path agar bisa mengimpor 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game_logic import Connect4Game, PLAYER_PIECE, AI_PIECE
from src.minimax import get_best_move
from src.analyzer import PerformanceAnalyzer

class TestAILogic(unittest.TestCase):
    """
    Kumpulan tes untuk verifikasi logika strategis algoritma Minimax.
    """

    def setUp(self):
        """
        Menyiapkan instance game dan analyzer yang bersih untuk setiap tes.
        """
        self.game = Connect4Game()
        self.analyzer = PerformanceAnalyzer()

    def test_ai_must_take_winning_move(self):
        """
        Tes 1: Memastikan AI memilih langkah yang langsung memberikannya kemenangan.
        Skenario: AI memiliki 3 bidak berjejer horizontal dengan satu slot kosong.
        AI harus menempatkan bidaknya di slot kosong tersebut.
        """
        print("\nMenjalankan Tes AI: Ambil Kemenangan...")
        # Pengaturan papan: AI (piece 2) akan menang di kolom 3
        #  . . . . . . .
        #  . . . . . . .
        #  . . . . . . .
        #  . . . . . . .
        #  . 1 . 1 1 . .  (Player = 1)
        #  . 2 2 2 . . .  (AI = 2) -> AI harus memilih kolom 3
        self.game.board[0][1] = AI_PIECE
        self.game.board[0][2] = AI_PIECE
        self.game.board[0][4] = AI_PIECE # Tiga bidak AI
        self.game.board[0][0] = PLAYER_PIECE # Bidak pengacau
        
        # Panggil AI dengan depth yang cukup untuk melihat kemenangan instan
        best_move_col = get_best_move(self.game, self.analyzer, depth=2)
        
        self.assertEqual(best_move_col, 3, "AI gagal memilih langkah kemenangan yang jelas.")

    def test_ai_must_block_opponent_win(self):
        """
        Tes 2: Memastikan AI memblokir langkah kemenangan lawan.
        Skenario: Player memiliki 3 bidak berjejer vertikal.
        AI harus menempatkan bidaknya di atas 3 bidak tersebut untuk blok.
        """
        print("\nMenjalankan Tes AI: Blokir Lawan...")
        # Pengaturan papan: Player (piece 1) akan menang di kolom 2
        #  . . . . . . .
        #  . . . . . . .
        #  . . . . . . . -> AI harus menempatkan bidak di sini (baris 3, kolom 2)
        #  . . 1 . . . .
        #  . . 1 . . . .
        #  . . 1 . 2 . .
        self.game.board[0][2] = PLAYER_PIECE
        self.game.board[1][2] = PLAYER_PIECE
        self.game.board[2][2] = PLAYER_PIECE
        self.game.board[0][5] = AI_PIECE # Bidak pengacau

        # Panggil AI. Depth 3 atau 4 diperlukan untuk melihat ancaman dan blok.
        best_move_col = get_best_move(self.game, self.analyzer, depth=4)
        
        self.assertEqual(best_move_col, 2, "AI gagal memblokir langkah kemenangan lawan.")


if __name__ == '__main__':
    print("Menjalankan unit tests untuk Logika AI...")
    unittest.main()
