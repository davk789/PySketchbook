"""
synth.py

Run the sequencer from python here.

"""
import time
import random
from scosc import controller

s = controller.Controller(("127.0.0.1", 57110))

lo = 40
hi = 1000
beat = 2.0
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
        ]

def doloop():
    while True:
        for i in range(int(random.random() * 125)):
            s.sendBundle(pow(random.random() * beat, 2),
                         [['s_new', random.choice(defs), -1, 0, 1,
                           'freq',  random.uniform(lo, hi),
                           'freq2', random.uniform(lo, hi),
                           'pan',   random.uniform(-1.0, 1.0),
                           'att',   random.uniform(0.0025, 0.04),
                           'rel',   random.uniform(0.1, 0.4),
                           'lmod',  random.uniform(0.001, 20.0),
                           'lfreq', random.uniform(1.0, 4.0),
                           'lag',   0.2,
                           'lev',   random.uniform(0.01, 0.15),
                           'rez',   random.uniform(0.2, 0.8)
                           ]]),
        time.sleep(random.random() * beat)

if __name__ == "__main__":
    doloop()

