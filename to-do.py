from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning, showerror
import json
import os

name_file = 'To-Do.json'

def load_tasks():
    if os.path.exists(name_file):
        with open(name_file, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    try:
        with open(name_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except PermissionError:
        showerror('Ошибка', 'Нет прав для записи в файл.')
    except Exception as e:
        showerror('Ошибка', f'Не удалось сохранить задачи: {str(e)}')

def refresh_list():
    task_listbox.delete(0, END)
    for task in tasks:
        task_listbox.insert(END, f"{task['task']}")

def add_task():
    task = task_entry.get()
    if task:
        tasks.append({"task": task})
        save_tasks(tasks)
        refresh_list()
        task_entry.delete(0, END)
        task_entry.focus()
    else:
        showwarning('Пустая задача', 'Введите текст задачи.')

def delete_task():
    selection = task_listbox.curselection()
    if not selection:
        showwarning('Не выбрана задача', 'Выберите задачу для удаления.')
        return
    try:
        for index in reversed(selection):
            del tasks[index]
        save_tasks(tasks)
        refresh_list()
    except Exception as e:
        showerror('Ошибка', f'Произошла ошибка при удалении: {str(e)}')


root = Tk()
root.title('To-Do list')
root.geometry('300x285')
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_width()) // 2
y = (root.winfo_screenheight() - root.winfo_height()) // 2
root.geometry(f"+{x}+{y}")
root.columnconfigure(index=0, weight=4)
root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=3)
root.rowconfigure(index=2, weight=1)
root.rowconfigure(index=3, weight=1)

tasks = load_tasks()

ttk.Label(text='Введите задачу:', font=('Arial', 14)).grid(column=0, row=0, padx=5, pady=5, sticky=EW)

task_entry = ttk.Entry()
task_entry.bind('<Return>', lambda e: add_task())
task_entry.grid(column=0, row=1, padx=6, pady=6, sticky=EW)
ttk.Button(text='Добавить', command=add_task).grid(column=1, row=1, padx=6, pady=6)

task_listbox = Listbox(selectmode=MULTIPLE)
task_listbox.grid(row=2, column=0, columnspan=2, sticky=EW, padx=5, pady=5)

ttk.Button(text='Удалить', command=delete_task).grid(row=3, column=1, padx=5, pady=5)

refresh_list()

root.mainloop()