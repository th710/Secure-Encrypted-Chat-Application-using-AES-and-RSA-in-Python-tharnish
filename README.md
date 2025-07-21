# Secure-Encrypted-Chat-Application-using-AES-and-RSA-in-Python-tharnish

# 🔐 Secure Chat Application

A secure end-to-end encrypted chat application using Python. It uses RSA for key exchange and AES for message encryption, ensuring confidentiality and privacy over unsecured networks.

## 🚀 Features

- AES-256 encryption for message confidentiality
- RSA encryption for secure key exchange
- Multi-threaded communication (simultaneous send/receive)
- Socket-based client-server architecture
- Lightweight and terminal-based

## 🛠️ Tech Stack

- **Programming Language**: Python 3
- **Libraries**: `socket`, `threading`, `Crypto (PyCryptodome)`, `lazyme`
- **Encryption**: RSA (2048 bits) + AES (256 bits)

## 📸 Screenshots (Optional)

_You can add screenshots of the terminal interface here._

## 📦 Installation


# Clone the repository
git clone https://github.com/your-username/secure-chat-app.git
cd secure-chat-app

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pycryptodome lazyme
🧪 Running the Application
Start the Server

python secure_server.py
Start the Client (in another terminal or machine)

python secure_client.py
Make sure both client and server are on the same network or IP reachable to each other.

🧠 How It Works
The server generates an RSA key pair.

The client connects and receives the server's public key.

The client generates a random AES key and encrypts it using the server's public key.

All chat messages are encrypted using AES (CBC/ECB).

Multi-threading is used to allow sending and receiving simultaneously.

📁 File Structure
bash
Copy
Edit
secure-chat-app/
├── secure_server.py   # Server-side logic
├── secure_client.py   # Client-side logic
└── README.md          # This file
