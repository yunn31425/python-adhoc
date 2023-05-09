import socket
import pickle
import threading

PORT = 9000

class pack:
    dest = ''
    returnValue = 0 # 0 if message go upward, 1 if message go downward    
    message = 'hello world from'

    def __init__(self, stt, dst, msg):
        self.start = stt
        self.dest = dst
        self.message = msg

    def setTarget(self, dst):
        self.dest = dst
    
    def setStart(self, st):
        self.start = st


def main():
       
    print('for 192.168.1.1')

    while(1):        
        sendmsg = pack('192.168.1.1', '192.168.1.3', 'hello world!')
        sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendSock.connect(('192.168.1.2', PORT))
        sendSock.sendall(pickle.dumps(sendmsg))

        recvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recvSock.bind(('', PORT))
        recvSock.listen(1)
        connetcionSocket, addr = recvSock.accept()
        received = pickle.loads(connetcionSocket.recv(1024))
        recvSock.close()

        print(received.message)
       
if __name__ == '__main__':
    main()