## All file content
import socket

clisock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
clisock.connect( ('', 8000) )
clisock.send("Hello World\n")
print clisock.recv(100)
clisock.close()



