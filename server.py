import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os
from lazyme.string import color_print

FLAG_READY = "Ready"
FLAG_QUIT = "quit"

def pad(s): return s + (16 - len(s) % 16) * '`'
def unpad(s): return s.replace('`', '')

def handle_client(client_socket, server_private_key, aes_key):
    # Send confirmation "Ready"
    iv = aes_key[::-1]
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    encrypted_ready = cipher_aes.encrypt(pad(FLAG_READY).encode())
    client_socket.sendall(encrypted_ready)

    # Receive client's name
    name = client_socket.recv(1024).decode()
    print(f"[+] Client name: {name}")

    threading.Thread(target=receive_messages, args=(client_socket, name, aes_key)).start()
    threading.Thread(target=send_messages, args=(client_socket, aes_key)).start()

def receive_messages(sock, name, aes_key):
    iv = aes_key[::-1]
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    while True:
        data = sock.recv(4096)
        if not data: break
        msg = unpad(cipher_aes.decrypt(data).decode())
        print(f"[{name}] {msg}")
        if msg == FLAG_QUIT:
            print(f"[!] {name} left the chat.")
            break

def send_messages(sock, aes_key):
    iv = aes_key[::-1]
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    while True:
        msg = input()
        encrypted = cipher_aes.encrypt(pad(msg).encode())
        sock.sendall(encrypted)
        if msg == FLAG_QUIT:
            print("[!] You left the chat.")
            break

def main():
    host = input("Host [0.0.0.0]: ") or "0.0.0.0"
    port = int(input("Port [9999]: ") or "9999")

    # Generate RSA keys
    server_rsa = RSA.generate(2048)
    server_pub_key = server_rsa.publickey()

    # Generate AES key (shared secret)
    aes_key = os.urandom(16)
    print(f"[+] AES session key: {aes_key.hex()}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    color_print(f"[+] Listening on {host}:{port}", color='green')

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Connection from {addr}")

        # Step 1: send server public key
        client_socket.sendall(server_pub_key.export_key())

        # Step 2: receive encrypted AES key from client
        encrypted_key = client_socket.recv(256)
        cipher_rsa = PKCS1_OAEP.new(server_rsa)
        decrypted_key = cipher_rsa.decrypt(encrypted_key)

        if decrypted_key == aes_key:
            color_print("[+] AES key match! Secure channel established.", color='green')
            handle_client(client_socket, server_rsa, aes_key)
        else:
            color_print("[!] AES key mismatch, closing connection.", color='red')
            client_socket.close()

if __name__ == "__main__":
    main()
