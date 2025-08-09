import sys
from typing import Union, Tuple

def parse_log_line(line: str) -> dict:
    # Розбиваємо рядок логу на дату, час, рівень логування та повідомлення (обмеження 3 пробілами)
    date, time, level, message = line.split(" ", 3)
    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message.strip(),  # Обрізаємо зайві пробіли на початку і в кінці повідомлення
    }

def load_logs(file_path: str) -> list:
    logs_list = []
    try:
        # Відкриваємо файл у текстовому режимі з кодуванням UTF-8
        with open(file=file_path, mode="r", encoding="UTF-8") as file:
            lines = file.readlines()  # Зчитуємо всі рядки з файлу
            for line in lines:
                logs_list.append(parse_log_line(line))  # Парсимо кожен рядок і додаємо до списку
        return logs_list
    except FileNotFoundError:
        print("ПОМИЛКА: Файл не знайдено")
        sys.exit(1)
    except (IOError, OSError):
        print("ПОМИЛКА: Помилка при зчитуванні файлу")
        sys.exit(1)
    except UnicodeDecodeError:
        print("ПОМИЛКА: Файл не є текстовим або має некоректне кодування")
        sys.exit(1)

def filter_logs_by_level(logs: list, level: str) -> list:
    filtered_logs = []
    # Фільтруємо логи, залишаючи тільки ті, що відповідають заданому рівню
    for log in logs:
        if log["level"] == level:
            filtered_logs.append(log)
    return filtered_logs

def count_logs_by_level(logs: list) -> dict:
    # Ініціалізуємо словник лічильників за рівнями логування
    levels_count = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "DEBUG": 0
    }

    # Рахуємо кількість логів для кожного рівня
    for log in logs:
        levels_count[log["level"]] += 1

    # Сортуємо результати за спаданням кількості логів
    sorted_levels = dict(sorted(levels_count.items(), key=lambda item: item[1], reverse=True))

    return sorted_levels

def display_log_counts(counts: dict):
    # Виводимо підрахунок логів по рівнях у вигляді таблиці
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16} | {count:>9}")
    print("\n")

def display_filtered_logs(logs: list, level: str):
    # Виводимо деталі логів певного рівня
    print(f"Деталі логів для рівня '{level}':")
    for log in logs:
        print(f"{log['date']} {log['time']} {log['message']}")

def get_user_input() -> Union[Tuple[str, None], Tuple[str, str]]:
    try:
        # Пробуємо взяти шлях до файлу з аргументів командного рядка
        file_path = sys.argv[1]
    except IndexError:
        print("ПОМИЛКА: Не передано шлях до лог файлу")
        sys.exit(1)

    # Якщо рівень не переданий, повертаємо шлях і None
    if len(sys.argv) < 3:
        return file_path, None

    # Якщо рівень переданий, переводимо його у верхній регістр і повертаємо разом з шляхом
    level = sys.argv[2].upper()

    return file_path, level

def main():
    # Отримуємо шлях до файлу і (за бажанням) рівень логування
    file_path, level = get_user_input()
    # Завантажуємо логи з файлу
    logs = load_logs(file_path)
    # Рахуємо кількість логів по кожному рівню
    count_logs = count_logs_by_level(logs)
    # Виводимо загальну статистику
    display_log_counts(count_logs)

    # Якщо задано рівень, фільтруємо логи та виводимо їх деталі
    if level:
        filtered_logs = filter_logs_by_level(logs, level)
        display_filtered_logs(filtered_logs, level)

if __name__ == "__main__":
    main()
