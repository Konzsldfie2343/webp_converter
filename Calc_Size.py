import os

class Calc_Size:
    def __init__(self):
        self.before_size = 0
        self.after_size = 0
    
    def add_before_size(self, file_path):
        if os.path.isfile(file_path):
            self.before_size += os.path.getsize(file_path)

    def add_after_size(self, file_path):
        if os.path.isfile(file_path):
            self.after_size += os.path.getsize(file_path)

    def size_diff(self):
        return self.before_size - self.after_size

    def size_rate(self):
        return self.size_diff() / self.before_size * 100

    def get_result(self):
        return self.format_size(self.size_diff()), self.size_rate()

    def format_size(self, size_in_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024