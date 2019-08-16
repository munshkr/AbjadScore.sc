#!/usr/bin/env python
"""
Abjad & OSC server

Requiere:
Lilypond >= 2.19??
Abjad

Default ip: 127.0.0.1
Default port: 5005
Default output path = './output'
"""

from abjad import *
import subprocess
import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

notes = {}

clef = Clef('bass')

class LeafGenerator:
    container = {}
    voices = {}
    #voices = { 'id1000' : {'upper' : Voice() ,'lower' : Voice()}, 'id1001' : {'upper' : Voice()} }

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.id not in self.container.keys():
            self.container[self.id] = Measure()

        if self.id not in self.voices.keys():
            self.voices[self.id] = { self.voice : Voice() }

        if self.voice not in self.voices[self.id].keys():
            self.voices[self.id]= { self.voice : Voice() }

    def make(self):
        if self.rest:
            fraction = Fraction(self.dur).limit_denominator(40)
            duration = Duration(fraction)
            pitch = None
            leaves = LeafMaker()(pitch, duration)
        else:
            pitch = NumberedPitch.from_hertz(self.freq)
            fraction = Fraction(self.dur).limit_denominator(40)
            duration = Duration(fraction)
            leaves = LeafMaker()(pitch, duration)

            try:
                if len(self.articulation) > 0:
                    articulation = Articulation(self.articulation, direction=self.articDirection)
                    for leaf in abjad.iterate(leaves).leaves():
                        attach(articulation, leaf)
            except AttributeError:
                print("Note has no Articulation attribute")

            try:
                if len(self.fermata) > 0:
                    fermata = Fermata(command = self.fermata)
                    for leaf in abjad.iterate(leaves).leaves():
                        attach(fermata, leaf)
            except AttributeError:
                print("Note has no Fermata attribute")

            try:
                markup = Markup(self.markup, direction=self.markupDirection)
                if len(self.markupCommand) > 0:
                    for command in self.markupCommand:
                        string = "markup."+command+"()"
                        markup = eval(string)
                for leaf in abjad.iterate(leaves).leaves():
                    attach(markup, leaf)
            except AttributeError:
                print("Note has no Markup attribute")

        self.voices[self.id][self.voice].append(leaves) #Agregar las notas al Voice
        self.container[self.id].append(self.voices[self.id][self.voice]) #Agregar el Voice al Measure
        attach(clef, select(self.container[self.id]).leaves()[0]) #Agrega el Clef al Measure
        self.container[self.id].automatically_adjust_time_signature = True #Ajusta el Measure a la métrica de compás

    def display(self, id):
        make_ly = persist(LeafGenerator.container[self.id]).as_ly()
        ly_path = make_ly[0]
        cmd = ['lilypond',
               '-dcrop',
               '-dpoint-and-click',
               '-ddelete-intermediate-files',
               '-dbackend=svg',
               '-o' + args.output,
               ly_path]
        subprocess.run(cmd)

def note_handler(unused_addr, args, eventData):
    event = eval("{" + eventData + "}")
    notes[event['id']] = LeafGenerator(**event)
    notes[event['id']].make()

def literal_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}") #eval elimina la posibilidad de "\\" para imprimir "\"?
    event['literal'] = event['literal'].replace("backlash-", "\\") #hack horrible
    id = event['id']
    attachTo = event['attachTo']
    literal = LilyPondLiteral(event['literal'], event['position'])
    if attachTo is None:
        attach(literal, notes[id].container[id])
    else:
        attach(literal, notes[id].container[id][attachTo])

def markup_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    event['markup'] = event['markup'].replace("backlash-", "\\") #hack horrible
    id = event['id']
    attachTo = event['attachTo']
    markup = Markup(event['markup'], direction=event['markupDirection'])
    #To-Do: handler para MarkupCommand que acepta argumentos
    try:
        if len(event['markupCommand']) > 0:
            for command in event['markupCommand']:
                string = "markup."+command+"()"
                markup = eval(string)
    except AttributeError:
        print("Event has no markup format attribute")

    attach(markup, notes[id].container[id][attachTo])

def display_handler(unused_addr, args, id):
    notes[id].display(id)


def main(args):
    dispatcher = Dispatcher()
    dispatcher.map("/literal_oneshot", literal_handler, "Literal")
    dispatcher.map("/markup_oneshot", markup_handler, "Markup")
    dispatcher.map("/note_event", note_handler, "Note")
    dispatcher.map("/note_display", display_handler, "Display")

    server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)

    print("Serving on {}".format(server.server_address))
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--ip",
        default="127.0.0.1",
        help="The ip to listen on")
    parser.add_argument("--port",
        type=int,
        default=5005,
        help="The port to listen on")
    parser.add_argument("--output",
        default='./output',
        help="Location of compiled .ly")

    args = parser.parse_args()

    main(args)
