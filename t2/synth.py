"""
synth.py

Run the sequencer from python here.

TODO:
1 - check that the data is all being generated properly: check that randsplit
    doesn't cause any problems with zero defs in a list

"""
import socket
import time
import random
from multiprocessing import Process, Value
from scosc import controller, tools

threads = []
#s = controller.Controller(("127.0.0.1", 57110))
s = controller.Controller(("192.168.2.5", 57110))
run_flag = Value('I', 1)
# all scales will be expressed as intervals
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

synthdefs = ["ts_sin_touch",
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
        "ts_vosim",
        "ts_vosimwoop",
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

def graingen(scale, face, defs, can_run):
    while can_run.value:
        #for i in range(100):
        for i in range(50):
            #beat = random.random() * random.choice([0.1, 0.2, 0.2, 0.4])
            beat = random.random() * random.choice([0.5, 0.25, 0.125])
            s.sendBundle(random.random() * beat + 2.0,
                         [['s_new', random.choice(defs), -1, 0, 1,
                           'freq',  random_note(scale),
                           'freq2', random_note(scale),
                           'pan',   next_value(face, -1.0, 1.0),
                           'att',   random.uniform(0.0025, 0.04),
                           'rel',   random.uniform(0.1, 0.4),
                           'lmod',  next_value(face, 0.001, 25.0),
                           'lfreq', next_value(face, 1.0, 4.0), # do not change range
                           'lag',   0.2,
                           'lev',   random.triangular(0.01, 0.1, 0.015),
                           'rez',   next_value(face, 0.2, 0.8)
                           ]])
        time.sleep(beat)

def next_value(data, low, high):
    if next_value.count >= len(data):
        next_value.count = 0

    range = high - low
    val = random.choice(data[next_value.count]) * range + low
    
    next_value.count += 1
    return val
next_value.count = 0

def doloop(scale, face, defs, can_run):
    threads.append(Process(target=graingen, args=[scale, face, defs, can_run]))
    threads[-1].start()

#def doloop(scale, face, defs, can_run):
#    graingen(scale, face, defs, can_run)

def randsplit(data, sections=2):
    """randomly split a list in to n number of sublists. does not check for
    empty lists, so watch out.
    """
    ret = [[] for i in range(sections)]
    for item in data:
        ret[random.randrange(sections)].append(item)
    return ret

def run(faces):
    "start or stop a synth loop"
    numvoices = len(faces)
    if numvoices > 0:
        run_flag.value = 1
        defs = randsplit(synthdefs, numvoices)
        for i in range(numvoices):
            scale = make_scale(scales["bohlen-pierce"])
            doloop(scale, faces[i], defs[i], run_flag)
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

def recv_msg(faces):
    "call run with the parameters properly parsed"
    run(osc_value('data', faces))

def osc_value(key, data):
    "assuming a list is a set of osc message pairs, get value for tag"
    return data[data.index(key)+1]

def stop():
    "Stops all running synth loops."
    global threads
    run_flag.value = 0
    #wait for threads to finish and then clear the list
    for thread in threads:
        thread.join()
    threads = []

def test(numvoices=1, quant=4):
    data = []
    for i in range(numvoices):
        face = [(random.randrange(0, quant) / float(quant-1),
                 random.randrange(0, quant) / float(quant-1))
                 for i in range(random.randrange(3, 15))]
        data.append(face)
    #run(data)
    run([])
        

if __name__ == "__main__":
    #start_listener()
    # example output
    # 
    test()

