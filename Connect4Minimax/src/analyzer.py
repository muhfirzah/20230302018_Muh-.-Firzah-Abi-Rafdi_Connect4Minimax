# src/analyzer.py

"""
Modul ini berisi kelas `PerformanceAnalyzer` yang berfungsi sebagai
wadah untuk menyimpan dan mengelola data analisis performa dari
algoritma Minimax.

Penggunaan kelas ini bertujuan untuk:
1. Enkapsulasi: Mengumpulkan semua metrik terkait performa di satu tempat.
2. Portabilitas: Memudahkan jika ingin mengubah cara data analisis
   disimpan atau ditampilkan tanpa mengubah logika inti algoritma.
3. Kerapian Kode: Mencegah variabel-variabel global atau passing parameter
   yang berlebihan antar fungsi.
"""

class PerformanceAnalyzer:
    """
    Kelas untuk menyimpan metrik performa eksekusi algoritma Minimax.
    """
    def __init__(self):
        """
        Inisialisasi semua metrik ke nilai default.
        """
        self.execution_time_ms = 0.0
        self.nodes_evaluated = 0
        self.search_depth = 0
        self.memory_usage_mb = 0.0

    def reset(self):
        """
        Mereset semua metrik ke nilai awal. Dipanggil setiap kali
        permainan baru dimulai atau di-restart.
        """
        self.execution_time_ms = 0.0
        self.nodes_evaluated = 0
        self.memory_usage_mb = 0.0
        # Search depth tidak direset karena merupakan konstanta,
        # tapi bisa diatur ulang jika diperlukan.

    def set_metrics(self, time_ms, nodes, depth, memory_mb):
        """
        Menyimpan nilai metrik yang baru dihitung.

        Args:
            time_ms (float): Waktu eksekusi dalam milidetik.
            nodes (int): Jumlah node yang dievaluasi.
            depth (int): Kedalaman pencarian yang digunakan.
            memory_mb (float): Penggunaan memori puncak dalam megabyte.
        """
        self.execution_time_ms = time_ms
        self.nodes_evaluated = nodes
        self.search_depth = depth
        self.memory_usage_mb = memory_mb

    def get_stats_string(self):
        """
        Mengembalikan string yang sudah diformat untuk ditampilkan di GUI.
        """
        return (
            f"Waktu Eksekusi: {self.execution_time_ms:.2f} ms\n"
            f"Jumlah Node: {self.nodes_evaluated}\n"
            f"Depth Pencarian: {self.search_depth}\n"
            f"Memori Puncak: {self.memory_usage_mb:.2f} MB"
        )

if __name__ == '__main__':
    # Contoh penggunaan
    analyzer = PerformanceAnalyzer()
    
    # Simulasikan hasil dari eksekusi Minimax
    analyzer.set_metrics(time_ms=58.1234, nodes=12345, depth=4, memory_mb=2.5)
    
    print("--- Analisis Performa AI ---")
    print(analyzer.get_stats_string())
    print("\nKompleksitas Teoritis: O(b^d)")

    # Reset untuk game berikutnya
    analyzer.reset()
    print("\n--- Setelah Reset ---")
    print(analyzer.get_stats_string())
