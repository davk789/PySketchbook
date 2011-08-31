"""
synth.py

Run the sequencer from python here.

"""
import socket
import time
import random
import threading
from scosc import controller, tools

s = controller.Controller(("127.0.0.1", 57110))

# all scales will be expressed as intervals
can_run = True
root = 55.0
scales = {'bohlen-pierce': (1.0/1.0,25.0/21.0,9.0/7.0,7.0/5.0,5.0/3.0,9.0/5.0,
                            15.0/7.0,7.0/3.0,25.0/9.0,3.0/1.0),
          'pythagorean':   (1.0/1.0, 9.0/8.0, 81.0/64.0,4.0/3.0,3.0/2.0,
                            27.0/16.0,243.0/128.0, 2.0/1.0),
          'partch':        (1.0/1.0,12.0/11.0,11.0/10.0,10.0/9.0,9.0/8.0,
                            8.0/7.0,7.0/6.0,6.0/5.0,11.0/9.0,5.0/4.0,
                            14.0/11.0,9.0/7.0,4.0/3.0,11.0/8.0,7.0/5.0,
                            10.0/7.0,16.0/11.0,3.0/2.0,14.0/9.0,11.0/7.0,
                            8.0/5.0,18.0/11.0,5.0/3.0,12.0/7.0,7.0/4.0,
                            16.0/9.0,9.0/5.0,20.0/11.0,11.0/6.0,2.0/1.0)
          }

defs = ["ts_sin_touch",
        "ts_swoop",
        "ts_sin_touch", # double the chances of the 2 straight sin oscs
        "ts_swoop",     # this one too
        "ts_hash",
        "ts_hash_blub",
        "ts_chorwow",
        "ts_formone",
        "ts_formoomp",
        "ts_zilk",
        "ts_zwoop",
        "ts_zwerp",
        "ts_bausch",
        "ts_bissosch",
        "ts_wassd",
        "ts_snxsd",
        "ts_snoossd",
        #"ts_vosim",
        #"ts_vosimwoop",
        "ts_tri",
        "ts_tru",
        "ts_tro",
        "ts_tree",
        "ts_trs",
        "ts_squine",
        "ts_squeene",
        "ts_squiine",
        "ts_wub",
        "ts_wubz",
        "ts_fammy",
        "ts_fammymodsw",
        "ts_fawwy", 
        "ts_fassy", 
        "ts_fatty",
        "ts_fabby", 
        "ts_cubxzx",
        "ts_cubyyy",
        ]
#defs = ["ts_fammy", "ts_fawwy"]

def make_scale(notes):
    ret = []
    for note in notes:
        if random.randrange(2):
            ret.append(note)
    
    if not notes[-1] == ret[-1]:
        ret.append(notes[-1])
    return ret
                

def random_note(scale, octave=None):
    note = random.choice(scale)
    if not octave: octave = random.randrange(3)
    omul = scale[-1] ** octave
    return note * root * omul

def graingen(scale):
    while graingen.can_run:
        print scale
        for i in range(200):
            beat = random.random() * random.choice([0.1, 0.2, 0.2, 0.4])
            #beat = random.random() * random.choice([6.0, 8.0, 10.0, 4.0])
            s.sendBundle(random.random() * beat,
                         [['s_new', random.choice(defs), -1, 0, 1,
                           'freq',  random_note(scale),
                           'freq2', random_note(scale),
                           'pan',   random.uniform(-1.0, 1.0),
                           'att',   random.uniform(0.0025, 0.04),
                           'rel',   random.uniform(0.1, 0.4),
                           'lmod',  random.uniform(0.001, 25.0),
                           'lfreq', random.uniform(1.0, 4.0), # do not change range
                           'lag',   0.2,
                           'lev',   random.uniform(0.01, 0.1),
                           'rez',   random.uniform(0.2, 0.8)
                           ]]),
        time.sleep(beat)
graingen.can_run = True

def doloop(scale):
    gg = threading.Thread(target=graingen, args=[scale])
    gg.start()

def run(numvoices):
    "can call this multiple times"
    print numvoices
    graingen.can_run = True
    if numvoices > 0:
        for i in range(numvoices):
            scale = make_scale(scales["bohlen-pierce"])
            doloop(scale)
    else:
        stop()
        
def start_listener():
    "This is how to receive data packets from a network."
    print "starting listener"
    udp_ip = "192.168.2.5" # the ip address of this computer on the network
    udp_port = 57199
    
    sock = socket.socket(socket.AF_INET,    # from internet
                         socket.SOCK_DGRAM) # UDP packet
    
    sock.bind((udp_ip, udp_port))
    
    while True:
        data = sock.recvfrom(2**13)
        
        recv_msg(tools.decode(data[0]))

def recv_msg(data):
    "call run with the parameters properly parsed"
    run(data[1])

def stop():
    "Stops all running synth loops."
    graingen.can_run = False

if __name__ == "__main__":
    start_listener()
    #run(1)

