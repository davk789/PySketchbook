"""
pyinst.midi: manage midi input and output for the instrument. Separate classes 
for input and output. Everything is done on a per-instance basis, so each voice
of the instrument will be able to have its own midi inputs and outputs.

"""
# should includes come from __init__.py?
from pygame import midi
import pygame
from pygame.locals import *

import types


# still not sure where this initialization should occur. definitely on a module 
# level, though
pygame.init()
midi.init()

class PyInstrumentMidiIn:
    """
    Manage midi input.
    """
    def __init__(self, indev=1):
        self.midi_in = None
        
        # shoud these be called in __init__.py?
        
        self._note_on_observers = []
        self._note_off_observers = []
        self._cc_observers = []
        self._bend_observers = []
        self._aftertouch_observers = []

        self.set_midi_in(indev)


    def set_midi_in(self, indev):
        "Set midi input number and establish midi.Input()"
        if self.midi_in:
            del self.midi_in
        
        self.input_device = indev
        self.midi_in = midi.Input(self.input_device)

    def start_loop(self):
        """Running two separate loops: an application loop and a midi loop
        **  is this okay?
        """
        running = True

        while running:
            events = pygame.event.get()
            for e in events:
                # quit from menu only -- add keystrokes to this
                if e.type in [KEYDOWN, QUIT]:
                    running = False

            if self.midi_in.poll():
                event = self.midi_in.read(10)
                msg = midi.midis2events(event, self.midi_in.device_id)
                
                self.receive_midi_msg(msg)

    def receive_midi_msg(self, msg):
        "Parse MIDI input message. Possibly process values as well."
        
        if msg[0].status in range(144, 160):
            # note on/off
            if msg[0].data2 == 0:
                self.do_note_off(msg[0].status - 144, msg[0].data1)
                return None
            self.do_note_on(msg[0].status - 144, msg[0].data1, msg[0].data2)
            
        elif msg[0].status in range(176, 192):
            # midi cc, including mod wheel
            self.do_cc(msg[0].status - 176, msg[0].data1, msg[0].data2)
            
        elif msg[0].status in range(208, 224):
            # aftertouch
            self.do_aftertouch(msg[0].status - 208, msg[0].data1)
        elif msg[0].status in range(224, 240):
            # bend
            self.do_bend(msg[0].status - 224, msg[0].data1, msg[0].data2)

    def do_note_on(self, chan, num, vel):
        for func in self._note_on_observers:
            func(chan, num, vel)
                
    def do_note_off(self, chan, num):
        for func in self._note_off_observers:
            func(chan, num)

    def do_cc(self, chan, num, val):
        for func in self._cc_observers:
            func(chan, num, val)
        
    def do_aftertouch(self, chan, val):
        for func in self._aftertouch_observers:
            func(chan, val)

    def do_bend(self, chan, val1, val2):
        """ WARNING: the bend value can come from either val1 or val2. for now, hardcode
        based on the given midi device number. This is a hack that should be remedied.
        """
        val = None
        if self.input_device == 0:   # from iac
            val = val1
        elif self.input_device == 1: # from axiom
            val = val2

        if type(val) is types.NoneType:
            print "WARNING!!!"
            print "WARNING!!!"
            print "WARNING!!!"
            print "A pitchbend bug forces me to use midi devices 0 or 1. Fix the bug to use any other devices."
            # probably a good idea to throw an error here

        for func in self._bend_observers:
            func(chan, val)

    def add_note_on(self, func):
        self._note_on_observers.append(func)
        return len(self._note_on_observers) - 1
        
    def add_note_off(self, func):
        self._note_off_observers.append(func)
        return len(self._note_off_observers) - 1

    def add_cc(self, func):
        self._cc_observers.append(func)
        return len(self._cc_observers) - 1

    def add_bend(self, func):
        self._bend_observers.append(func)
        return len(self._bend_observers) - 1

    def add_aftertouch(self, func):
        self._aftertouch_observers.append(func)
        return len(self._aftertouch_observers) - 1
        


if __name__ == "__main__":
    print "\n testing PyInstrumentMidiIn"

    def note_on(a,b,c):
        print "note on:", a,b,c
    def other_note_on(a,b,c):
        print "other note on:", a,b,c
    def note_off(a,b):
        print "note off:", a,b
    def cc(a,b,c):
        print "cc:", a,b,c
    def bend(a,b):
        print "bend:",a,b
    def aftertouch(a,c):
        print "touch:",a,c

    # 0 = IAC bus. 1 generally refers to the first midi controller, if present
    pi = PyInstrumentMidiIn(0)
    pi.add_note_on(note_on)
    pi.add_note_on(other_note_on)
    pi.add_note_off(note_off)
    pi.add_bend(bend)
    pi.add_aftertouch(aftertouch)
    pi.add_cc(cc)
    
    pi.start_loop()
    
    
