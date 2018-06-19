from socket import *
import threading
import time
import os

global luser 
global lconn 
global lip 
global lprivate

luser = [] # list of users
lconn = [] # list of connections
lip = [] # list of ip



class mult_thread(threading.Thread):
	def __init__(self, serverSocket,serverPort):
		threading.Thread.__init__(self)
		self.socket = serverSocket
		self.port = serverPort
	def run(self):
		connManager(self.socket,self.port)

def connManager(socket,port):
	connectionSocket, addr = socket.accept()
	if connectionSocket != 'localhost':
		Nickname_in_list = "false"
		while Nickname_in_list == "false":
			Nickname = connectionSocket.recv(1024) 
			Nickname_in_list = "true"
			for i in range(0, len(luser)):
				if Nickname == luser[i]:
					Nickname_in_list = "false"
					connectionSocket.send("Name already in use, choose another nickname:")
					break
		luser.append(Nickname+"")
		lconn.append(connectionSocket)
		lip.append(addr)
		sentence = "client " + Nickname + " has connected "
		print(sentence)
		for all_users in lconn:
			all_users.send(sentence)
		thread1 = mult_thread(socket,port)
		thread1.start()
		
		while True:
			sentence = connectionSocket.recv(1024)
			try:
				if sentence[0:5] == "nome(" and sentence[-1] == ')':
					New_Nickname_list = "false"
					if sentence == "nome()":
						New_Nickname_list = "false"
						connectionSocket.send("The name must not be empty")
					else:
						for i in range(0, len(luser)):
							if sentence[5:len(sentence)-1] == luser[i]:
								New_Nickname_list = "false"
								connectionSocket.send("Name already in use, choose another nickname:")
								break
							else:
								New_Nickname_list = "true"
					if New_Nickname_list == "true":
						luser[luser.index(Nickname)] = sentence[5:len(sentence)-1]
						for all_users in lconn:
							all_users.send(Nickname +" changed to " + sentence[5:len(sentence)-1])
						print(Nickname +" changed to " + sentence[5:len(sentence)-1])						
						Nickname = sentence[5:len(sentence)-1]
						continue
				elif sentence == "sair()":
					luser.remove(Nickname)
					lconn.remove(connectionSocket)
					lip.remove(addr)
					connectionSocket.close()
					print(Nickname + " left ")
					for all_users in lconn:
						all_users.send(Nickname + " left ")
					break
				elif sentence == 'lista()':
					for i in range(len(lconn)):
						connectionSocket.send("Nickname: " + luser[i] + " IP: " + lip[i][0] + " Port: " + str(port) + "\n"  )
					continue
				elif sentence != '':
					sentence = Nickname + " typed: " + sentence
				if sentence[0:5] != "nome(" and sentence[0:8] != "privado(":
					print(sentence)
					for all_users in lconn:
						all_users.send(sentence)
			except:
				break

serverName = ''
serverPort = 1200
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverName,serverPort)) 
serverSocket.listen(1) 
print("Welcome")
thread1 = mult_thread(serverSocket,serverPort)
thread1.start()
while True:
	config = raw_input('')
	if config == "sair()":
		for all_users in lconn:
				all_users.send("sair()")
		clientSocket.send('')					
		serverSocket.close()
		os._exit(1)
		break
	if config == "lista()":
		if len(luser) !=0:
			for i in range(len(luser)):
				print("Nickname: " + luser[i] + " IP: " + lip[i][0] + " Port: " + str(serverPort))
		else:
			print("No user logged in")
