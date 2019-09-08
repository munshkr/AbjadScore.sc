AbjadScore {
	var <>host, <>port;

	*new { |host="127.0.0.1", port=5005|
		^super.newCopyArgs(host, port);
	}

	render {
		NetAddr(host, port).sendMsg("/display", id, 'False');
	}

	preview {
		NetAddr(host, port).sendMsg("/display", id, 'True');
	}
}