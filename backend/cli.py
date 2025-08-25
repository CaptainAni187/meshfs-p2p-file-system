import sys
import json
import threading
import time
from .peer import Peer

# This will hold our running Peer instance
peer_instance = None

def send_response(response_type, payload):
    """Helper function to format and send a JSON response to stdout."""
    response = json.dumps({"type": response_type, "payload": payload})
    print(response, flush=True) # flush=True is crucial

def main_loop():
    """Listens for commands from stdin and processes them."""
    global peer_instance
    
    for line in sys.stdin:
        try:
            command = json.loads(line)
            cmd_type = command.get("type")
            payload = command.get("payload", {})

            if cmd_type == "START_PEER":
                port = payload.get("port", 65432)
                bootstrap_host = payload.get("bootstrap_host", "127.0.0.1")
                bootstrap_port = payload.get("bootstrap_port", 50000)

                if not peer_instance:
                    peer_instance = Peer('0.0.0.0', port, bootstrap_addr=(bootstrap_host, bootstrap_port))
                    
                    # Run the peer's server in a separate thread
                    server_thread = threading.Thread(target=peer_instance.start_server)
                    server_thread.daemon = True
                    server_thread.start()
                    time.sleep(1) # Give server time to start

                    # Register with bootstrap
                    peer_instance.register_with_bootstrap()
                    send_response("PEER_STARTED", {"port": port})
                else:
                    send_response("ERROR", {"message": "Peer already running."})
            
            elif cmd_type == "GET_PEERS":
                if peer_instance:
                    peers = peer_instance.get_peers_from_bootstrap()
                    send_response("PEER_LIST", {"peers": peers})
                else:
                    send_response("ERROR", {"message": "Peer not started."})

            # Add more command handlers here (e.g., for search, download)

        except json.JSONDecodeError:
            send_response("ERROR", {"message": "Invalid JSON command."})
        except Exception as e:
            send_response("ERROR", {"message": str(e)})


if __name__ == "__main__":
    # The CLI now enters a loop to be controlled by the Electron app
    main_loop()

