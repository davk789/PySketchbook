
// Audio 
~lo = 40;
~hi = 1000;



Tdef(\sins, {
	var period = 1.0;
	var defs = [
		'ts_sin_touch',
		'ts_swoop',
		'ts_swoopl',
	];
	loop{
		25.rand.do{
			s.sendBundle(period.rand ** 3, 
				[\s_new, defs.choose, -1, 0, 1, 
					'freq',  rrand(~lo, ~hi),
					'freq2', rrand(~lo, ~hi),
					'pan',   rrand(-1.0, 1.0),
					'att',   rrand(0.0025, 0.04),
					'rel',   rrand(0.1, 0.2),
				]
			);
		};
		period.rand.wait;
	}
});

Tdef(\sins).play;
Tdef(\sins).stop;


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

SynthDef("ts_swoopl",
	{ |freq=200, freq2=1000, att=0.01, rel=0.2, lev=0.2, pan=0.0|
		var kEnv = EnvGen.kr(Env.perc(att, rel), 1, lev, doneAction:2);
		var kLine = Line.kr(freq, freq2, att+rel);
		var aSig = SinOsc.ar(kLine, 0, kEnv);
		Out.ar(0, Pan2.ar(aSig, pan));
	}
).load(s);

