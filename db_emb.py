import sqlite3

class EmbeddingDB:
    def __init__(self, db_path="embeddings.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            embedding BLOB NOT NULL,
            source_file TEXT NOT NULL,
            UNIQUE(embedding, source_file)
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_embedding(self, embedding, source_file):
        query = "INSERT OR IGNORE INTO embeddings (embedding, source_file) VALUES (?, ?)"
        self.conn.execute(query, (embedding, source_file))
        self.conn.commit()

    def get_processed_files(self):
        query = "SELECT DISTINCT source_file FROM embeddings"
        result = self.conn.execute(query).fetchall()
        return {row[0] for row in result}

    def close(self):
        self.conn.close()
