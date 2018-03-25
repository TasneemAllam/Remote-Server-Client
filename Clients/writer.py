import socket
import random
import time
from sys import argv

# Create a socket
def socket_create():
    try:

        global s
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect(ip,port):
    try:

        global s
        s.connect((ip,int(port)))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))

def writercall(ip,port,id,num_access,*args):

    global s

    f = open('log' + str(id), 'w+')
    f.write('Client type: Writer\nClient Name: ' + str(id) + '\nrSeq\tsSeq\n')

    for i in range(0, int(num_access)):
        socket_create()
        socket_connect(ip,int(port))

        s.send("write," + str(id))
        rec = s.recv(1024)
    print "Request send from Writer ", id



writercall(*argv[1:])