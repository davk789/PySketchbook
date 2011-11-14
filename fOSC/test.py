'''
Created on Oct 23, 2011

@author: davk
'''

import socket
from scosc import tools, controller
from scsynth import voicer

class fOSCTestSynth(voicer.PolySynth):
    def __init__(self, name=None):
        super(fOSCTestSynth, self).__init__(name)
        self.name = "fOSC-polyVoice"
        self.params = {'mfreq' : 100,
                       'freq'  : 200,
                       'lev'   : 0.2 }
        self.s = controller.Controller(("192.168.1.100", 57111))
    
    def note_on(self, note, args):
        print "on", note, args
        super(fOSCTestSynth, self).note_on(note, args)
    
    def note_off(self, note, args):
        print "off", note, args
        super(fOSCTestSynth, self).note_off(note, args)
    
    def mod(self, note, args):
        print "move", note, args
        super(fOSCTestSynth, self).mod(note, args)


def create_socket(ip="192.168.1.100", port=57200):
    
    sock = socket.socket(socket.AF_INET,    # from internet
                         socket.SOCK_DGRAM) # UDP packet
    
    sock.bind((ip, port))
    return sock

def recv_msg(msg, synth):
    freq = msg[2] * 300 + 25
    mfreq = msg[3] * 300 + 25
    if msg[0] == '/fOSC/start':
        synth.note_on(msg[1], ('freq', freq, 'mfreq', mfreq))
    elif msg[0] == '/fOSC/end':
        synth.note_off(msg[1], ('freq', freq, 'mfreq', mfreq))
    elif msg[0] == '/fOSC/move':
        synth.mod(msg[1], ('freq', freq, 'mfreq', mfreq))
    
def start_server():
    "Start the server and run the synth."
    print "starting the audio server..."
    synth = fOSCTestSynth()
    sock = create_socket()
    while True:
        data = sock.recvfrom(2**13)
        
        recv_msg(tools.decode(data[0]), synth)
    print "all done"
    
class fOSCConverter(object):
    """make other osc clients communicate with the fOSC test server"""
    def __init__(self, synth):
        super(fOSCConverter, self).__init__()
        self.active_voices = {}
        self.active = False
        self.synth = synth
    
    def oscemote_process_message(self, msg):
        "Convert OSCemote message to fOSC format for the test server."
        voice_status = msg[-2][1:]
        if len(voice_status) > 0:
            for i in range(len(voice_status)):
                self.active_voices[voice_status[i]] = (msg[i+2][1], 
                                                  msg[i+2][2], 
                                                  msg[i+2][3])
            if not self.active:
                command = "/fOSC/start"
            else:
                command = "/fOSC/move"
            print self.active_voices
            for id, vals in self.active_voices.items():
                recv_msg((command, vals[0], vals[1], vals[2]), self.synth)
            self.active = True
        else:
            for id, vals in self.active_voices.items():
                recv_msg(("/fOSC/end", vals[0], vals[1], vals[2]), self.synth)
            self.active_voices = {}
            self.active = False
        

def start_oscemote_server():
    print "starting the OSCemote server..."
    sock = create_socket()
    synth = fOSCTestSynth()
    converter = fOSCConverter(synth)
    while True:
        data = sock.recvfrom(2**13)
        
        converter.oscemote_process_message(tools.decode(data[0]))
    print "all done"
    
def start_test_server():
    print "starting the test server..."
    sock = create_socket()
    while True:
        data = sock.recvfrom(2**13)
        
        print tools.decode(data[0])
    print "all done"

if __name__ == '__main__':
    #start_server()
    #start_test_server()
    start_oscemote_server()

