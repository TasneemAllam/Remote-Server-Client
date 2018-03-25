import socket
import random
import time
import Pyro4
from sys import argv

def readercall(ip,port,id,num_access,*args):

    f = open('log' + str(id), 'w+')
    f.write('Client type: Reader\nClient Name: ' + str(id) + '\nrSeq\tsSeq\toVal\n')

    ns = Pyro4.locateNS(host=ip)

    uri = ns.lookup('obj')

    Object = Pyro4.Proxy(uri)


    for i in range(0, int(num_access)):

        Oval ,s_seq ,pointer = Object.excute_reader(id)


    f.close()

readercall(*argv[1:])
