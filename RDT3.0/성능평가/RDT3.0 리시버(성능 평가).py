from socket import *
import time 
import threading
import random


serverPort = 20202
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1',serverPort))

print ('리시버 준비 완료')
print()

message, clientAddress = serverSocket.recvfrom(2048)
count=int(message.decode())
message, clientAddress = serverSocket.recvfrom(2048)
loss=float(message.decode())
#message, clientAddress = serverSocket.recvfrom(2048)
#pre_prob=float(message.decode())
message, clientAddress = serverSocket.recvfrom(2048)
mt=float(message.decode())
message, clientAddress = serverSocket.recvfrom(2048)
TIMEOUT=float(message.decode())
RTT=0

before_seq = -1
flag=0
message_count=0

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    if flag==0:
        flag=1
        st=time.time()#시작 시간
        
    if random.random() <loss:#패킷로스
        #print('패킷 로스')
        continue
    
    if random.random() < loss:#ack 로스
        if before_seq != int(message.decode()):
            #print(message.decode())#출력
            message_count+=1
        #print('ACK 로스')
        before_seq = int(message.decode())
        continue
    
    else:#ack로스가 아니면
        if before_seq == int(message.decode()):#중복 패킷이라면
            serverSocket.sendto(str(message.decode()).encode(), clientAddress)
        else:#중복 패킷이 아니라면
            before_seq = int(message.decode())
            #print(message.decode())#출력
            message_count+=1
            RTT=random.uniform(0.008,0.012)
            if RTT>TIMEOUT:#premature timeout
                time.sleep(TIMEOUT)
                #serverSocket.sendto(str(message.decode()).encode(), clientAddress)
                #print("premature timeout")
                #print()
            serverSocket.sendto(str(message.decode()).encode(), clientAddress)
    if time.time()-st>mt:
        break 
print("효율",message_count//mt)


