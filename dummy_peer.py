import sys
import threading
import time
from backend.peer import Peer

# Create and start a dummy peer
peer = Peer('0.0.0.0', 65431)

# Start the peer server in a background thread
server_thread = threading.Thread(target=peer.start_server, daemon=True)
server_thread.start()

# Give the server a moment to start
time.sleep(1)

# Register with bootstrap server
peer.register_with_bootstrap()

print('Dummy peer running on port 65431. Press Ctrl+C to stop.')

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\nShutting down dummy peer...')
