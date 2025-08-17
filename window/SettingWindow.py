from configparser import ConfigParser
import customtkinter as ctk
from tkinter import messagebox
import yt_dlp
from window import *
from util import *
import os

class SettingWindow(ctk.CTkToplevel):
    def __init__(self, *args, fg_color = None, language, config: ConfigParser, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.config = config
        self.language = language
        self.title(self.language['setting'])
        self.iconbitmap(R.path(os.path.join("image","tk-dlp.ico")))
        self.geometry("600x400")
        self.entries = {}  # ref

        # tab view
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)

        for section in config.sections():
            self.add_section_tab(tabview, section, config[section])

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        about_btn = ctk.CTkButton(btn_frame, text=f"{self.language['about']} tk-dlp", command=self.show_about)
        about_btn.grid(row=0, column=0, padx=5)

        save_btn = ctk.CTkButton(btn_frame, text=f"{self.language['save']}", command=self.save_config)
        save_btn.grid(row=0, column=1, padx=5)

    def show_about(self):
        about_win = AboutWindow(self, language=self.language, config=self.config)
        about_win.transient(self)
        about_win.grab_set()
        self.wait_window(about_win)

    def load_language(self):
        lst = [os.path.splitext(f)[0] for f in os.listdir(R.path("language"))]
        lst.insert(0, 'auto')
        return lst


    def add_section_tab(self, tabview, section_name, section_items):
        tab = tabview.add(section_name)
        self.entries[section_name] = {}

        row = 0
        for key, value in section_items.items():
            ctk.CTkLabel(tab, text=key).grid(row=row, column=0, sticky="w", padx=5, pady=5)

            if section_name == "common" and key in ("app_name", "version"):
                entry = ctk.CTkEntry(tab)
                entry.insert(0, value)
                entry.configure(state="readonly")
            elif section_name == "common" and key == "language":
                entry = ctk.CTkOptionMenu(tab, values=self.load_language())
                entry.set(self.config.get('common', 'language'))
            elif section_name == "common" and key == "appearance_mode":
                entry = ctk.CTkOptionMenu(tab, values=['system', 'dark', 'light'])
                entry.set(self.config.get('common', 'appearance_mode'))

            elif section_name == "log" and key == "level":
                entry = ctk.CTkOptionMenu(tab, values=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
                entry.set(self.config.get('log', 'level'))
            elif section_name == "proxy" and key == "enabled":
                entry = ctk.CTkOptionMenu(tab, values=['yes', 'no'])
                entry.set(self.config.get('proxy', 'enabled'))
            elif section_name == "update" and key in ("check_url", "download_url"):
                entry = ctk.CTkEntry(tab)
                entry.insert(0, value)
                entry.configure(state="readonly")
            elif section_name == "yt-dlp" and key == "buildin_version":
                entry = ctk.CTkLabel(tab, text=yt_dlp.version.__version__, anchor="w")
            elif section_name == "yt-dlp" and key == "enabled_cookiefile":
                entry = ctk.CTkOptionMenu(tab, values=['yes', 'no'])
                entry.set(self.config.get('yt-dlp', 'enabled_cookiefile'))
            elif section_name == "ffmpeg" and key == "enabled_system":
                entry = ctk.CTkOptionMenu(tab, values=['yes', 'no'])
                entry.set(self.config.get('ffmpeg', 'enabled_system'))
            elif section_name == "ffmpeg" and key == "system_version":
                ffmpeg_info = ProbUtil.prob_ffmpeg_info()
                if ffmpeg_info == None:
                    ffmpeg_info = self.language['not_found']
                entry = ctk.CTkLabel(tab, text=ffmpeg_info, anchor="w")
            else:
                entry = ctk.CTkEntry(tab)
                entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            tab.grid_columnconfigure(1, weight=1)

            self.entries[section_name][key] = entry
            row += 1

    def save_config(self):
        # check custom location
        if self.entries['ffmpeg']['enabled_system'].get() == 'no':
            custom_yt_dlp_location = self.entries['ffmpeg']['custom_location'].get()
            ret = ProbUtil.prob_ffmpeg_info(custom_yt_dlp_location)
            if ret == None:
                messagebox.showerror(
                    title=self.language['setting'],
                    message=f"ffmpeg:custom_location={custom_yt_dlp_location} \n{self.language['no_exec']}",
                    icon="error")
                return

        for section, keys in self.entries.items():
            for key, entry in keys.items():
                if isinstance(entry, ctk.CTkEntry) or isinstance(entry, ctk.CTkOptionMenu):
                    self.config[section][key] = entry.get()
                elif isinstance(entry, ctk.CTkLabel):
                    self.config[section][key] = entry.cget("text")
                else:
                    raise Exception("save_config failed, unkown entry type!")
        with open(R.path("config.ini"), "w", encoding="utf-8") as f:
            self.config.write(f)
        
        messagebox.showinfo(
            title=self.language['saved'],
            message=f"config.ini {self.language['saved']}", icon='info')
