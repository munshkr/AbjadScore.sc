AbjadScore {
	var <>host, <>port;

	*new { |host="127.0.0.1", port=5005|
		^super.newCopyArgs(host, port);
	}

	notes { |id, pbind|
		^AbjadPattern.new(this, id.asSymbol, pbind, \note).play;
	}

	render { |pattern|
		NetAddr(host, port).sendMsg("/display", pattern.id, \False);
	}

	preview { |pattern|
		NetAddr(host, port).sendMsg("/display", pattern.id, \True);
	}

	prSendEvents { |path, pairs|
		NetAddr(host, port).sendMsg(path, pairs.asString.drop(1).drop(-1));
		(pairs.asString + "\n").postln;
	}
}