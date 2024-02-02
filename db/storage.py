from sqlite3 import connect


class DatabaseManager:

    def __init__(self, path):
        self.conn = connect(path)
        self.conn.execute('pragma foreign_keys = on')