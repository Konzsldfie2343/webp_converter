from PIL import Image
import os

class Compressor:
    def __init__(self):
        self.selected_folder = None
        self.file_list = None
        self.target_extensions = ["jpeg", "jpg", "png"]
        self.is_converting = False
        self.compression_ratio = 85
        self.is_replace_original = False
        self.is_recursive = False

    def on_drop(self, event, is_recursive):
        self.refresh()
        self.is_recursive = is_recursive
        self.selected_folder = event.data.strip("{ }")
        if not self.selected_folder: return

        self.file_list = self.get_img_file_paths()

    def on_browse(self, folder_path, is_recursive):
        self.refresh()
        self.is_recursive = is_recursive
        self.selected_folder = folder_path.strip("{ }")
        if not self.selected_folder: return

        self.file_list = self.get_img_file_paths()
    
    def get_img_file_paths(self):
        # 追加: 渡されたパスがファイルの場合、そのファイルのみを対象とする
        if os.path.isfile(self.selected_folder):
            if self.selected_folder.lower().endswith(tuple(self.target_extensions)):
                return [self.selected_folder]
            else:
                return []
                
        file_paths = []
        for root, _, files in os.walk(self.selected_folder):
            file_paths.extend([os.path.join(root, f) for f in files if f.lower().endswith(tuple(self.target_extensions))])
            if not self.is_recursive:
                break
        return file_paths

    def run(self, compression_ratio, is_replace_original, is_recursive, progress_bar, status_label_text):
        if self.is_converting: return
        if not self.file_list: return

        self.compression_ratio = compression_ratio
        self.is_replace_original = is_replace_original
        self.is_recursive = is_recursive

        self.is_converting = True

        for index, file_name in enumerate(self.file_list, start=1):
            self.convert_to_webp(file_name)
            progress_bar.set(index / len(self.file_list))
            status_label_text.set(f"変換中...　{index} / {len(self.file_list)}")

        self.is_converting = False
            
    def convert_to_webp(self, file_path):
        output_img = f"{os.path.splitext(file_path)[0]}.webp"
        with Image.open(file_path) as img:
            img.save(output_img, "webp", quality=self.compression_ratio)
        if self.is_replace_original:
            os.remove(file_path)

    def refresh(self):
        self.selected_folder = None
        self.file_list = None

