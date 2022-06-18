"""Database setup"""
import sqlite3
import functools

from sherlock.utils import generateUuid

class DBFormatter:
    FUNCTION_LOCATION = lambda *args: f"INSERT INTO function (name, source_code_id,\
         lineNumber, colOffset, session_id, hash_id) VALUES {args}"

class Log2DB:

    _instance = None

    @classmethod
    def instance(cls, dbName=':memory:'):
        """Singleton instance"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance = {}
            cls._instance['dbName'] = dbName
            cls._instance['ready'] = False
            cls._instance['connection'] = cls.connect()
            cls.setUp()
            print('[+] Done Creating a new singleton instance of Sherlock DB')
        return cls

    @classmethod
    def connect(cls):
        """Create connection to db"""
        return sqlite3.connect(cls._instance['dbName'])

    @classmethod
    def getCursor(cls):
        """"Get db Cursor object"""
        return cls._instance['connection'].cursor()

    @classmethod
    @functools.lru_cache(maxsize=1) #if processing multiple session ever becomes a thing remove this line
    def getSession(cls):
        sql = """select * from session
                order by rowid desc
                limit 1"""
        cursor = cls.getCursor()
        try:
            return next(iter(cursor.execute(sql)))
        except Exception: #no session exist for this db/repo/directory
            raise Exception("Session needs to be created")

    @classmethod
    def setUp(cls):
        """Prep db"""
        cls.createTables()
        cls._instance['ready'] = True
        cls.createSession()

    @classmethod
    def createSession(cls, name=None):
        """Create a new sherlock stream session"""
        sql = f"""INSERT INTO session (name) VALUES ('{name if name else generateUuid()}')"""
        cursor = cls.getCursor()
        cursor.execute(sql)
        cls.save()

    @classmethod
    def createTables(cls):
        """Create relevant tables"""
        cursor = cls.getCursor()

        createSourceCodeTable = """
            CREATE TABLE IF NOT EXISTS source_code (
                source_code_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path       TEXT NOT NULL,
                session_id      INTEGER NOT NULL
            );
        """
        createSessionTable = """
            CREATE TABLE IF NOT EXISTS session (
                session_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL UNIQUE
            );
        """
        createFunctionTable = """
            CREATE TABLE IF NOT EXISTS function (
                function_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                source_code_id  INTEGER NOT NULL,
                name            TEXT NOT NULL,
                lineNumber      INTEGER NOT NULL,
                colOffset       INTEGER NOT NULL,
                session_id      INTEGER NOT NULL,
                hash_id          TEXT NOT NULL UNIQUE
            );
        """
        createProgramFlow = """
            CREATE TABLE IF NOT EXISTS function_call (
                function_call_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id          INTEGER NOT NULL,
                hash_id              TEXT NOT NULL
            );
        """

        print('Creating Tables...')
        queries = [createSourceCodeTable, createSessionTable, 
            createFunctionTable, createProgramFlow]

        for query in queries:
            cursor.execute(query)
        
        cls.save()
        print('Done Creating Tables')

    @classmethod
    def insertQuery(cls, query):
        query = query.strip()
        cursor = cls.getCursor()
        cursor.execute(query)
        return cursor.lastrowid

    @classmethod
    def save(cls):
        cls._instance['connection'].commit()
    
    @classmethod
    def close(cls):
        cls.getCursor().close()
        cls._instance['connection'].close()


    
if __name__ == '__main__':
    db = Log2DB.instance()