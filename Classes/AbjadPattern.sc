AbjadPattern {
	var <score, <id, <pbind, <type;

	classvar patternBuilder;

	*new { |score, id, pbind, type=\note|
		^super.newCopyArgs(score, id, pbind, type);
	}

	*initClass {
		patternBuilder = this.prPatternBuilder;
	}

	play {
		(patternBuilder <> (abjad: type, id: id, score: score) <> Pseq([(new: \True), pbind])).play;
	}

	render {
		score.render(this.id);
	}

	preview {
		score.preview(this.id);
	}

	//
	// oneshot messages
	//

	//'ppppp','pppp','ppp','pp','p','mp','mf','f','ff','fff','ffff'
	dynamic { |dynamic, index = 0, command = 'None', direction = 'Down', name_is_textual = 'None', tweaks = 'None'|
		//	name='f', command=None, direction=None, format_hairpin_stop=None, hide=None, leak=None, name_is_textual=None, ordinal=None, sforzando=None, tweaks=None
		var msg = "'id': " ++ id.asCompileString
		++ ", 'dynamic': " ++ dynamic.asCompileString
		++ ", 'command': " ++ command.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'name_is_textual': " ++ name_is_textual
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index;
		score.prSendMsg('/dynamic_oneshot', msg);
	}

	//'<' 'o<' '<|' 'o<|' '>' '>o' '|>' '|>o' '--'
	dynamicTrend { |shape, index = 0,  left_broken = 'None', tweaks = 'None'|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'shape': " ++ shape.asCompileString
		++ ", 'left_broken': " ++ left_broken
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index;
		score.prSendMsg('/dynamicTrend_oneshot', msg);
	}

	//[ 'italic', 'caps', 'center_align', 'circle', 'bold', 'box', 'bracket', 'huge', 'larger', 'normal_text', 'parenthesize', 'sans', 'small', 'smaller', 'tiny', 'upright', 'vcenter', 'whiteout' ]
	//Advertencia: no son todos combinables. Ej. 'italic' mata 'caps'
	// 'dynamic' choca con la tipografía de Dynamic() en lilypond (parece que si la usas en Dynamic() despues Markup('dynamic') no encuentra la tipografía)
	markup { |markup, direction = 'Up', markupCommand="", index = 0, tweaks = 'None'|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'markup': " ++ markup.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'markupCommand': " ++ markupCommand.asCompileString
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index;
		score.prSendMsg('/markup_oneshot', msg);
	}

	articulation { |articulation, index = 0, direction = 'Up', tweaks = 'None'|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'articulation': " ++ articulation.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index;
		score.prSendMsg('/articulation_oneshot', msg);
	}

	notehead { |notehead, index = 0|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'notehead': " ++ notehead.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/notehead_oneshot', msg);
	}

	barline { |bar_line, index = 0|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'bar_line': " ++ bar_line.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/bar_line_oneshot', msg);
	}

	slur { |slice, voice = 'upper', direction = "None"|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'slice': " ++ slice.asCompileString;
		score.prSendMsg('/slur_oneshot', msg);
	}

	tie { |slice, voice = 'upper', direction = "None", left_broken = "None", repeat = "None", right_broken = "None"|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'left_broken': " ++ left_broken
		++ ", 'repeat': " ++ repeat
		++ ", 'right_broken': " ++ right_broken
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'slice': " ++ slice.asCompileString;
		score.prSendMsg('/tie_oneshot', msg);
	}

	textSpanner { |slice, left_text = 'left_text', right_text = 'right_text', markupCommand = 'upright', style = 'solid_line_with_arrow', direction = 'None', staff_padding = 4,tweaks = 'None'|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'left_text': " ++ left_text.asCompileString
		++ ", 'right_text': " ++ right_text.asCompileString
		++ ", 'direction': " ++ direction.asCompileString
		++ ", 'markupCommand': " ++ markupCommand.asCompileString
		++ ", 'tweaks': " ++ tweaks
		++ ", 'style': " ++ style.asCompileString
		++ ", 'staff_padding': " ++ staff_padding
		++ ", 'slice': " ++ slice.asCompileString;
		score.prSendMsg('/text_spanner_oneshot', msg);
	}

	literal { |literal, position = \after, index = 'None', tweaks = 'None'|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'literal': " ++ literal.asCompileString
		++ ", 'position': " ++ position.asCompileString
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index; //REVISAR: Creo que corre por cuenta propia chequear cuál literal se puede attachear a cuál leaf para que el código de lilypond compile. Si index = 'None' entonces attachea a container[id]
		score.prSendMsg('/literal_oneshot', msg);
	}

	detach { |attachment, index = 0|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'attachment': " ++ attachment
		++ ", 'index': " ++ index;
		score.prSendMsg('/detach', msg);
	}

	remove { |index = 0, voice = 'upper'|
		var msg = "'id': " ++ id.asCompileString
		++ ", 'index': " ++ index
		++ ", 'voice': " ++ voice.asCompileString;
		score.prSendMsg('/remove', msg);
	}

	//
	// pbind pattern builder
	//

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