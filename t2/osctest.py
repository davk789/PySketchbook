"""
osctest.py

establish an OSC listener. Receiving messages from Open Sound Control should
not take any time, thought or testing in the python domain.

copying from http://wiki.python.org/moin/UdpCommunication
"""

import socket

udp_ip = "192.168.2.8"
udp_port = 57120

sock = socket.socket(socket.AF_INET,    # from internet
                     socket.SOCK_DGRAM) # UDP packet

sock.bind((udp_ip, udp_port))

while True:
    data, addr = sock.recvfrom(1024)
    print "received msg:", data
    