from configparser import ConfigParser
import customtkinter as ctk
from tkinter import messagebox
from window import *
from util import *
import os

class SettingWindow(ctk.CTkToplevel):
    def __init__(self, *args, fg_color = None, language, config: ConfigParser, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.config = config
        self.language = language
        self.title(self.language['setting'])
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
            elif section_name == "proxy" and key == "enabled":
                entry = ctk.CTkOptionMenu(tab, values=['yes', 'no'])
                entry.set(self.config.get('proxy', 'enabled'))
            else:
                entry = ctk.CTkEntry(tab)
                entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            tab.grid_columnconfigure(1, weight=1)

            self.entries[section_name][key] = entry
            row += 1

    def save_config(self):
        for section, keys in self.entries.items():
            for key, entry in keys.items():
                self.config[section][key] = entry.get()

        with open(R.path("config.ini"), "w", encoding="utf-8") as f:
            self.config.write(f)
        
        messagebox.showinfo(
            title=self.language['saved'],
            message=f"config.ini {self.language['saved']}", icon='info')
