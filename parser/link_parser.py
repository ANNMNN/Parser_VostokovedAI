import re
import requests
from bs4 import BeautifulSoup


class ArticleParser:
    def __init__(self, url):
        self.url = url
        self.html = None
        self.soup = None

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            response.encoding = 'utf-8'  # Устанавливаем кодировку
            self.html = response.text
            self.soup = BeautifulSoup(self.html, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return None


    def clean_html(self):
        if not self.soup:
            print("HTML не загружен.")
            return None

        # Удаление ненужных тегов
        for tag in self.soup(["script", "style", "meta", "link", "footer", "header", "nav", "aside"]):
            tag.decompose()

        comments = self.soup.find_all(string=lambda text: isinstance(text, str) and text.startswith("<!--"))
        for comment in comments:
            comment.extract()

    def extract_main_text(self):
        if not self.soup:
            print("HTML не обработан.")
            return None

        # Для китайских сайтов обычно нет тэга article
        article = self.soup.find("article")
        if article:
            return self.clean_text(article.get_text(separator=" "))

        # Попытка найти основной контент через параграфы (для китайских сайтов это более универсально)
        paragraphs = self.soup.find_all("p")
        main_content = " ".join(p.get_text(separator=" ") for p in paragraphs)

        # Убираем ненужные пробелы
        return self.clean_text(main_content)

    def clean_text(self, text):
        # Убираем лишние пробелы и символы
        text = re.sub(r"\s+", " ", text.strip())
        return text

    def parse(self):
        self.fetch_html()
        self.clean_html()
        return self.extract_main_text()
