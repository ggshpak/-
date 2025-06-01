def show_menu():
    print("\n==== МЕНЮ СИСТЕМЫ УЧЁТА ВИДЕОКАССЕТ ====")
    print("1. Показать список видеокассет")
    print("2. Выдать кассету")
    print("3. Показать информацию о клиентах с кассетами")
    print("4. Вернуть кассету")
    print("5. Добавить новую кассету")
    print("6. Показать кассеты в ремонте/на списании")
    print("7. Вернуть кассету из ремонта в коллекцию")
    print("8. Выход")


def list_cassettes(cassettes, status_filter=None):
    print("\nДоступные видеокассеты:")
    filtered = [(title, info) for title, info in cassettes.items() 
               if status_filter is None or info['status'] == status_filter]
    
    if not filtered:
        print("Нет кассет для отображения.")
        return False
    
    for i, (title, info) in enumerate(filtered, 1):
        if info['status'] == 'available':
            status = "Доступна"
        elif info['status'] == 'rented':
            status = f"У клиента: {info['client']}"
        elif info['status'] == 'repair':
            status = "В ремонте"
        print(f"{i}. {title} ({status})")
    return True


def rent_cassette(cassettes):
    if not list_cassettes(cassettes, 'available'):
        return
    
    try:
        choice = int(input("Выберите номер кассеты: ")) - 1
        available_cassettes = [title for title, info in cassettes.items() 
                             if info['status'] == 'available']
        
        if choice < 0 or choice >= len(available_cassettes):
            print("Неверный номер кассеты.")
            return
        
        title = available_cassettes[choice]
        client = input("Введите имя клиента: ").strip()
        if not client:
            print("Имя клиента не может быть пустым.")
            return
            
        cassettes[title]['status'] = 'rented'
        cassettes[title]['client'] = client
        print(f"Кассета '{title}' выдана клиенту {client}")
    except ValueError:
        print("Введите число.")


def show_rented(cassettes):
    print("\nИнформация о арендованных кассетах:")
    rented = [(title, info['client']) 
             for title, info in cassettes.items() 
             if info['status'] == 'rented']
    
    if not rented:
        print("Нет арендованных кассет.")
        return False
    
    for i, (title, client) in enumerate(rented, 1):
        print(f"{i}. Кассета '{title}' у клиента: {client}")
    return True


def return_cassette(cassettes):
    if not show_rented(cassettes):
        return
    
    try:
        choice = int(input("Выберите номер кассеты для возврата: ")) - 1
        rented = [title for title, info in cassettes.items() 
                 if info['status'] == 'rented']
        
        if choice < 0 or choice >= len(rented):
            print("Неверный номер кассеты.")
            return
            
        title = rented[choice]
        client = cassettes[title]['client']
        
        while True:
            condition = input("Кассета исправна? (да/нет): ").strip().lower()
            if condition == 'да':
                cassettes[title]['status'] = 'available'
                cassettes[title]['client'] = None
                print(f"Кассета '{title}' возвращена от клиента {client} и доступна для выдачи")
                break
            elif condition == 'нет':
                cassettes[title]['status'] = 'repair'
                cassettes[title]['client'] = None
                print(f"Кассета '{title}' помещена в ремонт/на списание")
                break
            else:
                print("Пожалуйста, введите 'да' или 'нет'")
    except ValueError:
        print("Введите число.")


def add_cassette(cassettes):
    title = input("Введите название новой кассеты: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    
    if title in cassettes:
        print("Кассета с таким названием уже существует.")
        return
    
    cassettes[title] = {
        'status': 'available',
        'client': None
    }
    print(f"Кассета '{title}' успешно добавлена в коллекцию.")


def show_repair_list(cassettes):
    print("\nКассеты в ремонте/на списании:")
    repair_list = [title for title, info in cassettes.items() 
                  if info['status'] == 'repair']
    
    if not repair_list:
        print("Нет кассет в ремонте/на списании.")
        return False
    
    for i, title in enumerate(repair_list, 1):
        print(f"{i}. {title}")
    return True


def return_from_repair(cassettes):
    if not show_repair_list(cassettes):
        return
    
    try:
        choice = int(input("Выберите номер кассеты для возврата в коллекцию: ")) - 1
        repair_list = [title for title, info in cassettes.items() 
                      if info['status'] == 'repair']
        
        if choice < 0 or choice >= len(repair_list):
            print("Неверный номер кассеты.")
            return
            
        title = repair_list[choice]
        cassettes[title]['status'] = 'available'
        print(f"Кассета '{title}' возвращена в коллекцию и доступна для выдачи")
    except ValueError:
        print("Введите число.")


def main():
    cassettes = {
        "Крестный отец": {"status": "available", "client": None},
        "Терминатор 2": {"status": "available", "client": None},
        "Форрест Гамп": {"status": "available", "client": None},
        "Матрица": {"status": "available", "client": None},
        "Побег из Шоушенко": {"status": "available", "client": None}
    }

    while True:
        show_menu()
        choice = input("Выберите действие: ")
        if choice == "1":
            list_cassettes(cassettes)
        elif choice == "2":
            rent_cassette(cassettes)
        elif choice == "3":
            show_rented(cassettes)
        elif choice == "4":
            return_cassette(cassettes)
        elif choice == "5":
            add_cassette(cassettes)
        elif choice == "6":
            show_repair_list(cassettes)
        elif choice == "7":
            return_from_repair(cassettes)
        elif choice == "8":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 1 до 8.")


if __name__ == "__main__":
    main()
