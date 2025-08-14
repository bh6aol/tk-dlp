import subprocess
import logging

class ProbUtil:
    @staticmethod
    def prob_ffmpeg_info(ffmpeg_path="ffmpeg"):
        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            first_line = result.stdout.splitlines()[0]
            return first_line  # eg "ffmpeg version 6.1.1 ..."
        except Exception as e:
            logging.exception(e)
            return None
    
    @staticmethod
    def prob_yt_dlp_info(ffmpeg_path="yt-dlp"):
        try:
            result = subprocess.run(
                [ffmpeg_path, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            first_line = result.stdout.splitlines()[0]
            return first_line  # eg "2025.07.21"
        except Exception as e:
            logging.exception(e)
            return None