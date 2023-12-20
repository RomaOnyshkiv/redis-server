import socket
import threading


def handle_client(client_socket, data_store):
    while True:
        try:
            command = client_socket.recv(1024).decode('utf-8').strip()
            if not command:
                break

            parts = command.split()
            cmd = parts[0].upper()
            print(f'Command {cmd} will be executed')

            if cmd == 'PING':
                response = 'PONG'

            elif cmd == 'ECHO':
                response = ' '.join(parts[1:])

            elif cmd == 'SET':
                data_store[parts[1]] = parts[2]
                response = 'OK'

            elif cmd == 'GET':
                response = data_store.get(parts[1], '(nil)')

            elif cmd == 'DEL':
                if parts[1] in data_store:
                    del data_store[parts[1]]
                    response = '1'
                else:
                    response = '0'

            elif cmd == 'EXISTS':
                response = '1' if parts[1] in data_store else '0'

            elif cmd in ('INCR', 'DECR'):
                if parts[1] in data_store and data_store[parts[1]].isdigit():
                    data_store[parts[1]] = str(int(data_store[parts[1]]) + (1 if cmd == 'INCR' else -1))
                    response = data_store[parts[1]]
                else:
                    response = 'ERROR'

            elif cmd in ('LPUSH', 'RPUSH'):
                if parts[1] not in data_store:
                    data_store[parts[1]] = []
                if cmd == 'LPUSH':
                    data_store[parts[1]].insert(0, parts[2])
                else:
                    data_store[parts[1]].append(parts[2])
                response = str(len(data_store[parts[1]]))

            elif cmd == 'LRANGE':
                if parts[1] in data_store and isinstance(data_store[parts[1]], list):
                    start, end = int(parts[2]), int(parts[3])
                    response = ' '.join(data_store[parts[1]][start:end+1])
                else:
                    response = '(empty list or set)'

            elif cmd == 'ALL':
                response = '\n'.join(data_store)
            else:
                response = 'ERROR: Unknown Command'

            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()


def start_server():
    host, port = '0.0.0.0', 6379
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    data_store = {}

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, data_store))
            client_handler.start()
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()
