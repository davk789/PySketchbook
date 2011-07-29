/**
    Let's try creating a set of synthdefs.
*/


SynthDef(
    "ts_mod0", 
    { arg freq=200, lev=0.2, att=0.01, rel=0.2, curve=(-2);
        var kEnv = EnvGen.kr(
        	Env.new([0, 1, 0], [att, rel], curve), 
        	lev, 
        	doneAction:2
        );
        var aSig = SinOsc.ar(freq, 0, kEnv);
        Out.ar(0, aSig.dup);
    }
).load(s);



