import socket

def main():
    """
    A simple server that listens for a connection and prints the received message.
    """
    # Define the host and port
    # '127.0.0.1' is the localhost address (your own computer)
    host = '127.0.0.1'
    port = 65432

    # Create a new socket object
    # AF_INET specifies the address family (IPv4)
    # SOCK_STREAM specifies the socket type (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the address and port
        s.bind((host, port))
        
        # Enable the server to accept connections
        s.listen()
        
        print(f"Server listening on {host}:{port}")
        
        # Block and wait for an incoming connection
        conn, addr = s.accept()
        
        with conn:
            print(f"Connected by {addr}")
            
            # Receive data from the client
            # The 1024 is the buffer size (max data to receive at once)
            data = conn.recv(1024)
            
            # If no data is received, the client has closed the connection
            if not data:
                print("No data received. Connection closed.")
            else:
                # Decode the bytes into a string and print it
                message = data.decode('utf-8')
                print(f"Received message: {message}")

if __name__ == "__main__":
    main()
