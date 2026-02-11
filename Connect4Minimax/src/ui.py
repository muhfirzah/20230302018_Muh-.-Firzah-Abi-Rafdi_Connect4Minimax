# src/ui.py

"""
Modul ini bertanggung jawab untuk membangun dan mengelola Antarmuka
Pengguna Grafis (GUI) dari aplikasi menggunakan library CustomTkinter.
Versi final dengan tema Neon, pop-up kustom, dan highlight kemenangan.
"""

import tkinter
from tkinter import messagebox
import customtkinter as ctk
import math
import threading

# Impor dari modul lain dalam proyek
from .game_logic import Connect4Game, PLAYER_PIECE, AI_PIECE, ROW_COUNT, COLUMN_COUNT
from .minimax import get_best_move, DEFAULT_DEPTH # DEFAULT_DEPTH masih digunakan untuk inisialisasi slider
from .analyzer import PerformanceAnalyzer

# --- Konstanta Tampilan ---
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE

# --- Skema Warna "Neon" (Red & Blue) ---
COLOR_BACKGROUND = "#B3B2B5"      # Hitam pekat
COLOR_BOARD = "#1A2238"           # Biru gelap
COLOR_PLAYER1 = "#FF0000"         # Merah Neon
COLOR_PLAYER2 = "#0000FF"         # Biru Neon
COLOR_EMPTY = "#282C34"           # Abu-abu gelap
COLOR_TEXT = "#EAEAEA"
COLOR_HIGHLIGHT = "#FFFF00"      # Kuning Neon untuk sorotan garis
COLOR_POPUP_BG = "#1F232A"

class App(ctk.CTk):
    def __init__(self, game, analyzer):
        super().__init__()

        self.game = game
        self.analyzer = analyzer
        self.turn = PLAYER_PIECE
        self.is_ai_thinking = False

        self.title("Connect-Four AI | Neon Edition (Red & Blue)")
        self.geometry(f"{WIDTH + 350}x{HEIGHT + 50}")
        ctk.set_appearance_mode("Dark")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=320)
        self.grid_rowconfigure(0, weight=1)

        self.board_frame = ctk.CTkFrame(self, fg_color=COLOR_BACKGROUND)
        self.board_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.canvas = ctk.CTkCanvas(self.board_frame, width=WIDTH, height=HEIGHT, bg=COLOR_BACKGROUND, highlightthickness=0)
        self.canvas.pack(expand=True)
        self.canvas.bind("<Motion>", self.handle_mouse_move)
        self.canvas.bind("<Button-1>", self.handle_mouse_click)

        self.control_panel = ctk.CTkFrame(self, width=300, fg_color=COLOR_BACKGROUND)
        self.control_panel.grid(row=0, column=1, sticky="ns", padx=(0, 20), pady=20)
        
        self.create_control_widgets()
        
        self.draw_board()
        self.update_status_label()

    def create_control_widgets(self):
        title_frame = ctk.CTkFrame(self.control_panel, fg_color=COLOR_BACKGROUND)
        title_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(title_frame, text="ANALISIS ALGORITMA", text_color=COLOR_TEXT, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        status_frame = ctk.CTkFrame(self.control_panel)
        status_frame.pack(pady=10, padx=10, fill="x")
        self.status_label = ctk.CTkLabel(status_frame, text="", font=ctk.CTkFont(size=16))
        self.status_label.pack(pady=10)

        analysis_frame = ctk.CTkFrame(self.control_panel)
        analysis_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(analysis_frame, text="Statistik Langkah AI Terakhir:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.analysis_label = ctk.CTkLabel(analysis_frame, text="Waktu Eksekusi: -\nJumlah Node: -\nDepth Pencarian: -\nMemori Puncak: -",
                                           font=ctk.CTkFont(size=12), justify="left")
        self.analysis_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # --- Slider untuk mengatur kedalaman AI ---
        difficulty_frame = ctk.CTkFrame(self.control_panel)
        difficulty_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(difficulty_frame, text="Tingkat Kesulitan AI (Depth):", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.depth_slider = ctk.CTkSlider(difficulty_frame, from_=2, to=6, number_of_steps=4,
                                          command=self.update_depth_label)
        self.depth_slider.set(DEFAULT_DEPTH) # Set nilai awal slider
        self.depth_slider.pack(fill="x", padx=10)
        
        self.depth_label = ctk.CTkLabel(difficulty_frame, text=f"Depth: {int(self.depth_slider.get())}", font=ctk.CTkFont(size=12, slant="italic"))
        self.depth_label.pack(anchor="w", padx=10, pady=(0, 10))

        complexity_frame = ctk.CTkFrame(self.control_panel)
        complexity_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(complexity_frame, text="Kompleksitas Waktu Teoritis", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        ctk.CTkLabel(complexity_frame, text="O(b^d)", font=ctk.CTkFont(size=20, family="monospace")).pack()
        ctk.CTkLabel(complexity_frame, text="b = cabang, d = kedalaman", font=ctk.CTkFont(size=10)).pack(pady=(0, 10))

        self.restart_button = ctk.CTkButton(self.control_panel, text="Restart Game", font=ctk.CTkFont(size=14), command=self.restart_game,
                                            fg_color=COLOR_PLAYER1, hover_color=COLOR_PLAYER2, text_color="#000000")
        self.restart_button.pack(pady=20, padx=10, fill="x", side="bottom")

    def update_depth_label(self, value):
        """Memperbarui teks label depth sesuai dengan nilai slider."""
        self.depth_label.configure(text=f"Depth: {int(value)}")

    def draw_board(self, highlight_col=None):
        self.canvas.delete("all")
        if self.turn == PLAYER_PIECE and not self.game.game_over and highlight_col is not None:
             self.canvas.create_oval(highlight_col * SQUARESIZE + 5, SQUARESIZE - 2*RADIUS - 5,
                                    highlight_col * SQUARESIZE + SQUARESIZE - 5, SQUARESIZE - 5,
                                    fill=COLOR_PLAYER1, outline="")
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                x1 = c * SQUARESIZE
                y1 = (ROW_COUNT - r) * SQUARESIZE
                x2 = x1 + SQUARESIZE
                y2 = y1 + SQUARESIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_BOARD, outline="black")
                center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
                piece = self.game.board[r][c]
                color = COLOR_EMPTY
                if piece == PLAYER_PIECE: color = COLOR_PLAYER1
                elif piece == AI_PIECE: color = COLOR_PLAYER2
                self.canvas.create_oval(center_x - RADIUS, center_y - RADIUS, center_x + RADIUS, center_y + RADIUS, fill=color, outline="")

    def highlight_winning_pieces(self, winning_coords):
        """Menggambar garis sorotan di atas bidak-bidak yang menang."""
        if not winning_coords: return

        # Dapatkan koordinat tengah dari bidak pertama dan terakhir yang menang
        r1, c1 = winning_coords[0]
        r4, c4 = winning_coords[3] # Ambil bidak keempat untuk garis

        start_x = c1 * SQUARESIZE + SQUARESIZE / 2
        start_y = (ROW_COUNT - r1) * SQUARESIZE + SQUARESIZE / 2
        end_x = c4 * SQUARESIZE + SQUARESIZE / 2
        end_y = (ROW_COUNT - r4) * SQUARESIZE + SQUARESIZE / 2

        self.canvas.create_line(start_x, start_y, end_x, end_y,
                                fill=COLOR_HIGHLIGHT, width=8, tags="winning_line")


    def handle_mouse_move(self, event):
        if self.turn == PLAYER_PIECE and not self.game.game_over and not self.is_ai_thinking:
            col = math.floor(event.x / SQUARESIZE)
            if 0 <= col < COLUMN_COUNT:
                self.draw_board(highlight_col=col)

    def handle_mouse_click(self, event):
        if self.turn != PLAYER_PIECE or self.game.game_over or self.is_ai_thinking:
            return

        col = math.floor(event.x / SQUARESIZE)
        if self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col, PLAYER_PIECE)
            self.draw_board()
            
            winning_coords = self.game.winning_move(PLAYER_PIECE)
            if winning_coords:
                self.game.game_over = True
                self.game.winner = PLAYER_PIECE
                self.update_status_label()
                self.highlight_winning_pieces(winning_coords)
                self._show_endgame_dialog("Permainan Selesai", "Selamat, Anda Menang!")
                return
            
            if self.game.is_board_full():
                self.game.game_over = True
                self.update_status_label()
                self._show_endgame_dialog("Permainan Selesai", "Permainan Berakhir Seri!")
                return

            self.turn = AI_PIECE
            self.update_status_label()
            self.is_ai_thinking = True
            self.depth_slider.configure(state="disabled") # Nonaktifkan slider saat AI berpikir
            
            threading.Thread(target=self._run_ai_calculation, daemon=True).start()

    def _run_ai_calculation(self):
        current_depth = int(self.depth_slider.get()) # Dapatkan depth dari slider
        col = get_best_move(self.game, self.analyzer, depth=current_depth)
        self.after(0, self._ai_move_callback, col)

    def _ai_move_callback(self, col):
        if col is not None and self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col, AI_PIECE)
            self.draw_board()
            self.analysis_label.configure(text=self.analyzer.get_stats_string())

            winning_coords = self.game.winning_move(AI_PIECE)
            if winning_coords:
                self.game.game_over = True
                self.game.winner = AI_PIECE
                self.update_status_label()
                self.highlight_winning_pieces(winning_coords)
                self._show_endgame_dialog("Permainan Selesai", "AI Menang!")
                return

            if self.game.is_board_full():
                self.game.game_over = True
                self.update_status_label()
                self._show_endgame_dialog("Permainan Selesai", "Permainan Berakhir Seri!")
                return
        
        self.turn = PLAYER_PIECE
        self.update_status_label()
        self.is_ai_thinking = False
        self.depth_slider.configure(state="normal") # Aktifkan kembali slider
        
    def _show_endgame_dialog(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.configure(fg_color=COLOR_POPUP_BG)
        
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20, padx=10)
        
        ok_button = ctk.CTkButton(dialog, text="OK", command=dialog.destroy,
                                  fg_color=COLOR_PLAYER1, hover_color=COLOR_PLAYER2, text_color="#000000")
        ok_button.pack(pady=10)
        
        # Center the dialog
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"{x}+{y}")
        dialog.wait_window()

    def update_status_label(self):
        if self.game.game_over:
            if self.game.winner == PLAYER_PIECE: self.status_label.configure(text="Selamat, Anda Menang!", text_color=COLOR_PLAYER1)
            elif self.game.winner == AI_PIECE: self.status_label.configure(text="AI Menang!", text_color=COLOR_PLAYER2)
            else: self.status_label.configure(text="Permainan Seri!", text_color="gray")
        else:
            if self.turn == PLAYER_PIECE: self.status_label.configure(text="Giliran Anda (Merah)", text_color=COLOR_PLAYER1)
            else: self.status_label.configure(text="AI Sedang Berpikir...", text_color=COLOR_PLAYER2)

    def restart_game(self):
        self.game.reset_game()
        self.analyzer.reset()
        self.turn = PLAYER_PIECE
        self.is_ai_thinking = False
        
        self.analysis_label.configure(text="Waktu Eksekusi: -\nJumlah Node: -\nDepth Pencarian: -\nMemori Puncak: -")
        self.update_status_label()
        
        self.draw_board()
        self.depth_slider.configure(state="normal") # Pastikan slider aktif saat game restart

if __name__ == '__main__':
    game_instance = Connect4Game()
    analyzer_instance = PerformanceAnalyzer()
    app = App(game=game_instance, analyzer=analyzer_instance)
    app.mainloop()
