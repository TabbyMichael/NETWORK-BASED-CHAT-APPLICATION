import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Function to receive messages from the server
def receive_messages(client_socket, text_area):
    while True:
        try:
            # Receive and print messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Use thread-safe method to update the GUI
                text_area.after(0, lambda: update_text_area(text_area, message))
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            client_socket.close()
            break

# Function to update the text area safely
def update_text_area(text_area, message):
    text_area.config(state=tk.NORMAL)  # Allow editing the text area
    text_area.insert(tk.END, message + '\n')  # Add the new message
    text_area.config(state=tk.DISABLED)  # Disable editing
    text_area.yview(tk.END)  # Auto-scroll to the end

# Function to send messages to the server
def send_message(client_socket, entry_field):
    message = entry_field.get()
    if message:  # Only send non-empty messages
        client_socket.send(message.encode('utf-8'))
        entry_field.delete(0, tk.END)  # Clear the entry field

# Function to start the GUI
def start_gui(client_socket):
    # Create the main window
    window = tk.Tk()
    window.title("Network-Based Chat Application")

    # Create a text area for displaying messages
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_area.config(state=tk.DISABLED)  # Make it read-only

    # Create an entry field for typing messages
    entry_field = tk.Entry(window, width=80)
    entry_field.pack(padx=10, pady=(0, 10), side=tk.LEFT, fill=tk.X, expand=True)

    # Create a button to send messages
    send_button = tk.Button(window, text="Send", command=lambda: send_message(client_socket, entry_field))
    send_button.pack(padx=(5, 10), pady=(0, 10), side=tk.RIGHT)

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_area))
    receive_thread.start()

    # Start the GUI main loop
    window.mainloop()

def start_client():
    server_ip = '127.0.0.1'
    server_port = 5555

    # Create a client socket (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Start the GUI
    start_gui(client_socket)

if __name__ == "__main__":
    start_client()
