import socket
import threading

# List to store all connected clients
clients = []

# Broadcast function to send message to all clients
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
    server_ip = '127.0.0.1'
    server_port = 5555

    # Create a server socket (IPv4, TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))

    # Listen for incoming connections (up to 5 clients)
    server.listen(5)
    print(f"Server started on {server_ip}:{server_port}")

    while True:
        # Accept new client connection
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")

        # Add the new client to the clients list
        clients.append(client_socket)

        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
