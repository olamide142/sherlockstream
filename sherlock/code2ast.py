'''Convert python source code to python's Abstract Syntax Tree'''
import ast

from sherlock.sherlock_data.persistence import Log2DB

class CodeToAst:

    def __init__(self, filePath):
        self.filePath = filePath
        self.sourceCode = None

    def reader(self):
        with open(self.filePath, 'r') as fileReader:
            self.sourceCode = fileReader.read()

    def convert(self):
        if not self.sourceCode:
            self.reader()
        return ast.parse(self.sourceCode)
    
    def saveFile(self):
        db = Log2DB.instance()
        sql = f"""
                    INSERT INTO source_code
                    (file_path, session_id)
                    VALUES('{self.filePath}', {db.getSession()[0]})
                """
        return db.insertQuery(sql)