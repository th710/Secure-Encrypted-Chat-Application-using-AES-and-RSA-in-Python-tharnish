import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from lazyme.string import color_print
import threading

FLAG_READY = "Ready"
FLAG_QUIT = "quit"

def pad(s): return s + (16 - len(s) % 16) * '`'
def unpad(s): return s.replace('`', '')

def receive_messages(sock, aes_key):
    iv = aes_key[::-1]
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    while True:
        data = sock.recv(4096)
        if not data: break
        msg = unpad(cipher_aes.decrypt(data).decode())
        print(f"[Server] {msg}")
        if msg == FLAG_QUIT:
            print("[!] Server ended the chat.")
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
    host = input("Server host [127.0.0.1]: ") or "127.0.0.1"
    port = int(input("Port [9999]: ") or "9999")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Step 1: receive server's public key
    server_pub_pem = sock.recv(2048)
    server_pub_key = RSA.import_key(server_pub_pem)

    # Step 2: AES key must match server
    aes_key = input("[*] Enter AES key (hex) from server: ").strip()
    aes_key = bytes.fromhex(aes_key)

    # Step 3: send encrypted AES key to server
    cipher_rsa = PKCS1_OAEP.new(server_pub_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    sock.sendall(encrypted_key)

    # Step 4: receive confirmation
    iv = aes_key[::-1]
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    data = sock.recv(4096)
    msg = unpad(cipher_aes.decrypt(data).decode())
    if msg == FLAG_READY:
        print("[+] Secure channel established!")
        name = input("Your name: ")
        sock.sendall(name.encode())
        threading.Thread(target=receive_messages, args=(sock, aes_key)).start()
        threading.Thread(target=send_messages, args=(sock, aes_key)).start()
    else:
        print("[!] Failed to establish secure channel.")

if __name__ == "__main__":
    main()
