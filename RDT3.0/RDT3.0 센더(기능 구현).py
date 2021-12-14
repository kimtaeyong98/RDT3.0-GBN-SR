import threading
import random
from socket import *
import time 

server = '127.0.0.1'
Port = 20202
clientSocket = socket(AF_INET, SOCK_DGRAM)

count=int(input("패킷 전송 수:"))
RTT=float(input("RTT(sec):"))
loss=float(input("패킷 손실 확률(0~1):"))
pre_prob=float(input("premature timeout 확률(0~1):"))
mt=float(input("시간(sec):"))


TIMEOUT = RTT
seqnum = 0
check = 0
ACK = -1
num=0

clientSocket.sendto(str(count).encode(), (server, Port))
clientSocket.sendto(str(loss).encode(), (server, Port))
clientSocket.sendto(str(pre_prob).encode(), (server, Port))
clientSocket.sendto(str(mt).encode(), (server, Port))
clientSocket.sendto(str(TIMEOUT).encode(), (server, Port))

def change_0_to_1():#0을 1로 바꾸고 1을 0으로 바꾸는 함수
    global seqnum
    if seqnum == 0:
        seqnum = 1
    else:
        seqnum = 0
        
def timeout():#타이머
    global pk_st
    global check
    while True:
        if check == 1:
            check = 0
            break
        elif time.time() - pk_st > TIMEOUT:
            clientSocket.sendto(message.encode(), (server, Port))
            pk_st = time.time()  # 시작 시간 저장
        else:
            continue
        

i = 0
runtime=time.time()
while True:
    message = str(seqnum)
    clientSocket.sendto(message.encode(), (server, Port))
    pk_st = time.time()
    
    t = threading.Thread(target=timeout, args=())
    t.start()

    ACK, Add = clientSocket.recvfrom(2048)
    num+=1
    check = 1
    ACK = int(ACK.decode())
    change_0_to_1()
    i+=1
    t.join()
    if num == count:
        break
    if time.time()-runtime>mt:
        break

print("송신 완료")
