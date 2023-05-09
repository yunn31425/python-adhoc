import socket
import pickle

PORT = 9000

class pack:
    start = ''
    dest = ''
    returnValue = 0
    message = ''

    def __init__(self, node):
        start = node.ip

    def setTarget(target):
        dest = target
    
    def setStart(st):
        start = st

def send(dst, msg):
    pass


def main():
    '''for 192.168.1.2'''    
    while(1):
        recvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recvSock.bind(('', PORT))
        recvSock.listen(1)
        connetcionSocket, addr = recvSock.accept()
        received = pickle.loads(connetcionSocket.recv(1024))
        recvSock.close()
        received.message += ' -> 192.168.1.2 ->'
        if received.returnValue == 0:
            # heading to 192.168.1.3
            sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sendSock.connect(('192.168.1.3', PORT))
            sendSock.sendall(pickle.dumps(received))
        
        elif received.returnValue == 1:
            # heading to 192.168.1.2
            sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sendSock.connect(('192.168.1.1', PORT))
            sendSock.sendall(pickle.dumps(received))

if __name__ == '__main__':
    main()