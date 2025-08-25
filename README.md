# MeshFS: A Decentralized Peer-to-Peer File System

**MeshFS** is a decentralized, resilient peer-to-peer (P2P) file system built with Python and React. It implements a custom TCP/IP protocol for efficient, chunk-based file sharing and synchronization across a distributed network of peers. This project is a practical demonstration of socket programming, distributed systems architecture, and modern desktop application development with Electron.

 

---

## Table of Contents

- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [Author](#author)

---

## Key Features

- **Decentralized Network**: No central server for file storage. Peers connect and share directly.
- **Peer Discovery**: A lightweight bootstrap server helps new peers find others on the network.
- **Distributed File Search**: Search for files across all connected peers in real-time.
- **Chunk-Based File Transfers**: Large files are split into smaller chunks for efficient and reliable downloading.
- **Cross-Platform Desktop UI**: An intuitive control panel built with Electron and React that runs on macOS, Windows, and Linux.
- **Real-Time Status**: Monitor peer connections, local files, and network activity from the UI.

---

## How It Works

1.  **Bootstrap**: A new peer first connects to the **bootstrap server** to get a list of other active peers.
2.  **Discovery**: The peer then establishes direct connections with the peers from the list.
3.  **Sharing**: Each peer makes files in its local `shared` directory available to the network.
4.  **Searching**: When a user initiates a search, the peer sends a query to all connected peers, which then search their local shared files.
5.  **Downloading**: To download a file, the peer requests it chunk by chunk from the peer that has it, ensuring the transfer is manageable and can be resumed if interrupted.

---

## System Architecture

MeshFS is composed of three main components that work together:

1.  **Python Backend (`/backend`)**:
    *   **`peer.py`**: The core P2P logic. Handles server listening, client connections, file querying, and chunk transfers.
    - **`cli.py`**: A command-line interface that acts as the communication bridge between the Electron frontend and the Python peer logic. It processes JSON commands from `stdin`.
    *   **`bootstrap_server.py`**: A simple, thread-safe server that maintains a list of active peers.

2.  **Electron Frontend (`/frontend`)**:
    *   **`electron.js`**: The main Electron process. It spawns the Python backend script as a child process and manages Inter-Process Communication (IPC) between Python and the React UI.
    *   **`App.js`**: The main React component that builds the user interface. It communicates with the Electron main process to send commands and receive updates.

3.  **Communication Protocol**:
    *   Communication between the Python backend and the Electron frontend is handled via `stdin` and `stdout`, with messages formatted as newline-delimited JSON objects.
    *   Communication between peers is done over TCP sockets using a custom JSON-based protocol for commands like `REGISTER`, `GET_PEERS`, `SEARCH_FILES`, and `GET_CHUNKS`.

---

## Getting Started

### Prerequisites

-   [Python](https://www.python.org/downloads/) (version 3.9 or higher)
-   [Node.js](https://nodejs.org/) (version 16 or higher) and npm
-   [Git](https://git-scm.com/)

### Installation

1.  **Clone the repository:**
    ```
    git clone https://github.com/CaptainAni187/meshfs-p2p-file-system.git
    cd meshfs-p2p-file-system
    ```

2.  **Set up the Python backend:**
    ```
    # Create and activate a virtual environment
    python3 -m venv .venv
    source .venv/bin/activate

    # (Optional) Install Python dependencies if any are added in the future
    # pip install -r requirements.txt 
    ```

3.  **Set up the Electron frontend:**
    ```
    cd frontend
    npm install
    ```

---

## Usage

You will need at least **three separate terminal windows** to run the full system for testing.

1.  **Terminal 1: Start the Bootstrap Server**
    *In the project root (`meshfs-p2p-file-system`)*
    ```
    source .venv/bin/activate
    python3 -m backend.bootstrap_server
    ```
    *This terminal will log peer registrations.*

2.  **Terminal 2: Start a Dummy Peer**
    *In the project root (`meshfs-p2p-file-system`)*
    *First, create a `dummy_peer.py` file in the root with the necessary code to start and register a peer.*
    ```
    source .venv/bin/activate
    python3 dummy_peer.py
    ```
    *This acts as another user on the network for your main app to discover.*

3.  **Terminal 3: Start the Desktop Application**
    *Navigate to the `frontend` directory*
    ```
    cd frontend
    npm run electron:start
    ```
    *The MeshFS Control Panel will launch.*

4.  **Interact with the App:**
    - Click **Start Peer**.
    - Click **Discover Peers** to see the dummy peer appear in the list.
    - Add files to the `/backend/shared` directory of the dummy peer and search for them in the app.

---

## Development

-   The Python backend is modular, allowing for easy addition of new features like file encryption or different P2P protocols.
-   The React frontend can be extended with features like download progress bars, more detailed peer information, or a settings panel.

---

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request for:
-   Bug fixes
-   Feature enhancements (e.g., peer-to-peer chat, swarm-based downloads)
-   Improved documentation
-   UI/UX improvements

---

## Author

**Animesh (CaptainAni187)**
-   **GitHub**: [CaptainAni187](https://github.com/CaptainAni187)
-   **Project Repository**: [meshfs-p2p-file-system](https://github.com/CaptainAni187/meshfs-p2p-file-system)
