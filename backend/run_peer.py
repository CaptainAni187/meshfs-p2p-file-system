import socket
import json
import threading
import time
import os
from .peer import Peer # We can import Peer directly
from .file_handler import create_meta_file, CHUNK_SIZE

# --- Main Application Logic ---

def download_file(peer_host, peer_port, meta_filename):
    """Connects to a peer and downloads a file chunk by chunk."""
    try:
        # First, we need the metafile info
        with open(os.path.join('backend/shared', meta_filename), 'r') as f:
            meta_data = json.load(f)
        
        filename = meta_data['filename']
        num_chunks = len(meta_data['chunk_hashes'])
        
        # Create a directory for downloads
        download_dir = "downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        output_path = os.path.join(download_dir, filename)

        with open(output_path, 'wb') as f:
            for i in range(num_chunks):
                print(f"Requesting chunk {i+1}/{num_chunks} for {filename}")
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((peer_host, peer_port))
                    
                    # Send GET_CHUNKS request
                    request = {
                        "type": "GET_CHUNKS",
                        "payload": {"filename": filename, "chunk_number": i}
                    }
                    s.sendall(json.dumps(request).encode('utf-8'))
                    
                    # Receive response
                    response_raw = s.recv(CHUNK_SIZE + 4096) # Buffer for metadata
                    response = json.loads(response_raw.decode('utf-8'))

                    if response['type'] == 'CHUNK_DATA':
                        chunk_data = bytes.fromhex(response['payload']['data'])
                        f.write(chunk_data)
                        print(f"Received and wrote chunk {i+1}")
                    else:
                        print("Error: Did not receive CHUNK_DATA")
                        break
        
        print(f"File '{filename}' downloaded successfully to '{output_path}'")

    except Exception as e:
        print(f"An error occurred during download: {e}")

def main():
    # --- Peer 1 (The Server/Uploader) ---
    # This peer will just run in the background and serve files.
    peer1 = Peer('127.0.0.1', 65432)
    
    # Create meta file for our sample text file
    create_meta_file('backend/shared/sample.txt', peer1.shared_dir)
    
    server_thread = threading.Thread(target=peer1.start_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Peer 1 is running in the background.")
    
    # --- Peer 2 (The Client/Downloader) ---
    # We will use this part of the script to initiate the download.
    # Give the server a moment to start up
    time.sleep(2) 

    # Let's simulate Peer 2 wanting to download the file from Peer 1
    print("\n--- Starting Download ---")
    download_file('127.0.0.1', 65432, 'sample.txt.meta')


if __name__ == "__main__":
    main()
