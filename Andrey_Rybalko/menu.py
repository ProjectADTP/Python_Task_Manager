from task_manager import TaskManager


def show_menu():
    print("\nСписок команд:")
    print("1. Добавить задачу")
    print("2. Отметить задачу выполненной")
    print("3. Удалить задачу")
    print("4. Показать список задач")
    print("5. Сохранить в файл")
    print("6. Загрузить из файла")
    print("0. Выход\n")


def get_user_input():
    return input("Выберите команду (0-6): ")


def main():
    manager = TaskManager()
    filename = "test_tasks.json"

    manager.load_from_json(filename)

    while True:
        show_menu()
        user_input = get_user_input()

        match user_input:
            case "1":
                manager.add_task(input("Введите описание задачи: "))

            case "2":
                try:
                    manager.complete_task(int(input("Введите индекс задачи: ")))
                except ValueError:
                    print("Индекс должен быть числом!")

            case "3":
                try:
                    manager.remove_task(int(input("Введите индекс задачи: ")))
                except ValueError:
                    print("Индекс должен быть числом!")

            case "4":
                manager.list_tasks()

            case "5":
                manager.save_to_json(filename)

            case "6":
                manager.load_from_json(filename)

            case "0":
                manager.save_to_json(filename)
                print("До свидания!")
                break

            case _:
                print("Неизвестная команда!")


if __name__ == "__main__":
    main()