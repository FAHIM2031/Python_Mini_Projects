# client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

HOST = '127.0.0.1'
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Kotha Barta - Enter Nickname")
        self.master.geometry("500x500")

        # Nickname entry frame
        self.nickname_frame = tk.Frame(master)
        self.nickname_frame.pack(pady=20)

        tk.Label(self.nickname_frame, text="Enter your nickname:").pack(side=tk.LEFT)
        self.nickname_entry = tk.Entry(self.nickname_frame)
        self.nickname_entry.pack(side=tk.LEFT, padx=5)
        self.nickname_entry.bind("<Return>", self.set_nickname)

        self.nickname_button = tk.Button(self.nickname_frame, text="Join Chat", command=self.set_nickname)
        self.nickname_button.pack(side=tk.LEFT, padx=5)

        # Chat frame (hidden initially)
        self.chat_frame = tk.Frame(master)
        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state='disabled')

        # Define tags for colors
        self.chat_area.tag_config("self", foreground="#2B488A", justify="right", font="bold")
        self.chat_area.tag_config("other", foreground="#248564", justify="left", font="bold")

        # Message input
        self.message_entry = tk.Entry(self.chat_frame, width=50)
        self.message_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

    def set_nickname(self, event=None):
        global nickname
        nickname = self.nickname_entry.get().strip()
        if nickname:
            self.master.title(f"Kotha Barta  [user = {nickname}]")
            self.nickname_frame.pack_forget()  # hide nickname entry
            self.chat_frame.pack(fill=tk.BOTH, expand=True)  # show chat
            # Start receiving messages
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        if message:
            timestamp = datetime.now().strftime('%H:%M')
            full_message = f"{nickname}: {message} [{timestamp}]"
            client.send(full_message.encode('utf-8'))
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, full_message + "\n", "self")
            self.chat_area.yview(tk.END)
            self.chat_area.config(state='disabled')

    def receive_messages(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "NICKNAME":
                    client.send(nickname.encode('utf-8'))
                else:
                    if message.startswith(nickname + ":"):
                        continue
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, message + "\n", "other")
                    self.chat_area.yview(tk.END)
                    self.chat_area.config(state='disabled')
            except:
                print("Connection closed!")
                client.close()
                break

root = tk.Tk()
app = ChatApp(root)
root.mainloop()
