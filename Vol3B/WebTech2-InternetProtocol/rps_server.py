import socket, random

moves = ['rock','paper','scissors']

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print 'starting up on ',server_address
sock.bind(server_address)
sock.listen(1)
keep_playing = True

while keep_playing:
	print 'waiting for a connection'
	connection, client_address = sock.accept()
	
	try:
		print 'connection from',client_address
		
		while True:
			data = connection.recv(16)
			
			if data:
				print 'received ',data
				
				if data in moves:
					mymoveindex = random.randint(0,2)
					mymove = moves[mymoveindex]
					yourmoveindex = moves.index(data)
					print data,' vs ',mymove
					if yourmoveindex == ((mymoveindex + 1) % 3):
						print 'sending congratulations'
						connection.sendall('you win!')
						keep_playing = False
					elif yourmoveindex == ((mymoveindex - 1) % 3):
						print 'gloating'
						connection.sendall('you lose!')
					else:
						print 'losing patience'
						connection.sendall('draw!')
				else:
					print 'criticizing poor decision'
					connection.sendall('Invalid move.')
				
			else:
				print 'no more data from',client_address
				break
            
	finally:
		connection.close()
