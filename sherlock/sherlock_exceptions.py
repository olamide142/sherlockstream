
from email import message


class EntryFileException(Exception):
    def __init__(self):
        self.message = f"""\n{'.'*30}\nuse case:\nfrom sherlock import Sherlock\nSherlock(__file__)"""
        super().__init__(self.message)

    def __str__(self):
        return self.message