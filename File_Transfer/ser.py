import socket
import threading
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Configuration
HOST = '127.0.0.1'
PORT = 9999
BUFFER_SIZE = 4096  # The size of data chunks to receive


class ServerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TCP File Server")
        self.geometry("450x350")
        self.config(bg='#f0f4f8')

        self.is_running = False
        self.server_socket = None

        # UI components
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f4f8')
        self.style.configure('TLabel', background='#f0f4f8', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6, foreground='#ffffff',
                             background='#4a69bd')
        self.style.map('TButton', background=[('active', '#3c5aa8')])

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=10, padx=20, fill='x')
        ttk.Label(header_frame, text="File Transfer Server", font=('Segoe UI', 14, 'bold'), anchor='center').pack(
            pady=5)
        ttk.Label(header_frame, text=f"Listening on {HOST}:{PORT}", font=('Segoe UI', 10, 'italic'),
                  anchor='center').pack(pady=2)

        # Status and Progress Frame
        status_frame = ttk.Frame(self)
        status_frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(status_frame, text="Status:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.status_var = tk.StringVar(value="Idle. Press Start.")
        ttk.Label(status_frame, textvariable=self.status_var, wraplength=350).grid(row=0, column=1, sticky='w', padx=10,
                                                                                   pady=5)

        ttk.Label(status_frame, text="File:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.file_var = tk.StringVar(value="N/A")
        ttk.Label(status_frame, textvariable=self.file_var, wraplength=350).grid(row=1, column=1, sticky='w', padx=10,
                                                                                 pady=5)

        # Progress Bar
        ttk.Label(status_frame, text="Progress:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w',
                                                                                      pady=5)
        self.progress_bar = ttk.Progressbar(status_frame, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)

        self.progress_label_var = tk.StringVar(value="0.00%")
        ttk.Label(status_frame, textvariable=self.progress_label_var).grid(row=4, column=0, columnspan=2, sticky='n',
                                                                           pady=2)

        status_frame.columnconfigure(1, weight=1)

        # Control Button
        self.start_button = ttk.Button(self, text="Start Server", command=self.start_server_thread, style='TButton')
        self.start_button.pack(pady=20, padx=20)

    def start_server_thread(self):
        if self.is_running:
            return

        self.is_running = True
        self.status_var.set("Server starting...")
        self.start_button.config(text="Server Running", state=tk.DISABLED)

        # Start the server listening in a separate thread
        server_thread = threading.Thread(target=self.run_server_loop, daemon=True)
        server_thread.start()
        messagebox.showinfo("Server Status", f"Server running on {HOST}:{PORT}. Waiting for client...")

    def run_server_loop(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # CRITICAL FIX: Allow the socket to reuse the address immediately after closing,
            # preventing the "Address already in use" error common during quick restarts.
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(1)  # Listen for one connection
            self.status_var.set("Listening for a connection...")

            while self.is_running:
                # Accept connection - this is a blocking call
                conn, addr = self.server_socket.accept()

                # Handle the client connection in a new thread
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                client_thread.start()

        except socket.error as e:
            if self.is_running:
                error_msg = f"Socket Error: {e}"
                print(error_msg)
                self.status_var.set(f"Error: {e}")
                self.cleanup_server()
                messagebox.showerror("Error", error_msg)
        except Exception as e:
            if self.is_running:
                error_msg = f"An unexpected error occurred: {e}"
                print(error_msg)
                self.status_var.set(f"Error: {e}")
                self.cleanup_server()
                messagebox.showerror("Error", error_msg)

    def handle_client(self, conn, addr):
        self.status_var.set(f"Connection established with {addr[0]}:{addr[1]}. Receiving file info...")

        try:
            # 1. Receive file name size (4 bytes fixed length)
            file_info_len_bytes = conn.recv(4)
            if not file_info_len_bytes:
                raise ConnectionResetError("Client disconnected during info exchange.")

            file_info_len = int.from_bytes(file_info_len_bytes, 'big')

            # 2. Receive file info (name and size)
            file_info_bytes = conn.recv(file_info_len)
            file_info_str = file_info_bytes.decode('utf-8')

            filename, filesize_str = file_info_str.split('|')
            filesize = int(filesize_str)

            self.file_var.set(f"{filename} ({filesize / (1024 * 1024):.2f} MB)")
            self.status_var.set(f"Receiving file: {filename}. Total size: {filesize} bytes.")

            # 3. Receive the file data
            received_bytes = 0

            # The file will be saved in the same directory as the script.
            filepath = os.path.join(os.getcwd(), filename)

            with open(filepath, "wb") as f:
                while received_bytes < filesize:
                    # Calculate how many bytes are still needed
                    remaining_bytes = filesize - received_bytes
                    # Receive either BUFFER_SIZE or the remaining bytes, whichever is smaller
                    bytes_to_read = min(BUFFER_SIZE, remaining_bytes)

                    # Receive the data chunk
                    data = conn.recv(bytes_to_read)

                    if not data:
                        raise ConnectionResetError("Connection lost before transfer completion.")

                    f.write(data)
                    received_bytes += len(data)

                    # Update progress bar in the main thread
                    progress_percent = (received_bytes / filesize) * 100
                    self.after(0, lambda p=progress_percent: self.update_progress(p))

            conn.sendall("File received successfully.".encode('utf-8'))
            self.status_var.set(f"Transfer of '{filename}' complete! Saved at: {filepath}")
            self.file_var.set("N/A")
            messagebox.showinfo("Success", f"File '{filename}' received successfully!")

        except ConnectionResetError as e:
            self.status_var.set(f"Client connection error: {e}")
            print(f"Client connection error: {e}")
        except socket.timeout:
            self.status_var.set("Connection timed out.")
            print("Connection timed out.")
        except Exception as e:
            self.status_var.set(f"Transfer failed: {e}")
            print(f"Transfer failed: {e}")
        finally:
            conn.close()
            # Reset progress after transfer attempt
            self.after(0, lambda: self.update_progress(0.0))
            # Go back to listening if server is still running
            if self.is_running:
                self.status_var.set("Listening for a connection...")

    def update_progress(self, percentage):
        """Updates the GUI progress bar and label."""
        self.progress_bar['value'] = percentage
        self.progress_label_var.set(f"{percentage:.2f}%")

    def cleanup_server(self):
        """Clean up and reset server state."""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None  # Ensure it's marked as closed
        self.start_button.config(text="Start Server", state=tk.NORMAL)
        self.status_var.set("Server stopped or encountered an error.")
        self.update_progress(0.0)
        self.file_var.set("N/A")

    def on_closing(self):
        """Handles window closing event."""
        if self.is_running:
            self.cleanup_server()
        self.destroy()


if __name__ == "__main__":
    app = ServerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()