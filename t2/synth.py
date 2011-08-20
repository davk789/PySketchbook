"""
synth.py

Run the sequencer from python here.

"""
import time
import random
import threading
from scosc import controller

s = controller.Controller(("127.0.0.1", 57110))

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
                            16.0/9.0,9.0/5.0,20.0/11.0,11.0/6.0,2.0/1)
          }
defs = ["ts_sin_touch",
        "ts_swoop",
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
        ]

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
    if not octave: octave = random.randrange(4)
    omul = scale[-1] ** octave
    return note * root * omul

def refresh_scale(notes):
    while True:
        doloop.scale = make_scale(notes)
        time.sleep(random.randrange(0, 16, 4))

def doloop():
    while True:
        print doloop.scale
        for i in range(400):
            beat = random.random() * random.choice([0.1, 0.2, 0.2, 0.4])
            s.sendBundle(random.random() * beat,
                         [['s_new', random.choice(defs), -1, 0, 1,
                           'freq',  random_note(doloop.scale),
                           'freq2', random_note(doloop.scale),
                           'pan',   random.uniform(-1.0, 1.0),
                           'att',   random.uniform(0.0025, 0.04),
                           'rel',   random.uniform(0.1, 0.4),
                           'lmod',  random.uniform(0.001, 25.0),
                           'lfreq', random.uniform(1.0, 4.0),
                           'lag',   0.2,
                           'lev',   random.uniform(0.01, 0.1),
                           'rez',   random.uniform(0.2, 0.8)
                           ]]),
        time.sleep(beat)
doloop.scale = make_scale(scales["partch"])


if __name__ == "__main__":
    refresh = threading.Thread(target=refresh_scale, args=[scales["partch"]])
    refresh.start()
    doloop()

