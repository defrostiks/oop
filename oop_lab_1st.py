import http.client
import json
import webbrowser
from urllib.parse import quote

class WikipediaSearch: # класс для поиска в википедии
    def __init__(self, query):
        self.query = query # хранение запроса
        self.results = [] # хранение разультатов

    def search(self): # выполнене запроса к API и сохранение результатов
        conn = http.client.HTTPSConnection("en.wikipedia.org") # для безопасного соединия
        params = f"/w/api.php?action=query&list=search&srsearch={quote(self.query)}&format=json&utf8=1" 
      
        conn.request("GET", params) # запрос
        response = conn.getresponse() # ответ
        
        if response.status == 200:
            data = response.read()
            parser = WikipediaParser()
            self.results = parser.parse(data) # парсинг
        else:
            print("Ошибка при выполнении запроса")

    def get_results(self): # возврат результатов поиска
        return self.results

class WikipediaParser: #парсинг
    def parse(self, data):
        parsed_data = json.loads(data)
        return parsed_data.get('query', {}).get('search', [])
    
class PageOpen: # открытие статьи
    def open_page(title):
        url = f"https://en.wikipedia.org/wiki/{quote(title)}"
        webbrowser.open(url)
        print("Открываю статью:", title)

class UserInputProcessing:  # класс обработки пользовательского ввода
    def get_search_query(self): 
        return input("Введите поисковый запрос: ")

    def get_article_choice(self, max_choice):
        while True:
            try:
                choice = int(input("Введите номер статьи для открытия (0 для выхода): "))
                if choice == 0:
                    return choice
                if 1 <= choice <= max_choice:
                    return choice
                else:
                    print("Некорректный номер статьи. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите номер статьи.")


class WorkConsole: # класс для консоли   
    def __init__(self):
        self.searcher = None
        self.input_handler = UserInputProcessing()

    def display_results(self, results): 
        if not results:
            print("Нет результатов для отображения")
            return
        
        print("Результаты поиска:")
        for index, result in enumerate(results):
            title = result['title']
            print(index + 1, title)

    def open_article(self, results): # открытие статьи в браузере
        choice = self.input_handler.get_article_choice(len(results))
        if choice == 0:
            print("Выход из программы")
            return
        
        article_title = results[choice - 1]['title']
        PageOpen.open_page(article_title)

    def run(self): # основной цикл
        while True:
            query = self.input_handler.get_search_query()
            if query.lower() == 'exit':
                print("Выход из программы")
                break
            
            self.searcher = WikipediaSearch(query)
            self.searcher.search()
            results = self.searcher.get_results()
            self.display_results(results)
            self.open_article(results)

work = WorkConsole()
work.run()
