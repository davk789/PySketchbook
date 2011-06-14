"""
general utility function dumping ground. Before this project is even suitable
to show to people, this module should be reorganized.
"""

import math

def next_node_id():
    """ generate synth ids based on a wrapping counter 1000 to 2^32 """
    try:
        if next_node_id.attr >= 2**32:
            next_node_id.attr = 1000
        else:
            next_node_id.attr += 1

        return next_node_id.attr
    except AttributeError:
        next_node_id.attr = 1000
        return next_node_id.attr


def flatten_dict(dict):
    ret = []
    for key, val in dict.items():
        ret += [key,val]
    return ret

def freqmidi(freq):
    "frequency to midi conversion"
    return 69 + 12*math.log(freq/440)/math.log(2)
    
def midifreq(note):
    "midi to frequency conversion"
    return 440.0 * (2**((note-69.0)/12.0))

def ampmidi(amp):
    "amplitude (0-1) to midi conversion"
    return math.sqrt(amp) * 127

def midiamp(num):
    "midi to amplitude (0-1) conversion"
    return (num / 127.0) ** 2

if __name__ == "__main__":
    for i in range(69, 89, 1):
        amp = midiamp(i)
        print amp
        print ampmidi(amp)
        print "__"
        
        
