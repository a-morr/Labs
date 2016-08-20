import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

sock.sendall('rock')

while True:
	data = sock.recv(16)
	if data == 'you win!':
		break
	else:
		sock.sendall('rock')

sock.close()
