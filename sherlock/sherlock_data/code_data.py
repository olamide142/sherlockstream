""" Sherlock stream base for data/structure"""
import uuid
from pathlib import Path
from typing import Optional

from sherlock.sherlock_data.common import mapThenList


class Id:

    def __init__(self):
        self._id = str(uuid.uuid4())


    def __repr__(self):
        return str(self._id)


class File:

    def __init__(self, fileName: Path):
        self.fileName = fileName
    

    def __repr__(self):
        return f'[File::{self.fileName}'


class Line:

    def __init__(self):
        self.file:File = None
        self.lineNumber = None
        self.endLineNumber= None
        self.colOffset = None
        self.endColOffset = None


    def parse(self, node, file: File):
        self.lineNumber = node.lineno
        self.colOffset = node.col_offset
        self.endLineNumber = node.end_lineno
        self.endColOffset = node.end_col_offset
        self.file = file
        return self.__repr__()


    def __repr__(self):
        return "::".join(mapThenList([
            self.file,
            self.lineNumber,
            self.colOffset,
            self.endLineNumber,
            self.endColOffset
        ], str))