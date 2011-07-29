/**
    Let's try creating a set of synthdefs.
*/

SynthDef(
    "ts_mod0", 
    { arg freq=200, lev=0.2, att=0.01, rel=0.2, curve=(-2);
        var aEnv = EnvGen.ar(Env.asr(att, lev, rel, curve))
        var aSig = SinOsc.ar(freq, 0);
        Out.ar(0, (aSig * env).dup);
    }
).load(s)

SynthDef(
    "ts_mod1",
    { arg freq=200, lev=0.2, att=0.01, rel=0.2, curve=(-2),
          mfreq=10, mod=0.5;
        var aEnv = EnvGen.ar(Env.asr(att, lev, rel, curve))
        var kMod = LFNoise0.kr(mfreq, mod * freq, freq);
        var aSig = SinOsc.ar(kMod, 0);
        Out.ar(0, (aSig * env).dup);
    }
).load(s)


