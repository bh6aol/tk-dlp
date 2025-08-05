import customtkinter as ctk
import configparser
import logging
import json
import os
import sys
from window import *
from util import *

class App(ctk.CTk):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.language = self.load_language()

        width = 400
        height = 150
        self.geometry(f"{width}x{height}")
        self.center_window(width, height)
        
        self.title(self.config.get('common', 'app_name'))

        self.button = ctk.CTkButton(self, text=self.language["about"], command=self.show_about)
        self.button.pack(padx=20, pady=20)

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
        about_win = AboutWindow(self, language=self.language, config=self.config)
        about_win.transient(self)
        about_win.grab_set()
        self.wait_window(about_win)



def main():

    # load cfg
    config = configparser.ConfigParser()
    config.read(R.path('config.ini'), encoding='utf-8')

    log_level = config.getint("log", "level")
    log_file = config.get("log", "file")

    # init log
    logging.basicConfig(
        filename=log_file,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=log_level
    )


    app = App(config)
    app.mainloop()


if __name__ == "__main__":
    main()
