import csv
import xml.etree.ElementTree as ET
from collections import defaultdict
import time


# Функция для чтения CSV файла
def load_csv(file_path):
    cities = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')  # Используем точку с запятой как разделитель
            for row in reader:
                cities.append(row)
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
    return cities


# Функция для чтения XML файла
def load_xml(file_path):
    cities = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Чтение данных из атрибутов элементов <item>
        for item in root.findall('item'):
            try:
                city_data = {
                    'city': item.get('city', 'Unknown'),
                    'street': item.get('street', 'Unknown'),
                    'house': item.get('house', 'Unknown'),
                    'floor': item.get('floor', 'Unknown')
                }
                cities.append(city_data)
            except Exception as e:
                print(f"Ошибка при обработке элемента: {e}")
    except Exception as e:
        print(f"Ошибка при чтении XML файла: {e}")
    return cities


# Функция для поиска дублирующихся записей (город, улица, дом, этаж)
def print_duplicates(cities):
    duplicates = defaultdict(int)

    # Используем кортежи с полными данными для поиска дубликатов
    for city in cities:
        city_tuple = (city['city'], city['street'], city['house'], city['floor'])
        duplicates[city_tuple] += 1

    print("Дублирующиеся записи и их количество:")
    for city_tuple, count in duplicates.items():
        if count > 1:  # Только записи с повторениями
            city, street, house, floor = city_tuple
            print(f"{city}, {street}, дом {house}, этаж {floor}: {count} раз(а)")


# Функция для статистики по этажам
def floor_statistics(cities):
    floor_counts = defaultdict(lambda: defaultdict(int))  # Словарь с подсчетом этажей для каждого города

    for city in cities:
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


# Основная функция, которая будет отображать меню
def main():
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

            if file_path.lower().endswith('.csv'):
                # Измеряем время на чтение CSV файла
                start_read_time = time.time()
                cities = load_csv(file_path)
                end_read_time = time.time()
            elif file_path.lower().endswith('.xml'):
                # Измеряем время на чтение XML файла
                start_read_time = time.time()
                cities = load_xml(file_path)
                end_read_time = time.time()
            else:
                print("Ошибка: поддерживаются только файлы CSV и XML.")
                continue

            if not cities:
                print("Ошибка: не удалось загрузить данные из файла.")
                continue

            # Вывод статистики
            start_processing_time = time.time()
            print_duplicates(cities)
            floor_statistics(cities)
            end_processing_time = time.time()

            # Время на чтение файла
            print(f"\nВремя на чтение файла: {end_read_time - start_read_time:.2f} секунд")
            # Время на обработку данных
            print(f"Время на обработку данных: {end_processing_time - start_processing_time:.2f} секунд")

        else:
            print("Неверный выбор. Пожалуйста, выберите 1 или 2.")


# Запуск программы
if __name__ == '__main__':
    main()
