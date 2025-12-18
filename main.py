import flet as ft
from datetime import datetime
from database import init_db, add_task, get_tasks, delete_task

def main(page: ft.Page):
    page.title = "ToDo App"
    page.window_width = 400
    page.window_height = 600

    init_db()

    task_input = ft.TextField(label="Новая задача", width=300)
    warning_text = ft.Text("", color=ft.Colors.RED)
    tasks_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    def load_tasks():
        """Обновление списка задач"""
        tasks_column.controls.clear()
        for task_id, task_text, created_at, completed in get_tasks():
            task_row = ft.Row(
                [
                    ft.Text(f"{created_at} - {task_text}", expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Удалить",
                        on_click=lambda e, id=task_id: remove_task(id)
                    )
                ]
            )
            tasks_column.controls.append(task_row)
        page.update()

    def add_new_task(e):
        task = task_input.value.strip()
        if not task:
            warning_text.value = "Задача не может быть пустой"
            page.update()
            return
        if len(task) > 100:
            warning_text.value = "Задача не может быть длиннее 100 символов"
            page.update()
            return
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_task(task, created_at)
        task_input.value = ""
        warning_text.value = ""
        load_tasks()

    def remove_task(task_id):
        delete_task(task_id)
        load_tasks()

    add_btn = ft.ElevatedButton("Добавить", on_click=add_new_task)

    page.add(
        ft.Text("📌 Мои задачи", size=22, weight=ft.FontWeight.BOLD),
        task_input,
        warning_text,
        add_btn,
        ft.Divider(),
        tasks_column
    )

    load_tasks()

ft.app(target=main)