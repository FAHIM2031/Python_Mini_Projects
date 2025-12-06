import socket
import threading
from datetime import datetime
import json  # For sending list of users as JSON

HOST = '127.0.0.1'
PORT = 55555

clients = []
nicknames = []

# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Send updated user list to all clients
def send_user_list():
    user_list = json.dumps({"type": "users", "users": nicknames})
    for client in clients:
        client.send(user_list.encode('utf-8'))

# Handle a single client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                # Log message with timestamp
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message.decode('utf-8')}")
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                nicknames.remove(nickname)
                broadcast(f"[{datetime.now().strftime('%H:%M')}] {nickname} left the chat.".encode('utf-8'))
                send_user_list()  # Update all clients
            break

# Receive new clients
def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname: {nickname}")
        broadcast(f"[{datetime.now().strftime('%H:%M')}] {nickname} joined the chat.".encode('utf-8'))
        client.send("Connected to server!".encode('utf-8'))

        send_user_list()  # Send updated user list to all clients

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
