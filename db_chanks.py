import sqlite3

class TextChunkDB:
    def __init__(self, db_path="text_chunks.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            source_file TEXT NOT NULL,
            UNIQUE(text, source_file)
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_chunk(self, text, source_file):
        query = "INSERT OR IGNORE INTO chunks (text, source_file) VALUES (?, ?)"
        self.conn.execute(query, (text, source_file))
        self.conn.commit()

    def get_processed_files(self):
        query = "SELECT DISTINCT source_file FROM chunks"
        result = self.conn.execute(query).fetchall()
        return {row[0] for row in result}

    def close(self):
        self.conn.close()
