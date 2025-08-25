import socket

def main():
    """
    A simple client that connects to the server and sends a message.
    """
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 65432        # The port used by the server

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((host, port))
        
        # The message to send
        message = "Hello, Peer"
        print(f"Sending message: '{message}'")
        
        # Encode the string into bytes and send it
        s.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    main()
