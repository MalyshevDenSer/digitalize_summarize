import socket

server = socket.create_server(('localhost', 8000))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.listen(10)

client_socket, address = server.accept()
recieved_data = client_socket.recv(1024).decode('utf-8')

print(recieved_data)

path = recieved_data.split()[1]
response = f'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n' \
            f'Привет! <br />Path :{path}'
client_socket.send(response.encode('utf-8'))
client_socket.shutdown(socket.SHUT_RDWR)

server.close()