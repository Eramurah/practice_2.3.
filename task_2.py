import tkinter as tk
import psutil


def cpu_mem_disk():
    a = psutil.cpu_percent()
    b = psutil.virtual_memory()
    c = psutil.disk_usage('/').percent

    label_cpu.config(text=f"Загрузка процессора: {a}%")
    label_mem.config(text=f"ОЗУ загружен на: {(b.used / 1024 ** 3):.3f} ГБ ({b.percent}%)")
    label_disk.config(text=f"Диск занят на: {c}%\n")

    root.after(2000, cpu_mem_disk)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("355x200+75+75")

    root.title("Cделано Эралиевым М-Р, гр. 646")
    root.minsize(355, 200)
    root.maxsize(355, 200)

    label_cpu = tk.Label(root, font=("Arial", 12))
    label_cpu.pack(pady=20)

    label_mem = tk.Label(root, font=("Arial", 12))
    label_mem.pack(pady=20)

    label_disk = tk.Label(root, font=("Arial", 12))
    label_disk.pack(pady=20)

    cpu_mem_disk()
    root.mainloop()
