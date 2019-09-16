//~score = AbjadScore.new("127.0.0.1", 5005);
~score = AbjadScore.new;
(
~a0 = ~score.notes(\multiphonics,
	Ptpar(
		[
			0,
			Pfindur(
				2,
				Pbind(
					\voice, 'lower',
					\dur, Prand([1/8, 1/4], inf),
					\notehead, \default,
					\octave, 3,
					\root, 2,
					\degree, Pwhite(0, 1),
					\ctranspose, Prand([-0.5, 0], inf)
				).collect(~event = _)
			),
			0.001,
			Pfindur(
				2,
				Pbind(
					\voice, 'upper',
					\dur, Pfunc({~event[\dur]}),
					\notehead, \default,
					\octave, 3,
					\root, Pfunc({~event[\root]}),
					\degree, Pfunc({~event[\degree]}),
					\ctranspose, 7 + Pfunc({~event[\ctranspose]}),
				)
			)
	])
)
)

~a0.render; // ./httpwatcherapp.py -I 'tuba' -P 5556 -W 'tuba'
~a0.preview; //  ./httpwatcherapp.py -I 'preview/tuba' -P 5557 -W 'preview/tuba'

~a0.clef(\bass, 0).preview
~a0.clef(\baritone, 1).preview
~a0.clef(\alto, 2).preview
~a0.clef(\soprano, 3).preview
~a0.clef(\treble, 3).preview
~a0.timeSignature([2,4], 0, hide: "False").preview
~a0.remove(0, [\upper, \lower]).preview
~a0.clef(\bass, 0).preview

~a0.slur(direction: \Up).preview
~a0.slur([], \upper, \Up).preview
~a0.detach('Slur', 0, \upper).preview
~a0.detach('Slur', 5, \upper).preview

~a0.glissando(voice: \upper, allow_repeats: \True).preview
~a0.glissando([],voice: \upper).preview
~a0.detach('Glissando', 0, \lower).preview



~a0.remove(-1, [\upper, \lower]).preview
~a0.preview;
~a0.render;
~a0.dynamic('niente', -1, '\\!').dynamicTrend(shape: '|>o', index: -3,  left_broken: 'False').preview;
~a0.dynamic('niente', 0, '\\!', voice: \lower).dynamic('mf', 5, voice: \lower).dynamicTrend(shape: 'o<|', index: 0,  left_broken: 'True', voice: \lower).preview;
~a0.detach('dynamic_trend', 1, \lower).preview


(0..8).do({|i| ~a0.articulation(['>', '-'].choose, i, 'Down', \lower)})


~a0.detach('Articulation', 1, \lower).preview
~a0.preview

~a0.textSpanner([0, 5], "air", "tone", 'upright', 'dashed_line_with_arrow', staff_padding: 3);

~a0.dynamic('mf', 5)


~a0.render
~a0.detach('text_spanner', 0)
~a0.remove(-1, [\upper, \lower]).preview

~a0.notehead('harmonic', 5, [\upper, \lower]).preview
~a0.repeat.preview
~a0.barline(':|.', -1).preview
~a0.barline(':|.|:', 1).preview
~a0.detach('BarLine', -2).preview
~a0.preview

~a0.detach('Repeat', -1, \upper).preview

~a0.literal('\\new Lyrics \\with { alignAboveContext = ' ++ '"' ++ \multiphonics ++ '"' ++ ' } { \\lyricsto ' ++ '"' ++ \upper ++ '"' ++ ' { _ _ _O - - E O E }}', \after).preview

~a0.render

//~a0.detach_literal('\\new Lyrics \\with { alignAboveContext = ' ++ '"' ++ \multiphonics ++ '"' ++ ' } { \\lyricsto ' ++ '"' ++ \upper ++ '"' ++ ' { O - - E O _ O E O }}', voice: 'upper').preview //TO DO


~a0.literal("\\addlyrics { _ _ _ _ _ _ O E}", \after, voice: \lower)
~a0.detach_literal("\\addlyrics { _ _ O E}", 0, voice: [\lower, \upper]) //NO FUNCIONA
~a0.detach_literal("LilypondLiteral('\\addlyrics { _ _ O E}', 'after')", 0, [\lower, \upper]) //NO FUNCIONA
~a0.preview;
~a0.detach_literal("LilypondLiteral", 0, voice: [\lower, \upper]) //NO FUNCIONA

~a0.barline('||:', 0).preview

[\upper].class
~a0.dynamic('mp', 8)


(
~a1 = ~score.notes(\melody,
	Pbind(
		\voice, 'lower',
		\dur, Pseq([1/4], 20),
		\notehead, \default,
		\octave, 3,
		\root, 1,
		\degree, Pseries(5, 1),
		//\ctranspose, Prand([-0.5, 0 , 0.5], inf)
	)
)
)

~a1.render
~a1.preview
~a1.dynamic('mp', -1)
~a1.detach('Dynamic', -1)





////Test all stuff
(
~a2 = ~score.notes(\testAll,
	Pbind(
		\voice, Prand([\upper, \lower], inf),
		\dynamicDirection, \Up, //no se envía como string porque hace referencia a un atributo. abjad.Up / abjad.Down
		//\amp, 0,
		\amp, Pseries(0.001, 0.1, inf),
		\dur, Pseries(16, -1, 8)/16,
		//\dur, Pseq([Pn(1/12,6),1/4,Pn(1/6, 3),1/4, Pn(1/16, 4) ], repeats: 1),
		//\dur, Pseq([Pn(1/12, 6), Pn(1/10, 5), 1/3, 2/3, Pn(1/8, 4) ], repeats: 1),
		\octave, 4,
		\root, 3,
		\markupCommand, "italic",
		\markup, "Allegro", //?
		\mtranspose, Pxrand([-2,2,0], inf),
		\scale, Scale.major,
		\degree, Pseries(0, 1, inf),
		\articulation, Pseq(['.', "", "", "", 'accent'], inf),
		\articDirection, \Down,
		\fermata, Pseq(["", "", "", "", "", 'fermata'], inf),
		\notehead, Prand(['altdefault','baroque','mensural','neomensural', 'petrucci','harmonic','harmonic-black', 'harmonic-mixed', 'diamond', 'cross', 'xcircle', 'triangle', 'slash', 'do','re','mi','fa','la','ti'], inf)
	)
).preview;
)
~a2.render;
~a2.detach('Dynamic', 0, \lower).render
~a2.remove(0, [\upper, \lower])
~a2.preview
~a2.markup('Allegro', \Up, ['italic'], 0, \upper).preview
~a2.detach('Markup', 0, \upper).preview