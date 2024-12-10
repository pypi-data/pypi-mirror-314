

class ByError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class SurahNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class VersetNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class FormatValueGet(Exception):
    def __init__(self, *args):
        super().__init__(*args)
