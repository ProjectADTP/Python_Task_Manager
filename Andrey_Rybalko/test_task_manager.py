import pytest
import json
import os
from task_manager import TaskManager


@pytest.fixture
def task_manager():
    return TaskManager()


@pytest.fixture
def temp_json_file():
    return "test_tasks.json"


def test_add_and_complete_task(task_manager):
    result = task_manager.add_task("Купить продукты")
    assert result, "Задача должна добавиться успешно"

    assert task_manager.get_task_count() == 1, "Должна быть 1 задача"

    tasks = task_manager.get_tasks()
    assert tasks[1].description == "Купить продукты"
    assert not tasks[1].completed, "Задача должна быть невыполненной"

    result = task_manager.complete_task(0)
    assert result, "Задача должна выполниться успешно"

    tasks = task_manager.get_tasks()
    assert tasks[1].completed, "Задача должна быть выполненной"


def test_remove_task(task_manager):
    task_manager.add_task("Задача 1")
    task_manager.add_task("Задача 2")
    task_manager.add_task("Задача 3")

    assert task_manager.get_task_count() == 3, "Должно быть 3 задачи"

    assert task_manager.remove_task(2), "Удаление должно быть успешным"
    assert not task_manager.complete_task(2), "Попытка выполнить несуществующую задачу должна вернуть False"

    assert task_manager.get_task_count() == 2, "Должно остаться 2 задачи"

    tasks = task_manager.get_tasks()
    assert tasks[1].description == "Задача 1"
    assert tasks[3].description == "Задача 3"

    assert not task_manager.remove_task(10), "Удаление несуществующей задачи должно вернуть False"


def test_save_and_load_json(task_manager, temp_json_file):
    task_manager.add_task("Задача 1")
    task_manager.add_task("Задача 2")
    task_manager.complete_task(1)

    assert task_manager.save_to_json(temp_json_file), "Сохранение должно быть успешным"

    assert os.path.exists(temp_json_file), "Файл должен существовать"

    with open(temp_json_file, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert len(saved_data) == 2, "В файле должно быть 2 задачи"
    assert saved_data["1"]["description"] == "Задача 1"
    assert saved_data["1"]["completed"]
    assert saved_data["2"]["description"] == "Задача 2"
    assert not saved_data["2"]["completed"]

    new_manager = TaskManager()
    assert new_manager.load_from_json(temp_json_file) is True, "Загрузка должна быть успешной"

    assert new_manager.get_task_count() == 2, "Должно быть 2 задачи"
    tasks = new_manager.get_tasks()
    assert tasks["1"]["description"] == "Задача 1"
    assert tasks["1"]["completed"], "Задача должна быть выполненной"
    assert tasks["2"]["description"] == "Задача 2"
    assert not tasks["2"]["completed"], "Задача должна быть невыполненной"