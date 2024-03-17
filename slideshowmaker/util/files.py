import glob
import os


class FileUtil:
    def get_input_files():
        files = glob.glob(os.path.join("", "data/", "*.*"))
        return files
