import pytest
import os
from task_manager import TaskManager


@pytest.fixture
def task_manager():
    manager = TaskManager()
    yield manager
    manager.tasks.clear()


@pytest.fixture
def temp_json_file():
    file_path = "test_tasks.json"
    yield str(file_path)


class TestAddTask:
    def test_add_single_task(self, task_manager):
        result = task_manager.add_task("Купить продукты")

        assert result, "Задача должна добавиться успешно"
        assert task_manager.get_task_count() == 1

    def test_add_empty_description(self, task_manager):
        result = task_manager.add_task("")

        assert not result, "Задача должна быть невыполненной"
        assert task_manager.get_task_count() == 0


class TestCompleteTask:
    def test_complete_existing_task(self, task_manager):
        task_manager.add_task("Задача 1")
        result = task_manager.complete_task(0)

        assert result, "Задача должна выполниться успешно"
        assert task_manager.get_tasks()[0].completed, "Задача должна быть выполненной"

    def test_complete_nonexistent_task(self, task_manager):
        result = task_manager.complete_task(999)

        assert not result, "Задачи не должно существовать"


class TestRemoveTask:
    def test_remove_existing_task(self, task_manager):
        task_manager.add_task("Задача 1")
        task_manager.add_task("Задача 2")

        result = task_manager.remove_task(0)

        assert result, "Задача должна удалиться успешно"
        assert task_manager.get_task_count() == 1, "В списке должна остаться одна задача"

    def test_remove_nonexistent_task(self, task_manager):
        result = task_manager.remove_task(999)

        assert not result, "Задачи не должно существовать"


class TestSaveLoadJson:
    def test_save_to_json(self, task_manager, temp_json_file):
        task_manager.add_task("Задача 1")

        result = task_manager.save_to_json(temp_json_file)

        assert result, "Сохранение должно быть успешным"
        assert os.path.exists(temp_json_file), "Файл должен существовать"

    def test_load_from_json(self, task_manager, temp_json_file):
        task_manager.add_task("Задача 1")
        task_manager.save_to_json(temp_json_file)

        new_manager = TaskManager()
        result = new_manager.load_from_json(temp_json_file)

        assert result, "Загрузка должна быть успешной"
        assert new_manager.get_task_count() == 1, "В списке должна быть одна задача"

    def test_load_from_nonexistent_file(self, task_manager):
        result = task_manager.load_from_json("nonexistent.json")

        assert not result, "Нельзя загрузить данные с файла которого нет"

    def test_save_load_preserves_data(self, task_manager, temp_json_file):
        task_manager.add_task("Задача 1")
        task_manager.complete_task(0)
        task_manager.save_to_json(temp_json_file)

        new_manager = TaskManager()
        new_manager.load_from_json(temp_json_file)

        tasks = new_manager.get_tasks()
        assert tasks["0"]["description"] == "Задача 1", "Задача должна иметь описание: \"Задача 1\""
        assert tasks["0"]["completed"], "Задача должна быть выполненной"