import tkinter as tk
import customtkinter as ctk
import configparser
import logging
import json
import os
import sys
from window import *
from util import *

class App(ctk.CTk):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.language = self.load_language()

        width = 400
        height = 150
        self.geometry(f"{width}x{height}")
        self.center_window(width, height)
        
        self.title(self.cfg.get('common', 'app_name'))

        menu_bar = tk.Menu(self)

        # help
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label=self.language['about'], accelerator="Ctrl+H", command=self.show_about)
        menu_bar.add_cascade(label=self.language['help'], menu=help_menu)

        # add menu_bar
        self.config(menu=menu_bar)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=(30, 20), padx=20, fill="x")

        self.url_entry = ctk.CTkEntry(search_frame, placeholder_text=self.language['url_placeholder'])
        self.url_entry.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(search_frame, width=1, text=" ").pack(side="left")

        self.search_button = ctk.CTkButton(search_frame, text=self.language['download'], 
                                           command=self.download, width=80)
        self.search_button.pack(side="left")

        video_info_frame = ctk.CTkFrame(self, fg_color="transparent")
        video_info_frame.pack(pady=(0, 0), padx=20, fill="x")
        ctk.CTkLabel(video_info_frame, width=1, text="Video name: ").pack(side="left")

        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(pady=(0, 0), padx=20, fill="x")
        progressbar = ctk.CTkProgressBar(progress_frame, width=300)
        progressbar.pack(fill="x")
        progressbar.set(0.5)  # set as 50%
        progressbar.start()   # unkown progress disp


    
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_half = int((screen_width - width) / 2)
        y_half = int((screen_height - height) / 2)

        self.geometry(f"{width}x{height}+{x_half}+{y_half}")


    def load_language(self):
        try:
            language = self.config.get("common", "language")
            if language == "auto":
                import locale
                default_locale = locale.getdefaultlocale()
                language = default_locale[0]
        except Exception as e:
            logging.exception(e)
            language = "en_US"
        try:
            with open(R.path(os.path.join("language", f"{language}.json")), "r", encoding="utf-8") as f:
                return LanguageDict(json.loads(f.read()))
        except Exception as e:
            logging.exception(e)
            sys.exit(-1)


    def show_about(self):
        about_win = AboutWindow(self, language=self.language, config=self.cfg)
        about_win.transient(self)
        about_win.grab_set()
        self.wait_window(about_win)

    def download(self):
        pass

def main():

    # load cfg
    cfg = configparser.ConfigParser()
    cfg.read(R.path('config.ini'), encoding='utf-8')

    log_level = cfg.getint("log", "level")
    log_file = cfg.get("log", "file")

    # init log
    logging.basicConfig(
        filename=log_file,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=log_level
    )


    app = App(cfg)
    app.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    main()
