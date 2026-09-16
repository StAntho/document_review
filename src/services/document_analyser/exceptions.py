class UnsupportedFormatError(Exception):
    def __init__(self, fmt: str):
        self.fmt = fmt
        super().__init__(f"Format non supporté: {fmt}")