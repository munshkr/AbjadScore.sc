s.boot
s.quit
(
n = NetAddr("127.0.0.1", 5005);

~render = {
	|id = "id0", ip = "127.0.0.1", port = 5005|
	NetAddr(ip, port).sendMsg("/note_display", id);
};
)
/*
(
var currentFolder = PathName(thisProcess.nowExecutingPath).parentPath;
var virtualenvPath = "/home/yako/.virtualenvs/abjad/bin/activate";
var scriptPath = currentFolder ++ "abjad-osc-server_0.10.py";
var outputPath = currentFolder ++ "output";
("source "++ virtualenvPath ++";" ++
"python "++ scriptPath ++ " --ip " ++ n.ip ++ " --port " ++ n.port ++ " --output " ++ outputPath).unixCmd { |res, pid| [\done, res, pid].postln };
)
//si queda zombie un server osc de python tira error silencioso (address already in use)
//mientras mejor debuggear corriendo el script de python desde la terminal
*/
(
~abjadPattern =
Pbind(
	\delta, 0,

	\dynamic, Pfunc({|e|
	//e[\amp].class.postln;
		if (e[\amp].class != {}.class,
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
				['server', 'delta', 'path', 'addr', 'type', 'abjad', 'finish'].includes(key)
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

				[\id, \articulation, \dynamic, \fermata, \markup, \markupCommand, \voice, \octave].do({|key| //send as String
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

		e.addr.sendMsg(path, selectedKeys.asString.drop(1).drop(-1));
		(selectedKeys.asString+"\n").postln;
});
)

////// Para el usuario
(
~id = \id1021;

a = Pbind(
	\abjad, \note,
	\voice, 'upper',
	\id, ~id,
	\addr, n,
	//\dynamicDirection, \Up, //no se envía como string porque hace referencia a un atributo. abjad.Up / abjad.Down
	//\amp, 0,
	//\amp, Pseries(0.001, 0.1, inf),
	\dur, Pseries(16, -1, 16)/16,
	//\dur, Pseq([Pn(1/16,4),Pn(1/6, 3), Pn(1/8, 4) ], repeats: 1),
	//\dur, Pseq([Pn(1/12, 6), Pn(1/10, 5), 1/3, 2/3, Pn(1/8, 4) ], repeats: 1),
	\octave, 3,
	\root, -3,
	\mtranspose, Pxrand([-1,1,0], inf),
	\scale, Scale.minorPentatonic,
	\degree, Pseries(0, 1, inf),
	//\articulation, Pseq(['.', "", "", "", 'accent'], inf),
	//\articDirection, \Up,
	//\fermata, Pseq(["", "", "", "", "", 'longfermata'], inf),
	//\markupDirection, \Up, //no se envía como string porque hace referencia a un atributo. abjad.Up / abjad.Down
	//\markup, "None",
	//\markupCommand, Pseq([ [""],[""],['italic'], ['box', 'sans'], ['tiny', 'box'], ['bold'] ],inf),
	//estaría bueno que no tenga que ser enviado como array cuando contiene solo un elemento (ver en python)
	//REVISAR: Cómo hacer para enviar un markup vacío??? "" -> genera un rest event
);
)

(
(~abjadPattern <> a).play;
)
(
~render.value(~id);
)
//oneshot msgs
//attach to container[x] element
(
~dynamic = {
	|id, dynamic, attachTo = 0, command = 'None', direction = 'Down', name_is_textual = 'None', ip = "127.0.0.1", port = 5005|
//	name='f', command=None, direction=None, format_hairpin_stop=None, hide=None, leak=None, name_is_textual=None, ordinal=None, sforzando=None, tweaks=None
	var msg = "'id': " ++ id.asCompileString
	++ ", 'dynamic': " ++ dynamic.asCompileString
	++ ", 'command': " ++ command.asCompileString
	++ ", 'direction': " ++ direction
	++ ", 'name_is_textual': " ++ name_is_textual
	++ ", 'attachTo': " ++ attachTo;
	NetAddr(ip, port).sendMsg('/dynamic_oneshot', msg);
}
//'ppppp','pppp','ppp','pp','p','mp','mf','f','ff','fff','ffff'
)

~dynamic.(~id, 'f', 4);
~dynamic.(~id, 'p', -1);
~dynamic.(~id, 'niente', -1 , 'backlash-!');
~render.value(~id);
(
~dynamicTrend = {
	|id, shape, attachTo = 0,  left_broken = 'None', tweaks = 'None', ip = "127.0.0.1", port = 5005|
	var msg = "'id': " ++ id.asCompileString
	++ ", 'shape': " ++ shape.asCompileString
	++ ", 'left_broken': " ++ left_broken
	++ ", 'tweaks': " ++ tweaks
	++ ", 'attachTo': " ++ attachTo;
	NetAddr(ip, port).sendMsg('/dynamicTrend_oneshot', msg);
}
//'<' 'o<' '<|' 'o<|' '>' '>o' '|>' '|>o' '--'
)

//~dynamicTrend.(~id, '|>o', 0 , tweaks: "[('color', 'blue')]" );
~dynamicTrend.(~id, '|>o', 0);
~render.value(~id);

~markup = {
	|id, markup, direction = 'Up', markupCommand="", attachTo = 0, ip = "127.0.0.1", port = 5005|
	var msg = "'id': " ++ id.asCompileString
	++ ", 'markup': " ++ markup.asCompileString
	++ ", 'direction': " ++ direction
	++ ", 'markupCommand': " ++ markupCommand.asCompileString
	++ ", 'attachTo': " ++ attachTo;
	NetAddr(ip, port).sendMsg('/markup_oneshot', msg);
}
//[ 'italic', 'caps', 'center_align', 'circle', 'bold', 'box', 'bracket', 'huge', 'larger', 'normal_text', 'parenthesize', 'sans', 'small', 'smaller', 'tiny', 'upright', 'vcenter', 'whiteout' ]
//Advertencia: no son todos combinables. Ej. 'italic' mata 'caps'
// 'dynamic' choca con la tipografía de Dynamic() en lilypond (parece que si la usas en Dynamic() despues Markup('dynamic') no encuentra la tipografía)
)

~markup.(~id, 'Adagio', 'Down', ['italic']);
~render.value(~id);
(
~literal = {
	|id, literal, position = \after, attachTo = 'None', ip = "127.0.0.1", port = 5005|
	var msg = "'id': " ++ id.asCompileString
	++ ", 'literal': " ++ literal.asCompileString
	++ ", 'position': " ++ position.asCompileString
	++ ", 'attachTo': " ++ attachTo; //REVISAR: Creo que corre por cuenta propia chequear cuál literal se puede attachear a cuál leaf para que el código de lilypond compile. Si attachTo = 'None' entonces attachea a container[id]
	NetAddr(ip, port).sendMsg('/literal_oneshot', msg);
}
)

~literal.(~id, 'backlash-addlyrics { qui- sie- ra ser un test }', \after);
~render.value(~id);
