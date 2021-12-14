import threading
from threading import Lock
from socket import *
import time


# 패킷 정보
class Pkt:
    def __init__(self, seqNum, time):
        self._seqNum = seqNum
        self._time = time

    def getSeq(self):
        return self._seqNum

    def getTime(self):
        return self._time

    def setTime(self, time):
        self._time = time


windowSize = int(input("Window size: "))
RTT = float(input("RTT(sec):"))
timeOut = RTT#RTT보다 늦게 돌아 오면 TIMEOUT
packetNum = int(input("몇개의 패킷을 보낼 것인가?"))
mt = float(input("몇초동안 보낼 것인가(sec): "))




windowLock = Lock()

window = [] # 보낸 패킷 저장
SndNum = 0
ACK = -1    # 받을 ack 값
init_time = time.time()


def recieve():
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
                if tmp.getSeq() <= ACK:
                    window.remove(tmp)#삭제

            if ACK == packetNum - 1:
                break


IP = "127.0.0.1"
Port = 20202

sndSocket = socket(AF_INET, SOCK_DGRAM)
sndSocket.bind(("127.0.0.1", 0))
sndSocket.sendto(str(mt).encode(), (IP, Port))
sndSocket.sendto(str(timeOut).encode(), (IP, Port))

t = threading.Thread(target=recieve, args=())
t.start()

st=time.time()
while True:
    with windowLock:
        # 모든 패킷 보낸 후 탈출
        if ACK == packetNum - 1:
            break

    # 타임 아웃
    with windowLock:
        if len(window) > 0 and time.time() - window[0].getTime() >= timeOut:#모든 패킷의 timer
            for tmp in window:#패킷 재전송
                sndSocket.sendto(str(tmp.getSeq()).encode(), (IP, Port))
                tmp.setTime(time.time())
            continue

        # window가 가득 찼으면
        if len(window) == windowSize:
            continue

    # 패킷 시작 시간 초기화
    if SndNum == 0:
        init_time = time.time()

    # window 윈도우가 가득 안찼으면
    if SndNum < packetNum:
        pkt = Pkt(SndNum, time.time())#패킷 추가

        with windowLock:
            window.append(pkt)

        sndSocket.sendto(str(pkt.getSeq()).encode(), (IP, Port))
        SndNum = SndNum + 1
        
    if(time.time()-st > mt):
        print("시간 끝")
        break
        
