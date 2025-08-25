import os
import json
import hashlib

CHUNK_SIZE = 1024 * 1024  # 1MB

def create_shared_directory(path="shared"):
    """Creates the directory to hold shared files if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_meta_file(filepath, shared_dir):
    """
    Splits a file into chunks and creates a .meta file for it.
    The .meta file contains the file's name, size, chunk size, and a list of chunk hashes.
    """
    try:
        # Calculate SHA-256 hashes for each chunk
        chunk_hashes = []
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                chunk_hashes.append(hashlib.sha256(chunk).hexdigest())

        # Create the metadata dictionary
        filename = os.path.basename(filepath)
        meta_data = {
            'filename': filename,
            'filesize': os.path.getsize(filepath),
            'chunk_size': CHUNK_SIZE,
            'chunk_hashes': chunk_hashes
        }
        
        # Write the metadata to a .meta file in the shared directory
        meta_filename = f"{filename}.meta"
        meta_filepath = os.path.join(shared_dir, meta_filename)
        with open(meta_filepath, 'w') as f:
            json.dump(meta_data, f, indent=4)
            
        print(f"Created meta file: {meta_filepath}")
        return meta_data

    except Exception as e:
        print(f"Error creating meta file for {filepath}: {e}")
        return None

def get_chunk(filepath, chunk_number):
    """Reads and returns a specific chunk from a file."""
    try:
        with open(filepath, 'rb') as f:
            f.seek(chunk_number * CHUNK_SIZE)
            return f.read(CHUNK_SIZE)
    except Exception as e:
        print(f"Error reading chunk {chunk_number} from {filepath}: {e}")
        return None
