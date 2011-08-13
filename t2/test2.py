'''
Created on Aug 10, 2011

Testing a few key concepts before moving on here.

@author: davk
'''
import threading
import scosc
import time

class ThreadTest(threading.Thread):
    def __init__(self, id=None):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        self.run_threaded()

    def run_threaded(self):
        for i in range(4):
            print("process: %i\titeration: %i\n" % 
                  (self.id, i))
            time.sleep(0.2)

def main_threading():

    print "checking threading"
    
    for i in range(8):
        t = ThreadTest()
        t.id = i
        t.start()
        # t.join would make the rest of the program wait before
        # the next iteration
        #t.join()
        time.sleep(0.1)

def mainsock():
    "This is how to receive data packets from a network."
    import socket
    from scosc import tools
    # rolling my own listener. I can double check this when it is time to 
    # use the library to send out data to sc.
    udp_ip = "192.168.2.8" # the ip address of this computer on the network
    udp_port = 57120 # the output port from TouchOSC
    
    sock = socket.socket(socket.AF_INET,    # from internet
                         socket.SOCK_DGRAM) # UDP packet
    
    sock.bind((udp_ip, udp_port))
    
    while True:
        data, addr = sock.recvfrom(2**13) # patrick uses this
        print tools.decode(data)
        print addr

def main():
    import scosc
    
    s = scosc.Controller(("192.168.2.8", 57120))
    
    print s.receive()
    
    
        
if __name__ == "__main__":
    main()
