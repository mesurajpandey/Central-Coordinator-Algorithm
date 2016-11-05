import socket
import sys
from thread import *
import os
from random import randint

messageType = ["REQUEST","RELEASE"]

def createSocket(hostName):
    try:
        sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error,msg:
        print 'Failed to create socket. Error code:' +str(msg[0])+ ', Error message: ' + msg[1]
        sys.exit()
    print 'socket created'
    host = hostName
    try:
        #remote_ip = socket.gethostbyname(host)
        remote_ip = socket.gethostbyaddr(hostName)
        print remote_ip[2]
    except socket.gaierror:
        print 'Host name could not be resolved.Exiting..'
        sys.exit()

    #remote_ip = socket.gethostbyaddr("10.200.1.109")
    #remote_ip = socket.gethostbyname(hostName)
    #sck.connect((str(remote_ip[2]),port))
    
    sck.connect(('127.0.0.1',port))
    print 'Socket cnnected to ' + host + ' on ip ' + str(remote_ip[2])
    return sck,remote_ip
    

def getAllHosts():
    os.system('net view > conn.tmp')
    f = open('conn.tmp','r')
    f.readline();f.readline();f.readline()

    conn = []
    host = f.readline()
    while host[0] == '\\':
        conn.append(host[2:host.find(' ')])
        host = f.readline()
    hosts = conn
    f.close()

def sendRandomRequest(sck):
    try:
        sck.sendall(message)
    except socket.error:
        print 'Send Failed'
        return 0
    print 'Client Send:'
    print message
    return 1

def listenAll(sck):
    print "Client Recieve:"
    print sck.recv(1024)

def runServer():
    HOST = ""
    PORT = 8881
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
        msg = conn.recv(1024)
        if msg:
            print msg
            if msg=="GRANTED":
                print "Critical Section Entered"
            #conn.sendall("RELEASE")

port = 8880
[clientsocket,ip] = createSocket("127.0.0.1")
message = ""
#sendMessage(clientsocket,"REQUEST")
#print clientsocket.recv(1024)
#sendRandomRequest(clientsocket)
#start_new_thread(sendRandomRequest,(clientsocket,))
while 1:
    message = raw_input("Enter Client Request")
    success = sendRandomRequest(clientsocket)
    if success:
        listenAll(clientsocket)
#start_new_thread(listenAll,(clientsocket,))


