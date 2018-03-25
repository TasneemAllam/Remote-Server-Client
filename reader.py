import socket

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
        s.connect((ip, port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))



def readercall(ip,port,id,num_access):
    global s
    for i in range(0,num_access):
        socket_create()
        socket_connect(ip,port)

        s.send("read,"+str(id))

