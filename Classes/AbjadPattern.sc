AbjadPattern {
	var <score;
	var <>id;
	var <pbind, <type;

	classvar patternBuilder;

	*new { |score, id, pbind, type=\note|
		^super.newCopyArgs(score, id, pbind, type);
	}

	*initClass {
		patternBuilder = this.prPatternBuilder;
	}

	play {
		(patternBuilder <> (abjad: type, id: id, score: score) <> pbind).play;
	}

	render {
		score.render(this);
	}

	preview {
		score.preview(this);
	}

	*prPatternBuilder {
		^Pbind(
			\delta, 0,
			\dynamic, Pfunc({|e|
				if (e[\amp].class != {}.class, //if \amp is explicited in parent event
					{
						if (e[\amp] != 0,
							{
								var index = e[\amp].linlin(0,1,0,10).round;
								['ppppp','pppp','ppp','pp','p','mp','mf','f','ff','fff','ffff'][index];
							},
							{
								"None"
							}
						)
					},
					{ "None" }
				)
			}),
			\amp, 0,
			\rest, Pfunc({|e|
				var string = e.isRest.asString;
				string[0] = string[0].toUpper;
				string; }),
			\finish, {|e|
				var path = "/" ++ e.abjad ++"_event";
				var selectedKeys;
				selectedKeys = e.reject( //general cleaning
					{
						|item, key|
						['server', 'delta', 'path', 'score', 'type', 'abjad', 'finish'].includes(key)
					}
				);

				switch ( e.abjad,

					\note, {
						[\freq, \dur].do({|key| //use current freq for event note, .value strip Rest() when \dur is Rest
							selectedKeys[key] = selectedKeys.use({('~'++key).interpret.value});
						});

						selectedKeys = selectedKeys.reject( //note event cleaning
							{
								|item, key|
								['scale', 'root', 'ctranspose', 'mtranspose'].includes(key)
							}
						);

						[\id, \articulation, \dynamic, \fermata, \markup, \markupCommand, \voice, \octave, \notehead].do({|key| //send as String
							selectedKeys[key] !? {
								selectedKeys[key] = selectedKeys[key].asCompileString
							}
						})
					},

					\literal, {
						selectedKeys[\position] ?? {selectedKeys[\position] = 'after'}; //set default position

						selectedKeys = selectedKeys.reject( //literal event cleaning
							{
								|item, key|
								['dur', 'freq', 'amp', 'rest','root','ctranspose', 'mtranspose'].includes(key)
							}
						);

						[\id, \literal, \position].do({|key| //send as String
							selectedKeys[key] !? {
								selectedKeys[key] = selectedKeys[key].asCompileString;
							}
					})}
				);

				selectedKeys.reject({|item, key|
					key.isNil
				});

				e.score.prSendEvents(path, selectedKeys);
		});
	}
}