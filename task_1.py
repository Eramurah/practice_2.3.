import requests, tkinter as tk


def check():
    text_area.config(state="normal")
    text_area.delete("1.0", tk.END)

    a = ["https://github.com/", "https://www.binance.com/en",
         "https://tomtit.tomsk.ru/", "https://moodle.tomtit-tomsk.ru"]

    for i in a:
        try:
            r = requests.get(i)
            b = 0
            for j in range(100):
                if r.status_code == (100 + b):
                    text_area.insert(tk.END, f"Сайт: {i}\nСтатус: Запрос получен, процесс продолжается - код {r.status_code}.\n{'-' * 30}\n")
                    break
                elif r.status_code == (200 + b):
                    text_area.insert(tk.END,f"Сайт: {i}\nСтатус: Запрос успешно принят и обработан - код {r.status_code}.\n{'-' * 30}\n")
                    break
                elif r.status_code == (300 + b):
                    text_area.insert(tk.END,f"Сайт: {i}\nДля выполнения запроса нужно выполнить другое действие - код {r.status_code}.\n{'-' * 30}\n")
                    break
                elif r.status_code == (400 + b):
                    text_area.insert(tk.END,f"Сайт: {i}\nОшибка в запросе, страница не найдена или нет доступа - код {r.status_code}.\n{'-' * 30}\n")
                    break
                elif r.status_code == (500 + b):
                    text_area.insert(tk.END,f"Сайт: {i}\nСервер не выполнил запрос - код {r.status_code}.\n{'-' * 30}\n")
                    break
                b = b + 1

        except requests.exceptions.RequestException:
            text_area.insert(tk.END, f"Сайт: {i}\nСтатус: Ошибка подключения\n{'-' * 30}\n")

    root.after(15000, check)


if "__main__" == __name__:
    root = tk.Tk()
    root.geometry("425x250+75+75")

    root.title("Cделано Эралиевым М-Р, гр. 646")
    root.minsize(425, 250)
    root.maxsize(425, 250)

    text_area = tk.Text(root, font=("Arial", 12), wrap="word", padx=10, pady=10)
    text_area.pack(expand=True, fill="both")

    check()
    root.mainloop()


