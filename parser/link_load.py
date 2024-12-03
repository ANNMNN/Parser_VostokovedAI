import pandas as pd
from parser.link_parser import ArticleParser
from db_chanks import TextChunkDB
from langchain_integration.embeddings import EmbeddingProcessor
from db_emb import EmbeddingDB

def load_links_from_excel(excel_path):
    try:
        sheet = pd.read_excel(excel_path)  # Чтение Excel
        # Получаем ссылки из четвертого столбца (индекс 3)
        links = sheet.iloc[:, 3].dropna().tolist()
        print("Загруженные ссылки:", links)
        return links
    except Exception as e:
        print(f"Ошибка при чтении файла Excel: {e}")
        return []

def process_links_from_excel(file_path, column_index):
    """
    Обработка ссылок из Excel-файла.
    :param file_path: Путь к Excel-файлу.
    :param column_index: Индекс столбца с ссылками (нумерация начинается с 0).
    """
    try:
        data = pd.read_excel(file_path)
        links = data.iloc[:, column_index]

        text_db = TextChunkDB()
        embedding_processor = EmbeddingProcessor()
        embedding_db = EmbeddingDB()

        for link in links:
            if isinstance(link, str) and link.startswith("http"):
                print(f"Обрабатываю ссылку: {link}")
                parser = ArticleParser(link)
                article_text = parser.parse()

                if article_text:
                    # Разделяем текст на чанки
                    chunks = split_text_into_chunks(article_text)
                    print(f"Ссылка: {link}\nНайдено {len(chunks)} чанков.")
                    print(chunks)
                    # Сохраняем чанки в БД
                    for chunk in chunks:
                        text_db.insert_chunk(chunk, link)

                    # Создаем эмбеддинги
                    embeddings = embedding_processor.create_embeddings([{"text": chunk} for chunk in chunks])

                    # Сохраняем эмбеддинги
                    for embedding in embeddings:
                        embedding_db.insert_embedding(embedding, link)
                else:
                    print(f"Не удалось извлечь текст по ссылке: {link}")
            else:
                print(f"Неверная ссылка: {link}")

        text_db.close()
        embedding_db.close()

    except Exception as e:
        print(f"Ошибка при обработке Excel файла: {e}")

def split_text_into_chunks(text, chunk_size=500):
    """
    Разделяет текст на чанки фиксированного размера.
    :param text: Исходный текст.
    :param chunk_size: Максимальный размер одного чанка.
    :return: Список чанков.
    """
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
