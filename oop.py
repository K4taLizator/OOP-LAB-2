import csv
import xml.etree.ElementTree as ET
from collections import defaultdict
import time


# Класс для загрузки данных из файлов CSV и XML
class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cities = []

    # Функция для чтения CSV файла
    def load_csv(self):
        try:
            with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')  # Используем точку с запятой как разделитель
                for row in reader:
                    self.cities.append(row)
        except Exception as e:
            print(f"Ошибка при чтении CSV файла: {e}")

    # Функция для чтения XML файла
    def load_xml(self):
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()

            # Чтение данных из атрибутов элементов <item>
            for item in root.findall('item'):
                city_data = {
                    'city': item.get('city', 'Unknown'),
                    'street': item.get('street', 'Unknown'),
                    'house': item.get('house', 'Unknown'),
                    'floor': item.get('floor', 'Unknown')
                }
                self.cities.append(city_data)
        except Exception as e:
            print(f"Ошибка при чтении XML файла: {e}")

    # Основная функция для загрузки данных
    def load_data(self):
        if self.file_path.lower().endswith('.csv'):
            self.load_csv()
        elif self.file_path.lower().endswith('.xml'):
            self.load_xml()
        else:
            print("Ошибка: поддерживаются только файлы CSV и XML.")


# Класс для анализа данных (поиск дубликатов и статистика по этажам)
class DataAnalyzer:
    def __init__(self, cities):
        self.cities = cities

    # Функция для поиска дублирующихся записей (город, улица, дом, этаж)
    def print_duplicates(self):
        duplicates = defaultdict(int)

        # Используем кортежи с полными данными для поиска дубликатов
        for city in self.cities:
            city_tuple = (city['city'], city['street'], city['house'], city['floor'])
            duplicates[city_tuple] += 1

        print("Дублирующиеся записи и их количество:")
        for city_tuple, count in duplicates.items():
            if count > 1:  # Только записи с повторениями
                city, street, house, floor = city_tuple
                print(f"{city}, {street}, дом {house}, этаж {floor}: {count} раз(а)")

    # Функция для статистики по этажам
    def floor_statistics(self):
        floor_counts = defaultdict(lambda: defaultdict(int))  # Словарь с подсчетом этажей для каждого города

        for city in self.cities:
            city_name = city['city']
            try:
                floor = int(city['floor'])  # Преобразуем этаж в целое число
                if floor >= 1 and floor <= 5:  # Учитываем только этажи от 1 до 5
                    floor_counts[city_name][floor] += 1
            except ValueError:
                pass  # Если не удалось преобразовать этаж в число, игнорируем

        print("\nСтатистика по этажам для каждого города:")
        for city, floors in floor_counts.items():
            print(f"\nГород: {city}")
            for floor, count in sorted(floors.items()):
                print(f"  {floor}-этажных зданий: {count}")


# Класс для основной логики программы
class MainProgram:
    def __init__(self):
        self.cities = []

    # Основная функция для работы с программой
    def run(self):
        while True:
            print("\nМеню:")
            print("1. Ввести путь к файлу")
            print("2. Выйти из программы")

            choice = input("Выберите действие (1 или 2): ").strip()

            if choice == '2':
                print("Завершаем программу...")
                break

            elif choice == '1':
                file_path = input("Введите путь к файлу (CSV или XML): ").strip()

                # Загружаем данные
                data_loader = DataLoader(file_path)
                start_read_time = time.time()
                data_loader.load_data()
                end_read_time = time.time()

                self.cities = data_loader.cities

                if not self.cities:
                    print("Ошибка: не удалось загрузить данные из файла.")
                    continue

                # Выполняем анализ данных
                data_analyzer = DataAnalyzer(self.cities)
                start_processing_time = time.time()
                data_analyzer.print_duplicates()
                data_analyzer.floor_statistics()
                end_processing_time = time.time()

                # Время на чтение файла
                print(f"\nВремя на чтение файла: {end_read_time - start_read_time:.2f} секунд")
                # Время на обработку данных
                print(f"Время на обработку данных: {end_processing_time - start_processing_time:.2f} секунд")

            else:
                print("Неверный выбор. Пожалуйста, выберите 1 или 2.")


# Запуск программы
if __name__ == '__main__':
    program = MainProgram()
    program.run()
