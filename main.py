import threading
from tkinter import messagebox
import customtkinter as ctk
import configparser
import logging
import json
import os
import sys
import re
import yt_dlp
from window import *
from util import *

class App(ctk.CTk):
    def __init__(self, cfg: configparser.ConfigParser):
        super().__init__()
        self.cfg = cfg
        self.language = self.load_language()

        self.ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

        width = 400
        height = 150
        self.geometry(f"{width}x{height}")
        self.center_window(width, height)
        
        self.title(self.cfg.get('common', 'app_name'))

        # setting frame
        setting_frame = ctk.CTkFrame(self, fg_color="transparent")
        setting_frame.pack(pady=(5, 0), padx=20, fill="x")

        # setting btn
        self.setting_button = ctk.CTkButton(setting_frame, text=self.language['setting'], 
                                           command=self.show_setting, width=20)
        self.setting_button.pack(side="left")


        # proxy checkbox
        self.proxy_check_var = ctk.StringVar(value=self.cfg.get("proxy", "enabled", fallback="no"))
        proxy_checkbox = ctk.CTkCheckBox(setting_frame, text="Enable Proxy", command=self.proxy_checkbox_event,
                                            variable=self.proxy_check_var, onvalue="yes", offvalue="no")
        proxy_checkbox.pack(side="left", padx=20,)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=(10, 20), padx=20, fill="x")

        self.url_entry = ctk.CTkEntry(search_frame, placeholder_text=self.language['url_placeholder'])
        self.url_entry.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(search_frame, width=1, text=" ").pack(side="left")

        self.download_button = ctk.CTkButton(search_frame, text=self.language['download'], 
                                           command=self.start_download_thread, width=80)
        self.download_button.pack(side="left")

        video_info_frame = ctk.CTkFrame(self, fg_color="transparent")
        video_info_frame.pack(pady=(0, 0), padx=20, fill="x")
        self.video_info_label = ctk.CTkLabel(video_info_frame, width=1, text="")
        self.video_info_label.pack(side="left")

        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(pady=(0, 0), padx=20, fill="x")
        self.progressbar = ctk.CTkProgressBar(progress_frame, width=300)
        self.progressbar.set(0.0)

    
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_half = int((screen_width - width) / 2)
        y_half = int((screen_height - height) / 2)

        self.geometry(f"{width}x{height}+{x_half}+{y_half}")

    def proxy_checkbox_event(self):
        val = self.proxy_check_var.get()
        self.cfg.set("proxy", "enabled", val)
        with open(R.path("config.ini"), "w", encoding="utf-8") as f:
            self.cfg.write(f)


    def load_language(self):
        try:
            language = self.cfg.get("common", "language")
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

    def show_setting(self):
        about_win = SettingWindow(self, language=self.language, config=self.cfg)
        about_win.transient(self)
        about_win.grab_set()
        self.wait_window(about_win)
        # update some staff
        self.proxy_check_var.set(self.cfg.get("proxy", "enabled", fallback="no"))

    def start_download_thread(self):
        self.download_button.configure(text="Runing...", state="disabled", fg_color="gray")
        threading.Thread(target=self.download, args=('downloads',), daemon=True).start()

    def download(self, output_path='downloads'):
        self.after(0, lambda: self.video_info_label.configure(text='Preparing...'))
        self.after(0, lambda: self.progressbar.set(0))

        url = self.url_entry.get()
        if self.cfg.get('proxy', 'enabled', fallback='no') == 'yes':
            proxy = self.cfg.get('proxy', 'https', fallback='')
        else:
            proxy = ''
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': 'best',
            'progress_hooks': [self.yt_dlp_hook],
            'proxy': proxy,
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydlp:
                ydlp.download([url])
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(
                title=self.cfg.get("common", "app_name"),
                message=e,
                icon="error")
            self.after(0, lambda: self.video_info_label.configure(text=""))
            self.progressbar.pack_forget()
        finally:
            self.download_button.configure(text=self.language['download'], state="normal", fg_color="#3a7ebf")



    def yt_dlp_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            total_str = FmtUtil.sizeof_fmt(total) if total else "Unknown size"
            eta = d.get('eta')
            eta_str = FmtUtil.time_fmt(int(eta)) if eta is not None else '--'
            msg = f"{d['_percent_str']} of {total_str} at {d['_speed_str']} ETA {eta_str}"
            msg = self.ansi_escape.sub('', msg)
        elif d['status'] == 'finished':
            if d.get('downloaded_bytes', 0) == 0:
                msg = f"Exist: {d['filename'][:24]}..."
            else:
                msg = f"Destination: {d['filename'][:24]}"
        elif d['status'] == 'postprocessing':
            msg = "Postprocessing..."
        else:
            messagebox.showerror(
                title=self.cfg.get("common", "app_name"),
                message=d,
                icon="error")
        self.after(0, lambda: self.video_info_label.configure(text=msg))
        percent_str = self.ansi_escape.sub('', d['_percent_str'])
        progress = float(percent_str.split('%')[0]) / 100.0
        if progress > 0 and not self.progressbar.winfo_ismapped():
            self.after(0, lambda: self.progressbar.pack(fill="x"))
                    
        self.after(0, lambda: self.progressbar.set(progress))


def main():

    # load cfg
    cfg = configparser.ConfigParser()
    cfg.read(R.path('config.ini'), encoding='utf-8')

    log_level = cfg.get("log", "level", fallback="NOTSET")
    log_file = cfg.get("log", "file", fallback="./tk-dlp.log")

    # init log
    logging.basicConfig(
        filename=log_file,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=log_level
    )

    appearance_mode = cfg.get("common", "appearance_mode", fallback="system")
    ctk.set_appearance_mode(appearance_mode)

    app = App(cfg)
    app.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    main()
