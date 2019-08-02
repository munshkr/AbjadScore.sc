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
#from os import path
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

notes = {}

class NoteSC: #mejorar el nombre de la clase
    container = {}
    #staff = {}
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.id not in self.container.keys():
            self.container[self.id] = Container()
            #self.staff[self.id] = Staff(self.container[self.id]) #Hacer un Staff para meter los containers genericos??

    def make(self):
        if self.rest:
            note = Rest(Duration(self.dur))
        else:
            note = Note(NumberedPitch.from_hertz(self.freq), Duration(self.dur))

        self.container[self.id].append(note)

    def display(self, id):
        make_ly = persist(NoteSC.container[self.id]).as_ly()
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
    notes[event['id']] = NoteSC(**event)
    notes[event['id']].make()


def literal_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}") #eval elimina la posibilidad de "\\" para imprimir "\"?
    event['literal'] = event['literal'].replace("backlash-", "\\") #hack horrible
    #lyrics = LilyPondLiteral(r'\addlyrics {' + event['lyrics'] + '}', 'after') #Manejando LilyPondLiteral en server, mmm... no es buena idea, tendria que duplicar el codigo por cada posible LilyPondLiteral
    literal = LilyPondLiteral(event['literal'], event['position']) #Manejando LilyPondLiteral en client
    attach(literal, notes[event['id']].container[event['id']]) #Algo en el diseno esta mal, quiero que el scope de containers sea accesible de afuera pero no se si es la manera. Ademas es igual a escribir NoteSC.container[event['id']] ?


def display_handler(unused_addr, args, id):
    notes[id].display(id)


def main(args):
    dispatcher = Dispatcher()
    dispatcher.map("/literal_event", literal_handler, "Literal")
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
    #parser.add_argument("--output",
    #    default=path.expanduser('./output'),
    #    help="Location of compiled .ly")
    parser.add_argument("--output",
        default='./output',
        help="Location of compiled .ly")

    args = parser.parse_args()

    main(args)
