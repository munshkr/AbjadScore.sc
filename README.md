# AbjadScore.sc

Render Abjad scores (Lylipond) using SuperCollider Patterns.

## Requirements

* SuperCollider 3.7+
* Lilypond 2.18+
* Python 3 and pip

## Install

Open a new document on your SuperCollider IDE and type:

```supercollider
Quarks.install("https://github.com/munshkr/AbjadScore.sc");
```

Then, on a terminal, go to the Quark directory and install AbjadOSC server:

```bash
pip install -r requirements.txt
```

## Usage

First run AbjadOSC server from the Quark directory:

```
./abjad-osc-server.py
```

Then, on SC, for example:

```supercollider
~score = AbjadScore.new;
// you can connect to a remote AbjadOSC server at 192.168.0.5 for example:
//~score = AbjadScore.new("192.168.0.5", 5005);

(
~foo = ~score.notes(\foo, Pbind(
	\voice, \upper,
	\dur, Pseq([Pn(1/12,6),1/4,Pn(1/6, 3),1/4, Pn(1/16, 4) ], repeats: 1),
	\octave, 4,
	\degree, Pser([0, 2, 6], 16),
));
)

~foo.preview;
~foo.render;

// oneshot messages
~foo.slur([4, 7]);
~foo.textSpanner([4], "aire", "tono", staff_padding: 6);
```

## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/munshkr/AbjadScore.sc. This project is intended to be a safe,
welcoming space for collaboration, and contributors are expected to adhere to
the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

## LICENSE

See [LICENSE](LICENSE)
