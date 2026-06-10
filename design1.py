import customtkinter as ctk
from PIL import Image
import os
import threading
import time

from design2 import HealtripApp

IMAGE_PATH = "dashboard.png"

WINDOW_WIDTH  = 868
WINDOW_HEIGHT = 570

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class HealtripImageApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Surabaya HealTrip")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color="#cce8f4")

        self._progress = 0
        self._loading_done = False

        self._build_ui()

        # Mulai animasi loading setelah UI siap
        self.after(300, self._start_loading)

    def _build_ui(self):
        # ── Layer 1: Gambar background ──
        if os.path.isfile(IMAGE_PATH):
            pil_img = Image.open(IMAGE_PATH).resize(
                (WINDOW_WIDTH, WINDOW_HEIGHT), Image.LANCZOS
            )
            self._bg = ctk.CTkImage(
                light_image=pil_img,
                dark_image=pil_img,
                size=(WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            bg_label = ctk.CTkLabel(self, image=self._bg, text="")
            bg_label.place(x=0, y=0)
        else:
            ctk.CTkLabel(self, text=f"File tidak ditemukan:\n{IMAGE_PATH}",
                         text_color="red").place(relx=0.5, rely=0.5, anchor="center")
            return

        # ── Layer 2: Progress bar (overlay di atas gambar) ──
        # Label teks loading
        self.loading_label = ctk.CTkLabel(
            self,
            text="Memuat data graph destinasi wisata...",
            font=("Arial", 12),
            text_color="#6a8aaa",
            fg_color="transparent"
        )
        self.loading_label.place(relx=0.5, y=415, anchor="n")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=420,
            height=13,
            corner_radius=10,
            fg_color="#c0d8ea",
            progress_color="#2a7abf"
        )
        self.progress_bar.set(0)
        self.progress_bar.place(relx=0.5, y=450, anchor="n")

        # Label persentase
        self.pct_label = ctk.CTkLabel(
            self,
            text="0%",
            font=("Arial", 14, "bold"),
            text_color="#2a9d5c",
            fg_color="transparent"
        )
        self.pct_label.place(relx=0.5, y=470, anchor="n")

    def _start_loading(self):
        """Jalankan animasi loading di thread terpisah."""
        threading.Thread(target=self._run_loading, daemon=True).start()

    def _run_loading(self):
        """Animasi progress bar dari 0% ke 100%."""
        steps = 100
        for i in range(1, steps + 1):
            time.sleep(0.07)  # Kecepatan loading (lebih kecil = lebih cepat)
            self._progress = i / steps
            # Update UI dari thread utama
            self.after(0, self._update_progress, i)

        # Setelah 100%, tunggu sebentar lalu lanjut ke halaman utama
        time.sleep(0.8)
        self.after(0, self._on_loading_done)

    def _on_loading_done(self):
        """Aksi setelah loading selesai — ganti ke tampilan siap."""
        # Sembunyikan progress section
        self.loading_label.place_forget()
        # Setelah 1 detik, tampilkan tombol mulai
        self.after(1000, self._show_start_button)

    def _update_progress(self, pct_int):
        self.progress_bar.set(pct_int / 100)
        self.pct_label.configure(text=f"{pct_int}%")
    
    def _show_start_button(self):
        """Tampilkan tombol Mulai Jelajahi setelah loading selesai."""
        # Sembunyikan elemen loading
        self.loading_label.place_forget()
        self.progress_bar.place_forget()
        self.pct_label.place_forget()

        # Tampilkan tombol
        self.start_btn = ctk.CTkButton(
            self,
            text="🗺️  Mulai Jelajahi Surabaya",
            font=("Arial", 14, "bold"),
            fg_color="#2a7abf",
            hover_color="#1a5a9a",
            text_color="white",
            corner_radius=25,
            width=280,
            height=46,
            command=self._on_start
        )
        self.start_btn.place(relx=0.5, y=440, anchor="n")

    def _on_start(self):
        """Aksi saat tombol ditekan."""
        # Ganti teks tombol jadi loading
        self.start_btn.configure(
            text="🔍  Mencari rute terbaik...",
            state="disabled",
            fg_color="#888"
        )
        # Simulasi proses — bisa diganti dengan logika DFS kamu
        self.after(1500, self._open_main_window)

    def _open_main_window(self):
        # Tutup splash screen
        self.destroy()
        # Buka aplikasi utama DFS
        app = HealtripApp()
        app.mainloop()
        # TODO: Ganti dengan pemanggilan window utama DFS kamu
        # Contoh: MainWindow(self)

if __name__ == "__main__":
    app = HealtripImageApp()
    app.mainloop()