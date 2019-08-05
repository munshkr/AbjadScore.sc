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
				[\id, \articulation, \fermata].do({|key| //send as String
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
						['dur', 'freq', 'amp', 'rest'].includes(key)
					}
				);

				[\id, \literal, \position].do({|key| //send as String
					selectedKeys[key] !? {
						selectedKeys[key] = selectedKeys[key].asCompileString;
					}
			})},

			\markup, {
				selectedKeys[\direction] ?? {selectedKeys[\direction] = 'Up'}; //set default direction. Do not send as String

				selectedKeys = selectedKeys.reject( //literal event cleaning
					{
						|item, key|
						['dur', 'freq', 'amp', 'rest'].includes(key)
					}
				);

				[\id, \markup, \format].do({|key| //send as String
					selectedKeys[key] !? {
						selectedKeys[key] = selectedKeys[key].asCompileString;
					};
			})}
		);

		selectedKeys.reject({|item, key|
			key.isNil
		});

		e.addr.sendMsg(path, selectedKeys.asString.replace("(", "").replace(")", ""));
		(selectedKeys.asString+"\n").postln;
});
)

////// Para el usuario
(
~id = \id0;

a = Pbind(
	\abjad, \note,
	\id, ~id,
	\addr, n,
	\dur, Pseq([1/8, 3/8, 1/8, 1/8, 1/8, 1], 1),
	\degree, Pseq([4, 4, 4, 5, 6, 7], inf),
	\articulation, Pseq(["", "", "", "", "", 'accent'], 1),
	\articDirection, \Down,
	\fermata, Pseq(["", "", "", "", "", 'longfermata'], 1),
);

b = Pbind(
	\abjad, \literal,
	\addr, n,
	\id, ~id,
	\position, \after,
	\literal, 'backlash-addlyrics { Qui- sie- ra ser un test }', //backlash- -> hack horrible
	\dur, Pseq([1]),
);

c = Pbind(
	\abjad, \markup,
	\addr, n,
	\id, ~id,
	\direction, \Up, //no se envía como string porque hace referencia a un atributo. abjad.Up / abjad.Down
	\markup, 'Allegro grassoso',

	//debería ser \command porque abjad.MarkupCommand ?
	\format, [ 'italic', 'sans', 'box'], //[ 'italic', 'caps', 'center_align', 'circle', 'bold', 'box', 'bracket', 'huge', 'larger', 'normal_text', 'parenthesize', 'sans', 'small', 'smaller', 'tiny', 'upright', 'vcenter', 'whiteout' ] //Advertencia: no son todos combinables. Ej. 'italics' mata 'caps'
	\dur, Pseq([1]),
);
)

(
(~abjadPattern <> a).play;
(~abjadPattern <> b).play;
(~abjadPattern <> c).play;
)
~render.value(~id);