import socket
import json
import struct
import os
import tkinter as tk
from tkinter import filedialog

HOST = '127.0.0.1'
PORT = 5001
KEY = 0x42

os.makedirs("client_download", exist_ok=True)


def process_data(data: bytes, key: int, decrypt=False) -> bytes:
    result = bytearray()
    for byte in data:
        if not decrypt:
            processed = ((byte << 2) | (byte >> 6)) & 0xFF
            processed ^= key
        else:
            byte ^= key
            processed = ((byte >> 2) | (byte << 6)) & 0xFF
        result.append(processed)
    return bytes(result)


def send_data(sock, data: bytes):
    sock.sendall(struct.pack("!I", len(data)))
    sock.sendall(data)


def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            break
        data += packet
    return data


def recv_data(sock):
    raw_len = recv_exact(sock, 4)
    if not raw_len:
        return None
    length = struct.unpack("!I", raw_len)[0]
    return recv_exact(sock, length)


def upload_file():
    path = filedialog.askopenfilename()
    if not path:
        return

    filename = os.path.basename(path)

    with open(path, "rb") as f:
        data = f.read()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            cmd = {"action": "upload", "filename": filename}
            send_data(s, json.dumps(cmd).encode())
            send_data(s, data)

            response = recv_data(s)
            log("SERVER: " + response.decode())
    except Exception as e:
        log("Ошибка: " + str(e))


def download_file():
    filename = entry.get()
    if not filename:
        return

    filename += ".bin"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            cmd = {"action": "download", "filename": filename}
            send_data(s, json.dumps(cmd).encode())

            data = recv_data(s)

            if data.startswith(b"ERROR"):
                log(data.decode())
                return

            decrypted = process_data(data, KEY, decrypt=True)

            output_path = os.path.join("client_download", filename.replace(".bin", ""))

            with open(output_path, "wb") as f:
                f.write(decrypted)

            log("Сохранено: " + output_path)

    except Exception as e:
        log("Ошибка: " + str(e))


def log(message):
    text.insert(tk.END, message + "\n")
    text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Client")
    root.geometry("500x400")

    tk.Button(root, text="Upload файл", command=upload_file).pack(pady=5)

    tk.Label(root, text="Имя файла (без .bin)").pack()
    entry = tk.Entry(root)
    entry.pack()

    tk.Button(root, text="Download файл", command=download_file).pack(pady=5)

    text = tk.Text(root)
    text.pack(expand=True, fill="both", padx=10, pady=10)

    root.mainloop()