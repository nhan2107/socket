import socket
import webbrowser

def CreateServer(host, port): 
	Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Server.bind((host,port))
	Server.listen(6)
	return Server

def ReadRequest(Client):
	re = ""
	Client.settimeout(1)
	try:
		re = Client.recv(1024).decode()
		while (re):
			re += Client.recv(1024).decode()
	except socket.timeout:
		if not re:
			print("Didn't receive data! [Timeout]")
	finally:
		return re

def ReadHTTPRequest(Server): 
	re = ""
	while (re == ""):
		Client, address = Server.accept()
		print("Client: ", address," connected to the server")
		re = ReadRequest(Client)
	return Client, re

def SendFileIndex(Client): 
	f = open ("index.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Length: %d

"""%len(L)
	print("-----------HTTP responce  Index.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def MovePageIndex(Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8001/index.html

"""
	print("--------------HTTP responce move Index.html: ")
	print(header)
	Client.send(bytes(header,'utf-8'))

def MoveHomePage(Server, Client, Request):
	if "GET /index.html HTTP/1.1" in Request: 
		SendFileIndex(Client)
		Server.close()
		return True
	if "GET / HTTP/1.1" in Request:
		MovePageIndex(Client)
		Server.close()
		Server = CreateServer("localhost", 8001)
		Client, Request = ReadHTTPRequest(Server)
		print("------------------HTTP request: ")
		print(Request)
		MoveHomePage(Server, Client, Request)
		return True


def CheckPass(Request): 
	if "POST / HTTP/1.1" not in Request:
		return 0
	if "Username=admin&Password=admin" in Request: 
		return 1
	if "Username=files&Password=files" in Request: 
		return 2
	else: 
		return 0


def Move404Error(Server, Client): 
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8002/404.html

"""
	print("HTTP responce: ")
	print(header)
	Client.send(bytes(header,"utf-8"))
	Server.close()

def SendFile404Error(Client): 
	f = open ("404.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L) 
	print("HTTP responce file 404.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def Send404Error(Server, Client): 
	Server = CreateServer("localhost", 8002)
	Client, Request = ReadHTTPRequest(Server)
	print("HTTP Request: ")
	print(Request)
	if "GET /404.html HTTP/1.1" in Request:
		SendFile404Error(Client)
	Server.close()

def MoveFiles(Server, Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8002/files.html

"""
	print("HTTP responce: ")
	print(header)
	Client.send(bytes(header,"utf-8"))
	Server.close()

def SendFileFiles(Client): 
	f = open ("files.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
	print("-----------------HTTP responce  Files.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))	

def SendFiles(Server, Client):
	Server = CreateServer("localhost", 8002)
	Client, Request = ReadHTTPRequest(Server)
	print("HTTP Request: ")
	print(Request)
	if "GET /files.html HTTP/1.1" in Request:
		SendFileFiles(Client)
	Server.close()

def MoveInfo(Server, Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8002/info.html

"""
	print("HTTP responce: ")
	print(header)
	Client.send(bytes(header,"utf-8"))
	Server.close()

def SendFileInfo(Client): 
	f = open ("info.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
	print("-----------------HTTP responce  Info.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def SendInfo(Server, Client):
	Server = CreateServer("localhost", 8002)
	Client, Request = ReadHTTPRequest(Server)
	print("HTTP Request: ")
	print(Request)
	if "GET /info.html HTTP/1.1" in Request:
		SendFileInfo(Client)
	Server.close()

if __name__ == "__main__":
	print("Open a web browser and access the server ...")
	ulr="http://127.0.0.1:8000/index.html"
	webbrowser.open_new(ulr)
	Server = CreateServer("localhost",8000)
	Client, Request = ReadHTTPRequest(Server)
	print("-------------HTTP request: " )
	print(Request)
	MoveHomePage(Server, Client, Request)

	Server = CreateServer("localhost",10000)
	Client, Request = ReadHTTPRequest(Server)
	print("-------------HTTP request: " )
	print(Request)
	if CheckPass(Request) == 1: 
		MoveInfo(Server, Client)
		SendInfo(Server, Client)
	if CheckPass(Request) == 2: 
		MoveFiles(Server, Client)
		SendFiles(Server, Client)
	else: 
		Move404Error(Server, Client)
		Send404Error(Server, Client)