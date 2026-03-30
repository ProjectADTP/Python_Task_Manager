from task_manager import TaskManager

class Menu:
    def __init__(self, manager: TaskManager, filename: str) -> None:
        self.manager = manager
        self.filename = filename
        self._init_commands()

    def _init_commands(self):
        self.commands = {
            "1": (self._add_task, "Добавить задачу"),
            "2": (self._complete_task, "Отметить задачу выполненной"),
            "3": (self._remove_task, "Удалить задачу"),
            "4": (self._list_tasks, "Показать список задач"),
            "5": (self._save, "Сохранить в файл"),
            "6": (self._load, "Загрузить из файла"),
            "0": (self._exit, "Выход"),
        }

    def _add_task(self):
        self.manager.add_task(input("Введите описание задачи: "))
        return True

    def _complete_task(self):
        try:
            self.manager.complete_task(int(input("Введите индекс задачи: ")))
        except ValueError:
            print("Индекс должен быть числом!")
        return True

    def _remove_task(self):
        try:
            self.manager.remove_task(int(input("Введите индекс задачи: ")))
        except ValueError:
            print("Индекс должен быть числом!")
        return True

    def _list_tasks(self):
        self.manager.list_tasks()
        return True

    def _save(self):
        self.manager.save_to_json(self.filename)
        return True

    def _load(self):
        self.manager.load_from_json(self.filename)
        return True

    def _exit(self):
        self.manager.save_to_json(self.filename)
        print("\nРабота программы завершена!")
        return False

    def show(self):
        print("\nСписок задач:")

        for key, (_, description) in sorted(self.commands.items()):
            print(f"{key}. {description}")

    def execute_command(self, choice: str):
        if choice in self.commands:
            return self.commands[choice][0]()
        else:
            print("Неизвестная команда!")
            return True


def main():
    manager = TaskManager()
    filename = "test_tasks.json"

    manager.load_from_json(filename)

    menu = Menu(manager, filename)
    menu.show()

    running = True
    while running:
        running = menu.execute_command(input("\nВведите команду: "))


if __name__ == "__main__":
    main()