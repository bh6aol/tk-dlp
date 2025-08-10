class FmtUtil:
    @staticmethod
    def sizeof_fmt(total_bytes, suffix='iB'):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(total_bytes) < 1024.0:
                return f"{total_bytes:3.1f}{unit}{suffix}"
            total_bytes /= 1024.0
        return f"{total_bytes:.1f}Y{suffix}"

    @staticmethod
    def time_fmt(seconds):
        units = [
            ("year", 60 * 60 * 24 * 365),
            ("day", 60 * 60 * 24),
            ("hour", 60 * 60),
            ("min", 60),
            ("sec", 1),
        ]
        for unit_name, unit_seconds in units:
            if abs(seconds) >= unit_seconds:
                value = seconds / unit_seconds
                return f"{value:.1f} {unit_name}{'' if value == 1 else 's'}"
        return "0 sec"