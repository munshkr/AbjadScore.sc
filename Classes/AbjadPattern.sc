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
	/*	Pseq([
			(abjad: type, id: id, score: score, new: \True),
			patternBuilder <> (abjad: type, id: id, score: score) <> pbind
		]).play;
	*/
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
	dynamic { |dynamic, index = 0, command = 'None', voice = \upper, direction = 'Down', name_is_textual = 'None', tweaks = 'None'|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		command = command.asString.replace("\\", "backlash-");
		msg = "'id': " ++ id.asCompileString
		++ ", 'dynamic': " ++ dynamic.asCompileString
		++ ", 'command': " ++ command.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'name_is_textual': " ++ name_is_textual
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index;
		score.prSendMsg('/dynamic_oneshot', msg);
	}

	//'<' 'o<' '<|' 'o<|' '>' '>o' '|>' '|>o' '--'
	dynamicTrend { |shape, index = 0,  left_broken = 'None', voice = \upper, tweaks = 'None'|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'shape': " ++ shape.asCompileString
		++ ", 'left_broken': " ++ left_broken
		++ ", 'tweaks': " ++ tweaks
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/dynamicTrend_oneshot', msg);
	}

	//[ 'italic', 'caps', 'center_align', 'circle', 'bold', 'box', 'bracket', 'huge', 'larger', 'normal_text', 'parenthesize', 'sans', 'small', 'smaller', 'tiny', 'upright', 'vcenter', 'whiteout' ]
	//Advertencia: no son todos combinables. Ej. 'italic' mata 'caps'
	// 'dynamic' choca con la tipografía de Dynamic() en lilypond (parece que si la usas en Dynamic() despues Markup('dynamic') no encuentra la tipografía)
	markup { |markup, direction = 'Up', markupCommand='upright', index = 0, voice = \upper, tweaks = 'None'|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		if (markupCommand.class != Array, {markupCommand = [markupCommand]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'markup': " ++ markup.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'markupCommand': " ++ markupCommand.asCompileString
		++ ", 'tweaks': " ++ tweaks
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/markup_oneshot', msg);
	}

	articulation { |articulation, index = 0, direction = 'Up', voice = \upper, tweaks = 'None'|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'articulation': " ++ articulation.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index;
		score.prSendMsg('/articulation_oneshot', msg);
	}

	notehead { |notehead, index = 0, voice = \upper|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'notehead': " ++ notehead.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/notehead_oneshot', msg);
	}

	barline { |bar_line, index = 0, voice = \upper|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'bar_line': " ++ bar_line.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/bar_line_oneshot', msg);
	}

	clef { |clef = \bass, index = 0, voice = \upper|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'clef': " ++ clef.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/clef_oneshot', msg);
	}

	timeSignature { |pair, index = 0, partial = "None", hide = "None", voice = \upper|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'pair': " ++ pair.asCompileString
		++ ", 'partial': " ++ partial
		++ ", 'hide': " ++ hide
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/time_signature_oneshot', msg);
	}

	staff { |type|
		var msg;
		msg = "'id': " ++ id.asCompileString
		++ ", 'lilypond_type': " ++ type.asCompileString;
		score.prSendMsg('/staff_oneshot', msg);
	}

	repeat { |container, index = 0|
		var msg;
		container ?? {container = id};
		msg = "'id': " ++ id.asCompileString
		++ ", 'container': " ++ container.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/repeat_oneshot', msg);
	}

	slur { |slice, voice = \upper, direction = "None"|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'slice': " ++ slice.asArray.asCompileString;
		score.prSendMsg('/slur_oneshot', msg);
	}

	glissando { |slice, voice = \upper,  allow_repeats="None", allow_ties="None", parenthesize_repeats="None", right_broken="None", stems="None", style="line"|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'allow_repeats': " ++ allow_repeats // True/False
		++ ", 'allow_ties': " ++ allow_ties // True/False
		++ ", 'parenthesize_repeats': " ++ parenthesize_repeats // True/False
		++ ", 'right_broken': " ++ right_broken // True/False
		++ ", 'stems': " ++ stems // True/False
		++ ", 'style': " ++ style.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'slice': " ++ slice.asArray.asCompileString;
		score.prSendMsg('/glissando_oneshot', msg);
	}

	tie { |slice, voice = \upper, direction = "None", left_broken = "None", repeat = "None", right_broken = "None"|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'direction': " ++ direction
		++ ", 'left_broken': " ++ left_broken
		++ ", 'repeat': " ++ repeat
		++ ", 'right_broken': " ++ right_broken
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'slice': " ++ slice.asArray.asCompileString;
		score.prSendMsg('/tie_oneshot', msg);
	}

	textSpanner { |slice, left_text = 'left_text', right_text = 'right_text', markupCommand = 'upright', style = 'solid_line_with_arrow', direction = 'None', staff_padding = 4, voice = \upper, tweaks = 'None'|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		markupCommand = markupCommand.asString.replace("\\", "backlash-");
		msg = "'id': " ++ id.asCompileString
		++ ", 'left_text': " ++ left_text.asCompileString
		++ ", 'right_text': " ++ right_text.asCompileString
		++ ", 'direction': " ++ direction.asCompileString
		++ ", 'markupCommand': " ++ markupCommand.asCompileString
		++ ", 'tweaks': " ++ tweaks
		++ ", 'style': " ++ style.asCompileString
		++ ", 'staff_padding': " ++ staff_padding
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'slice': " ++ slice.asArray.asCompileString;
		score.prSendMsg('/text_spanner_oneshot', msg);
	}

	literal { |literal, position = \after, index = 'None', voice = \upper, tweaks = 'None'|
		var msg;
		literal = literal.asString.replace("\\", "backlash-");
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'literal': " ++ literal.asCompileString
		++ ", 'position': " ++ position.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'tweaks': " ++ tweaks
		++ ", 'index': " ++ index; //REVISAR: Creo que corre por cuenta propia chequear cuál literal se puede attachear a cuál leaf para que el código de lilypond compile. Si index = 'None' entonces attachea a container[id]
		score.prSendMsg('/literal_oneshot', msg);
	}

	detach { |attachment, index = 0, voice = \upper|
		var msg;
		attachment = attachment.asString.replace("\\", "backlash-");
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'attachment': " ++ attachment
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/detach', msg);
	}

	detach_literal { |attachment, index = 0, voice = "None"|
		var msg;
		attachment = attachment.asString.replace("\\", "backlash-");
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
		++ ", 'attachment': " ++ attachment.asCompileString
		++ ", 'voice': " ++ voice.asCompileString
		++ ", 'index': " ++ index;
		score.prSendMsg('/detach_literal', msg);
	}

	remove { |index = 0, voice = \upper|
		var msg;
		if (voice.class != Array, {voice = [voice]});
		msg = "'id': " ++ id.asCompileString
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
						});
						/*
					[\markupCommand].do({|key| //send as Array
							selectedKeys[key] !? {
							selectedKeys[key] = [selectedKeys[key]].asCompileString
							}
						});
						*/
					},

					\literal, {
						selectedKeys[\position] ?? {selectedKeys[\position] = 'after'}; //set default position
					    selectedKeys[\literal] = selectedKeys[\literal].asString.replace("\\", "backlash-"); //awful hack

						selectedKeys = selectedKeys.reject( //literal event cleaning
							{
								|item, key|
								['dur', 'freq', 'amp', 'rest','root','ctranspose', 'mtranspose'].includes(key)
							}
						);

						[\id, \literal, \position, \voice].do({|key| //send as String
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