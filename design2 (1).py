import customtkinter as ctk  # Library GUI modern berbasis tkinter
from PIL import Image   # Untuk membaca & menampilkan gambar
import tkinter as tk  # Library GUI bawaan Python
import time  # Untuk delay animasi DFS
from tkinter import Toplevel  # Membuat window/pop-up baru

# CONFIG
WINDOW_WIDTH = 868
WINDOW_HEIGHT = 570

# Menyimpan lokasi file gambar, Dipakai untuk background / halaman tertentu
IMAGE_PATH = "design_referensi.png"
ANALISIS_IMAGE = "design_analisis.png"
TENTANG_IMAGE = "design_tentang.png"


# DATA LOKASI, Nantinya dipakai untuk dropdown / pilihan tujuan user
locations = [
    "B. Monumen Tugu Pahlawan",
    "C. Ekowisata Mangrove Wonorejo",
    "D. Surabaya North Quay",
    "E. Kebun Bibit Wonorejo",
    "F. Taman Bungkul",
    "G. Atlantis Land",
    "H. Pantai Ria Kenjeran",
    "I. Kebun Binatang Surabaya",
    "J. Jalan Tunjungan",
    "K. Alun-alun Surabaya",
    "L. Wisata Perahu Kalimas",
    "M. Monumen Kapal Selam"
]

# CUSTOMTKINTER
ctk.set_appearance_mode("light")  # Mode tampilan aplikasi → light mode
ctk.set_default_color_theme("blue")  # Tema warna utama aplikasi

# APP
class HealtripApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # WINDOW
        self.title("SURABAYA HEALTRIP DFS")  # Judul window aplikasi
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")  # Mengatur ukuran window
        self.resizable(False, False)  # Window tidak bisa diperbesar/dikecilkan

        # DFS STATE
        self.selected_destination = None  # Menyimpan tujuan wisata yang dipilih user
        self.current_animation_route = []  # Menyimpan rute DFS untuk animasi
        self.current_dijkstra_route = []  # Menyimpan hasil jalur terpendek (Dijkstra)
        self.destination_ready = False  # Mengecek apakah tujuan sudah dipilih
        self.show_all_nodes = False   # Mengatur apakah semua node ditampilkan

        # GRAPH DFS menggunakkan adjacency list
        self.graph = {

            "Stasiun Gubeng": [
                "Taman Bungkul",
                "Jalan Tunjungan",
                "Monumen Kapal Selam",
                "Kebun Binatang Surabaya",
                "Alun-alun Surabaya",
                "Wisata Perahu Kalimas"
            ],
            "Taman Bungkul": [
                "Jalan Tunjungan",
                "Stasiun Gubeng"
            ],

            "Jalan Tunjungan": [
                "Taman Bungkul",
                "Monumen Kapal Selam",
                "Stasiun Gubeng"
            ],

            "Monumen Kapal Selam": [
                "Jalan Tunjungan",
                "Stasiun Gubeng",
                "Monumen Tugu Pahlawan"
            ],

            "Monumen Tugu Pahlawan": [
                "Monumen Kapal Selam"
            ],

            "Kebun Binatang Surabaya": [
                "Stasiun Gubeng"
            ],

            "Wisata Perahu Kalimas": [
                "Stasiun Gubeng",
                "Atlantis Land",
                "Kebun Bibit Wonorejo"
            ],

            "Atlantis Land": [
                "Wisata Perahu Kalimas",
                "Surabaya North Quay",
                "Ekowisata Mangrove Wonorejo"
            ],

            "Ekowisata Mangrove Wonorejo": [
                "Atlantis Land"
            ],

            "Kebun Bibit Wonorejo": [
                "Wisata Perahu Kalimas"
            ],

            "Alun-alun Surabaya": [
                "Stasiun Gubeng",
                "Pantai Ria Kenjeran"
            ],

            "Pantai Ria Kenjeran": [
                "Alun-alun Surabaya",
                "Surabaya North Quay"
            ],

            "Surabaya North Quay": [
                "Pantai Ria Kenjeran",
                "Atlantis Land"
            ]
        }

        # EDGE DISTANCE
        self.edge_distance = {
        # Menyimpan bobot/jarak antar node. Dipakai untuk algoritma shortest path
            ("Kebun Binatang Surabaya", "Stasiun Gubeng"): 4.8, # Artinya: Jarak dari KBS ke Stasiun Gubeng = 4.8 km
            ("Stasiun Gubeng", "Alun-alun Surabaya"): 0.9,
            ("Alun-alun Surabaya", "Pantai Ria Kenjeran"): 7.7,
            ("Pantai Ria Kenjeran", "Surabaya North Quay"): 7.6,

            ("Surabaya North Quay", "Atlantis Land"): 12.8,
            ("Atlantis Land", "Ekowisata Mangrove Wonorejo"): 14.3,

            ("Atlantis Land", "Wisata Perahu Kalimas"): 8.5,
            ("Wisata Perahu Kalimas", "Kebun Bibit Wonorejo"): 10.8,

            ("Wisata Perahu Kalimas", "Stasiun Gubeng"): 1.6,

            ("Stasiun Gubeng", "Taman Bungkul"): 3.9,
            ("Stasiun Gubeng", "Jalan Tunjungan"): 3.2,
            ("Stasiun Gubeng", "Monumen Kapal Selam"): 0.28,

            ("Taman Bungkul", "Jalan Tunjungan"): 6.6,
            ("Jalan Tunjungan", "Monumen Kapal Selam"): 2.3,

            ("Monumen Kapal Selam", "Monumen Tugu Pahlawan"): 4.4,
        }
        # Bobot edge digunakan untuk: 1. Menghitung total jarak perjalanan, 2. Menentukan jalur tercepat, 3. Visualisasi analisis graph
        
        # BACKGROUND
        self.bg_image = ctk.CTkImage(  # Membuat objek gambar background utama
            light_image=Image.open(IMAGE_PATH),
            size=(WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        self.bg_label = ctk.CTkLabel(   # Label digunakan sebagai wadah gambar background
            self,
            image=self.bg_image,
            text=""
        )

        self.bg_label.place(x=0, y=0)   # Menempatkan background mulai dari pojok kiri atas
        # BACKGROUND ANALISIS
        self.analisis_image = ctk.CTkImage(    # Background khusus halaman analisis
            light_image=Image.open(ANALISIS_IMAGE),
            size=(WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        # FRAME ANALISIS
        self.analisis_frame = ctk.CTkFrame(   # Frame = wadah/container halaman analisis
            self,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            fg_color="white"
        )

        self.analisis_bg = ctk.CTkLabel( 
            self.analisis_frame,
            image=self.analisis_image,   # Menampilkan background analisis di dalam frame
            text=""
        )

        self.analisis_bg.place(x=0, y=0)

        # NAVBAR MENU
        self.menu_frame = ctk.CTkFrame(
            self,
            width=690,
            height=55,
            fg_color="#C6E2F4",
            corner_radius=0,     # ← hilangkan sudut melengkung
            border_width=0 
        )

        self.menu_frame.place(x=190, y=14)

        # DASHBOARD BUTTON
        self.dashboard_btn = ctk.CTkButton(   
            self.menu_frame,
            text="Dashboard",
            width=70,
            height=25,
            corner_radius=8,
            fg_color="#004B87",
            hover_color="#AFD3F0",
            text_color="white",
            font=("Plus Jakarta Sans", 15, "bold"),
            border_width=0,
            command=self.show_dashboard
        )
        # Tombol menuju halaman dashboard
        self.dashboard_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        # ANALISIS BUTTON
        # Tombol untuk membuka halaman analisis graph
        self.analisis_btn = ctk.CTkButton(
            self.menu_frame,
            text="Analisis",
            width=70,
            height=25,
            corner_radius=10,
            fg_color="#004B87",
            hover_color="#AFD3F0",
            text_color="#FFFFFF",
            font=("Plus Jakarta Sans", 15, "bold"),
            border_width=0,
            command=self.show_analysis_screen
        )

        self.analisis_btn.grid(
            row=0,
            column=1,
            padx=8
        )

        # TENTANG BUTTON
        self.tentang_btn = ctk.CTkButton(
            self.menu_frame,
            text="Tentang",
            width=70,
            height=25,
            corner_radius=10,
            fg_color="#004B87",
            hover_color="#AFD3F0",
            text_color="#FFFFFF",
            font=("Plus Jakarta Sans", 15, "bold"),
            border_width=0,
            command=self.show_tentang_screen
        )
        # Tombol menuju halaman informasi aplikasi
        self.tentang_btn.grid(
            row=0,
            column=2,
            padx=8
        )

        # BUTTON KELUAR (X)
        self.quit_button = ctk.CTkButton(
            self.menu_frame,
            text="✕",
            width=35,
            height=25,
            corner_radius=8,
            fg_color="#D9534F",
            hover_color="#C9302C",
            text_color="white",
            font=("Plus Jakarta Sans", 14, "bold"),
            border_width=0,
            command=self.quit_app
        )
        # Tombol keluar aplikasi
        self.quit_button.grid(
            row=0,
            column=3,
            padx=(330, 10)
        )

        self.tentang_image = ctk.CTkImage(   # Gambar background halaman tentang
            light_image=Image.open(TENTANG_IMAGE),
            size=(WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        # FRAME TENTANG
        self.tentang_frame = ctk.CTkFrame(
            self,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            fg_color="white"
        )

        self.tentang_bg = ctk.CTkLabel(   # Container halaman tentang
            self.tentang_frame,
            image=self.tentang_image,
            text=""
        )

        self.tentang_bg.place(x=0, y=0)   # Menampilkan background halaman tentang
        # GOAL DROPDOWN
        goal_options = [lokasi.split(". ", 1)[1] for lokasi in locations] # Mengambil nama lokasi tanpa huruf depan, Contoh: "B. Monumen Tugu Pahlawan" menjadi "Monumen Tugu Pahlawan"

        self.goal_var = ctk.StringVar(value="pilih lokasi tujuan") # Nilai default dropdown

        self.goal_menu = ctk.CTkComboBox(  # ComboBox digunakan untuk memilih destinasi wisata
            self,
            values=goal_options,
            variable=self.goal_var,
            width=170,
            height=35,
            font=("Plus Jakarta Sans", 11),
            fg_color="white",
            border_color="#b0cfe8",
            button_color="#2a7abf",
            dropdown_fg_color="white",
            command=self.change_destination
        )

        self.goal_menu.place(x=155, y=95)

        # BUTTON DFS
        self.search_button = ctk.CTkButton(  # Tombol menjalankan algoritma DFS, Untuk mencari rute perjalanan
            self,
            text="CARI RUTE DFS",
            width=120,
            height=42,
            corner_radius=10,
            fg_color="#004B87",
            hover_color="#003866",
            font=("Plus Jakarta Sans", 13, "bold"),
            command=self.search_route
        )

        self.search_button.place(x=339, y=94)

        # BUTTON RESET
        self.reset_button = ctk.CTkButton(   # Tombol untuk mengembalikan aplikasi, ke kondisi awal/default
            self,
            text="RESET",
            width=120,
            height=42,
            corner_radius=10,
            fg_color="#B9CCDB",
            text_color="#173B67",
            hover_color="#A6BECE",
            font=("Plus Jakarta Sans", 13, "bold"),
            command=self.reset_app
        )

        self.reset_button.place(x=470, y=94)

        # BUTTON NODES
        self.nodes_button = ctk.CTkButton(   # Tombol untuk menampilkan seluruh node, pada graph wisata Surabaya
            self,
            text="SEMUA NODES",
            width=120,
            height=42,
            corner_radius=10,
            fg_color="#7FB3E8",
            text_color="#173B67",
            hover_color="#6CA4DD",
            font=("Plus Jakarta Sans", 13, "bold"),
            command=self.show_nodes
        )

        self.nodes_button.place(x=600, y=94)

        # BUTTON BANDINGKAN
        self.compare_button = ctk.CTkButton(    # Tombol untuk membuka halaman analisis, atau membandingkan hasil pencarian rute
            self,
            text="BANDINGKAN",
            width=120,
            height=42,
            corner_radius=10,
            fg_color="#EDE4FF",
            text_color="#7A3FF2",
            hover_color="#DDD0FF",
            border_width=1,
            border_color="#BFA6FF",
            font=("Plus Jakarta Sans", 13, "bold"),
            command=self.show_analysis_screen
        )

        self.compare_button.place(x=731, y=94)
# SIDEBAR
        self.sidebar_frame = ctk.CTkFrame(
            self,
            width=150,
            height=540,
            fg_color="#CFE3F1"
        )
        self.sidebar_frame.place(x=1, y=204)

        # SCROLL CANVAS
        self.scroll_canvas = tk.Canvas(
            self.sidebar_frame,
            width=228,
            height=520,
            bg="#CFE3F1",
            highlightthickness=0
        )

        self.v_scroll = tk.Scrollbar(
            self.sidebar_frame,
            orient="vertical",
            command=self.scroll_canvas.yview
        )

        self.h_scroll = tk.Scrollbar(
            self.sidebar_frame,
            orient="horizontal",
            command=self.scroll_canvas.xview
        )

        self.scroll_canvas.configure(
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        # FRAME DI DALAM CANVAS
        self.scroll_frame = tk.Frame(
            self.scroll_canvas,
            bg="#CFE3F1"
        )

        self.canvas_window = self.canvas_window = self.scroll_canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        def update_scroll(event):
            self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")
            )

        self.scroll_frame.bind("<Configure>", update_scroll)
        # MOUSE WHEEL SCROLL
        self.scroll_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.scroll_canvas.yview_scroll(
                int(-1 * (e.delta / 120)),
                "units"
            )
        )

        # BUTTON LOKASI
        for lokasi in locations:

            clean_name = lokasi.split(". ", 1)[1]

            # FRAME PEMBATAS
            item_frame = tk.Frame(
                self.scroll_frame,
                bg="#EAF4FB",          # warna card
                bd=1,
                relief="solid",
                highlightbackground="#B7D3E8",
                highlightthickness=1
            )

            item_frame.pack(
                fill="x",
                padx=8,
                pady=4
            )

            # BUTTON DI DALAM FRAME
            btn = tk.Button(
                item_frame,
                text=lokasi,
                font=("Plus Jakarta Sans", 14, "bold"),
                fg="#173B67",
                bg="#EAF4FB",
                activebackground="#D6EAF8",
                activeforeground="#173B67",
                relief="flat",
                anchor="w",
                padx=12,
                pady=10,
                borderwidth=0,
                command=lambda tujuan=clean_name:
                self.change_destination(tujuan)
            )

            btn.pack(fill="x")

        # CANVAS GRAF
        self.graph_canvas = tk.Canvas(  
            self,
            width=620,
            height=390,
            bg="#EEF1FF",
            highlightthickness=0
        )
        # Canvas digunakan untuk menggambar: Node, Edge, Animal DFS
        self.graph_canvas.place(x=270, y=315)

        # DFS LOG
        self.log_frame = ctk.CTkFrame(   # Frame untuk menampilkan proses DFS
            self,
            width=145,
            height=400,
            fg_color="transparent"
        )

        self.log_frame.place(x=680, y=203)

        self.log_box = ctk.CTkTextbox(
            self.log_frame,
            width=186,
            height=170,
            font=("Plus Jakarta Sans", 8),
            text_color="#333333",
            fg_color="#F8F8FC",
            border_width=0,
            corner_radius=8
        )
        # Textbox digunakan untuk menampilkan: urutan node dikunjungi, proses traversal DFS
        self.log_box.pack()

        # HASIL PENCARIAN
        self.result_frame = ctk.CTkFrame(
            self,
            width=187,
            height=170,
            fg_color="#F7F3F7",
            corner_radius=0,
            border_width=0,
            border_color="#E7C9D5"
        )
        # Frame hasil pencarian DFS
        self.result_frame.place(x=680, y=400)

        self.result_status = ctk.CTkLabel(
            self.result_frame,
            text="✅ RUTE DFS DITEMUKAN!",
            font=("Plus Jakarta Sans", 12, "bold"),
            text_color="#1B7A2F"
        )
        # Menampilkan status keberhasilan pencarian
        self.result_status.place(x=15, y=10)

        self.result_route = ctk.CTkLabel(
            self.result_frame,
            text="-",
            font=("Plus Jakarta Sans", 11, "bold"),
            text_color="#73E91E",
            justify="left"
        )
        # Menampilkan rute DFS yang ditemukan
        self.result_route.place(x=15, y=40)

        # BOX TOTAL JARAK
        self.distance_box = ctk.CTkFrame(
            self.result_frame,
            width=82,
            height=55,
            fg_color="#F9F2F7"
        )
        # Box informasi total jarak perjalanan
        self.distance_box.place(x=5, y=65)

        self.distance_title = ctk.CTkLabel(
            self.distance_box,
            text="TOTAL JARAK",
            font=("Plus Jakarta Sans", 8, "bold"),
            text_color="#A66B8A"
        )

        self.distance_title.place(x=5, y=1)

        self.distance_value = ctk.CTkLabel(
            self.distance_box,
            text="0 KM",
            font=("Plus Jakarta Sans", 12, "bold"),
            text_color="#E91E63"
        )
        # Nilai total kilometer perjalanan
        self.distance_value.place(x=5, y=20)

        # BOX NODE
        self.node_box = ctk.CTkFrame(
            self.result_frame,
            width=82,
            height=55,
            fg_color="#F9F2F7"
        )

        self.node_box.place(x=95, y=61)

        self.node_title = ctk.CTkLabel(
            self.node_box,
            text="NODE DIKUNJUNGI ",
            font=("Plus Jakarta Sans", 8, "bold"),
            text_color="#A66B8A"
        )
        # Menampilkan jumlah node yang telah dikunjungi DFS
        self.node_title.place(x=5, y=5)

        self.node_value = ctk.CTkLabel(
            self.node_box,
            text="0 Node",
            font=("Plus Jakarta Sans", 12, "bold"),
            text_color="#11A84B"
        )

        self.node_value.place(x=5, y=23)

        # BOX EDGE
        self.edge_box = ctk.CTkFrame(
            self.result_frame,
            width=82,
            height=55,
            fg_color="#F9F2F7"
        )
        # Menampilkan jumlah edge/jalur yang dilalui DFS
        self.edge_box.place(x=5, y=108)
 
        self.edge_title = ctk.CTkLabel(
            self.edge_box,
            text="EDGE DILALUI",
            font=("Plus Jakarta Sans", 8, "bold"),
            text_color="#A66B8A"
        )

        self.edge_title.place(x=5, y=5)

        self.edge_value = ctk.CTkLabel(
            self.edge_box,
            text="0",
            font=("Plus Jakarta Sans", 12, "bold"),
            text_color="#3F51B5"
        )

        self.edge_value.place(x=5, y=25)

        # BOX WAKTU
        self.time_box = ctk.CTkFrame(
            self.result_frame,
            width=82,
            height=55,
            fg_color="#F9F2F7"
        )

        self.time_box.place(x=95, y=108)

        self.time_title = ctk.CTkLabel(
            self.time_box,
            text=" WAKTU EKSEKUSI",
            font=("Plus Jakarta Sans", 8, "bold"),
            text_color="#A66B8A"
        )
        # Menampilkan waktu proses algoritma DFS
        self.time_title.place(x=5, y=5)

        self.time_value = ctk.CTkLabel(
            self.time_box,
            text="0 ms",
            font=("Plus Jakarta Sans", 12, "bold"),
            text_color="#FF9800"
        )

        self.time_value.place(x=5, y=25)

        self.draw_graph()  # Memanggil fungsi untuk menggambar seluruh graph wisata

        # ── VISITED ARRAY (TAMBAHAN) ──────────────────────────────────────────

        # Urutan node A–M sesuai node_labels(), # Digunakan untuk menyimpan urutan node yang dikunjungi DFS
        self.node_order = [
            "Stasiun Gubeng",           # A
            "Monumen Tugu Pahlawan",    # B
            "Ekowisata Mangrove Wonorejo",  # C
            "Surabaya North Quay",      # D
            "Kebun Bibit Wonorejo",     # E
            "Taman Bungkul",            # F
            "Atlantis Land",            # G
            "Pantai Ria Kenjeran",      # H
            "Kebun Binatang Surabaya",  # I
            "Jalan Tunjungan",          # J
            "Alun-alun Surabaya",       # K
            "Wisata Perahu Kalimas",    # L
            "Monumen Kapal Selam"       # M
        ]
        
        # Panel background visited array
        self.visited_array_frame = ctk.CTkFrame(
            self,
            width=507,
            height=68,
            fg_color="#FEFEFE",
            corner_radius=6
        )
        self.visited_array_frame.place(x=173, y=475)
        
        self.visited_label = ctk.CTkLabel(   # # Label judul untuk visualisasi visited array DFS
            self.visited_array_frame,
            text="VISITED ARRAY RUTE DFS",
            font=("Plus Jakarta Sans", 9, "bold"),
            text_color="#555555"
        )
        self.visited_label.place(x=8, y=-5)

        # Buat cell untuk tiap node
        self.visited_cells = {}
        labels = self.node_labels()   #  Mengambil label node. Contoh: A = Stasiun Gubeng

        for i, node in enumerate(self.node_order):  # enumerate digunakan untuk: i = index, node  = nama node
            cell_frame = ctk.CTkFrame(   # Frame kecil sebagai cell array
                self.visited_array_frame,
                width=25,
                height=36,
                fg_color="white",
                border_color="#CCCCCC",
                border_width=1,
                corner_radius=4
            )
            cell_frame.place(x=8 + i * 28, y=18)   # Posisi cell dibuat berjajar horizontal

            lbl = ctk.CTkLabel(    # Label huruf node. Contoh: A, B, C, D
                cell_frame,
                text=labels[node],
                font=("Plus Jakarta Sans", 8, "bold"),
                text_color="#555555"
            )
            lbl.place(relx=0.5, y=-5, anchor="n")

            val = ctk.CTkLabel(    # Nilai awal visited array = 0. Artinya node belum dikunjungi
                cell_frame,
                text="0",
                font=("Plus Jakarta Sans", 9, "bold"),
                text_color="#AAAAAA"
            )
            val.place(relx=0.5, y=11, anchor="n")

            self.visited_cells[node] = {   # Menyimpan frame dan value ke dictionary visited_cells
                "frame": cell_frame,
                "value": val
            }

    # UPDATE VISITED ARRAY (TAMBAHAN)
    def update_visited_array(self, visited_nodes):   # Fungsi untuk memperbarui tampilan visited array saat DFS berjalan
        for node, cell in self.visited_cells.items():
            if node in visited_nodes:   # Jika node sudah dikunjungi
                cell["frame"].configure(
                    fg_color="#D4EDDA",
                    border_color="#28A745"   # Warna berubah hijau
                )
                cell["value"].configure(
                    text="1",   # Nilai berubah menjadi 1. Artinya node sudah visited
                    text_color="#155724"
                )
            else:   # Jika node belum dikunjungi
                cell["frame"].configure(
                    fg_color="white",
                    border_color="#CCCCCC"   # Warna kembali default
                )
                cell["value"].configure(
                    text="0",   # Nilai kembali 0. Artinya belum dikunjungi
                    text_color="#AAAAAA"
                )

    # SEARCH ROUTE
    def search_route(self):   # Fungsi utama menjalankan DFS

        start_time = time.perf_counter()   # Menghitung waktu mulai eksekusi

        destination = self.goal_var.get()   # Mengambil tujuan dari ComboBox

        if destination == "pilih lokasi tujuan":  # Jika user belum memilih tujuan maka fungsi dihentikan
            return

        self.selected_destination = destination   # Menyimpan tujuan wisata yang dipilih

        self.current_animation_route = []   # Reset animasi sebelumnya
        self.destination_ready = False   # Status tujuan direset

        self.draw_graph()   # Menggambar ulang graph

        path = self.dfs(   # Menjalankan algoritma DFS. Start node = Stasiun Gubeng. Goal node  = destinasi user
            "Stasiun Gubeng",
            destination
        )
        
        # HITUNG JALUR DIJKSTRA
        dijkstra_path, _ = self.dijkstra(   # Menjalankan algoritma Dijkstra untuk membandingkan jalur terpendek
            "Stasiun Gubeng",
            destination
        )

        # SIMPAN EDGE DIJKSTRA
        self.current_dijkstra_route = []

        if dijkstra_path:
            for i in range(len(dijkstra_path) - 1):
                self.current_dijkstra_route.append(
                    (dijkstra_path[i], dijkstra_path[i + 1])  # Menyimpan edge hasil Dijkstra untuk divisualisasikan di graph
                )

        end_time = time.perf_counter()

        self.execution_time = (
            end_time - start_time
        ) * 1000   # Mengubah waktu ke milisecond
        self.dfs_time_saved = round(self.execution_time, 4)  # Membulatkan hasil waktu eksekusi

        route_edges = []

        if path:

            for i in range(len(path) - 1):

                route_edges.append(
                    (path[i], path[i + 1])  # Mengubah path menjadi pasangan edge agar mudah divisualisasikan
                )

        self.log_box.delete("1.0", "end")   # Menghapus log sebelumnya
 # Menampilkan proses awal DFS seperti stack push dan visit node
        self.log_box.insert(
            "end",
            "INFO  : Mulai DFS\n\n"
        )

        self.log_box.insert(
            "end",
            "START : A (Stasiun Gubeng)\n\n"
        )

        self.log_box.insert(
            "end",
            "PUSH  : A\n"
        )

        self.log_box.insert(
            "end",
            "VISIT : A (Stasiun Gubeng)\n\n"
        )
# RESET HASIL TAMPILAN. Mengembalikan hasil tampilan ke default
        self.result_route.configure(text="-")
        self.distance_value.configure(text="0 KM")
        self.node_value.configure(text="0 Node")
        self.edge_value.configure(text="0")
        self.time_value.configure(text="0 ms")

        # Reset visited array sebelum animasi mulai
        self.update_visited_array([]) # Semua node dikembalikan menjadi 0 sebelum animasi DFS dimulai

        self.animate_route(   # Menjalankan animasi traversal DFS
            route_edges,
            path
        )

    # RESET
    def reset_app(self):  # Mengembalikan seluruh data aplikasi ke kondisi awal/default

        self.selected_destination = None   # Menghapus tujuan wisata yang dipilih
        self.current_animation_route = []   # Menghapus jalur animasi DFS
        self.current_dijkstra_route = []    # Menghapus jalur Dijkstra
        self.destination_ready = False     # Status tujuan dikembalikan menjadi False
        self.show_all_nodes = False    # Menonaktifkan tampilan semua node

        self.goal_var.set("pilih lokasi tujuan")   # Mengembalikan ComboBox ke pilihan awal

        self.log_box.delete("1.0", "end")  # Menghapus seluruh isi log DFS

        self.result_route.configure(text="-")   # Menghapus tampilan rute
        self.distance_value.configure(text="0 KM")   # Reset total jarak
        self.node_value.configure(text="0 Node")    # Reset jumlah node
        self.edge_value.configure(text="0")    # Reset jumlah edge
        self.time_value.configure(text="0 ms")   # Reset waktu eksekusi
        # HAPUS DATA ANALISIS. List widget yang akan dihapus dari halaman analisis
        analysis_widgets = [
            "dfs_distance",
            "dfs_node",
            "dfs_edge",
            "dfs_time",
            "dJ_distance",
            "dj_distance",
            "dj_node",
            "dj_edge",
            "dj_time",
            "chart_frame",
            "kesimpulan_label"
        ]

        for widget in analysis_widgets:
            if hasattr(self, widget):
                getattr(self, widget).destroy()   # Menghapus widget dari tampilan
                delattr(self, widget)   # Menghapus atribut object
        if hasattr(self, "card_dfs"):    # Menghapus card hasil DFS
            self.card_dfs.destroy()
            del self.card_dfs

        if hasattr(self, "card_dj"):    # Menghapus card hasil Dijkstra
            self.card_dj.destroy()
            del self.card_dj

        if hasattr(self, "dfs_found"):  # Menghapus label DFS ditemukan
            self.dfs_found.destroy()

        if hasattr(self, "dj_found"):   # Menghapus label Dijkstra ditemukan
            self.dj_found.destroy()
            
        self.draw_graph()   # Menggambar ulang graph ke kondisi default

        # Reset visited array
        self.update_visited_array([])   # Mengembalikan seluruh node menjadi belum dikunjungi

        self.draw_graph()  # Draw graph kembali setelah reset

    # SHOW NODES
    def show_nodes(self):   # Fungsi untuk menampilkan  seluruh node graph

        self.show_all_nodes = not self.show_all_nodes  # Toggle:  True  → tampilkan node, False → sembunyikan node

        self.draw_graph()   # Menggambar ulang graph

        node_text = ""  # Membuat daftar label node

        for key, value in self.node_labels().items():
            node_text += f"{value} = {key}\n"

        self.log_box.delete("1.0", "end")  # Menghapus isi log sebelumnya
        self.log_box.insert("end", node_text)   # Menampilkan daftar node ke log box
    
    # MENU NAVIGATION
    def reset_menu_color(self):   # Mengembalikan warna semua menu ke kondisi default

        self.dashboard_btn.configure(
            fg_color="transparent",
            text_color="#004B87"
        )

        self.analisis_btn.configure(
            fg_color="transparent",
            text_color="#004B87"
        )

        self.tentang_btn.configure(
            fg_color="transparent",
            text_color="#004B87"
        )

    # DASHBOARD
    def show_dashboard(self): # Fungsi menampilkan dashboard utama

        self.analisis_frame.place_forget()   # Menyembunyikan halaman analisis
        self.tentang_frame.place_forget()    # Menyembunyikan halaman tentang

        self.reset_menu_color()  # Reset warna navbar

        self.dashboard_btn.configure(   # Menandai menu dashboard aktif
            fg_color="#004B87",
            text_color="white"
        )
        self.menu_frame.lift()   # Navbar selalu berada di layer atas
        # ANALISIS
    def show_analysis_screen(self):   # Fungsi membuka halaman analisis

        self.tentang_frame.place_forget()  # Menyembunyikan halaman tentang

        self.analisis_frame.place(x=0, y=0)   # Menampilkan frame analisis
        self.analisis_frame.lift()   # Membawa halaman analisis ke depan

        self.reset_menu_color()   # Reset warna menu navbar

        self.analisis_btn.configure(   # Menandai menu analisis aktif
            fg_color="#004B87",
            text_color="white"
        )

        self.menu_frame.lift()   # Navbar tetap di atas
        
        # LABEL RUTE ANALISIS
        if hasattr(self, "analysis_route_label"):  # Jika label lama ada,maka dihapus terlebih dahulu
            self.analysis_route_label.destroy()

        self.analysis_route_label = ctk.CTkLabel(   # Label menampilkan rute analisis dari start node ke tujuan
            self.analisis_frame,
            text=f"Stasiun Gubeng  →  {self.selected_destination}",
            font=("Plus Jakarta Sans", 14, "bold"),
            text_color="#3D5A80",
            bg_color="#EDF4FA"
        )

        self.analysis_route_label.place(x=460, y=63)

        # ANALISIS DFS VS DIJKSTRA
        if not self.selected_destination:   # Jika user belum memilih tujuan, maka proses analisis dihentikan
            return

        start = "Stasiun Gubeng"   # Titik awal pencarian
        goal = self.selected_destination  # Titik tujuan dipilih user

        #  DFS 
        dfs_path = self.dfs(start, goal)   # Menjalankan algoritma DFS
        dfs_time = self.dfs_time_saved   # Mengambil waktu eksekusi DFS
        dfs_distance = 0   # Variabel total jarak DFS

        for i in range(len(dfs_path) - 1):  # Mengambil pasangan node

            a = dfs_path[i]
            b = dfs_path[i + 1]

            if (a, b) in self.edge_distance:   # Jika edge ditemukan langsung
                dfs_distance += self.edge_distance[(a, b)]

            elif (b, a) in self.edge_distance:   # Karena graph dua arah, maka dicek arah sebaliknya juga
                dfs_distance += self.edge_distance[(b, a)]

        dfs_nodes = len(dfs_path)      # Jumlah node yang dikunjungi DFS
        dfs_edges = len(dfs_path) - 1  # Jumlah edge yang dilalui DFS

        #DIJKSTRA 
        dj_start = time.perf_counter()  # Mulai menghitung waktu Dijkstra

        dijkstra_path, dijkstra_distance = self.dijkstra(    # Menjalankan algoritma Dijkstra
            start,
            goal
        )

        dj_end = time.perf_counter()   # Waktu selesai Dijkstra

        dijkstra_time = round(   # Mengubah waktu menjadi milisecond
            (dj_end - dj_start) *1000 ,
            4
        )

        dijkstra_nodes = len(dijkstra_path)  # Jumlah node pada jalur Dijkstra
        dijkstra_edges = len(dijkstra_path) - 1  # Jumlah edge jalur Dijkstra

        # DFS
        self.analisis_bg.configure(text="")  # Menghapus teks background analisis

        dfs_text = f"""   # Ringkasan hasil DFS
        {round(dfs_distance,1)} KM
        {dfs_nodes} Node
        {dfs_edges} Edge
        {dfs_time}s
"""

        # DIJKSTRA
        dijkstra_text = f"""
        {round(dijkstra_distance,1)} KM
        {dijkstra_nodes} Node
        {dijkstra_edges} Edge
        {dijkstra_time}s
"""

        # HAPUS LABEL LAMA. Menghapus tampilan analisis lama agar tidak menumpuk
        if hasattr(self, "dfs_analysis_label"):
            self.dfs_analysis_label.destroy()

        if hasattr(self, "dijkstra_analysis_label"):
            self.dijkstra_analysis_label.destroy()

        if hasattr(self, "kesimpulan_label"):
            self.kesimpulan_label.destroy()

        # LABEL DFS
        # JALUR
        self.dfs_found = ctk.CTkLabel(   # Menandakan jalur DFS ditemukan
            self.analisis_frame,
            text="YA",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#1D395E",
            bg_color="#D1E5FE"
        )
        
        self.dfs_found.place(x=400, y=150)
        # JARAK. Menampilkan total jarak DFS
        self.dfs_distance = ctk.CTkLabel(
            self.analisis_frame,
            text=f"{round(dfs_distance,1)} KM",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#1D395E",
            bg_color="#D1E5FE"
        )
        self.dfs_distance.place(x=370, y=178)
        
        # NODE Menampilkan jumlah node DFS
        self.dfs_node = ctk.CTkLabel(
            self.analisis_frame,
            text=f"{dfs_nodes} Node",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#1D395E",
            bg_color="#D1E5FE"
        )
        self.dfs_node.place(x=375, y=210)
        
        # EDGE Menampilkan jumlah edge DFS
        self.dfs_edge = ctk.CTkLabel(
            self.analisis_frame,
            text=f"{dfs_edges} Edge",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#1D395E",
            bg_color="#D1E5FE"
        )
        self.dfs_edge.place(x=375, y=245)
        
        self.dfs_time = ctk.CTkLabel(   # Menampilkan waktu eksekusi DFS
            self.analisis_frame,
            text=f"{dfs_time}ms",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#1D395E",
            bg_color="#D1E5FE"
)
        self.dfs_time.place(x=360, y=280)  

        # LABEL DIJKSTRA
        # JALUR Menandakan jalur Dijkstra ditemukan
        self.dj_found = ctk.CTkLabel(   
            self.analisis_frame,
            text="YA",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#D1E5FE",
            bg_color="#243A5F"
        )
        self.dj_found.place(x=810, y=145)

        # JARAK Menampilkan total jarak Dijkstra
        self.dj_distance = ctk.CTkLabel(
            self.analisis_frame,
            text=f"{round(dijkstra_distance,1)} KM",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#D1E5FE",
            bg_color="#243A5F"
        )
        self.dj_distance.place(x=780, y=179)
        
        # NODE  Menampilkan jumlah node Dijkstra
        self.dj_node = ctk.CTkLabel(
            self.analisis_frame,
            text=f"{dijkstra_nodes} Node",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#D1E5FE",
            bg_color="#243A5F"
        )
        self.dj_node.place(x=785, y=211)
        
        # EDGE  Menampilkan jumlah edge Dijkstra
        self.dj_edge = ctk.CTkLabel(
            self.analisis_frame,
            text=f"{dijkstra_edges} Edge",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#D1E5FE",
            bg_color="#243A5F"
        )
        self.dj_edge.place(x=785, y=245)
        
        # WAKTU Menampilkan waktu eksekusi Dijkstra
        self.dj_time = ctk.CTkLabel(
            self.analisis_frame,
            text=f"{dijkstra_time}ms",
            font=("Plus Jakarta Sans", 15, "bold"),
            text_color="#D1E5FE",
            bg_color="#243A5F"
        )

        self.dj_time.place(x=772, y=280)

        if hasattr(self, "chart_frame"):  # Menghapus chart lama
            self.chart_frame.destroy()

        self.chart_frame = ctk.CTkFrame(
            self.analisis_frame,   # Frame untuk grafik perbandingan
            width=820, height=125,
            fg_color="transparent"
        )
        self.chart_frame.place(x=30, y=320)

        charts = [            # Data yang dibandingkan:   1. Jarak 2. Node 3. Edge 4. Waktu
            ("TOTAL JARAK (KM)", dfs_distance,   dijkstra_distance, "KM"),
            ("NODE DIKUNJUNGI",  dfs_nodes,       dijkstra_nodes,    ""),
            ("EDGE DILALUI",     dfs_edges,       dijkstra_edges,    ""),
            ("WAKTU (ms)",       dfs_time,        dijkstra_time,     "ms"),
        ]

        for i, (judul, val_dfs, val_dijk, satuan) in enumerate(charts):   # Card untuk tiap grafik

            card = ctk.CTkFrame(
                self.chart_frame,
                width=190, height=124,
                fg_color="white",
                corner_radius=12,
                border_width=1,
                border_color="#E0E8F0"
            )
            card.place(x=i * 200, y=0)

            ctk.CTkLabel(
                card,
                text=judul,  # Judul grafik
                font=("Plus Jakarta Sans", 9, "bold"),
                text_color="#5B8DB8"
            ).place(x=10, y=8)

            c = tk.Canvas(card, width=170, height=95,  # Canvas untuk menggambar bar chart
                          bg="white", highlightthickness=0)
            c.place(x=60, y=70)

            max_val = max(val_dfs, val_dijk, 0.0001)   # Mengambil nilai terbesar agar tinggi bar proporsional
            bar_max_h = 70    # Tinggi maksimum grafik batang

            # Bar DFS hijau
            h_dfs = int((val_dfs / max_val) * bar_max_h)   # Menghitung tinggi batang DFS
            c.create_rectangle(15, bar_max_h - h_dfs, 75, bar_max_h,
                               fill="#4CAF50", outline="")   # Membuat batang DFS warna hijau
            c.create_text(   # Menampilkan nilai pada batang DFS
                45,
                bar_max_h - (h_dfs / 2),
                text=f"{round(val_dfs, 4)}",
                font=("Plus Jakarta Sans", 9, "bold"),
                fill="white"
            )

            # Bar Dijkstra biru
            h_dijk = int((val_dijk / max_val) * bar_max_h)   # Menghitung tinggi batang Dijkstra berdasarkan nilai maksimum
            c.create_rectangle(90, bar_max_h - h_dijk, 150, bar_max_h,   # Membuat batang grafik Dijkstra warna biru
                               fill="#2196F3", outline="")
            c.create_text(   # Menampilkan nilai di tengah batang Dijkstra
                120,
                bar_max_h - (h_dijk / 2),
                text=f"{round(val_dijk, 4)}",
                font=("Plus Jakarta Sans", 9, "bold"),
                fill="white"
            )

            # Label X
            c.create_text(42,  bar_max_h + 10, text="DFS",
                          font=("Plus Jakarta Sans", 8), fill="#666")   # Label batang DFS
            c.create_text(117, bar_max_h + 10, text="Dijkstra",
                          font=("Plus Jakarta Sans", 8), fill="#666")   # Label batang Dijkstra

        # KESIMPULAN
        conclusion = (
    f"Berdasarkan hasil analisis, DFS menemukan jalur "
    f"dari Stasiun Gubeng ke {goal} dengan total jarak {round(dfs_distance,1)} KM "
    f"melewati {dfs_nodes} node dan {dfs_edges} edge dalam waktu {dfs_time} ms. "
    f"Sementara Dijkstra menemukan jalur terpendek {round(dijkstra_distance,1)} KM "
    f"melewati {dijkstra_nodes} node dan {dijkstra_edges} edge dalam waktu {dijkstra_time} ms. "
    f"DFS lebih panjang {round(dfs_distance - dijkstra_distance, 1)} KM dibanding Dijkstra. "
    f"Kesimpulan: DFS tidak menjamin jalur terpendek, "
    f"sedangkan Dijkstra selalu menghasilkan jalur optimal."
)   # Membuat kesimpulan otomatis berdasarkan hasil analisis algoritma

        self.kesimpulan_label = ctk.CTkLabel(   # Label untuk menampilkan kesimpulan analisis
            self.analisis_frame,
            text=conclusion,
            wraplength=800,
            justify="left",
            font=("Plus Jakarta Sans", 14),
            text_color="#243A5F",
            bg_color="#EDF4FA" 
        )

        self.kesimpulan_label.place(x=45, y=485)
    
    # TENTANG
    def show_tentang_screen(self):   # Fungsi untuk membuka halaman tentang aplikasi

        self.analisis_frame.place_forget()      # Menyembunyikan halaman analisis

        self.tentang_frame.place(x=0, y=0)   # Menampilkan halaman tentang
        self.tentang_frame.lift()   # Membawa frame tentang ke depan

        self.reset_menu_color()   # Reset warna menu navbar

        self.tentang_btn.configure(    # Menandai menu tentang aktif
            fg_color="#004B87",
            text_color="white"
        )
        self.menu_frame.lift()   # Navbar tetap di layer atas

    #keluar aplikasi
    def quit_app(self):
        from tkinter import messagebox  # Import messagebox untuk dialog konfirmasi
        if messagebox.askyesno("Keluar", "Yakin ingin keluar dari aplikasi?"):  # Jika user memilih YA,  aplikasi akan ditutup
            self.destroy()
       
    # DFS
    def dfs(self, start, goal, path=None):  # Fungsi DFS menggunakan rekursi

        if path is None:  # Jika path kosong, buat list baru
            path = []

        path = path + [start]  # Menambahkan node saat ini ke path

        if start == goal:   # Jika node saat ini adalah goal, maka jalur dikembalikan
            return path

# The above code is iterating over each neighbor of a given node `start` in a graph data structure. It
# is accessing the list of neighbors of the node `start` in the `self.graph` dictionary and then
# iterating over each neighbor to perform some operation.
        for neighbor in self.graph[start]: #perulangan untuk mengecek semua tetangga atau node yang terhubung dengan node saat ini.

            if neighbor not in path:   # Mengecek agar node tidak dikunjungi ulang
                #stack(rekursi)
                new_path = self.dfs(
                    neighbor,
                    goal,
                    path
                ) # Rekursi DFS ke node berikutnya

                if new_path:   # Jika goal ditemukan, maka path dikembalikan
                    return new_path

        return None   # Jika tidak ada jalur ditemukan

    # DIJKSTRA
    def dijkstra(self, start, goal):  # Fungsi mencari jalur terpendek menggunakan algoritma Dijkstra

        unvisited = {}  # Menyimpan node yang belum dikunjungi
        previous = {} # Menyimpan node sebelumnya untuk membangun path

        for node in self.graph:  # Semua node awalnya bernilai infinity
            unvisited[node] = float("inf")

        unvisited[start] = 0   # Node awal memiliki jarak 0

        while unvisited:  

            current = min(  # Mengambil node dengan jarak terkecil
                unvisited,
                key=unvisited.get
            )

            current_distance = unvisited[current]

            if current == goal:  # Jika goal ditemukan, proses dihentikan
                break

            for neighbor in self.graph[current]:   # Variabel biaya edge

                edge_cost = 0

                if (current, neighbor) in self.edge_distance:  # Karena graph dua arah, maka dicek dua arah
                    edge_cost = self.edge_distance[(current, neighbor)]

                elif (neighbor, current) in self.edge_distance:
                    edge_cost = self.edge_distance[(neighbor, current)] #Program mengambil nilai bobot atau biaya antara node saat ini dan node tetangga.

                new_distance = current_distance + edge_cost  # Menghitung jarak baru (jika ditemukan jalur yang lebih pendek, jalur node&sebelumnya diperbarui)

                if neighbor in unvisited and new_distance < unvisited[neighbor]:  # Update jarak terpendek dan simpan node sebelumnya

                    unvisited[neighbor] = new_distance
                    previous[neighbor] = current #Jika ditemukan jalur yang lebih pendek, jarak node dan jalur sebelumnya akan diperbarui.

            unvisited.pop(current)  # Node current dianggap selesai (tetangganya sudah diperiksa)

        # BUILD PATH
        path = []
        current = goal

        while current != start:

            path.insert(0, current)  

            if current not in previous: # Jika tidak ada jalur
                return None, 0

            current = previous[current]

        path.insert(0, start) # Menambahkan start node

        total_distance = 0  # Menghitung total jarak final

        for i in range(len(path) - 1):

            a = path[i]
            b = path[i + 1]

            if (a, b) in self.edge_distance:
                total_distance += self.edge_distance[(a, b)]

            elif (b, a) in self.edge_distance:
                total_distance += self.edge_distance[(b, a)]

        return path, total_distance  # Mengembalikan path dan total jarak
    # ANIMASI DFS
    def animate_route(self, route, path_nodes, index=0):  # Fungsi animasi traversal DFS

        if index >= len(route):  # Jika animasi selesai

            self.destination_ready = True
            self.draw_graph()  # Menggambar graph final

            # Update visited array saat selesai (semua node di path)
            self.update_visited_array(path_nodes)  # Semua node path menjadi visited

            self.log_box.insert(  # Menampilkan status DFS selesai
                "end",
                f"\nGOAL  : {self.selected_destination}\n"
            )

            self.log_box.insert(
                "end",
                "STATUS: TARGET DITEMUKAN\n\n"
            )

            self.log_box.insert(
                "end",
                "SELESAI"
            )

            self.log_box.see("end")   # Auto scroll ke bawah

            short_route = []  # Mengubah nama node menjadi label contoh: Stasiun Gubeng → A

            for p in path_nodes:
                short_route.append(self.node_labels()[p])

            route_text = " → ".join(short_route)  # Menampilkan rute hasil DFS
            self.result_route.configure(
                text=route_text
            )

            total_distance = 0

            for i in range(len(path_nodes) - 1):

                a = path_nodes[i]
                b = path_nodes[i + 1]

                if (a, b) in self.edge_distance:
                    total_distance += self.edge_distance[(a, b)]

                elif (b, a) in self.edge_distance:
                    total_distance += self.edge_distance[(b, a)]

            self.distance_value.configure(
                text=f"{round(total_distance,1)} KM"
            )

            self.node_value.configure(
                text=f"{len(path_nodes)} Node"
            )

            self.edge_value.configure(
                text=f"{len(route)} Edge"
            )

            self.time_value.configure(
                text=f"{round(self.execution_time, 4)} ms"
            )

            return

        self.destination_ready = False

        self.current_animation_route = route[:index + 1]
 
        self.draw_graph()   # Menggambar ulang graph

        # Update visited array step by step (node yang sudah dikunjungi)
        self.update_visited_array(path_nodes[:index + 2])

        current_node = path_nodes[index + 1]

        short = self.node_labels()[current_node]

        self.log_box.insert(  # Menampilkan proses traversal DFS
            "end",
            f"PUSH  : {short}\n"
        )

        self.log_box.insert(
            "end",
            f"VISIT : {short} ({current_node})\n\n"
        )

        self.log_box.see("end")

        self.after(
            500,  # Animasi berjalan tiap 500 ms
            lambda:
            self.animate_route(
                route,
                path_nodes,
                index + 1
            )
        )

    # CHANGE DESTINATION
    def change_destination(self, destination):  # Fungsi untuk mengganti lokasi tujuan 
        self.selected_destination = destination  # Menyimpan tujuan yang dipilih user
        self.goal_var.set(destination)   # Mengubah isi ComboBox sesuai pilihan

    # LABEL NODE
    def node_labels(self):  # Fungsi untuk mengubah nama lokasi menjadi label huruf A–M

        return {  # Label digunakan agar graph lebih ringkas dan mudah dibaca
            "Stasiun Gubeng": "A",
            "Monumen Tugu Pahlawan": "B",
            "Ekowisata Mangrove Wonorejo": "C",
            "Surabaya North Quay": "D",
            "Kebun Bibit Wonorejo": "E",
            "Taman Bungkul": "F",
            "Atlantis Land": "G",
            "Pantai Ria Kenjeran": "H",
            "Kebun Binatang Surabaya": "I",
            "Jalan Tunjungan": "J",
            "Alun-alun Surabaya": "K",
            "Wisata Perahu Kalimas": "L",
            "Monumen Kapal Selam": "M"
        }

    # DRAW GRAPH
    def draw_graph(self):  # Fungsi untuk menggambar graph pada canvas

        self.graph_canvas.delete("all")  # Menghapus gambar graph lama agar bisa digambar ulang

        positions = {  # Menentukan koordinat setiap node pada canvas graph

            "Stasiun Gubeng": (230, 145),

            "Taman Bungkul": (70, 45),
            "Jalan Tunjungan": (170, 35),
            "Monumen Kapal Selam": (285, 35),
            "Monumen Tugu Pahlawan": (420, 45),

            "Kebun Binatang Surabaya": (30, 145),

            "Wisata Perahu Kalimas": (190, 260),
            "Atlantis Land": (340, 260),

            "Kebun Bibit Wonorejo": (140, 340),
            "Ekowisata Mangrove Wonorejo": (360, 340),

            "Alun-alun Surabaya": (360, 145),
            "Pantai Ria Kenjeran": (500, 145),

            "Surabaya North Quay": (520, 260),
        }

        edges = [   # Edge merepresentasikan hubungan antar node beserta bobot jaraknya

            ("Kebun Binatang Surabaya", "Stasiun Gubeng", "4.8 KM"),
            ("Stasiun Gubeng", "Alun-alun Surabaya", "900 M"),
            ("Alun-alun Surabaya", "Pantai Ria Kenjeran", "7.7 KM"),
            ("Pantai Ria Kenjeran", "Surabaya North Quay", "7.6 KM"),

            ("Surabaya North Quay", "Atlantis Land", "12.8 KM"),
            ("Atlantis Land", "Ekowisata Mangrove Wonorejo", "14.3 KM"),

            ("Atlantis Land", "Wisata Perahu Kalimas", "8.5 KM"),
            ("Wisata Perahu Kalimas", "Kebun Bibit Wonorejo", "10.8 KM"),

            ("Wisata Perahu Kalimas", "Stasiun Gubeng", "1.6 KM"),

            ("Stasiun Gubeng", "Taman Bungkul", "3.9 KM"),
            ("Stasiun Gubeng", "Jalan Tunjungan", "3.2 KM"),
            ("Stasiun Gubeng", "Monumen Kapal Selam", "280 M"),

            ("Taman Bungkul", "Jalan Tunjungan", "6.6 KM"),
            ("Jalan Tunjungan", "Monumen Kapal Selam", "2.3 KM"),

            ("Monumen Kapal Selam", "Monumen Tugu Pahlawan", "4.4 KM"),
        ]

        node_labels = self.node_labels()  # Mengambil label huruf node

        # DRAW EDGE
        for start, end, distance in edges:  # Mengambil koordinat node awal dan akhir

            x1, y1 = positions[start]
            x2, y2 = positions[end]

            # DFS (PINK) Mengecek apakah edge termasuk jalur DFS
            is_dfs = (   
                (start, end) in self.current_animation_route
                or
                (end, start) in self.current_animation_route
            )

            # DIJKSTRA (UNGU)  Mengecek apakah edge termasuk jalur Dijkstra
            is_dijkstra = (
                (start, end) in self.current_dijkstra_route
                or
                (end, start) in self.current_dijkstra_route
            )
            
            # EDGE DFS
            is_dfs = (
                (start, end) in self.current_animation_route
                or
                (end, start) in self.current_animation_route
            )

            # EDGE DIJKSTRA
            is_dijkstra = (
                (start, end) in self.current_dijkstra_route
                or
                (end, start) in self.current_dijkstra_route
            )

            # JIKA KEDUANYA SAMA
            if is_dfs and is_dijkstra:

                # GARIS PINK Menampilkan jalur DFS
                self.graph_canvas.create_line(
                    x1 - 2, y1 - 2,
                    x2 - 2, y2 - 2,
                    fill="#00C853",
                    width=4,
                    smooth=True
                )

                # GARIS UNGU Menampilkan jalur Dijkstra
                self.graph_canvas.create_line(
                    x1 + 2, y1 + 2,
                    x2 + 2, y2 + 2,
                    fill="#D32F2F",
                    width=4,
                    smooth=True
                )

            # HANYA DFS Jalur DFS diberi warna pink
            elif is_dfs:

                self.graph_canvas.create_line(
                    x1, y1,
                    x2, y2,
                    fill="#00C853",
                    width=5,
                    smooth=True
                )

            # HANYA DIJKSTRA Jalur Dijkstra diberi warna ungu
            elif is_dijkstra:

                self.graph_canvas.create_line(
                    x1, y1,
                    x2, y2,
                    fill="#D32F2F",
                    width=5,
                    smooth=True
                )

            # EDGE BIASA. Edge biasa diberi warna soft pink
            else:

                self.graph_canvas.create_line(
                    x1, y1,
                    x2, y2,
                    fill="#E7A6C3",
                    width=2,
                    smooth=True
                )
            # POSISI LABEL JARAK Menghitung titik tengah edge
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2

            self.graph_canvas.create_text(  # Menampilkan jarak edge
                mx,
                my - 8,
                text=distance,
                fill="#B67E9B",
                font=("Plus Jakarta Sans", 10, "bold")
            )

        # DRAW NODE
        for node, (x, y) in positions.items():

            radius = 18   # Radius lingkaran node

            is_destination = (  # Node tujuan akan diberi warna khusus jika target ditemukan
                node == self.selected_destination
                and self.destination_ready
            )

            is_nodes_mode = self.show_all_nodes # Mengecek apakah mode tampil semua node aktif

            if is_destination:  # Warna node tujuan (destination)
                node_fill = "#FFD6E5"
                node_outline = "#FF4F87"

            elif is_nodes_mode:  # Warna node yang sedang dalam mode pemilihan
                node_fill = "#FFF4A3"
                node_outline = "#F2B705"

            else:       # Warna default node biasa
                node_fill = "#F8F8F8"
                node_outline = "#D4D4D4"

            self.graph_canvas.create_oval(     # Gambar bayangan node
                x - radius + 2,
                y - radius + 2,
                x + radius + 2,
                y + radius + 2,
                fill="#E7E7E7",
                outline=""
            )

            self.graph_canvas.create_oval(     # Gambar lingkaran utama node dengan warna sesuai kondisi
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=node_fill,
                outline=node_outline,
                width=3
            )

            self.graph_canvas.create_text(  # Tampilan label singkat di tengah node
                x,
                y,
                text=node_labels[node],
                fill="#333333",
                font=("Plus Jakarta Sans", 10, "bold")
            )

            self.graph_canvas.create_text(      # Tampilkan nama lengkap node di bawah lingkaran
                x,
                y + 38,
                text=node,
                fill="#6E6E6E",
                font=("Plus Jakarta Sans", 5, "bold"),
                width=95,
                justify="center"
            ) 

# Menjalankan Aplikasi
if __name__ == "__main__":
    app = HealtripApp()
    app.mainloop()