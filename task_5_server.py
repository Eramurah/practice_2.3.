import socket
import os
import json
import struct
import xml.etree.ElementTree
import threading
import tkinter as tk

HOST = '0.0.0.0'
PORT = 5001
KEY = 0x42
STORAGE_DIR = 'server_storage'

os.makedirs(STORAGE_DIR, exist_ok=True)


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
            return None
        data += packet
    return data


def recv_data(sock):
    raw_len = recv_exact(sock, 4)
    if not raw_len:
        return None
    length = struct.unpack("!I", raw_len)[0]
    return recv_exact(sock, length)


def validate_json(data):
    try:
        json.loads(data.decode())
        return True
    except:
        return False


def validate_xml(data):
    try:
        xml.etree.ElementTree.fromstring(data.decode())
        return True
    except:
        return False


def handle_client(conn, addr):
    log(f"Client: {addr}")
    try:
        cmd_data = recv_data(conn)
        if not cmd_data:
            return

        command = json.loads(cmd_data.decode())
        action = command.get("action")
        filename = command.get("filename")

        if action == "upload":
            file_data = recv_data(conn)

            if filename.endswith(".json") and not validate_json(file_data):
                send_data(conn, b"ERROR: Invalid JSON")
                return

            if filename.endswith(".xml") and not validate_xml(file_data):
                send_data(conn, b"ERROR: Invalid XML")
                return

            encrypted = process_data(file_data, KEY)

            path = os.path.join(STORAGE_DIR, filename + ".bin")

            with open(path, "wb") as f:
                f.write(encrypted)

            send_data(conn, f"OK: {filename}.bin".encode())
            log(f"Saved: {filename}.bin")

        elif action == "download":
            path = os.path.join(STORAGE_DIR, filename)

            if not os.path.exists(path):
                send_data(conn, b"ERROR: File not found")
                return

            with open(path, "rb") as f:
                data = f.read()

            send_data(conn, data)

    finally:
        conn.close()


def start_server():
    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            log("Server started...")

            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    threading.Thread(target=run, daemon=True).start()


def log(msg):
    text.insert(tk.END, msg + "\n")
    text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Server")
    root.geometry("500x400")

    tk.Button(root, text="Запустить сервер", command=start_server).pack(pady=5)

    text = tk.Text(root)
    text.pack(expand=True, fill="both", padx=10, pady=10)

    root.mainloop()