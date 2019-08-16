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
	\amp, 0,
	\rest, Pfunc({|e|
		var string = e.isRest.asString;
		string[0] = string[0].toUpper;
		string; }),

	\finish, {|e|
		var path = "/" ++ e.abjad ++"_event";
		var selectedKeys = e.reject( //general cleaning
			{
				|item, key|
				['server', 'delta', 'path', 'addr', 'type', 'abjad', 'finish'].includes(key)
			}
		);

		switch ( e.abjad,

			\note, {
				[\freq, \dur].do({|key| //use current freq for event note, strip Rest() when \dur is Rest
					selectedKeys[key] = selectedKeys.use({('~'++key).interpret.value});
				});
				[\id, \articulation, \fermata, \markup, \markupCommand, \voice, \octave].do({|key| //send as String
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
						['Dur', 'freq', 'amp', 'rest'].includes(key)
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
~id = \id105;

a = Pbind(
	\abjad, \note,
	\voice, 'upper',
	\id, ~id,
	\addr, n,
	\dur, Pseq([Pn(1/12, 6), Pn(1/10, 5), 1/3, 2/3, Pn(1/8, 4) ], repeats: 1),
	\octave, 4,
	\degree, Pseq([4, 4, 4, 5, 6, 7], inf),
	\articulation, Pseq(["", "", "", "", "", 'accent'], inf),
	\articDirection, \Down,
	\fermata, Pseq(["", "", "", "", "", 'longfermata'], inf),
	\markupDirection, \Up, //no se envía como string porque hace referencia a un atributo. abjad.Up / abjad.Down
	\markup, Pseq(['Allegro', 'sfz', 'sffz', 'flurry'], inf),
	\markupCommand, Pseq([ ['italic'], ['dynamic', 'sans'], ['dynamic', 'box'], ['bold']],inf),
	//estaría bueno que no tenga que ser enviado como array cuando contiene solo un elemento (ver en python)
	//REVISAR: Cómo hacer para enviar un markup vacío??? "" -> genera un rest event :-(
);
)

(~abjadPattern <> a).play;
~render.value(~id);

//oneshot msgs
//attach to container[x] element
(
~markup = {
	|id, markup, markupDirection = 'Up', format="", attachTo = 0, ip = "127.0.0.1", port = 5005|
	var msg = "'id': " ++ id.asCompileString
	++ ", 'markup': " ++ markup.asCompileString
	++ ", 'markupDirection': " ++ markupDirection
	++ ", 'markupCommand': " ++ markupCommand.asCompileString
	++ ", 'attachTo': " ++ attachTo;
	NetAddr(ip, port).sendMsg('/markup_oneshot', msg);
}
//[ 'italic', 'caps', 'center_align', 'circle', 'bold', 'box', 'bracket', 'huge', 'larger', 'normal_text', 'parenthesize', 'sans', 'small', 'smaller', 'tiny', 'upright', 'vcenter', 'whiteout' ]
//Advertencia: no son todos combinables. Ej. 'italic' mata 'caps'
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
