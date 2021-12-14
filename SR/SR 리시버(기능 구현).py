from socket import *
import time
import random

rcvIP = "127.0.0.1"
rcvPort = 12000

dpp=float(input("premature timeout 확률(0~1) "))
windowSize = int(input("Window size: "))

rcvSocket = socket(AF_INET, SOCK_DGRAM)
rcvSocket.bind((rcvIP, rcvPort))

print("리시버 준비 완료", end="\n\n")


message, clientAddress = rcvSocket.recvfrom(2048)
mt=float(message.decode())
message, clientAddress = rcvSocket.recvfrom(2048)
timeout=float(message.decode())
message, clientAddress = rcvSocket.recvfrom(2048)
packet_loss_prob=float(message.decode())
message, clientAddress = rcvSocket.recvfrom(2048)
packetNum=int(message.decode())

window=[0]
flag=0
copy=-1
expectedSeq = 0# 받을 seq 번호
expectedSeq2 = -1
nextseq=1
o=0

while True:
    message, clientAddress = rcvSocket.recvfrom(2048)
    if(flag==0):
        flag=1
        st=time.time()
    if(time.time()-st>mt):
        break
    
    message = message.decode()
    if int(message)>copy:
        if len(window) < windowSize:
            window.append(int(message))
            
        if int(message) == expectedSeq :
            set2=set(window)
            window=list(set2)
            window.sort()
            for i in range(0,nextseq):
                print(window[0])
                del window[0]

            expectedSeq = expectedSeq + nextseq
            copy=int(message)   

        else:
            if len(window) == windowSize:
                continue
            nextseq=+1

        if random.random() < packet_loss_prob:#ack loss
            print("ack loss",'[',message,']')
            o+=1
        else:
            if random.uniform(0,1)<dpp:
                print("premature timeout",'[',message,']')
                time.sleep(timeout)
            expectedSeq2+=1    
            rcvSocket.sendto(str(expectedSeq2).encode(), clientAddress)
#print(int(message))        
         


