import os
import time
from parser.parser import FileParser
from parser.link_load import process_links_from_excel, load_links_from_excel, split_text_into_chunks
from db_chanks import TextChunkDB
from db_emb import EmbeddingDB
from langchain_integration.embeddings import EmbeddingProcessor


def process_file(file_path, source_file):
    parser = FileParser(file_path)

    chunks = parser.parse()
    print(f"Обработан файл {source_file}. Найдено {len(chunks)} чанков.")

    # Сохранение чанков в базу данных
    text_db = TextChunkDB()
    for chunk in chunks:
        if chunk["text"].strip():
            text_chunks = split_text_into_chunks(chunk["text"], chunk_size=500)
            for text_chunk in text_chunks:
                text_db.insert_chunk(text_chunk, source_file)

        # Сохранение текста из таблиц
        for table in chunk["tables"]:
            table_text = "\n".join(["\t".join(row) for row in table])  # Преобразование таблицы в текст
            table_chunks = split_text_into_chunks(table_text, chunk_size=500)
            for table_chunk in table_chunks:
                text_db.insert_chunk(table_chunk, source_file)

    text_db.close()

    # Создание эмбеддингов и сохранение в базу данных
    embedding_processor = EmbeddingProcessor()
    embeddings = embedding_processor.create_embeddings(chunks)

    embedding_db = EmbeddingDB()
    for embedding in embeddings:
        embedding_db.insert_embedding(embedding, source_file)
    embedding_db.close()


def main(excel_path=None, directory_path=None, column_index=3):
    num = 0
    start_time = time.time()

    # Обработка локальных файлов
    if directory_path:
        if not os.path.isdir(directory_path):
            print(f"Ошибка: директория {directory_path} не существует")
            return

        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith((".docx", ".html", ".pdf", ".djvu")):
                source_file = file_name
                try:
                    process_file(file_path, source_file)
                    num += 1
                except Exception as e:
                    print(f"Ошибка при обработке файла {file_name}: {e}")

    # Обработка ссылок из Excel
    if excel_path:
        load_links_from_excel(excel_path)
        process_links_from_excel(excel_path, column_index)

    end_time = time.time()
    print(f" Время обработки {end_time - start_time}")
    print(f"Обработано {num} файл(-ов)")


if __name__ == "__main__":
    directory_path = "C:/Users/user/Desktop/Parser_VostokovedAI/data"
    excel_path = "C:/Users/user/Desktop/Parser_VostokovedAI/links/tst.xlsx"
    main(excel_path, directory_path)
