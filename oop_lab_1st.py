import http.client
import json
import webbrowser
from urllib.parse import quote

class WikipediaSearcher: # класс для поиска в википедии
    def __init__(self, query):
        self.query = query # хранение запроса
        self.results = [] # хранение разультатов

    def search(self): # выполнене запроса к API и сохранение результатов
        conn = http.client.HTTPSConnection("en.wikipedia.org") # для безопасного соединия
        params = f"/w/api.php?action=query&list=search&srsearch={quote(self.query)}&format=json&utf8=1" # кодирует запрос, не оч понимаю как работает
      
        conn.request("GET", params) # запрос
        response = conn.getresponse() # ответ
        
        if response.status == 200:
            data = response.read()
            self.results = json.loads(data).get('query', {}).get('search', []) # парсинг
        else:
            print("Ошибка при выполнении запроса")

    def get_results(self): # возврат результатов поиска
        return self.results

class WikipediaInterface: # класс для консоли   
    def __init__(self):
        self.searcher = None

    def get_search_query(self): 
        return input("Введите поисковый запрос: ")

    def display_results(self, results): 
        if not results:
            print("Нет результатов для отображения")
            return
        
        print("Результаты поиска:")
        for index, result in enumerate(results):
            title = result['title']
            snippet = result['snippet']
            print(f"{index + 1}. {title} - {snippet}...")

    def open_article(self, results): # открытие статьи в браузере
        try:
            choice = int(input("Введите номер статьи для открытия (0 для выхода): "))
            if choice == 0:
                print("Выход из программы")
                return
            
            if 1 <= choice <= len(results):
                article_title = results[choice - 1]['title']
                url = f"https://en.wikipedia.org/wiki/{quote(article_title)}"
                webbrowser.open(url)
                print(f"Открываю статью: {article_title}")
            else:
                print("Некорректный номер статьи")
        except ValueError:
            print("Пожалуйста, введите номер статьи")

    def run(self): # основной цикл
        while True:
            query = self.get_search_query()
            if query.lower() == 'exit':
                print("Выход из программы")
                break
            
            self.searcher = WikipediaSearcher(query)
            self.searcher.search()
            results = self.searcher.get_results()
            self.display_results(results)
            self.open_article(results)

interface = WikipediaInterface()
interface.run()
