import sys


def parse_log_line(line):
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(line)
    date, time, level, message = parts
    return {"date": date, "time": time, "level": level.upper(), "message": message}


def load_logs(file_path):
    logs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError:
                continue
    return logs


def filter_logs_by_level(logs, level):
    level = level.upper()
    return list(filter(lambda log: log["level"] == level, logs))


def count_logs_by_level(logs):
    counts = {}
    for log in logs:
        level = log["level"]
        if level in counts:
            counts[level] += 1
        else:
            counts[level] = 1
    return counts


def display_log_counts(counts):
    print("Рівень логу | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def main():
    if len(sys.argv) < 2:
        print("Треба шлях до лог-файлу: python task_3.py logfile.log [рівень]")
        return

    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
        return
    except OSError as e:
        print(f"Не вдалось прочитати файл: {e}")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_filter:
        filtered = filter_logs_by_level(logs, level_filter)
        print(f"\nДеталі логів для рівня '{level_filter.upper()}':")
        for log in filtered:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()
