from socket import *
import time
import random

IP = "127.0.0.1"
Port = 20202

loss= float(input("패킷 손실 확률(0~1) "))
#dpp=float(input("premature timeout 확률(0~1) "))

rcvSocket = socket(AF_INET, SOCK_DGRAM)
rcvSocket.bind((IP, Port))

print("리시버 준비 완료", end="\n\n")


message, clientAddress = rcvSocket.recvfrom(2048)
mt=float(message.decode())
message, clientAddress = rcvSocket.recvfrom(2048)
timeout=float(message.decode())

flag=0

expectedSeq = -1    # 받을 seq 번호 
message_count=0
while True:
    message, clientAddress = rcvSocket.recvfrom(2048)
    if(flag==0):
        flag=1
        st=time.time()
    message = message.decode()

    
    if int(message) == expectedSeq + 1:
        if random.random() < loss:#패킷 loss
            #print("data loss",'[',message,']')
            continue
        #print(message)
        message_count+=1
        expectedSeq = expectedSeq + 1
        if random.random() < loss:#loss패
            #print("ack loss",'[',message,']')
            continue
        else:
            RTT=random.uniform(0.008,0.012)
            if RTT>timeout:
                #print("premature timeout",'[',message,']')
                time.sleep(timeout)  
            rcvSocket.sendto(str(expectedSeq).encode(), clientAddress)

    if(time.time()-st>mt):
        break

print("효율:",float(message_count)//mt)
print("효율:",float(message)//mt)

