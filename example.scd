~score = AbjadScore.new;
//~score = AbjadScore.new("127.0.0.1", 5005);

(
~a0 = ~score.notes(\multiphonics,
	Ptpar([
		0,
		Pbind(
			\voice, 'lower',
			\dur, Pseq([1/4], 20),
			\notehead, \default,
			\octave, 3,
			\root, 1,
			\degree, Pseries(5, 1),
			//\ctranspose, Prand([-0.5, 0 , 0.5], inf)
		).collect(~event = _),
		0.001,
		Pbind(
			\voice, 'upper',
			\dur, Pseq([1/4], 20),
			\notehead, \harmonic,
			\octave, 3,
			\root, Pfunc({~event[\root]}),
			\degree, Pfunc({~event[\degree]}),
			\ctranspose, 7,
			//\ctranspose, Prand([-0.5, 0 , 0.5], inf)
		)
	])
)
)
'\\\\!'
~a0.preview;
~a0.render;
~a0.dynamic('niente', -1, '\\\\!').dynamicTrend(shape: '>o', index: 0,  left_broken: 'True');
~a0.dynamic('niente', -1, 'backlash-!').dynamicTrend(shape: 'o<|', index: 0,  left_broken: 'True');

~a0.textSpanner([0], "air", "tone", 'upright', 'dashed_line_with_arrow', staff_padding: 3);

~a0.detach('Dynamic', 0)
~a0.detach('text_spanner', 0)
~a0.remove(1)

~a0.literal('backlash-addlyrics { O E}', \after, 0)

~a0.dynamic('mp', 0)
