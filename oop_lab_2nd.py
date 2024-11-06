from collections import defaultdict, Counter
import csv
import time

class Building: #класс для здания
    def __init__(self, city, street, house, floors):
        self.city = city
        self.street = street
        self.house = house
        self.floors = floors
    
    def __hash__(self): #чтобы объекты могли быть ключами
        return hash((self.city, self.street, self.house))
    
    def __eq__(self, other): #без этой штуки мы не можем сравнивать
        return (self.city, self.street, self.house) == (other.city, other.street, other.house)

class Anailysys: #класс для анализа
    def __init__(self):
        self.house_floor_count = defaultdict(int) #кол-во этажей в здании
        self.duplicate = Counter() #дублирующиеся записи
        self.city_floor_count = defaultdict(lambda: defaultdict(int)) #кол-во зданий по этажам в городе
        self.skipped_lines = 0 #пропущенные строки
        self.count_lines = 0 #счётчик строк

    def csv_processing(self, name): #обработка файла csv
        try:
            with open(name, mode='r', encoding='utf-8') as file:
                read_lines = csv.reader(file, delimiter=';')
                next(read_lines)

                for lines in read_lines: #обработка строк
                    self.count_lines += 1

                    if len(lines) < 4: #подсчёт некорректнных строк
                        self.skipped_lines += 1
                        continue
                    
                    city = lines[0].strip()
                    street = lines[1].strip()
                    house = lines[2].strip()
                    floors = int(lines[3].strip())

                    building = Building(city, street, house, floors)
                    self.house_floor_count[building] += floors #прибавляем кол-во этажей задния
                    self.duplicate[building] += 1 #увеличиваем счётчик дубликатов
                    self.city_floor_count[city][floors] += 1 #увеличиваем счётчик зданий с конкретным кол-вом этажей

            self.print_results()

        except FileNotFoundError:
            print('Файл не найден')

    def print_results(self): #вывод результатов
        print("Обработано строк: ", self.count_lines, ", Пропущено строк: ", self.skipped_lines)

        print("\nДублирующиеся записи: ")
        for building, count in self.duplicate.items():
            if count > 1:
                print(building.city, ",", building.street, ",", building.house, ": ", count, "раз(а)")

        print("\nКоличество зданий в каждом городе по этажам:") 
        for city, floors in self.city_floor_count.items():
            print(city, ": ")
            for floor_count in range(1,6):
                print(floor_count, " этаж(ей): ", floors[floor_count])

anailysys = Anailysys()
while True:
    input_text = input("Введите путь до файла CSV (или 'exit' для выхода): ")

    if input_text.lower() == 'exit':
        break

    start_time = time.time()
    anailysys.csv_processing(input_text)
    finish_time = time.time() - start_time
    print("\nВремя обработки файла: ", finish_time, " секунд\n")













