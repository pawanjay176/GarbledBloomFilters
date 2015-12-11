import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '127.0.0.1' # Get local machine name
port = 3000                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
s.send("Ye lo pk0")
