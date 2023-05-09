import socket
import pickle
import threading

PORT = 9000
IP = '192.168.1.1' # need to be changed for each node in subnet 192.168.1.0

class pack:
    dest = ''
    returnValue = 0 # 0 if message go upward, 1 if message go downward    
    message = 'hello world'

    def __init__(self, stt, dst, msg):
        self.start = stt
        self.dest = dst
        self.message = msg

    def setTarget(self, dst):
        self.dest = dst
    
    def setStart(self, st):
        self.start = st


def main():

    if IP == '192.168.1.1':
        #send message
        sendmsg = pack('192.168.1.1', '192.168.1.3', 'hello world!')
        sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendSock.connect(('192.168.1.2', PORT))
        sendSock.sendall(pickle.dumps(sendmsg))
        print("message send")
        sendSock.close()

    while(1):    

        recvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recvSock.bind(('', PORT))
        recvSock.listen(1)
        connetcionSocket, addr = recvSock.accept()
        received = pickle.loads(connetcionSocket.recv(1024))
        recvSock.close()

        if IP == '192.168.1.1':
            print('received ' + received.message)

        else:    
            tgt = ''
            if IP == '192.168.1.2':
                # relay message
                received.message += (' -> ' + IP)
                if received.returnValue == 0:
                    tgt = '192.168.1.3'
                elif received.returnValue == 1:
                    tgt = '192.168.1.1'
                print('relay message :' + received.message)
            
            elif IP == '192.168.1.3':
                # return messag
                received.message += (' -> ' + IP)
                received.returnValue = 1
                tgt = '192.168.1.2'
                print('return message :' + received.message)

            sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sendSock.connect((tgt, PORT))
            sendSock.sendall(pickle.dumps(received))
       
if __name__ == '__main__':
    main()