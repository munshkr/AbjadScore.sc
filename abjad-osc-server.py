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

notes = {} #store {'id' : [generated leaves]}

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

#Voice(components=None, lilypond_type='Voice', is_simultaneous=None, name=None)
        if self.id not in self.voices.keys():
            self.voices[self.id] = { self.voice : Voice(name = self.voice) }
        if self.voice not in self.voices[self.id].keys():
            self.voices[self.id]= { self.voice : Voice(name = self.voice) }

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
            #LeafMaker(decrease_monotonic=True, forbidden_duration=None, metrical_hierarchy=None, skips_instead_of_rests=False, repeat_ties=False, use_multimeasure_rests=False)

            try:
                if len(self.articulation) > 0:
                    articulation = Articulation(
                            self.articulation,
                            direction=self.articDirection
                            )
                    for leaf in abjad.iterate(leaves).leaves():
                        attach(articulation, leaf)
            except AttributeError:
                print("Note has no Articulation attribute")

            try:
                if len(self.dynamic) > 0:
                    dynamic = Dynamic(
                            self.dynamic,
                            direction=self.dynamicDirection
                            )
                    for leaf in abjad.iterate(leaves).leaves():
                        attach(dynamic, leaf)
            except AttributeError:
                print("Note has no Dynamic attribute")

            try:
                if len(self.fermata) > 0:
                    fermata = Fermata(command = self.fermata)
                    for leaf in abjad.iterate(leaves).leaves():
                        attach(fermata, leaf)
            except AttributeError:
                print("Note has no Fermata attribute")

            try:
                markup = Markup(
                        self.markup,
                        direction=self.markupDirection)
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
        includes = ['/home/yako/.virtualenvs/abjad/lib/python3.7/site-packages/abjad/docs/source/_stylesheets/default.ily']
        lilypond_file = LilyPondFile.new(
               music = LeafGenerator.container[self.id],
               includes = includes
        )
        make_ly = persist(lilypond_file).as_ly()
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
    index = event['index']
    literal = LilyPondLiteral(
            event['literal'],
            event['position'],
            tweaks=event['tweaks']
            )
    if index is None:
        attach(literal, notes[id].container[id])
    else:
        attach(literal, notes[id].container[id][index])

def dynamic_handler(unused_addr, args, eventData):
    #name='f', *, command=None, direction=None, format_hairpin_stop=None, hide=None, leak=None, name_is_textual=None, ordinal=None, sforzando=None, tweaks=None
    event = eval("{ " + eventData + "}")
    print(event)
    id = event['id']
    if event['command'] == 'None':
        event['command'] = None
    else:
        event['command'] = event['command'].replace("backlash-", "\\") #hack horrible
    dynamic = Dynamic(
            event['dynamic'],
            command = event['command'],
            direction = event['direction'],
            name_is_textual=event['name_is_textual'],
            tweaks=event['tweaks']
            )
    detach( DynamicTrend,
            select(notes[id].container[id]).leaves()[event['index']]
            )
    detach( Dynamic,
            select(notes[id].container[id]).leaves()[event['index']]
            )
    attach( dynamic,
            select(notes[id].container[id]).leaves()[event['index']]
            )

def dynamicTrend_handler(unused_addr, args, eventData):
    # shape='<', *, left_broken=None, tweaks=None
    event = eval("{ " + eventData + "}")
    id = event['id']
    dynamicTrend = DynamicTrend(
            shape=event['shape'],
            left_broken=event['left_broken'],
            tweaks=event['tweaks']
            )
    #DynamicTrend convive con Dynamic en el mismo leaf, pero puede eliminarlo on 'left_broken'
    detach( DynamicTrend,
            select(notes[id].container[id]).leaves()[event['index']]
            )
    attach( dynamicTrend,
            select(notes[id].container[id]).leaves()[event['index']]
            )

def markup_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    event['markup'] = event['markup'].replace("backlash-", "\\") #hack horrible
    id = event['id']
    markup = Markup(
            event['markup'],
            direction=event['direction'],
            tweaks=event['tweaks']
            )
    #To-Do: handler para MarkupCommand que acepta argumentos
    try:
        if len(event['markupCommand']) > 0:
            for command in event['markupCommand']:
                string = "markup."+command+"()"
                markup = eval(string)
    except AttributeError:
        print("Event has no markup format attribute")

    attach( markup,
            select(notes[id].container[id]).leaves()[event['index']]
            )

def articulation_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    event['articulation'] = event['articulation'].replace("backlash-", "\\") #hack horrible
    id = event['id']
    articulation = Articulation(
            event['articulation'],
            direction=event['direction'],
            tweaks=event['tweaks']
            )

    attach( articulation,
            select(notes[id].container[id]).leaves()[event['index']]
            )


def detach_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    detach( event['attachment'],
            select(notes[id].container[id]).leaves()[event['index']]
            )

def remove_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    voice = notes[id].container[id][0] #Para arreglar: VOICE HARDCODEADA EN MEASURE[0]
    voice.remove(voice[event['index']])
   #notes[id].container[id].pop([event['index']])

def display_handler(unused_addr, args, id):
    notes[id].display(id)

def main(args):
    dispatcher = Dispatcher()
    dispatcher.map("/remove", remove_handler, "Remove")
    dispatcher.map("/detach", detach_handler, "Detach")
    dispatcher.map("/articulation_oneshot", articulation_handler, "Articulation")
    dispatcher.map("/dynamic_oneshot", dynamic_handler, "Dynamic")
    dispatcher.map("/dynamicTrend_oneshot", dynamicTrend_handler, "DynamicTrend")
    dispatcher.map("/literal_oneshot", literal_handler, "Literal")
    dispatcher.map("/markup_oneshot", markup_handler, "Markup")
    dispatcher.map("/note_event", note_handler, "Note")
    dispatcher.map("/display", display_handler, "Display")

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
