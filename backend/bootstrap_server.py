import socket
import threading
import json
import time

# A simple thread-safe dictionary to store active peers { (ip, port): last_seen_time }
active_peers = {}
peers_lock = threading.Lock()

def handle_peer_requests(client_socket, addr):
    """Handles REGISTER and GET_PEERS requests from peers."""
    try:
        request_data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(request_data)

        command = request.get('command')
        port = request.get('port')
        peer_addr = (addr[0], port)

        if command == 'REGISTER':
            with peers_lock:
                active_peers[peer_addr] = time.time()
            print(f"Registered peer: {peer_addr}")
            client_socket.sendall(json.dumps({"status": "success"}).encode('utf-8'))

        elif command == 'GET_PEERS':
            with peers_lock:
                # --- THIS IS THE FIX ---
                # Return all peers except the one asking (check both IP and port)
                peers_list = [p for p in active_peers.keys() if p != peer_addr]
            print(f"Sending peers list to {peer_addr}: {peers_list}")
            client_socket.sendall(json.dumps(peers_list).encode('utf-8'))

    except Exception as e:
        print(f"Error handling request from {addr}: {e}")
    finally:
        client_socket.close()

def cleanup_inactive_peers():
    """Periodically removes peers that haven't checked in recently."""
    while True:
        time.sleep(60) # Check every 60 seconds
        with peers_lock:
            current_time = time.time()
            inactive_threshold = 120 # 2 minutes
            inactive = [p for p, t in active_peers.items() if current_time - t > inactive_threshold]
            for p in inactive:
                print(f"Removing inactive peer: {p}")
                del active_peers[p]

def main():
    host = '0.0.0.0'
    port = 50000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)
    print(f"Bootstrap server listening on {host}:{port}")

    cleanup_thread = threading.Thread(target=cleanup_inactive_peers, daemon=True)
    cleanup_thread.start()

    while True:
        client_sock, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handler_thread = threading.Thread(target=handle_peer_requests, args=(client_sock, addr))
        handler_thread.start()

if __name__ == "__main__":
    main()
