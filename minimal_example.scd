n = NetAddr("127.0.0.1", 5005);

(
var virtualenvPath = "/home/yako/.virtualenvs/abjad/bin/activate";
var scriptPath = "/home/yako/python-code/abjad-osc-server_0.02.py";
("source "++ virtualenvPath ++";"++
"python "++ scriptPath ++ " --ip " ++ n.ip ++ " --port " ++ n.port).unixCmd { |res, pid| [\done, res, pid].postln };
)

(
Pbindef(
	\oscTest,
	\note, Pwhite(0,12,2),
	\dur, 1,
	\send, Pfunc ({|event|
			n.sendMsg("/note_event", event.asString.removeBrackets);
			event.postln;
		})
).play
)