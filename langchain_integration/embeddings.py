# Создание эмбеддингов
from sentence_transformers import SentenceTransformer

class EmbeddingProcessor:
    def __init__(self, model_name="all-MiniLM-L6-v2"):

        # Инициализация модели для генерации эмбеддингов.

        self.model = SentenceTransformer(model_name)

    def create_embeddings(self, chunks):

        texts = [chunk["text"] for chunk in chunks if chunk["text"]]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        #print(embeddings)
        return embeddings
