import socket
import sys
from Queue import *
from thread import *
import threading

HOST = ""
PORT = 8880
hostQueue = Queue(maxsize = 10)
criticalSection = 0

def clientthreadrun(conn):
    global criticalSection
    global hostQueue
    while True:
        msg = conn.recv(1024)
        lock = threading.Lock()
        if msg:
            print "Coordinator recieved:"
            print msg
            if msg=="REQUEST":
                if criticalSection == 0:
                    #with lock:
                    criticalSection=1
                    print "Coordinator send:"
                    print "GRANTED"
                    conn.sendall('GRANTED')
                else:
                    hostQueue.put("added")
                    print "Coordinator send:"
                    print "DENIED"
                    conn.sendall("DENIED")
            elif msg=="RELEASE":
                if not hostQueue.empty():
                    hostQueue.get()
                    if hostQueue.empty():
                        criticalSection = 0
                    print "Coordinator send:"
                    print "GRANTED"
                    conn.sendall("GRANTED")
                else:
                    print "Coordinator send:"
                    print "DENIED"
                    conn.sendall("DENIED")
        if not msg:
            break
    conn.close()

try:
    sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error,msg:
    print 'Failed to create socket. Error code:' +str(msg[0])+ ', Error message: ' + msg[1]
    sys.exit()
print 'Server socket created'
    
try:
    sck.bind((HOST,PORT))
except socket.error,msg:
    print 'Bind Failed. Error code: ' + str(msg[0]) + ' message: ' + msg[1]
    sys.exit()

print 'Socket Bind Complete'
sck.listen(10)
print 'Socket now listening'
while 1:
    conn,addr = sck.accept()
    print 'Connected with ' + addr[0] + ' : ' + str(addr[1])
    start_new_thread(clientthreadrun,(conn,))
    
sck.close()
