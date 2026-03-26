import json, os


class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, description: str):
        if not isinstance(description, str) or not description.strip():
            print("Описание задачи не может быть пустым!")
            return False

        self.tasks[self._get_next_id()] = Task(description)
        print(f"Добавлена новая задача - \"{description}\"")
        return True

    def _get_next_id(self):
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def complete_task(self, index: int):
        if self.is_valid_index(index):
            if self.tasks[index].completed:
                print("Задача уже выполнена")
                return False
            self.tasks[index].completed = True
            return True
        print("Задачи с таким индексом нету")
        return False

    def remove_task(self, index: int):
        if self.is_valid_index(index):
            task_description = self.tasks[index].description
            del self.tasks[index]
            print(f"\nЗадача \"{task_description}\" удалена")
            return True
        print("Задачи с таким индексом нету")
        return False


    def save_to_json(self, filename: str):
        try:
            data = {
                task_id: task.to_dict() for task_id, task in self.tasks.items()
            }

            with open(filename, "w", encoding="UTF-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Задачи сохранены в файл: {filename}")
            return True
        except Exception as exception:
            print(f"Ошибка сохранения: {exception}")
            return False

    def load_from_json(self, filename: str):
        if not os.path.exists(filename):
            print(f"Файл не найден: {filename}")
            return False

        try:
            with open(filename, "r", encoding="utf-8") as file:
                self.tasks = json.load(file)
            print(f"Задачи загружены из файла: {filename}")
            return True
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON: {filename}")
            return False
        except Exception as exception:
            print(f" Ошибка загрузки: {exception}")
            return False

    def list_tasks(self):
        print("Список задач:")

        if not self.tasks:
            print("Список задач пуст!")
        else:
            for i, task in self.tasks:
                print(f"{i}. {task}")

    def get_task_count(self):
        return len(self.tasks)

    def get_tasks(self):
        return self.tasks.copy()

    def is_valid_index(self, index: int):
        return isinstance(index, int) and index in self.tasks.keys()


class Task:
    def __init__(self, description: str, is_completed: bool = False):
        self.description = description.strip()
        self.completed = is_completed

    def to_dict(self):
        return {
            "description": self.description,
            "completed": self.completed
        }

    def __str__(self):
        return f"{self.description} [{"Выполнена" if self.completed else "Не выполнена"}] "