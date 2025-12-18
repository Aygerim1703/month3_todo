import sqlite3
from config import path_db

MAX_TASK_LENGTH = 100


CREATE_TABLE_TASK = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    created_at TEXT NOT NULL,
    completed INTEGER DEFAULT 0
);
"""

INSERT_TASK = "INSERT INTO tasks (task, created_at) VALUES (?, ?);"
SELECT_TASK = "SELECT id, task, created_at, completed FROM tasks;"
DELETE_TASK = "DELETE FROM tasks WHERE id = ?;"
UPDATE_TASK = "UPDATE tasks SET task = ?, completed = ? WHERE id = ?;"



def init_db():
    """Создание таблицы задач"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_TASK)
    conn.commit()
    conn.close()


def add_task(task, created_at):
    """Добавление новой задачи"""
    if not task:
        raise ValueError("Задача не может быть пустой")
    if len(task) > MAX_TASK_LENGTH:
        raise ValueError("Задача не может быть длиннее 100 символов")

    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(INSERT_TASK, (task, created_at))
    conn.commit()
    conn.close()


def get_tasks():
    """Получение всех задач"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(SELECT_TASK)
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(task_id, new_task=None, completed=None):
    """Обновление задачи"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if new_task is not None:
        if len(new_task) > MAX_TASK_LENGTH:
            raise ValueError("Задача не может быть длиннее 100 символов")
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))

    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    """Удаление задачи"""
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()