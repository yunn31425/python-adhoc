import socket
import pickle
import threading

PORT = 9000
IP = '192.168.1.1' # ip of current node, need to be changed for each node in subnet 192.168.1.0
START_IP = '192.168.1.1' # node which send message to the next node

class pack:
    start = ''
    dest = ''
    returnValue = 1 # 1 if message go upward, -1 if message go downward    
    message = 'hello world'

    def __init__(self, stt, dst, msg):
        self.start = stt
        self.dest = dst
        self.message = msg

    def setDest(self, dst):
        self.dest = dst
    
    def setStart(self, st):
        self.start = st

    def turnAround(self):
        tmp = self.dest
        self.dest = self.start
        self.start = tmp
        self.returnValue = self.returnValue*(-1)

def initRevSock():
    recvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recvSock.bind(('', PORT))
    recvSock.listen(1)

    return recvSock

def initmsg():
    return pack('192.168.1.1', '192.168.1.3', 'start - 192.168.1.1')

def rcvMsg(recvSock) -> pack:
    connectionSocket, addr = recvSock.accept()
    received = pickle.loads(connectionSocket.recv(1024))

    return received

def sendMsg(port, ipAdr, msg=None):
    if msg is None:
        msg = initmsg()
    
    sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sendSock.connect((ipAdr, port))
    sendSock.sendall(pickle.dumps(msg))
    print("message send")
    sendSock.close()

def SetDest(ipadr, twd):
    return ipadr[:-1] + str(int(ipadr[-1]) + twd)

def main(): 

    if IP == START_IP:
        sendMsg(PORT, '192.168.1.2')

    recvSock = initRevSock()
    
    while(1):            
        received = rcvMsg(recvSock)
        print('msg arrived :' + received.message)

        if received.dest == IP:            
            if received.returnValue == -1:
                break # got back
      
            received.turnAround()     

        received.message += " -> " + IP
        sendMsg(PORT, SetDest(IP, received.returnValue), received)
       
if __name__ == '__main__':
    main()
