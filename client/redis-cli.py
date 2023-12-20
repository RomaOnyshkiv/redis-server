import os
import socket


def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        r = os.getenv("server2") if os.getenv("server2") else '127.0.0.1'
        sock.connect((f'{r}', 6379))
        sock.sendall(command.encode('utf-8'))
        response = sock.recv(1024)
        print(response.decode('utf-8'))


def main():
    while True:
        cmd = input("redis-cli> ")
        if cmd.lower() in ['exit', 'quit']:
            break
        send_command(cmd)


if __name__ == '__main__':
    main()
