from modules.core.singleton import Singleton


class WordService(metaclass=Singleton):
    def __init__(self):
        pass

    def splitter(self, limit: int, text: str):
        pieces = text.split()
        return (" ".join(pieces[i : i + limit]) for i in range(0, len(pieces), limit))
