from socket import *
import threading
global message
global sentence
message = ''
class sendMsg_thread(threading.Thread):
	def __init__(self,serverName,serverPort,clientSocket):
		threading.Thread.__init__(self)
		self.name = serverName
		self.port = serverPort
		self.client = clientSocket
	def run(self):
			sendMsg(self.name,self.port,self.client)
def sendMsg(serverName,serverPort,clientSocket):
	global message
	global sentence
	while True:
		try:
			
			if sentence != 'sair()':	
				message = raw_input()
				clientSocket.sendto(message,(serverName, serverPort))
			if message == "sair()" or sentence == 'sair()':
				clientSocket.close() 
				break	
		except:
			clientSocket.close() 		
			break
	
serverName = '' 
serverPort = 1200
clientSocket = socket(AF_INET,SOCK_STREAM) 
clientSocket.connect((serverName, serverPort)) 
while True:
	count = 0
	sentence = raw_input('Nickname: ')
	size = len(sentence)
	for i in sentence:
		if i == ' ':
			count = count + 1
	if count == size:
		print 'invalid Nickname'				
	if count != size:
		break
clientSocket.send(sentence)
print("welcome to the chat! \n Menu: \n sair() : Close the chat \n lista() : Show the chat users \n nome('new name') : to change Nickname   \n")
reciveSentence = clientSocket.recv(1024)
print '\r'+reciveSentence+''
msg = sendMsg_thread(serverName,serverPort,clientSocket)
msg.start()
while 1:
	if(message == "sair()"):
		print "leaving the chat"
		break
	if(sentence != 'sair()'):	
		sentence = clientSocket.recv(1024)
	elif(sentence == 'sair()'):
		print 'Server out'
		clientSocket.close()
		break
	print sentence
