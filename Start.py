import threading
from Server import servercall
from reader  import readercall
from writer import writercall
import paramiko
import sys
def ssh(command):
    nbytes = 4096
    hostname = '172.20.10.14'
    port = 22
    username = 'rana'
    password = 'rana95'
    client = paramiko.Transport((hostname, port))
    client.connect(username=username, password=password)

    stdout_data = []
    stderr_data = []
    session = client.open_channel(kind='session')

    session.exec_command(command)

    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(nbytes))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(nbytes))
        if session.exit_status_ready():
            break

    print 'exit status: ', session.recv_exit_status()
    print ''.join(stdout_data)
    print ''.join(stderr_data)


class serverth(threading.Thread):
    def __init__(self,ip,port,num_access):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.num_access = num_access

    #run the thread
    def run(self):
        servercall(self.ip, self.port,self.num_access)

    #read from the file
def read_file():
    Dic = {}
    with open("System.properties") as f:
        for line in f:
            name, value = line.split("=")
            Dic[name.strip()] = value.strip()
        print Dic
    return Dic

#readers thread to intiate readers with id
class readerth(threading.Thread):
    def __init__(self, ip, port, num_access,id):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.num_access = num_access
        self.id =id

    def run(self):
       command = 'python ./PycharmProjects/Clients/reader.py ' \
                 + str(self.ip) + ' ' + str(self.port) + ' ' + str(self.id) + ' ' + str(self.num_access)
       ssh(command)



#client thread to intiate writers id
class writerth(threading.Thread):
    def __init__(self, ip, port, num_access,id):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.num_access = num_access
        self.id = id

    def run(self):
        command = 'python ./PycharmProjects/Clients/writer.py ' \
                  + str(self.ip) + ' ' + str(self.port) + ' ' + str(self.id) + ' ' + str(self.num_access)
        ssh(command)

#create files
def create_files():
    for i in range(0, 8):
        f = open('log' + str(i), 'w+')
        if i < 4:
            f.write('Client type: Reader\nClient Name: ' + str(i) + '\nrSeq\tsSeq\toVal\n' )
        else:
            f.write('Client type: Writer\nClient Name: ' + str(i) + '\nrSeq\tsSeq\n')

    f = open('readers ', 'w+')
    f.write('sSeq\toVal\trID\t\trNum\trSeq\n')

    f = open('writers ', 'w+')
    f.write('sSeq\toVal\twID\t\trSeq\n')

create_files()
#read system.properties
r = read_file()
#create server with the values readed from read file
thread = serverth(r["server"],int (r["server.port"]), int(r["numberOfAccesses"]))

#start server with the values returned from serverth
thread.start()


for i in range(0, int (r["numberOfReaders"])):
    #start each reader thread
    reader = readerth(r["server"],int (r["server.port"]), int (r["numberOfAccesses"]),i)
    reader.start()


for i in range(0, int(r["numberOfWriters"])):
    #start each writers thread
    writer = writerth(r["server"],int (r["server.port"]), int (r["numberOfAccesses"]),i+int(r["numberOfReaders"]))
    writer.start()