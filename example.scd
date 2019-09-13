~score = AbjadScore.new;
//~score = AbjadScore.new("127.0.0.1", 5005);

(
~foo = ~score.notes(\foo, Pbind(
	\voice, \upper,
	\dur, Pseq([3/4, Rest(1/4)], repeats: 1),
	\octave, 4,
	\degree, Pwhite(5,7),
));
)

~foo.preview;
~foo.render;
~foo.dynamic('niente', -1, 'backlash-!').dynamicTrend(shape: '>o', index: 0,  left_broken: 'True');


// oneshot messages
~foo.slur([4, 15]);
~foo.textSpanner([9], "aire", "tono", staff_padding: 1);

