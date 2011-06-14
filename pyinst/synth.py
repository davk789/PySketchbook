"""
synth.py
First attempt to connect midi controller to scsynth process.

Eventually this file or another will have the following features:
- inheritance to simplify the creation of classes based on interface
- insert effects/main mixer, like the old instrument
- presets support (using pickle?)

"""
import midi
from scosc import controller
import pyinst

# classes

class PyInstrumentSynthVoice(object):
    """
    Give each voice an instance of this class -- possibly use this
    instead of a Synth class from the sc module. 

    ** reinventing a wheel here. don't ponder design decisions too deeply!
    """
    def __init__(self, params, server):
        self.params = params
        self.node_num = pyinst.next_node_id()
        self.s = controller.Controller(server)

    def start_voice(self):
        # stupid patrick
        self.s.listSendMsg(["s_new", "pi-test", self.node_num, 0, 1] + 
                           pyinst.flatten_dict(self.params))

    def end_voice(self):
        self.s.sendMsg("n_set", self.node_num, "gate", 0)

class PyInstrumentTestSynth(object): # get in the habit of using new-style classes
    """
    Mockup class that will control one simple sine wave oscillator.
    """
    def __init__(self, indev=0):
        # all editable params go here
        self.server = ("127.0.0.1", 57110) # default server
        self.params = {
            'freq' : 440,
            'lev'  : 0.5,
        }

        # this class should contain its own midi responder
        self.midi_in = midi.PyInstrumentMidiIn(indev)
        self.voices = {} # contains PyInstrumentSynthVoice
        self.init_midi()

    def init_midi(self):
        """
        needs a midi out instance.
        """
        self.midi_in.add_note_on(self.note_on)
        self.midi_in.add_note_off(self.note_off)
        self.midi_in.add_cc(self.cc)
        self.midi_in.add_bend(self.bend)
        self.midi_in.add_aftertouch(self.aftertouch)

        self.midi_in.start_loop()

    def note_on(self,chan,num,vel):
        freq = pyinst.midifreq(num)
        amp = pyinst.midiamp(vel)
        params = self.params.copy()
        params['freq'] = freq
        params['lev'] = amp
        print chan, num, vel
        if not num in self.voices:
            self.voices[num] = [PyInstrumentSynthVoice(params, self.server)]
            self.voices[num][0].start_voice()
        else:
            self.voices[num].append(PyInstrumentSynthVoice(params, self.server))
            self.voices[num][-1].start_voice()

    def note_off(self,chan,num):
        self.voices[num][-1].end_voice()
        self.voices[num].pop()

    def cc(self,chan,num,val):
        print "inside PyInstrumentTestSynth cc", chan, num, val

    def aftertouch(self,chan,num):
        print "inside PyInstrumentTestSynth aftertouch", chan, num

    def bend(self,chan,num):
        print "inside PyInstrumentTestSynth bend", chan, num


    
    
if __name__ == "__main__":
    print "in testing mode for synth.py"
    ts = PyInstrumentTestSynth(0)
    print "all done"
    
