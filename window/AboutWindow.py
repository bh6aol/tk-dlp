from configparser import ConfigParser
import logging
import threading
from packaging import version
import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from util import *
from PIL import Image

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, *args, fg_color = None, language: LanguageDict, config: ConfigParser, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.language = language
        self.config = config
        self.title(language["about"])
        self.resizable(False, False)
        self.geometry("350x180")

        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        label = ctk.CTkLabel(frame, 
            text=f"tk-dlp App\n{self.language["version"]} {config.get("common", "version",fallback="N/A")}\n© 2025 BH6AOL")
        label.pack(pady=(10, 5))

        github_icon = ctk.CTkImage(
            light_image=Image.open(R.path("image/github-logo.png")),  
            dark_image=Image.open(R.path("image/github-logo.png")),
            size=(18, 18)
        )

        x_icon = ctk.CTkImage(
            light_image=Image.open(R.path("image/x-logo.png")),  
            dark_image=Image.open(R.path("image/x-logo.png")),
            size=(18, 18)
        )

        bilibili_icon = ctk.CTkImage(
            light_image=Image.open(R.path("image/bilibili-logo.ico")),  
            dark_image=Image.open(R.path("image/bilibili-logo.ico")),
            size=(18, 18)
        )
        # 水平布局容器
        link_frame = ctk.CTkFrame(frame, fg_color="transparent")  
        link_frame.pack(pady=5)

        link_text_color = "#66CCFF" if ctk.get_appearance_mode() == "Dark" else "#0000FF"

        link_github = ctk.CTkLabel(
            link_frame,
            text=" GitHub",
            image=github_icon,
            compound="left",
            text_color=link_text_color,
            cursor="hand2"
        )
        link_github.pack(side="left", padx=5)
        link_github.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bh6aol/tk-dlp"))

        link_x = ctk.CTkLabel(
            link_frame,
            text=" X(Twitter)",
            image=x_icon,
            compound="left",
            text_color=link_text_color,
            cursor="hand2"
        )
        link_x.pack(side="left", padx=5)
        link_x.bind("<Button-1>", lambda e: webbrowser.open("https://x.com/bh6aol"))


        link_bilibili = ctk.CTkLabel(
            link_frame,
            text=" Bilibili",
            image=bilibili_icon,
            compound="left",
            text_color=link_text_color,
            cursor="hand2"
        )
        link_bilibili.pack(side="left", padx=5)
        link_bilibili.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/10883577"))

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")  
        button_frame.pack(pady=10)
        self.update_button = ctk.CTkButton(
            button_frame, 
            text=self.language["update"], 
            width=80, 
            command=self.update
        )
        self.ok_button = ctk.CTkButton(
            button_frame, 
            text=self.language["ok"], 
            width=80,
            command=self.destroy
        )
        self.update_button.pack(side="left", padx=5)
        self.ok_button.pack(side="left", padx=5)

    def update(self):
        self.update_button.configure(text=f"{self.language['loading']}...", state="disabled")
        threading.Thread(target=self.get_latest_version).start()

    def get_latest_version(self):
        try:
            uh = UpdateHelper(self.config)
            latest_version_text = uh.get_latest_version()
            latest_version = version.parse(latest_version_text)
            current_version = version.parse(self.config.get("common", "version"))
            if current_version < latest_version:
                answer = messagebox.askyesno(
                    title=self.config.get("common", "app_name"),
                    message=f"{self.language['find_new_version']}: {latest_version}\n{self.language['yn_go_to_download']}",
                    icon="info"
                )
                if answer:
                    url = f"{self.config.get('update', 'download_url')}/{latest_version_text}"
                    webbrowser.open(url)
            else:
                messagebox.showinfo(
                    title=self.config.get("common", "app_name"),
                    message=f"{self.config.get('common','app_name')} {self.language['is_up_to_date']}",
                    icon="info")
        except Exception as e:
            logging.exception(e)
        finally:
            self.update_button.after(
                300, 
                lambda: self.update_button.configure(text=self.language["update"], state="normal")
            )
