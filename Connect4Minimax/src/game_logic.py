# src/game_logic.py

"""
Modul ini bertanggung jawab atas semua logika inti dari permainan Connect-Four.
Termasuk di dalamnya adalah representasi papan, mekanisme menjatuhkan bidak,
validasi langkah, dan deteksi kondisi akhir permainan (menang, seri).
Modul ini tidak memiliki dependensi pada GUI (Tkinter) dan sepenuhnya
bisa diuji secara terpisah.
"""

import numpy as np

# --- Konstanta Permainan ---
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2

class Connect4Game:
    """
    Kelas yang merepresentasikan dan mengelola state dari sebuah sesi
    permainan Connect-Four.
    """
    def __init__(self):
        """
        Inisialisasi papan permainan.
        Papan direpresentasikan sebagai array NumPy 6x7.
        Nilai 0 merepresentasikan slot kosong.
        Nilai 1 merepresentasikan bidak Player.
        Nilai 2 merepresentasikan bidak AI.
        """
        self.board = self.create_board()
        self.game_over = False
        self.winner = None

    def create_board(self):
        """
        Membuat dan mengembalikan papan permainan kosong (diisi dengan nol).
        """
        return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

    def drop_piece(self, row, col, piece):
        """
        Menempatkan bidak (piece) pada posisi (row, col) yang diberikan.
        """
        self.board[row][col] = piece

    def is_valid_location(self, col):
        """
        Mengecek apakah sebuah kolom masih valid untuk ditempati.
        Sebuah kolom valid jika baris teratasnya (baris 5) masih kosong (bernilai 0).
        """
        return self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        """
        Mencari dan mengembalikan indeks baris kosong berikutnya pada kolom yang diberikan.
        """
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r
        return None # Seharusnya tidak pernah terjadi jika is_valid_location dipanggil dulu

    def winning_move(self, piece):
        """
        Mengecek apakah pemain dengan bidak 'piece' telah memenangkan permainan.
        Kemenangan terjadi jika ada 4 bidak yang sama berurutan.

        Args:
            piece (int): Bidak pemain (1 untuk Player, 2 untuk AI).

        Returns:
            tuple of tuples or None: Koordinat dari 4 bidak yang menang, atau None jika tidak ada kemenangan.
        """
        # Cek kemenangan horizontal
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return ((r, c), (r, c+1), (r, c+2), (r, c+3))

        # Cek kemenangan vertikal
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return ((r, c), (r+1, c), (r+2, c), (r+3, c))

        # Cek kemenangan diagonal (positif /)
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return ((r, c), (r+1, c+1), (r+2, c+2), (r+3, c+3))

        # Cek kemenangan diagonal (negatif \)
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return ((r, c), (r-1, c+1), (r-2, c+2), (r-3, c+3))
        
        return None

    def is_board_full(self):
        """
        Mengecek apakah papan sudah terisi penuh.
        Ini mengindikasikan kondisi permainan seri jika tidak ada pemenang.
        """
        # Cek apakah ada nilai 0 (slot kosong) di seluruh papan
        return not np.any(self.board == 0)

    def get_valid_locations(self):
        """
        Mengembalikan daftar semua kolom yang masih bisa diisi.
        Ini digunakan oleh algoritma Minimax untuk mengetahui langkah apa saja yang mungkin.
        """
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def reset_game(self):
        """
        Mereset state permainan kembali ke kondisi awal.
        """
        self.board = self.create_board()
        self.game_over = False
        self.winner = None

if __name__ == '__main__':
    # Contoh penggunaan dan pengujian sederhana modul game_logic
    game = Connect4Game()
    print("Papan Awal:")
    print(np.flip(game.board, 0)) # Dibalik agar visualnya benar (0 di bawah)

    # Player menjatuhkan bidak di kolom 3
    if game.is_valid_location(3):
        row = game.get_next_open_row(3)
        game.drop_piece(row, 3, PLAYER_PIECE)
    
    # AI menjatuhkan bidak di kolom 4
    if game.is_valid_location(4):
        row = game.get_next_open_row(4)
        game.drop_piece(row, 4, AI_PIECE)

    print("\nPapan Setelah Beberapa Langkah:")
    print(np.flip(game.board, 0))

    print(f"\nKolom yang valid: {game.get_valid_locations()}")
