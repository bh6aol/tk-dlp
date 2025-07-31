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
        self.geometry("400x150")
        self.title("tk-dlp")

        self.button = ctk.CTkButton(self, text=self.language["about"], command=self.show_about)
        self.button.pack(padx=20, pady=20)


    def load_language(self):
        try:
            language = self.config.get("common", "language")
            if language == "auto":
                import locale
                default_locale = locale.getdefaultlocale()
                language = default_locale[0]
        except Exception as e:
            logging.error(e)
            language = "en_US"
        try:
            with open(os.path.join("language", f"{language}.json"), "r", encoding="utf-8") as f:
                return LanguageDict(json.loads(f.read()))
        except Exception as e:
            logging.error(e)
            sys.exit(-1)


    def show_about(self):
        about_win = AboutWindow(self, language=self.language, config=self.config)
        about_win.transient(self)
        about_win.grab_set()
        self.wait_window(about_win)



def main():
    # load cfg
    config = configparser.ConfigParser()
    config.read('config.ini')

    log_level = config.getint("log", "log_level")
    log_file = config.get("log", "log_file")

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
