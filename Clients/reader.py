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
        s.connect((ip, int(port)))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))



def readercall(ip,port,id,num_access,*args):
    global s

    f = open('log' + str(id), 'w+')
    f.write('Client type: Reader\nClient Name: ' + str(id) + '\nrSeq\tsSeq\toVal\n')

    socket_create()
    socket_connect(ip,int(port))

    for i in range(0, int(num_access)):
        s.send("read,"+str(id))
        rec = s.recv(1024)
    print "Request send from Reader ", id


    f.close()

readercall(*argv[1:])
