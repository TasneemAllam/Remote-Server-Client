import socket
import threading
import random
import time

global oval , s_seq, rnum ,busy, rseq , pointer_list
busy = False
oval = -1
s_seq = 1
rnum = 0
rseq = 0

def create_files():
    for i in range(0, 8):
        f = open('log' + str(i), 'w+')
        if i < 4:
            f.write('Client type: Reader\nClient Name: ' + str(i) + '\nrSeq\tsSeq\toVal\n' + str(rseq)+'\t'+str(sseq)+'\t'+str(oval)+'\n')
        else:
            f.write('Client type: Writer\nClient Name: ' + str(i) + '\nrSeq\tsSeq\n'+str(rseq)+'\t'+str(sseq)+'\n')


#client threading with the connection and address returned from accept
class clientth(threading.Thread):
    def __init__(self,conn,address,num_access):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.num_access = num_access
    #recive client connection with id and type if the type read send data if write override oval id with the conn_id
    def run(self):
        global oval, s_seq, rnum ,busy ,pointer_list , rseq
        pointer_list = { }

        for i in range (0,int(self.num_access)):
            rec = self.conn.recv(1024)
            print "received req", rec
            typ, id = rec.split(',',1)
            rseq +=1
            f_read = open('readers ', 'a+')
            f_write = open('writers ', 'a+')
            if typ == 'read':
                self.conn.send(str(oval))
                if  i == 0:
                    rnum += 1
                    #print "rnumb",rnum
                #write in the readers file
                f_read.write(str(s_seq)+"\t\t"+str(oval)+"\t\t"+ str(id) +"\t\t"+str(rnum)+ "\t\t"+str(rseq) + "\n")
                #create_files(rseq,s_seq)
            elif typ == 'write':
                while busy: print busy
                busy = True
                oval = id
                #pointer_list[pointer]
                self.conn.send("OK.")
                f_write.write(str(s_seq)+"\t\t"+str(oval)+"\t\t"+str(id)+"\t\t"+str(rseq)+"\n")
                #create_files(rseq,s_seq,oval)
                busy = False

            f_write.close()
            f_read.close()
            pointer = str(id) + str(i)
            s_seq+=1
            pointer_list[pointer] = rseq
            print "pointer list " , pointer_list , "\n"
            time.sleep(random.randint(0,60))
        if typ == 'read':
            rnum -=1
            #print " rnumf ",rnum

        self.conn.close()


# Create socket (allows two computers to connect)
def socket_create():
    try:

        global s
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind socket to port (he host and port the communication will take place) and wait for connection from client
def socket_bind(ip, port):
    try:

        global s
        print("Binding socket to port: " + str(port))
        s.bind((ip, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")


# Establish connection with client (socket must be listening for them)
def socket_accept(num_access):
    conn, address = s.accept()
    print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))

    #initiate thread with conn, address
    thread = clientth(conn , address, num_access)
    thread.start()

def servercall(ip,port,num_access):
    socket_create()
    socket_bind(ip, port)
    while True:
        socket_accept(num_access)


