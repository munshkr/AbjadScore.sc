~score = AbjadScore.new;
//~score = AbjadScore.new("127.0.0.1", 5005);

(
~foo = ~score.notes(\foo, Pbind(
	\voice, \upper,
	\dur, Pseq([Pn(1/12,6),1/4,Pn(1/6, 3),1/4, Pn(1/16, 4) ], repeats: 1),
	\octave, 4,
	\degree, Pser([0, 2, 6], 16),
));
)

~foo.preview;
~foo.render;

// oneshot messages
~foo.slur([4, 7]);
~foo.textSpanner([4], "aire", "tono", staff_padding: 6);


