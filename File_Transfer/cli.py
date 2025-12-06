import socket
import threading
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Configuration
HOST = '127.0.0.1'
PORT = 9999
BUFFER_SIZE = 4096  # The size of data chunks to send


class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TCP File Client")
        self.geometry("450x380")
        self.config(bg='#f0f4f8')

        self.selected_filepath = None

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
        ttk.Label(header_frame, text="File Transfer Client", font=('Segoe UI', 14, 'bold'), anchor='center').pack(
            pady=5)
        ttk.Label(header_frame, text=f"Connecting to {HOST}:{PORT}", font=('Segoe UI', 10, 'italic'),
                  anchor='center').pack(pady=2)

        # File Selection Frame
        select_frame = ttk.Frame(self)
        select_frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(select_frame, text="Selected File:").grid(row=0, column=0, sticky='w', pady=5)
        self.file_var = tk.StringVar(value="No file selected.")
        self.file_label = ttk.Label(select_frame, textvariable=self.file_var, wraplength=350, foreground='#2c3e50')
        self.file_label.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5)

        self.select_button = ttk.Button(select_frame, text="Browse File", command=self.select_file)
        self.select_button.grid(row=0, column=1, sticky='e', padx=10)

        # Status and Progress Frame
        status_frame = ttk.Frame(self)
        status_frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(status_frame, text="Status:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(status_frame, textvariable=self.status_var, wraplength=350).grid(row=0, column=1, sticky='w', padx=10,
                                                                                   pady=5)

        # Progress Bar
        ttk.Label(status_frame, text="Progress:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky='w',
                                                                                      pady=5)
        self.progress_bar = ttk.Progressbar(status_frame, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)

        self.progress_label_var = tk.StringVar(value="0.00%")
        ttk.Label(status_frame, textvariable=self.progress_label_var).grid(row=3, column=0, columnspan=2, sticky='n',
                                                                           pady=2)

        status_frame.columnconfigure(1, weight=1)

        # Control Button
        self.send_button = ttk.Button(self, text="Send File", command=self.start_send_thread, style='TButton',
                                      state=tk.DISABLED)
        self.send_button.pack(pady=20, padx=20)

    def select_file(self):
        """Opens a file dialog for the user to select a file."""
        filepath = filedialog.askopenfilename()
        if filepath:
            self.selected_filepath = filepath
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            self.file_var.set(f"{filename}\nSize: {filesize / (1024 * 1024):.2f} MB")
            self.send_button.config(state=tk.NORMAL)
            self.status_var.set("File selected. Ready to send.")
        else:
            self.selected_filepath = None
            self.file_var.set("No file selected.")
            self.send_button.config(state=tk.DISABLED)
            self.status_var.set("Ready.")
            self.update_progress(0.0)

    def start_send_thread(self):
        """Starts the file sending process in a separate thread."""
        if not self.selected_filepath:
            messagebox.showwarning("Warning", "Please select a file first.")
            return

        self.send_button.config(state=tk.DISABLED, text="Sending...")
        self.status_var.set("Connecting to server...")

        # Start sending in a separate thread to keep the GUI responsive
        send_thread = threading.Thread(target=self.send_file, daemon=True)
        send_thread.start()

    def send_file(self):
        """Handles the main logic for connecting and sending the file."""
        client_socket = None

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 5-second timeout for connection attempts
            client_socket.settimeout(5)
            client_socket.connect((HOST, PORT))
            self.status_var.set("Connected to server. Preparing file data...")

            filepath = self.selected_filepath
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)

            # Prepare file information (Name|Size)
            file_info = f"{filename}|{filesize}"
            file_info_bytes = file_info.encode('utf-8')

            # 1. Send file information size (4 bytes fixed length)
            file_info_len_bytes = len(file_info_bytes).to_bytes(4, 'big')
            client_socket.sendall(file_info_len_bytes)

            # 2. Send file information
            client_socket.sendall(file_info_bytes)

            self.status_var.set(f"Sending '{filename}'...")

            # 3. Send the file data in chunks
            sent_bytes = 0

            with open(filepath, "rb") as f:
                while sent_bytes < filesize:
                    # Read a chunk from the file
                    bytes_read = f.read(BUFFER_SIZE)

                    if not bytes_read:
                        # Should not happen if size is correct, but safe check
                        break

                        # Send the chunk
                    client_socket.sendall(bytes_read)
                    sent_bytes += len(bytes_read)

                    # Update progress bar in the main thread
                    progress_percent = (sent_bytes / filesize) * 100
                    self.after(0, lambda p=progress_percent: self.update_progress(p))

            # 4. Receive server confirmation
            # Set a timeout for receiving confirmation
            client_socket.settimeout(10)
            confirmation = client_socket.recv(1024).decode('utf-8')

            self.status_var.set(f"Transfer complete. Server response: {confirmation}")
            messagebox.showinfo("Success", f"File '{filename}' sent successfully!")

        except socket.timeout:
            error_msg = "Connection attempt timed out. Ensure the server is running."
            self.status_var.set(error_msg)
            messagebox.showerror("Error", error_msg)
        except ConnectionRefusedError:
            error_msg = "Connection refused. Server might not be running or the address/port is incorrect."
            self.status_var.set(error_msg)
            messagebox.showerror("Error", error_msg)
        except FileNotFoundError:
            error_msg = "Selected file not found. Please re-select."
            self.status_var.set(error_msg)
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            error_msg = f"An error occurred during transfer: {e}"
            self.status_var.set(error_msg)
            messagebox.showerror("Error", error_msg)
        finally:
            if client_socket:
                client_socket.close()
            # Reset UI elements
            self.send_button.config(state=tk.NORMAL, text="Send File")
            self.update_progress(0.0)

    def update_progress(self, percentage):
        """Updates the GUI progress bar and label."""
        self.progress_bar['value'] = percentage
        self.progress_label_var.set(f"{percentage:.2f}%")


if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()