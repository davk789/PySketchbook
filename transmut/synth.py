"""
synth.py

Run the supercollider synths from this python script. In short, I am generating
granular-ish sounds that draw from the cam.py for parameter data.

To be more specific about the sounds: Python will generate large numbers of 
short notes. The main paramters will be pitch, duration, and "direction" -- that
is, the synths will be modulated somehow.
"""

import sc
import time

# ctl handles all the SuperCollider-style server messaging
ctl = sc.scsynth.server.connect()

class SCNodeManager(object):
    def __init__(self):
        self.node_id = 1000
        self.node_max = pow(2, 32)
    
    def next_node_id(self):
        if self.node_id == self.node_max:
            self.node_id = 1000
        ret = self.node_id
        self.node_id += 1
        return ret
    

def main():
    nm = SCNodeManager()
    for i in range(25):
        print "generating grain ", i
        ctl.sendBundle((i / 20.0) + 1.0, [['s_new', "ts_mod0", nm.next_node_id(), 0, 1]])
        #ctl.sendMsg('s_new', "ts_mod0", nm.next_node_id(), 0, 1)
        #time.sleep(0.05)
    print "all done"

if __name__ == "__main__":
    main()


