from PIL import Image
import io

def process_image(document):
    images = []
    for rel in document.part.rels.values():
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob  # Получаем бинарные данные изображения
            try:
                image = Image.open(io.BytesIO(image_data))  # Преобразуем данные в объект изображения
                images.append(image)
            except Exception as e:
                print(f"Ошибка при обработке изображения: {e}")
    return images