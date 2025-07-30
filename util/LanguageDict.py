
class LanguageDict(dict):
    def __getitem__(self, key):
        return super().get(key, "?")
