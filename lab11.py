import csv

# Зчитуємо дані з файлу
def read_csv(filename):
    data = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
        return []
    except IOError:
        print(f"Помилка: Не вдалося відкрити файл '{filename}'.")
        return []
    
# Уникаємо дублікатів, використовуючи словник для збереження останнього значення для кожної країни та року
def filter_by_range(data, lower_bound, upper_bound):
    filtered_data = {}
    for row in data:
        try:
            country = row['Country Name']
            year = row['Time']
            value = float(row['Value'])  # Отримуємо значення
            if lower_bound <= value <= upper_bound:
                # Якщо комбінація країни та року вже є в словнику, оновлюємо значення
                filtered_data[(country, year)] = row
        except ValueError:
            continue
    return list(filtered_data.values())  # Повертаємо лише унікальні значення

# Сортуємо дані за назвою країни
def sort_by_country(data):
    return sorted(data, key=lambda x: x['Country Name'])

# Записуємо результати пошуку у новий .csv файл
def write_csv(filename, data):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            # Вказуємо потрібні поля для запису
            fieldnames = ['Country Name', 'Time', 'Value']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Записуємо лише вибрані поля
            for row in data:
                filtered_row = {key: row[key] for key in fieldnames}  # Обираємо тільки потрібні ключі
                writer.writerow(filtered_row)
        print(f"Дані успішно записані в файл '{filename}'.")
    except IOError:
        print(f"Помилка: Не вдалося записати файл '{filename}'.")

# Головна функція
def main():
    input_file = 'lab11.csv'  # Назва файлу
    output_file = 'filtered_lab11_exports.csv'  # Файл для збереження результатів
    
    # Читаємо файл з даними
    data = read_csv(input_file)

    if not data:
        print("Помилка: Вхідний файл не містить даних або не був зчитаний.")
        return

    # Отримуємо діапазон від користувача
    lower_bound = float(input("Введіть нижню межу для значення: "))
    upper_bound = float(input("Введіть верхню межу для значення: "))

    # Фільтруємо дані
    filtered_data = filter_by_range(data, lower_bound, upper_bound)

    # Сортуємо за назвою країни
    sorted_data = sort_by_country(filtered_data)

    # Виводимо на екран результати фільтрації
    if sorted_data:
        print(f"Країни, які відповідають діапазону від {lower_bound} до {upper_bound} (в алфавітному порядку):")
        for row in sorted_data:
            print(row['Country Name'], row['Time'], row['Value'])
    else:
        print(f"Немає країн, які відповідають діапазону від {lower_bound} до {upper_bound}.")

    # Записуємо результат у новий .csv файл
    write_csv(output_file, sorted_data)

if __name__ == "__main__":
    main()
