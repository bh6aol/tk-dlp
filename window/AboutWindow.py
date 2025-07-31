from configparser import ConfigParser
import customtkinter as ctk
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
        win_width, win_height = 350, 180
        self.geometry(f"{win_width}x{win_height}")

        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        label = ctk.CTkLabel(frame, 
            text=f"📦 tk-dlp App\n{self.language["version"]} {config.get("common", "version",fallback="N/A")}\n© 2025 BH6AOL")
        label.pack(pady=(10, 5))

        github_icon = ctk.CTkImage(
            light_image=Image.open("image/github-logo.png"),  
            dark_image=Image.open("image/github-logo.png"),
            size=(18, 18)
        )

        bilibili_icon = ctk.CTkImage(
            light_image=Image.open("image/bilibili-logo.ico"),  
            dark_image=Image.open("image/bilibili-logo.ico"),
            size=(18, 18)
        )
        # 水平布局容器
        link_frame = ctk.CTkFrame(frame, fg_color="transparent")  
        link_frame.pack(pady=5)

        link_text_color = "#66CCFF" if ctk.get_appearance_mode() == "Dark" else "#0000FF"

        link1 = ctk.CTkLabel(
            link_frame,
            text=" GitHub",
            image=github_icon,
            compound="left",
            text_color=link_text_color,
            cursor="hand2"
        )
        link1.pack(side="left", padx=5)
        link1.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/bh6aol/tk-dlp"))

        link2 = ctk.CTkLabel(
            link_frame,
            text=" Bilibili",
            image=bilibili_icon,
            compound="left",
            text_color=link_text_color,
            cursor="hand2"
        )
        link2.pack(side="left", padx=5)
        link2.bind("<Button-1>", lambda e: webbrowser.open("https://space.bilibili.com/10883577/bh6aol"))

        ok_button = ctk.CTkButton(frame, text=self.language["ok"], width=80, command=self.destroy)
        ok_button.pack(pady=10)

