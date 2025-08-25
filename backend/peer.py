import socket
import threading
import json
import os
import sys  # <-- Added this import for stderr
from . import file_handler

class Peer:
    def __init__(self, host, port, bootstrap_addr=('127.0.0.1', 50000), shared_dir='shared'):
        """
        A single, combined constructor for the Peer.
        """
        self.host = host
        self.port = port
        self.bootstrap_addr = bootstrap_addr
        self.shared_dir = file_handler.create_shared_directory(os.path.join('backend', shared_dir))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.peers = {} # To store connections to other peers

    def start_server(self):
        """Starts the peer's server to listen for incoming connections."""
        self.server_socket.listen(5)
        # LOGGING: Print to stderr to avoid polluting the JSON stdout stream
        print(f"Peer server started at {self.host}:{self.port}", file=sys.stderr, flush=True)
        
        while True:
            client_socket, addr = self.server_socket.accept()
            # LOGGING: Print to stderr
            print(f"Accepted connection from {addr}", file=sys.stderr, flush=True)
            handler_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            handler_thread.daemon = True
            handler_thread.start()

    def handle_client(self, client_socket):
        """Handles incoming messages from another peer."""
        try:
            while True:
                message_raw = client_socket.recv(4096)
                if not message_raw:
                    break
                
                message = json.loads(message_raw.decode('utf-8'))
                msg_type = message.get('type')
                payload = message.get('payload', {})
                
                # LOGGING: Print to stderr
                print(f"Received message of type: {msg_type}", file=sys.stderr, flush=True)

                if msg_type == 'QUERY_FILES':
                    self.handle_query_files(client_socket)
                elif msg_type == 'GET_CHUNKS':
                    self.handle_get_chunks(client_socket, payload)

        except Exception as e:
            # LOGGING: Print to stderr
            print(f"Error handling client: {e}", file=sys.stderr, flush=True)
        finally:
            client_socket.close()

    def handle_query_files(self, client_socket):
        """Responds with a list of available .meta files."""
        meta_files = [f for f in os.listdir(self.shared_dir) if f.endswith('.meta')]
        response = {
            'type': 'FILE_LIST',
            'payload': {'files': meta_files}
        }
        client_socket.sendall(json.dumps(response).encode('utf-8'))

    def handle_get_chunks(self, client_socket, payload):
        """Responds with the data for a requested file chunk."""
        filename = payload.get('filename')
        chunk_number = payload.get('chunk_number')
        actual_filepath = os.path.join(self.shared_dir, filename)

        if not os.path.exists(actual_filepath):
            return

        chunk_data = file_handler.get_chunk(actual_filepath, chunk_number)
        
        if chunk_data:
            response = {
                'type': 'CHUNK_DATA',
                'payload': {
                    'filename': filename,
                    'chunk_number': chunk_number,
                    'data': chunk_data.hex() # Send binary data as hex
                }
            }
            client_socket.sendall(json.dumps(response).encode('utf-8'))

    def register_with_bootstrap(self):
        """Contacts the bootstrap server to register itself."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.bootstrap_addr)
                message = json.dumps({"command": "REGISTER", "port": self.port})
                s.sendall(message.encode('utf-8'))
                response_raw = s.recv(1024).decode('utf-8')
                # LOGGING: Print to stderr
                response_json = json.loads(response_raw)
                print(f"Bootstrap registration response: {response_json}", file=sys.stderr, flush=True)
        except Exception as e:
            # LOGGING: Print to stderr
            print(f"Could not register with bootstrap server: {e}", file=sys.stderr, flush=True)

    def get_peers_from_bootstrap(self):
        """Gets a list of active peers from the bootstrap server."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.bootstrap_addr)
                message = json.dumps({"command": "GET_PEERS", "port": self.port})
                s.sendall(message.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                peers_list = json.loads(response)
                # LOGGING: Print to stderr
                print(f"Received peers: {peers_list}", file=sys.stderr, flush=True)
                return peers_list
        except Exception as e:
            # LOGGING: Print to stderr
            print(f"Could not get peers from bootstrap server: {e}", file=sys.stderr, flush=True)
            return []

