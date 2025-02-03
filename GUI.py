from tkinter import PhotoImage, StringVar, IntVar, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image as PILImage
import os
import time
import threading
import ipdb

class Calc_folder_size:
    def __init__(self):
        self.path = ""
        self.size = 0

    def calc_size(self, path):
        self.path = path
        self.size = 0
        if os.path.isdir(self.path):
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    self.size += os.path.getsize(os.path.join(root, file))
            return self.size
        elif os.path.isfile(self.path):
            return os.path.getsize(self.path)
        return 0

    def format_size(self, size_in_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024

class GUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.geometry("900x600")
        self.root.title("Compressor")
        self.root.configure(bg="#1C1C1C")
        self.root.resizable(False, False)
        
        self.compression_ratio = IntVar(value=85)
        self.compression_label_text = StringVar(value=f"圧縮率: {self.compression_ratio.get()}%")
        self.compression_quality_text = StringVar(value=f"{self.explain_compression_ratio(self.compression_ratio.get())}")
        self.progress_bar = ctk.CTkProgressBar(self.root, progress_color="#00ADB5", height=10)
        self.progress_bar.set(0)
        self.is_replace_original = IntVar()
        self.is_recursive = IntVar()
        self.status_label_text = StringVar(value="フォルダ未選択")

        self.before_size = 0
        self.after_size = 0

        self.reduction_rate = StringVar(value="ファイル・フォルダをドロップ\nしてください")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.setup_ui()
        self.enable_drag_and_drop()
        
    def setup_ui(self):

        self.left_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=10, 
            fg_color="#2E2E2E", 
            border_width=2, 
            border_color="#00ADB5"
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.right_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=10, 
            fg_color="#2E2E2E", 
            border_width=2, 
            border_color="#00ADB5"
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.create_left_widgets()
        self.create_right_widgets()
        
    def create_left_widgets(self):
        ctk.CTkLabel(
            self.left_frame, 
            text="画像を自動で軽量化します", 
            font=("Arial", 30, "bold"), 
            fg_color="transparent", 
            text_color="#FFFFFF"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            self.left_frame, 
            textvariable=self.compression_label_text, 
            font=("Arial", 15), 
            fg_color="transparent", 
            text_color="#FFFFFF"
        ).pack(pady=5)

        ctk.CTkLabel(
            self.left_frame, 
            textvariable=self.compression_quality_text, 
            font=("Arial", 12), 
            fg_color="transparent", 
            text_color="#FFFFFF"
        ).pack(pady=5)
        
        self.quality_slider = ctk.CTkSlider(
            self.left_frame, 
            from_=100, 
            to=10, 
            height=10, 
            fg_color="#FFFFFF", 
            button_hover_color="#00ADB5", 
            bg_color="#2E2E2E", 
            progress_color="#00CED1", 
            button_color="#00ADB5", 
            border_color="#00ADB5", 
            border_width=2, 
            orientation="horizontal", 
            variable=self.compression_ratio, 
            command=self.update_compression_label
        )
        self.quality_slider.pack(pady=10, padx=20)
        
        ctk.CTkCheckBox(
            self.left_frame, 
            text="変換後に元の画像を置き換える", 
            fg_color="#2E2E2E", 
            variable=self.is_replace_original, 
            text_color="#FFFFFF", 
            border_width=2, 
            border_color="#00ADB5", 
            hover_color="#2E2E2E"
        ).pack(pady=5)

        ctk.CTkCheckBox(
            self.left_frame, 
            text="すべてのフォルダを対象にする", 
            fg_color="#2E2E2E", 
            variable=self.is_recursive, 
            text_color="#FFFFFF", 
            border_width=2, 
            border_color="#00ADB5", 
            hover_color="#2E2E2E"
        ).pack(pady=5)
        
        self.listbox = ctk.CTkTextbox(
            self.left_frame, 
            width=300, 
            height=150, 
            font=("Arial", 12), 
            wrap="word", 
            border_width=2, 
            bg_color="#2E2E2E", 
            fg_color="#2E2E2E", 
            text_color="#FFFFFF", 
            border_color="#00ADB5"
        )
        self.listbox.pack(expand=True, fill="both", pady=10, padx=10)
        self.listbox.configure(state="disabled")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.left_frame, 
            width=300, 
            fg_color="#2E2E2E", 
            progress_color="#00ADB5", 
            mode="determinate", 
            border_color="#00ADB5", 
            border_width=2
        )
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            self.left_frame, 
            textvariable=self.status_label_text, 
            font=("Arial", 15), 
            fg_color="transparent", 
            text_color="#FFFFFF"
        )
        self.status_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(
            self.left_frame, 
            width=300, 
            height=10,
            fg_color="#2E2E2E", 
            progress_color="#00ADB5", 
            mode="determinate", 
            border_color="#00ADB5", 
            border_width=1
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
    
    def create_right_widgets(self):
        image = PILImage.open("assets/dragarea/folder.png")
        self.icon = CTkImage(light_image=image, size=(100, 100))
        self.icon_label = ctk.CTkLabel(
            self.right_frame, 
            image=self.icon, 
            fg_color="transparent", 
            text="DROP", 
            font=("Arial", 20, "bold"), 
            text_color="#FFFFFF"
        )
        self.icon_label.pack(pady=20)
        
        self.refresh_button = ctk.CTkButton(
            self.right_frame, 
            text="再読み込み", 
            text_color="#FFFFFF", 
            font=("Arial", 15), 
            border_color="#00ADB5", 
            border_width=1, 
            fg_color="#00ADB5", 
            hover_color="#00CED1", 
            command=self.refresh
        )
        self.refresh_button.pack(pady=10)
        
        self.run_button = ctk.CTkButton(
            self.right_frame, 
            text="実行", 
            text_color="#FFFFFF", 
            font=("Arial", 15), 
            border_color="#00ADB5", 
            border_width=1, 
            fg_color="#00ADB5", 
            hover_color="#00CED1", 
            command=self.run_conversion
        )
        self.run_button.pack(pady=10)

        self.browse_button = ctk.CTkButton(
            self.right_frame, 
            text="フォルダを選択", 
            text_color="#FFFFFF", 
            font=("Arial", 15), 
            border_color="#00ADB5", 
            border_width=1, 
            fg_color="#00ADB5", 
            hover_color="#00CED1", 
            command=self.browse_folder
        )
        self.browse_button.pack(pady=10)

        self.reduction_rate_label = ctk.CTkLabel(
            self.right_frame, 
            textvariable=self.reduction_rate, 
            font=("Arial", 15), 
            fg_color="transparent", 
            text_color="#FFFFFF"
        )
        self.reduction_rate_label.pack(pady=10)

        app_icon = PhotoImage(file="assets/icon.png")
        self.root.iconphoto(False, app_icon)

    def enable_drag_and_drop(self):
        self.right_frame.drop_target_register(DND_FILES)
        self.right_frame.dnd_bind("<<Drop>>", self.on_drop)

    def browse_folder(self):
        self.refresh()
        temp_folder_path = filedialog.askdirectory()
        if not os.path.basename(temp_folder_path): return
        self.compressor.on_browse(temp_folder_path, self.is_recursive.get())
        self.status_label_text.set(f"選択中：{os.path.basename(self.compressor.selected_folder)}")
        self.update_status("success")
        self.folder_path = self.compressor.selected_folder
        self.display_file_names(self.compressor.file_list)
    
    def on_drop(self, event):
        self.refresh()
        self.compressor.on_drop(event, self.is_recursive.get())
        self.status_label_text.set(f"選択中：{os.path.basename(self.compressor.selected_folder)}")
        self.reduction_rate.set("ドロップされました")
        self.update_status("success")
        self.folder_path = self.compressor.selected_folder
        self.display_file_names(self.compressor.file_list)

    def run_conversion(self):
        if not hasattr(self, 'folder_path'):
            return

        self.status_label_text.set(f"{os.path.basename(self.folder_path)} を変換中...")
        self.refresh_button.configure(state="disabled")
        self.run_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")

        def conversion_task():
            # 変換前のサイズを計算
            self.before_size = Calc_folder_size().calc_size(self.folder_path)
        
            # 画像変換の実行（処理中にプログレスバーなどが更新されると仮定）
            self.compressor.run(
                self.compression_ratio.get(),
                self.is_replace_original.get(),
                self.is_recursive.get(),
                self.progress_bar,
                self.status_label_text
            )
        
            # バグ発見！変換後の拡張子は.webpに変わっているので、このままでは変換後のサイズを計算できない
            # 変換後のサイズを計算
            if os.path.isdir(self.folder_path):
                self.after_size = Calc_folder_size().calc_size(self.folder_path)
            else:
                self.after_size = os.path.getsize(f"{self.folder_path.split('.')[0]}.webp")

            saved_size = 0
            if self.is_replace_original.get():
                saved_size = self.before_size - self.after_size
            else:
                converted_img_size = self.after_size - self.before_size
                saved_size = self.before_size - converted_img_size

            if self.before_size != 0:
                saved_rate = saved_size / self.before_size * 100
            else:
                saved_rate = 0

            if not os.path.isdir(f"{self.folder_path.split('.')[0]}.webp"):
                if not self.is_replace_original.get():
                    saved_size = self.before_size - self.after_size
                    saved_rate = saved_size / self.before_size * 100

            if self.before_size == self.after_size:
                saved_size = 0
                saved_rate = 0
        
            # メインスレッドでUIの更新を実施
            self.root.after(0, lambda: self.update_after_conversion(saved_size, saved_rate))

        threading.Thread(target=conversion_task).start()

        # XXX:修正作業中
        result = 0
        if not self.before_size == 0:
            result = int(self.after_size / self.before_size * 100)

    def update_after_conversion(self, saved_size, saved_rate):
        self.after_size = Calc_folder_size().calc_size(self.folder_path)
        self.reduction_rate.set(f"{saved_rate:.1f}%軽量化\n{Calc_folder_size().format_size(abs(saved_size))}削減")
        self.refresh_button.configure(state="normal")
        self.run_button.configure(state="normal")
        self.browse_button.configure(state="normal")
        self.status_label_text.set(f"{os.path.basename(self.folder_path)} を変換完了")
    
    def update_status(self, status):
        status_images = {
            "success": "assets/dragarea/dropped.png", 
            "error": "assets/dragarea/error.png", 
            "pending": "assets/dragarea/folder.png"
        }
        self.icon = CTkImage(light_image=PILImage.open(status_images[status]), size=(100, 100))
        self.icon_label.configure(image=self.icon)
    
    def display_file_names(self, file_names):
        self.listbox.configure(state="normal")
        self.listbox.delete(1.0, "end")
        for file_name in file_names:
            self.listbox.insert("end", os.path.basename(file_name) + "\n")
        self.listbox.configure(state="disabled")
    
    def refresh(self):
        if hasattr(self, 'folder_path'):
            del self.folder_path
    
        self.listbox.configure(state="normal")
        self.listbox.delete(1.0, "end")
        self.listbox.configure(state="disabled")
    
        self.progress_bar.set(0)

        self.reduction_rate.set("フォルダをドロップ\nしてください")
    
        if not hasattr(self, 'folder_path'):
            self.status_label_text.set("フォルダ未選択")
            self.update_status("pending")
        else:
            self.update_status("pending")
            self.status_label_text.set("準備完了")

        self.compressor.refresh()
    
    def update_compression_label(self, event=None):
        self.compression_label_text.set(f"圧縮率: {self.compression_ratio.get()}%")
        self.compression_quality_text.set(self.explain_compression_ratio(self.compression_ratio.get()))

    def explain_compression_ratio(self, compression_ratio):
        if compression_ratio <= 50:
            return "△非推奨　サイズ減少量：大きい　劣化：激しい"
        elif 50 < compression_ratio < 85:
            return "サイズ減少量：中程度　劣化：中程度"
        elif 85 <= compression_ratio:
            return "◯推奨　サイズ減少量：小さい　劣化：少ない"
    
    def run(self, compressor):
        self.compressor = compressor
        self.root.mainloop()