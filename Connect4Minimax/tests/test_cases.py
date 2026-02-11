# tests/test_cases.py

"""
Unit tests untuk modul game_logic.py.

Tujuan dari file ini adalah untuk memverifikasi kebenaran dari logika inti
permainan (state management, aturan, deteksi kemenangan) secara terisolasi,
tanpa bergantung pada GUI atau algoritma AI.

Ini adalah praktik pengembangan perangkat lunak yang baik (Test-Driven Development
atau TDD) dan menunjukkan bahwa aplikasi dibangun di atas fondasi yang kokoh.
"""

import unittest
import numpy as np
import sys
import os

# Menambahkan direktori root proyek ke path agar bisa mengimpor 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game_logic import Connect4Game, PLAYER_PIECE, AI_PIECE, ROW_COUNT, COLUMN_COUNT

class TestGameLogic(unittest.TestCase):
    """
    Kumpulan tes untuk kelas Connect4Game.
    """

    def setUp(self):
        """
        Metode ini dipanggil sebelum setiap metode tes dijalankan.
        Digunakan untuk menyiapkan objek atau state yang bersih untuk setiap tes.
        """
        self.game = Connect4Game()

    def test_initial_board_is_empty(self):
        """Tes 1: Memastikan papan permainan awalnya kosong (berisi nol)."""
        expected_board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
        self.assertTrue(np.array_equal(self.game.board, expected_board), "Papan awal seharusnya kosong.")

    def test_drop_piece(self):
        """Tes 2: Memastikan fungsi drop_piece() bekerja dengan benar."""
        self.game.drop_piece(row=0, col=3, piece=PLAYER_PIECE)
        self.assertEqual(self.game.board[0][3], PLAYER_PIECE, "Bidak tidak ditempatkan dengan benar.")
        self.assertEqual(self.game.board[0][0], 0, "Slot lain seharusnya tidak berubah.")

    def test_is_valid_location(self):
        """Tes 3: Memverifikasi validasi kolom."""
        self.assertTrue(self.game.is_valid_location(0), "Kolom kosong seharusnya valid.")
        # Isi penuh satu kolom
        for r in range(ROW_COUNT):
            self.game.drop_piece(r, 0, AI_PIECE)
        self.assertFalse(self.game.is_valid_location(0), "Kolom yang penuh seharusnya tidak valid.")

    def test_get_next_open_row(self):
        """Tes 4: Memverifikasi penemuan baris kosong yang benar."""
        self.assertEqual(self.game.get_next_open_row(2), 0, "Baris kosong pertama di kolom kosong seharusnya 0.")
        self.game.drop_piece(row=0, col=2, piece=PLAYER_PIECE)
        self.assertEqual(self.game.get_next_open_row(2), 1, "Baris kosong berikutnya setelah satu bidak seharusnya 1.")

    def test_winning_move_horizontal(self):
        """Tes 5: Deteksi kemenangan secara horizontal."""
        for c in range(4):
            self.game.board[0][c] = PLAYER_PIECE
        self.assertIsNotNone(self.game.winning_move(PLAYER_PIECE), "Gagal mendeteksi kemenangan horizontal.")
        self.assertIsNone(self.game.winning_move(AI_PIECE), "Seharusnya tidak ada kemenangan untuk AI.")

    def test_winning_move_vertical(self):
        """Tes 6: Deteksi kemenangan secara vertikal."""
        for r in range(4):
            self.game.board[r][0] = AI_PIECE
        self.assertIsNotNone(self.game.winning_move(AI_PIECE), "Gagal mendeteksi kemenangan vertikal.")
        self.assertIsNone(self.game.winning_move(PLAYER_PIECE), "Seharusnya tidak ada kemenangan untuk Player.")

    def test_winning_move_diagonal_positive(self):
        """Tes 7: Deteksi kemenangan secara diagonal positif (/)."""
        for i in range(4):
            self.game.board[i][i] = PLAYER_PIECE
        self.assertIsNotNone(self.game.winning_move(PLAYER_PIECE), "Gagal mendeteksi kemenangan diagonal positif.")

    def test_winning_move_diagonal_negative(self):
        """Tes 8: Deteksi kemenangan secara diagonal negatif (\)."""
        for i in range(4):
            self.game.board[3-i][i] = AI_PIECE
        self.assertIsNotNone(self.game.winning_move(AI_PIECE), "Gagal mendeteksi kemenangan diagonal negatif.")

    def test_board_full_is_draw(self):
        """Tes 9: Deteksi kondisi papan penuh (seri)."""
        # Membuat pola papan catur yang tidak memungkinkan kemenangan
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                piece = PLAYER_PIECE if (r + c) % 2 == 0 else AI_PIECE
                self.game.board[r][c] = piece
        
        self.assertTrue(self.game.is_board_full(), "Papan seharusnya terdeteksi penuh.")
        self.assertIsNone(self.game.winning_move(PLAYER_PIECE))
        self.assertIsNone(self.game.winning_move(AI_PIECE))

if __name__ == '__main__':
    # Menjalankan semua tes yang ada di dalam kelas ini
    print("Menjalankan unit tests untuk Game Logic...")
    unittest.main()
