'''
Created on Aug 10, 2011

@author: davk
'''
import sys
import socket
#import pyo
import scosc
#import time


def main():
    
    def print_message(msg):
        print 'GOT MESSAGE: %s' % msg
        
    listener = scosc.listener.Listener(socket.socket(57120))
    listener.register(None, print_message)

    print "Listening for messages, press enter to quit."
    listener.start()
    sys.stdin.read(1)
    listener.quit()
    listener.join()

if __name__ == "__main__":
    main()
