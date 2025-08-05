import sys
import os

class R:
    
    @staticmethod
    def path(res_path):
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller temp dir
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, res_path)