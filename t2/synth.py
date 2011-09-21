"""
synth.py

Run the sequencer from python here.

TODO:
1 - base the parameters of the scale generator on the facial data
2 - the rhythmic quantization should be based on the facial data, rather than
    a random generator
3 - wrap the granular synth code in to a class, and add a separate delay or
    sampler class of some sort to artifically increast the density of the sound

"""
import socket
import time
import random
from multiprocessing import Process, Value
from scosc import controller, tools, patterns

threads = []
s = [controller.Controller(("192.168.2.5", 57110)),
     controller.Controller(("192.168.2.5", 57210))]
# all scales will be expressed as intervals
root = 55.0

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
             "ts_wabbd",
             "ts_waggd",
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

class GranuSynth(Process):
    """GranuSynth is a Process instance -- a granular synth loop with all 
    necessary data encapsulated in the instance."""
    def __init__(self, notes, face, defs):
        Process.__init__(self)
        self.notes = notes
        self.data = face
        self.defs = defs
        self.can_run = Value('I', 1)
        self.scale = self.make_fscale()
        self.fseq = patterns.Pseq(self.scale)
        # seems somehow un-pythonic to have such specialized (i.e. non-
        # parametric) data initialized here like this
        self.valcounter = 0 # used only by self.next_value()
        self.unitval = 1.0 # used only by self.get_unit()

    def run(self):
        self.graingen()
    
    def stop(self):
        self.can_run.value = 0
        self.join()

    def graingen(self):
        delay = 1.0 # compensate for network latency
        while self.can_run.value:
            server = get_server() # cycle through available servers
            basetime = time.time()
            #for i in range(100):
            beat = random.random() * random.choice([0.5, 0.25, 0.125])
            for i in range(50):
                #beat = random.random() * random.choice([0.1, 0.2, 0.2, 0.4])
                
                #beat = random.random() * random.choice([1.5, 1.25, 1.125])
                # the quantization factor should be calculated from a face
                quant = random.choice([4,8,16,8,8,2,32])
                rbeat = random.randrange(quant) * (1.0/float(quant))# 0-1 value, quantized
                server.sendBundleAbs(rbeat * beat + basetime + delay,
                             [['s_new', random.choice(self.defs), -1, 0, 1,
                               'freq',  self.ratio_to_freq(self.fseq.next()),
                               'freq2', self.ratio_to_freq(self.fseq.next()),
                               'pan',   self.next_value(-1.0, 1.0),
                               'att',   random.uniform(0.0025, 0.01),
                               'rel',   self.next_value(0.04, 0.4),
                               'lmod',  self.next_value(0.001, 25.0),
                               'lfreq', self.next_value(1.0, 4.0), # do not change range
                               'lag',   0.2,
                               'lev',   random.triangular(0.01, 0.1, 0.015),
                               'rez',   self.next_value(0.2, 0.8)
                               ]])
            time.sleep(beat)
            
    def next_value(self, low, high):
        if self.valcounter >= len(self.data):
            self.valcounter = 0
    
        range = high - low
        val = random.choice(self.data[self.valcounter]) * range + low
        
        self.valcounter += 1
        return val

    def make_fscale(self):
        "make a scale with note choice based on the image data."
        coef = 1.0 / self.get_unit(self.data)
        seq = []
        for point in self.data:
            loc = [v * coef for v in point] 
            index = loc[0] + (loc[1] * (coef+1))
            seq.append(index)
        result = [self.notes[int(i)%len(self.notes)] for i in seq]
        return result

    def ratio_to_freq(self, note):
        "get frequency in a random octave for a specified ratio"
        #octave = random.randrange(3) # 3 for tritave, 4 for octave scales
        osize = self.notes[-1]
        octave = random.randrange(4) # 3 for tritave, 4 for octave scales
        omul = osize ** octave         # ******** octave size must match
        return root * note * omul

    def get_unit(self, data, max=1.0):
        """get unit value in quantized multidimensional array. Assumes numbers or 
        list/tuple only. Instead of making the facial analysis module deliver 
        "grain" parameter directly, deduce the value algorithmically."""
        self.unitval = max
        for item in data:
            if isinstance(item, (list, tuple)):
                self.get_unit(item, self.unitval)
            elif item < max and item > 0.0:
                self.unitval = item
        return self.unitval


class Sampler(object):
    """
    Manage buffers and synth for a sampler voice to artificially thicken the sound.
    """
    def __init__(self):
        pass
    

# *** GLOBAL UTILITY FUNCTIONS ***

def make_scale(ratio, size=7, oct=2.0):
    """procedurally generate a just scale by stacking a single interval until
    it is no longer possible to add an interval larger than the specified 
    minimum."""
    # convert minimum ratio to minimum difference. this makes semantic sense, 
    # but looks kinda stupid anyway
    note = 1.0
    scale = []

    # with pythagorean tuning: building upward only will effectively create a
    # scale with a root on the 4th note of the list. presumably, building upward
    # with other stacked ratios will exhibit the same behavior. So, this 
    # complicates writing melodies by indexing directly in to the scale list, 
    # which does not relate to my purpose.
    for i in range(size):
        scale.append(note)
        note *= ratio
        if note > oct:
            note /= oct
    scale.append(oct)
    scale.sort()
    return scale

def get_server():
    server = s[get_server.index]
    get_server.index = (get_server.index + 1) % len(s)
    return server
get_server.index = 0

def doloop(scale, face, defs):
    threads.append(GranuSynth(scale, face, defs))
    threads[-1].start()

def randsplit(data, sections=2):
    """randomly split a list in to n number of sublists. does not check for
    empty lists, so watch out.
    """
    ret = [[] for i in range(sections)]
    for item in data:
        ret[random.randrange(sections)].append(item)
    return ret

# *** OSC LISTENER FUNCTIONS ***
# ***   NOT USED RIGHT NOW   ***
        
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

# *** INTERFACE COMMANDS ***

def stop():
    "Stops all running synth loops."
    global threads # check if I can get rid of this now
    for thread in threads:
        thread.stop()
    
def run(faces):
    "start or stop a synth loop"
    numvoices = len(faces)
    # only the first three will ever get selected
    rchoices = [3.0/2.0, 5.0/4.0, 8.0/7.0, 9.0/8.0, 11.0/10.0, 13.0/12.0]
    # doesn't check for bounding errors. watch for a bug here.
    ratio = rchoices[len(faces)-1]
    if numvoices > 0:
        defs = randsplit(synthdefs, numvoices)
        for i in range(min(numvoices, 7)): # limit the number of synth voices to 6
            scale = make_scale(ratio, len(faces[i]))
            # MAIN SYNTH LOOP
            doloop(scale, faces[i], defs[i])
            # **** ***** ****
    else:
        stop()

# *** TESTING ***

def test(numvoices=1, quant=4):
    data = []
    for i in range(numvoices):
        face = random_face(quant)
        data.append(face)
    run(data)

def test_scale(numvoices):
    for i in range(numvoices):
        face = random_face()
        notes = make_scale(3.0/2.0, len(face))
        print GranuSynth.make_fscale(notes, face)

def random_face(quant=4):
    return [(random.randrange(0, quant) / float(quant-1),
            random.randrange(0, quant) / float(quant-1))
            for i in range(random.randrange(3, 15))]

# *** MAIN LOOP ***

if __name__ == "__main__":
    #start_listener()
    test(2)
    #test_scale(2)

