/**
 * 
 * Contain only the SynthDefs. Try to run the synths routine through python only.
 * 
 */
SynthDef("ts_sin_touch",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = SinOsc.ar(freq, 0, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_swoop",
	{ |freq=200, freq2=1000, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq, freq2, att+rel);
		var aSig = SinOsc.ar(kLine, 0, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_hash",
	{ arg freq=200, freq2=1000, att=0.01, rel=0.2, lev=0.2, pan=0.0,
		lfreq=1.5, lmod=0.5;
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq, freq2, att+rel);
		var aSig = SinOscFB.ar(kLine, kEnv*lmod, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);


SynthDef("ts_hash_blub",
	{ arg freq=200, freq2=1000, att=0.01, rel=0.2, lev=0.2, pan=0.0,
		lfreq=1.5, lmod=0.5, lag=0.2;
		var aIn = LocalIn.ar(1);
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq, freq2, att+rel);
		// this maxes out the server's memory (before the processor overloads I believe)
		var aFBLag = DelayC.ar(Lag.ar(aIn, lag), 0.2, SinOsc.ar((att+rel)*5, 0, 0.1, 0.1));
		var aSig = SinOsc.ar(kLine, kEnv*lmod*aIn, kEnv);
		LocalOut.ar(aSig);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_chorwow",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, lfreq=1.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig1 = SinOsc.ar(freq, 0, kEnv * 0.5);
		var aSig2 = SinOsc.ar(freq + (lfreq*2), 0, kEnv * 0.5);
		Out.ar(0, Pan2.ar((aSig1 + aSig2) * 0.5, pan));
	}
).load(s);

SynthDef("ts_formone",
	{ |freq=200, freq2=300, lmod=1.0, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = Formant.ar(freq, freq2, lmod*freq, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_formoomp",
	{ |freq=200, freq2=300, lmod=1.0, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq, freq2, att+rel);
		var aSig = Formant.ar(kLine, freq2, lmod*freq, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_zilk",
	{ |freq=200, freq2=100, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aPhase1 = Phasor.ar(0, (freq/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aRMPhase = (aPhase1/2pi).neg + 1;
		var aPhase2 = Phasor.ar(aRMPhase, (freq2/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aOsc1 = SinOsc.ar(0, aPhase1, kEnv);
		var aOsc2 = SinOsc.ar(0, aPhase2, kEnv * aRMPhase);
		var aSig = LPF.ar((aOsc1 + aOsc2) * 0.5, freq, 0.5);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_zwoop",
	{ |freq=200, freq2=100, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kLine1 = XLine.kr(freq, freq2, att+rel);
		var kLine2 = XLine.kr(freq2, freq, att+rel);
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aPhase1 = Phasor.ar(0, (kLine1/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aRMPhase = (aPhase1/2pi).neg + 1;
		var aPhase2 = Phasor.ar(aRMPhase, (kLine2/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aOsc1 = SinOsc.ar(0, aPhase1, kEnv);
		var aOsc2 = SinOsc.ar(0, aPhase2, kEnv * aRMPhase);
		var aSig = LPF.ar((aOsc1 + aOsc2) * 0.5, freq, 0.5);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_zwerp",
	{ |freq=200, freq2=100, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kLine = XLine.kr(freq, freq2, att+rel);
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aPhase1 = Phasor.ar(0, (kLine/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aRMPhase = (aPhase1/2pi).neg + 1;
		var aPhase2 = Phasor.ar(aRMPhase, (freq2/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aOsc1 = SinOsc.ar(0, aPhase1, kEnv);
		var aOsc2 = SinOsc.ar(0, aPhase2, kEnv * aRMPhase);
		var aSig = LPF.ar((aOsc1 + aOsc2) * 0.5, kLine, 0.5);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_zow",
	{ |freq=200, freq2=100, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kLine = XLine.kr(freq, freq2, att+rel);
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aPhase1 = Phasor.ar(0, (freq/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aRMPhase = (aPhase1/2pi).neg + 1;
		var aPhase2 = Phasor.ar(aRMPhase, (kLine/8192).min(8192), 0, 2pi, DC.ar(2pi*0.25));
		var aOsc1 = SinOsc.ar(0, aPhase1, kEnv);
		var aOsc2 = SinOsc.ar(0, aPhase2, kEnv * aRMPhase);
		var aSig = LPF.ar((aOsc1 + aOsc2) * 0.5, freq2, 0.5);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_bausch",
	{ |freq=200, freq2=100, att=0.01, rel=0.2, lev=0.2, pan=0.0, rez=0.5|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq2, freq, att+rel);
		var aPH1 = Phasor.ar(0, freq, 1, 0);
		var aPH2 = Phasor.ar(0, kLine, 1, 0);
		var aSQ = (aPH1 - aPH2) * kEnv;
		var aSig = RLPF.ar(aSQ, kLine, rez);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_bissosch",
	{ |freq=200, freq2=100, att=0.01, rel=0.2, lev=0.2, pan=0.0, rez=0.5|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aPH1 = Phasor.ar(0, freq, 1, 0);
		var aPH2 = Phasor.ar(aPH1, freq2, 1, 0);
		var aSQ = (aPH1 - aPH2) * kEnv;
		var aSig = RLPF.ar(aSQ, freq2, rez);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_wassd",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, rez=0.5|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = VarSaw.ar(freq, 0, rez, kEnv); // using rez for bw
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_snxsd",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, freq2=201|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aOsc = SyncSaw.ar(freq2, freq, kEnv); // using rez for bw
		var aSig = LPF.ar(aOsc, freq2 * 2);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_snoossd",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, freq2=201|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq2, freq, att+rel);
		var aOsc = SyncSaw.ar(kLine, freq, kEnv); // using rez for bw
		var aSig = RLPF.ar(aOsc, kLine * 1.5, 0.25);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);



/*
// osx only 
SynthDef("ts_vosimwoop",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, freq2=201, lfreq=2, rez=0.5|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq.max(freq2), freq2.min(freq), att+rel);
		var aTrig = Phasor.ar(0, kLine, 1, -1);
		var aOsc = VOSIM.ar(aTrig, freq2.max(freq), lfreq, rez, kEnv);
		//var aOsc = SyncSaw.ar(freq2, freq, kEnv); // using rez for bw
		var aSig = RLPF.ar(aOsc, kLine * 4, 0.1);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_vosim",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, freq2=201, lfreq=2, rez=0.5|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aTrig = Phasor.ar(0, freq, 1, -1);
		var aOsc = VOSIM.ar(aTrig, freq2.max(freq), lfreq, rez, kEnv);
		//var aOsc = SyncSaw.ar(freq2, freq, kEnv); // using rez for bw
		var aSig = RLPF.ar(aOsc, freq * 4, 0.1);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);
*/

SynthDef("ts_tri",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = LFTri.ar(freq, 0, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_tree",
	{ |freq=200, freq2=230, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq, freq2, att+rel);
		var aSig = LFTri.ar(freq, 0, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_tru",
	{ |freq=100, att=0.01, rel=0.2, lev=0.2, pan=0.0, lfreq=1.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = Phasor.ar(0, freq / s.sampleRate, 0.0, lfreq*4).fold(-1, 1) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_tro",
	{ |freq=100,freq2=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, lfreq=1.0|
		var kPer = freq.reciprocal;
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = XLine.kr(freq2/freq, freq/freq2, att+rel);
		var aSig = Phasor.ar(0, freq / s.sampleRate, 0.0, kLine*4).fold(-1, 1) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_trs",
	{ |freq=100,freq2=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, lfreq=1.0|
		var kPer = freq.reciprocal;
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kWav = XLine.kr(freq2/freq, freq/freq2, att+rel);
		var kFreq = XLine.kr(freq2, freq, att+rel);
		var aMaster = Impulse.ar(freq);
		var aSig = Phasor.ar(aMaster, kFreq / s.sampleRate, 0.0, kWav*4).fold(-1, 1) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_squine",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = SinOsc.ar(freq, 0)*SinOsc.ar(freq, 0)*SinOsc.ar(freq, 0) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_squeene",
	{ |freq=200, freq2=300, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = SinOsc.ar(freq, 0)*SinOsc.ar(freq2, 0)*SinOsc.ar(freq, 0) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_squiine",
	{ |freq=200, freq2=300, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kfrq1 = XLine.kr(freq, freq2, att+rel);
		var kfrq2  = XLine.kr(freq2, freq, att+rel);
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var aSig = SinOsc.ar(freq, 0)*SinOsc.ar(kfrq1, 0)*SinOsc.ar(kfrq2, 0) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_wub",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, lfreq=2|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kOff = lfreq * (att+rel).reciprocal;
		var aSig = Mix([SinOsc.ar(freq, 0, 0.61), SinOsc.ar(freq+kOff, 0, 0.61)]) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

SynthDef("ts_wubz",
	{ |freq=200, att=0.01, rel=0.2, lev=0.2, pan=0.0, lfreq=2|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kOff = lfreq * (att+rel).reciprocal;
		var kfrq = XLine.kr(freq+kOff, freq, att+rel);
		var aSig = Mix([SinOsc.ar(freq, 0, 0.61), SinOsc.ar(kfrq, 0, 0.61)]) * kEnv;
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);
