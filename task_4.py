import requests
import tkinter as tk


def get_user_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    text.delete(1.0, tk.END)

    if response.status_code != 200:
        text.insert(tk.END, "Пользователь не найден")
        return

    data = response.json()

    result = f"""===== ПРОФИЛЬ =====
Имя: {data.get('name')}
Логин: {data.get('login')}
Ссылка: {data.get('html_url')}
Публичные репозитории: {data.get('public_repos')}
Подписки: {data.get('following')}
Подписчики: {data.get('followers')}
Описание: {data.get('bio')}
"""
    text.insert(tk.END, result)


def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    text.delete(1.0, tk.END)

    if response.status_code != 200:
        text.insert(tk.END, "Ошибка получения репозиториев")
        return

    repos = response.json()

    if not repos:
        text.insert(tk.END, "Нет репозиториев")
        return

    text.insert(tk.END, "===== РЕПОЗИТОРИИ =====\n\n")

    for repo in repos:
        result = f"""Название: {repo.get('name')}
Ссылка: {repo.get('html_url')}
Язык: {repo.get('language')}
Видимость: {'private' if repo.get('private') else 'public'}
Основная ветка: {repo.get('default_branch')}

"""
        text.insert(tk.END, result)


def search_repositories(query):
    url = f"https://api.github.com/search/repositories?q={query}"
    response = requests.get(url)

    text.delete(1.0, tk.END)

    if response.status_code != 200:
        text.insert(tk.END, "Ошибка поиска")
        return

    data = response.json()
    items = data.get("items", [])

    text.insert(tk.END, f"===== РЕЗУЛЬТАТЫ ПОИСКА ({len(items)}) =====\n")

    for repo in items[:10]:
        result = f"""
Название: {repo.get('name')}
Владелец: {repo.get('owner', {}).get('login')}
Ссылка: {repo.get('html_url')}
Язык: {repo.get('language')}
"""
        text.insert(tk.END, result)


def handle_profile():
    username = entry.get()
    if username:
        get_user_profile(username)


def handle_repos():
    username = entry.get()
    if username:
        get_user_repos(username)


def handle_search():
    query = entry.get()
    if query:
        search_repositories(query)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("GitHub Viewer")
    root.geometry("400x300")

    tk.Label(root, text="Username / Поиск").pack(pady=5)
    entry = tk.Entry(root)
    entry.pack(fill="x", padx=10)

    tk.Button(root, text="Профиль", command=handle_profile).pack(pady=3)
    tk.Button(root, text="Репозитории", command=handle_repos).pack(pady=3)
    tk.Button(root, text="Поиск репозиториев", command=handle_search).pack(pady=3)

    text = tk.Text(root)
    text.pack(expand=True, fill="both", padx=10, pady=10)

    root.mainloop()