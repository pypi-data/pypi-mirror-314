class VerbiaError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WordInvalidError(VerbiaError):
    def __init__(self, word: str, language: str):
        super().__init__(f"Word '{word}' is not valid in language {language}")
