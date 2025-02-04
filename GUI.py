from tkinter import PhotoImage, StringVar, IntVar, filedialog
# os.environ["TKDND_LIB"] = "venv/lib/tkinterdnd2"
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image as PILImage
import os
import time
import threading
import ipdb
<<<<<<< HEAD
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

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
=======
from styles import *
import os
from Compressor import Compressor
>>>>>>> branch-A-recovery

class GUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.geometry("800x500")
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
            width=500,
            **frame_styles
        )
        self.left_frame.grid(column=0 , **frame_grid_styles)
        self.left_frame.grid_propagate(False)
        self.left_frame.pack_propagate(False)
        self.left_frame.propagate(False)
        
        self.right_frame = ctk.CTkFrame(
            self.root, 
            width=300,
            **frame_styles
        )
        self.right_frame.grid(column=1, **frame_grid_styles)
        self.right_frame.grid_propagate(False)
        self.right_frame.pack_propagate(False)
        self.right_frame.propagate(False)
        
        self.create_left_widgets()
        self.create_right_widgets()
        
    def create_left_widgets(self):
        ctk.CTkLabel(
            self.left_frame, 
            text="画像を自動で軽量化します", 
            font=("Arial", 30, "bold"), 
            **text_base_style
        ).pack(pady=10)
        
        ctk.CTkLabel(
            self.left_frame, 
            textvariable=self.compression_label_text, 
            font=("Arial", 15), 
            **text_base_style
        ).pack(pady=5)

        ctk.CTkLabel(
            self.left_frame, 
            textvariable=self.compression_quality_text, 
            font=("Arial", 12), 
            **text_base_style
        ).pack(pady=5)
        
        self.quality_slider = ctk.CTkSlider(
            self.left_frame, 
            **quality_silider_style,
            variable=self.compression_ratio, 
            command=self.update_compression_label
        )
        self.quality_slider.pack(pady=10, padx=20)
        
        self.is_replace_original_checkbox = ctk.CTkCheckBox(
            self.left_frame, 
            text="変換後に元の画像を置き換える", 
            variable=self.is_replace_original, 
            **checkbox_style
        ).pack(pady=5)

        self.is_recursive_checkbox = ctk.CTkCheckBox(
            self.left_frame, 
            text="すべてのフォルダを対象にする", 
            variable=self.is_recursive, 
            **checkbox_style
        ).pack(pady=5)
        
        self.listbox = ctk.CTkTextbox(
            self.left_frame, 
            **listbox_style
        )
        self.listbox.pack(expand=True, fill="both", pady=10, padx=10)
        self.listbox.configure(state="disabled")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.left_frame, 
            **progress_bar_style
        )
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            self.left_frame, 
            textvariable=self.status_label_text, 
            font=("Arial", 15), 
            **text_base_style
        )
        self.status_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(
            self.left_frame, 
            **progress_bar_style
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
    
    def create_right_widgets(self):
        image = PILImage.open(os.path.join(base_path, "assets/dragarea/folder.png"))
        self.icon = CTkImage(light_image=image, size=(100, 100))
        self.icon_label = ctk.CTkLabel(
            self.right_frame, 
            image=self.icon, 
            text="DROP", 
            font=("Arial", 20, "bold"), 
            **text_base_style
        )
        self.icon_label.pack(pady=20)
        
        self.refresh_button = ctk.CTkButton(
            self.right_frame, 
            text="再読み込み", 
            **button_style,
            command=self.refresh
        )
        self.refresh_button.pack(pady=10)
        
        self.run_button = ctk.CTkButton(
            self.right_frame, 
            text="実行", 
            **button_style,
            command=self.run_conversion
        )
        self.run_button.pack(pady=10)

        self.browse_button = ctk.CTkButton(
            self.right_frame, 
            text="フォルダを選択", 
            **button_style,
            command=self.browse_folder
        )
        self.browse_button.pack(pady=10)

        self.reduction_rate_label = ctk.CTkLabel(
            self.right_frame, 
            textvariable=self.reduction_rate, 
            font=("Arial", 15), 
            **text_base_style
        )
        self.reduction_rate_label.pack(pady=10)

        app_icon = PhotoImage(file=os.path.join(base_path, "assets/icon.png"))
        self.root.iconphoto(False, app_icon)

    def enable_drag_and_drop(self):
        self.right_frame.drop_target_register(DND_FILES)
        self.right_frame.dnd_bind("<<Drop>>", self.on_drop)

    def change_UI_mode(self, mode):
        UI_ELEMENTS = [
            self.refresh_button,
            self.run_button,
            self.browse_button,
        ]
        for element in UI_ELEMENTS:
            if element:
                element.configure(state=mode)

    def browse_folder(self):
        self.refresh()
        temp_folder_path = filedialog.askdirectory()
        if not os.path.basename(temp_folder_path): return
        self.compressor.on_browse(temp_folder_path, self.is_recursive.get())
        self.status_label_text.set(f"選択中：{os.path.basename(self.compressor.selected_folder)}")
        self.update_status("success")
        self.path = self.compressor.selected_folder
        self.display_file_names(self.compressor.file_list)
    
    def on_drop(self, event):
        self.refresh()
        self.compressor.on_drop(event, self.is_recursive.get())
        self.status_label_text.set(f"選択中：{os.path.basename(self.compressor.selected_folder)}")
        self.reduction_rate.set("ドロップされました")
        self.update_status("success")
        self.path = self.compressor.selected_folder
        self.display_file_names(self.compressor.file_list)

    def run_conversion(self):
        if not hasattr(self, 'path'): return

        self.change_UI_mode("disabled")

        def conversion_task():
        
            self.compressor.run(
                self.compression_ratio.get(),
                self.is_replace_original.get(),
                self.is_recursive.get(),
                self.progress_bar,
                self.status_label_text
            )
        
<<<<<<< HEAD
            # 変換後のサイズを計算
            self.after_size = Calc_folder_size().calc_size(self.folder_path)

            saved_size = 0
            if os.path.isdir(self.folder_path):
                if self.is_replace_original.get():
                    saved_size = self.before_size - self.after_size
                else:
                    converted_img_size = self.after_size - self.before_size
                    saved_size = self.before_size - converted_img_size

            if self.before_size == 0:
                saved_size = 0
            else:
                saved_rate = saved_size / self.before_size * 100

            if self.before_size == self.after_size:
                saved_size = 0
                saved_rate = 0
        
            # メインスレッドでUIの更新を実施
            self.root.after(0, lambda: self.update_after_conversion(saved_size, saved_rate))
=======
            self.root.after(0, lambda: self.update_after_conversion())
>>>>>>> branch-A-recovery

        threading.Thread(target=conversion_task).start()

    def update_after_conversion(self):
        size_diff, size_rate = self.compressor.get_result()
        self.reduction_rate.set(f"削減量：{size_diff} 削減率：{size_rate:.1f}%")
        self.change_UI_mode("normal")
        self.status_label_text.set(f"{os.path.basename(self.path)} を変換完了")
    
    def update_status(self, status):
        status_images = {
            "success": os.path.join(base_path, "assets/dragarea/dropped.png"), 
            "error": os.path.join(base_path, "assets/dragarea/error.png"), 
            "pending": os.path.join(base_path, "assets/dragarea/folder.png")
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
        if hasattr(self, 'path'):
            del self.path
    
        self.listbox.configure(state="normal")
        self.listbox.delete(1.0, "end")
        self.listbox.configure(state="disabled")
    
        self.progress_bar.set(0)

        self.reduction_rate.set("フォルダをドロップ\nしてください")
    
        if not hasattr(self, 'path'):
            self.status_label_text.set("フォルダ未選択")
            self.update_status("pending")
        else:
            self.update_status("pending")
            self.status_label_text.set("準備完了")

        self.compressor = Compressor()
    
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
    
    def run(self):
        self.compressor = Compressor()
        self.root.mainloop()