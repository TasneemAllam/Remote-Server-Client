import socket
import threading
import random
import time
import Pyro4

global oval , s_seq, rnum ,busy, rseq , pointer_list
busy = False
oval = -1
s_seq = 1
rnum = 0
rseq = 0

# def create_files():
#     for i in range(0, 8):
#         f = open('log' + str(i), 'w+')
#         if i < 4:
#             f.write('Client type: Reader\nClient Name: ' + str(i) + '\nrSeq\tsSeq\toVal\n' + str(rseq)+'\t'+str(sseq)+'\t'+str(oval)+'\n')
#         else:
#             f.write('Client type: Writer\nClient Name: ' + str(i) + '\nrSeq\tsSeq\n'+str(rseq)+'\t'+str(sseq)+'\n')

def servercall(ip,port,num_access):
    @Pyro4.expose
    class Clients:
        def execute_reader(self, id):
            global oval, s_seq, rnum, busy, pointer_list, rseq
            pointer_list = {}

            for i in range(0, int(num_access)):
                rseq += 1
                pointer = str(id) + str(i)
                pointer_list[pointer] = rseq
                print "pointer list ", pointer_list, "\n"
                f_read = open('readers ', 'a+')
                f = open('log' + str(id), 'a+')
                oval_temp = str(oval)
                if i == 0:
                    rnum += 1
                    # print "rnumb",rnum
                    # write in the readers file
                f_read.write(str(s_seq) + "\t\t" + str(oval) + "\t\t" + str(id) + "\t\t" + str(rnum) + "\t\t" + str(
                        pointer_list[pointer]) + "\n")
                f.write( str(pointer_list[pointer]) +"\t" + str(s_seq)+"\t"+ str(oval_temp)+"\n")
                    # create_files(rseq,s_seq)
                f_read.close()
                s_seq += 1
                time.sleep(random.randint(0, 60))
                rnum -= 1
                return oval_temp, s_seq, pointer_list[pointer]

        def execute_writer(self,id):
            global oval, s_seq, rnum, busy, pointer_list, rseq
            pointer_list = {}

            for i in range(0, int(self.num_access)):
                rseq += 1
                pointer = str(id) + str(i)
                pointer_list[pointer] = rseq
                print "pointer list ", pointer_list, "\n"

                f_write = open('writers ', 'a+')
                f = open('log' + str(id), 'a+')

                while busy: print busy
                busy = True
                oval = id
                # pointer_list[pointer]
                confirm = "OK."
                f_write.write(str(s_seq) + "\t\t" + str(oval) + "\t\t" + str(id) + "\t\t" + str(pointer_list[pointer]) + "\n")
                f.write(str(pointer_list[pointer]) + "\t" +str(s_seq) +"\n")
                # create_files(rseq,s_seq,oval)
                busy = False
                f_write.close()
                s_seq += 1
                time.sleep(random.randint(0, 60))
                rnum -= 1
                return confirm, s_seq ,pointer_list[pointer]

    daemon = Pyro4.Daemon(host= ip, port= port)

    uri = daemon.register(Clients)
    ns = Pyro4.locateNS()
    ns.register('obj', uri)
    print(uri)

    daemon.requestLoop()



