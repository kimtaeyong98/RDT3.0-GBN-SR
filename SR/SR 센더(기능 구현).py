from socket import *
import time
import threading
from threading import Lock
import random

# 패킷 정보
class Pkt:
    def __init__(self, seqNum, time):
        self._seqNum = seqNum
        self._time = time

    def getSeqNum(self):
        return self._seqNum

    def getTime(self):
        return self._time

    def setTime(self, time):
        self._time = time


windowSize = int(input("Window size: "))
RTT = float(input("RTT(sec):"))
timeOut = RTT#RTT보다 늦게 돌아 오면 TIMEOUT
packet_loss_prob=float(input("패킷 손실 확률(0~1): "))
packetNum = int(input("몇개의 패킷을 보낼 것인가?"))
mt = float(input("몇초동안 보낼 것인가(sec): "))




windowLock = Lock()

window = [] # 보낸 패킷 저장
pktSndNum = 0
ACK = -1    # 받을 ack 값
init_time = time.time()


def listener():
    global sndSocket
    global ACK
    global init_time
    global window
    global packetNum

    while True:
        ack, rcvAddress = sndSocket.recvfrom(2048)
        ack = int(ack.decode())
        

        with windowLock:
            if ack <= ACK:
                continue

            ACK = ack
            for tmp in window:
                if tmp.getSeqNum() <= ACK:
                    window.remove(tmp)#삭제

            if ACK == packetNum-1 :
                break


rcvIP = "127.0.0.1"
rcvPort = 12000

sndSocket = socket(AF_INET, SOCK_DGRAM)
sndSocket.bind(("127.0.0.1", 0))

sndSocket.sendto(str(mt).encode(), (rcvIP, rcvPort))
sndSocket.sendto(str(timeOut).encode(), (rcvIP, rcvPort))
sndSocket.sendto(str(packet_loss_prob).encode(), (rcvIP, rcvPort))
sndSocket.sendto(str(packetNum).encode(), (rcvIP, rcvPort))




t = threading.Thread(target=listener, args=())
t.start()

st=time.time()
while True:
    # 타임 아웃
    with windowLock:
        for k in range(0,len(window)-1):
            if len(window) > 0 and time.time() - window[k].getTime() >= timeOut:#개별 타이머
                sndSocket.sendto(str(window[k].getSeqNum()).encode(), (rcvIP, rcvPort))
            #continue    
            


        # window가 가득 찼으면
        if len(window) == windowSize:
            continue

    # 패킷 시작 시간 초기화
    if pktSndNum == 0:
        init_time = time.time()

    # window 윈도우가 가득 안찼으면
    if pktSndNum < packetNum:
        pkt = Pkt(pktSndNum, time.time())#패킷 추가

        with windowLock:
            window.append(pkt)

        sndSocket.sendto(str(pkt.getSeqNum()).encode(), (rcvIP, rcvPort))
        pktSndNum = pktSndNum + 1
        
    if(time.time()-st > mt):
        print("시간 끝")
        break

    with windowLock:
        # 모든 패킷 보낸 후 탈출
        if ACK == packetNum-1:
            break
        
