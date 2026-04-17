import requests
import json
import os
import tkinter as tk
from tkinter import messagebox

FILE_NAME = "groups.json"


def get_currencies():
    try:
        data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
        return data["Valute"]
    except:
        messagebox.showerror("Ошибка", "Не удалось загрузить данные")
        return {}


def load_groups():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_groups():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=4, ensure_ascii=False)


def create_group():
    name = group_entry.get()
    if not name:
        return

    if name in groups:
        messagebox.showinfo("Ошибка", "Группа уже есть")
    else:
        groups[name] = []
        save_groups()
        update_groups_list()


def add_to_group():
    name = group_entry.get()
    code = currency_entry.get().upper()

    if name not in groups:
        messagebox.showinfo("Ошибка", "Группа не найдена")
        return

    if code not in currencies:
        messagebox.showinfo("Ошибка", "Валюта не найдена")
        return

    if code not in groups[name]:
        groups[name].append(code)
        save_groups()
        messagebox.showinfo("OK", "Добавлено")


def remove_from_group():
    name = group_entry.get()
    code = currency_entry.get().upper()

    if name not in groups:
        messagebox.showinfo("Ошибка", "Группа не найдена")
        return

    if code in groups[name]:
        groups[name].remove(code)
        save_groups()
        messagebox.showinfo("OK", "Удалено")
    else:
        messagebox.showinfo("Ошибка", "Нет такой валюты в группе")


def show_group():
    name = group_entry.get()
    text.delete(1.0, tk.END)

    if name not in groups:
        text.insert(tk.END, "Группа не найдена")
        return

    if not groups[name]:
        text.insert(tk.END, "Группа пустая")
        return

    for code in groups[name]:
        if code in currencies:
            info = currencies[code]
            text.insert(tk.END, f"{code}: {info['Value']} RUB\n")


def update_groups_list():
    listbox.delete(0, tk.END)
    for g in groups:
        listbox.insert(tk.END, g)


def select_group(event):
    selection = listbox.curselection()
    if selection:
        group_entry.delete(0, tk.END)
        group_entry.insert(0, listbox.get(selection))


def show_all():
    text.delete(1.0, tk.END)
    for code, info in currencies.items():
        text.insert(tk.END, f"{code}: {info['Value']} RUB\n")


def find_currency():
    code = currency_entry.get().upper()
    text.delete(1.0, tk.END)

    if code in currencies:
        info = currencies[code]
        text.insert(tk.END, f"{code}: {info['Name']} = {info['Value']} RUB")
    else:
        text.insert(tk.END, "Не найдено")


if __name__ == "__main__":
    currencies = get_currencies()
    groups = load_groups()

    root = tk.Tk()
    root.title("Курсы валют с группами")
    root.geometry("300x500")

    tk.Label(root, text="Код валюты").pack()
    currency_entry = tk.Entry(root)
    currency_entry.pack()

    tk.Button(root, text="Найти валюту", command=find_currency).pack(pady=5)
    tk.Button(root, text="Показать все", command=show_all).pack(pady=5)

    tk.Label(root, text="Имя группы").pack()
    group_entry = tk.Entry(root)
    group_entry.pack()

    tk.Button(root, text="Создать группу", command=create_group).pack(pady=3)
    tk.Button(root, text="Добавить валюту", command=add_to_group).pack(pady=3)
    tk.Button(root, text="Удалить валюту", command=remove_from_group).pack(pady=3)
    tk.Button(root, text="Показать группу", command=show_group).pack(pady=3)

    listbox = tk.Listbox(root)
    listbox.pack(pady=3, fill="x")
    listbox.bind("<<ListboxSelect>>", select_group)

    update_groups_list()

    text = tk.Text(root)
    text.pack(expand=True, fill="both", padx=5, pady=5)

    root.mainloop()