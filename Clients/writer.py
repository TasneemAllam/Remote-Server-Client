import socket
import random
import time
import Pyro4
from sys import argv

def writercall(ip,port,id,num_access,*args):

    global s

    f = open('log' + str(id), 'w+')
    f.write('Client type: Writer\nClient Name: ' + str(id) + '\nrSeq\tsSeq\n')
    import Pyro4

    ns = Pyro4.locateNS(host = ip)

    uri = ns.lookup('obj')

    Object = Pyro4.Proxy(uri)

    for i in range(0, int(num_access)):
       confirm, s_seq, pointer  = Object.execute_writer(id)




writercall(*argv[1:])