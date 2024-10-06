import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Global variables for sockets
server_socket = None
client_socket = None

# List to store all connected clients
clients = []

# Broadcast function to send messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error sending message to a client: {e}")
                clients.remove(client)

# Function to handle client communication
def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024)
            if message:
                # Format message to include the sender's address
                formatted_message = f"{client_socket.getpeername()}: {message.decode('utf-8')}"
                print(f"Received message: {formatted_message}")  # Log received message
                # Broadcast message to other clients
                broadcast(formatted_message.encode('utf-8'), client_socket)
            else:
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            clients.remove(client_socket)
            break

# Main server function to accept connections
def start_server():
    global server_socket
    server_ip = '127.0.0.1'
    server_port = 5555

    # Create a server socket (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections (up to 5 clients)
    server_socket.listen(5)
    print(f"Server started on {server_ip}:{server_port}")

    while True:
        # Accept new client connection
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # Add the new client to the clients list
        clients.append(client_socket)

        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

# Function to receive messages from the server
def receive_messages():
    global client_socket
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Use thread-safe method to update the GUI
                text_area.after(0, lambda: update_text_area(message))
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            client_socket.close()
            break

# Function to update the text area safely
def update_text_area(message):
    sender, text = message.split(': ', 1)  # Split sender and message text
    formatted_message = f"{sender}:\n\t{text}\n"
    
    # Display the message in a formatted style
    text_area.config(state=tk.NORMAL)  # Allow editing the text area
    text_area.insert(tk.END, formatted_message)  # Add the new message
    text_area.config(state=tk.DISABLED)  # Disable editing
    text_area.yview(tk.END)  # Auto-scroll to the end

# Function to send messages to the server
def send_message(entry_field):
    global client_socket
    message = entry_field.get()
    if message:  # Only send non-empty messages
        client_socket.send(message.encode('utf-8'))
        entry_field.delete(0, tk.END)  # Clear the entry field

# Function to start the client
def start_client():
    global client_socket
    server_ip = '127.0.0.1'
    server_port = 5555

    # Create a client socket (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

# GUI Setup
def setup_gui():
    window = tk.Tk()
    window.title("Network-Based Chat Application")

    # Create a frame for buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=(10, 0))  # Add padding to the top

    # Create a button to start the server
    start_server_button = tk.Button(button_frame, text="Start Server", command=lambda: threading.Thread(target=start_server, daemon=True).start())
    start_server_button.pack(side=tk.LEFT, padx=10)

    # Create a button to start the client
    start_client_button = tk.Button(button_frame, text="Start Client", command=start_client)
    start_client_button.pack(side=tk.LEFT, padx=10)

    # Create a text area for displaying messages
    global text_area
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    text_area.pack(padx=10, pady=(10, 10), fill=tk.BOTH, expand=True)
    text_area.config(state=tk.DISABLED)  # Make it read-only

    # Create an entry field for typing messages
    entry_field = tk.Entry(window, width=80)
    entry_field.pack(padx=10, pady=(0, 10), side=tk.LEFT, fill=tk.X, expand=True)

    # Create a button to send messages
    send_button = tk.Button(window, text="Send", command=lambda: send_message(entry_field))
    send_button.pack(padx=(5, 10), pady=(0, 10), side=tk.RIGHT)

    window.mainloop()

if __name__ == "__main__":
    setup_gui()
