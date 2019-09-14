#!/usr/bin/env python
"""
Abjad & OSC server

Requiere:
Lilypond >= 2.19??
Abjad
Lilypond custom stylesheets from Abjad '/docs/source/_stylesheets/default.ily'

Default ip: 127.0.0.1
Default port: 5005
Default output path = './output'
"""

from abjad import *
import subprocess
import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import os
from flask import Flask, render_template, request, escape

DEFAULT_INCLUDES = [os.path.join(os.path.dirname(os.path.realpath(__file__)), 'styles', 'default.ily')]

notes = {} #store {'id' : [generated leaves]} //refactor cuando tenga claro que hacer con los containers Voice -> Measure -> Staff

message = "Test message";

clef = Clef('bass')

class LeafGenerator:
    container = {}
    voices = {}
    #voices = { 'id1000' : {'upper' : Voice() ,'lower' : Voice()}, 'id1001' : {'upper' : Voice()} }
    includes = []

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.id not in self.container.keys():
            #self.container[self.id] = Measure()
            self.container[self.id] = Staff()

#Voice(components=None, lilypond_type='Voice', is_simultaneous=None, name=None)
        #print(self.voice)

        if self.id not in self.voices.keys():
            self.voices[self.id] = { self.voice : Voice(name = self.voice) }
        if self.voice not in self.voices[self.id].keys():
            self.voices[self.id][self.voice] = Voice(name = self.voice)


    def add_leaf_to_voice(self, leaf, voice):
        #print(len(select(voice).leaves()))
        #print(voice)
        if len(select(voice).leaves()) > 0:
            lastLeaf = voice[-1]
            if type(leaf[0]) is type(Tuplet()):
                if type(lastLeaf) is type(leaf[0]):
                    if leaf[0].multiplier == lastLeaf.multiplier:
                        lastLeaf.extend(leaf[0])
                    else:
                        voice.append(leaf)
                else:
                        voice.append(leaf)
            else:
                voice.append(leaf)
        else:
            voice.append(leaf)

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
                #print("Note has no Articulation attribute")
                None

            try:
                if len(self.dynamic) > 0:
                    dynamic = Dynamic(
                            self.dynamic,
                            direction=self.dynamicDirection
                            )
                    for leaf in abjad.iterate(leaves).leaves():
                        attach(dynamic, leaf)
            except AttributeError:
                #print("Note has no Dynamic attribute")
                None

            try:
                if len(self.fermata) > 0:
                    fermata = Fermata(command = self.fermata)
                    for leaf in abjad.iterate(leaves).leaves():
                        attach(fermata, leaf)
            except AttributeError:
                None
                #print("Note has no Fermata attribute")

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
                #print("Note has no Markup attribute")
                None

            try:
                if len(self.notehead) > 0:
                    if self.notehead == 'transparent':
                        for leaf in abjad.iterate(leaves).leaves():
                            override(leaf).note_head.transparent = True
                    else:
                        for leaf in abjad.iterate(leaves).leaves():
                            override(leaf).note_head.style = self.notehead
            except AttributeError:
                None
                #print("Note has no Notehead attribute")



        #self.container[self.id].automatically_adjust_time_signature = True #Ajusta el Measure a la métrica de compás

        self.add_leaf_to_voice(leaves, self.voices[self.id][self.voice])
        #self.voices[self.id][self.voice].append(leaves) #Agregar las notas al Voice
        self.container[self.id].append(self.voices[self.id][self.voice]) #Agregar el Voice al Container
        attach(clef, select(self.container[self.id]).leaves()[0]) #Agrega el Clef al Measure

    def display(self, id, preview):
        music = LeafGenerator.container[self.id]
        voice_direction = {}
        if len(music) > 1:
            music.is_simultaneous = True
            for i, voice in enumerate(music):
                if i % 2 == 0: #if voice number is even
                    direction = Down
                else:
                    direction = Up
                voice_direction[voice.name] = direction
                override(voice).stem.direction = direction
        else:
            voice = music[0]
            voice_direction[voice.name] = None


        output_path = args.output
        if preview == True:
            output_path = args.output + '_preview'
            colors = ['blue', 'darkblue', 'cyan', 'darkcyan']
            for voice_num, voice in enumerate(music):
                for leaf_num, leaf in enumerate(voice):
                    number = str(voice_num) + '-' + str(leaf_num)
                    markup = Markup(number, direction = voice_direction[voice.name]).tiny().with_color(colors[voice_num])
                    attach(markup, leaf, tag='PREVIEW')
                voice_markup = Markup('Voice '+ str(voice_num) + ':' + voice.name, direction = voice_direction[voice.name]).box().with_color(colors[voice_num])
                attach(voice_markup, voice[0], tag='PREVIEW')
            id_markup = Markup('ID: ' + id, direction = Up).box().with_color(SchemeColor('purple'))
            attach(id_markup, select(music).leaves()[0], tag='PREVIEW')
        else:
            for voice_num, voice in enumerate(music):
                for leaf_num, leaf in enumerate(voice):
                    wrapper = inspect(leaf).wrappers(Markup)
                    try:
                        tag = wrapper[0].tag
                        if tag == Tag('PREVIEW'):
                            detach(Markup, leaf)
                    except:
                        None

        lilypond_file = LilyPondFile.new(
               music = music,
               includes = self.includes
        )
        make_ly = persist(lilypond_file).as_ly()
        ly_path = make_ly[0]
        cmd = ['lilypond',
               '-dcrop',
               '-dno-point-and-click',
               '-ddelete-intermediate-files',
               '-dbackend=svg',
               '-o' + output_path,
               ly_path]
        subprocess.run(cmd)

    def clear(id):
        if id in LeafGenerator.container:
            del LeafGenerator.container[id]
        if id in LeafGenerator.voices:
            del LeafGenerator.voices[id]

## Handlers ##
### Leaves ###

def note_handler(unused_addr, args, eventData):
    global message
    event = eval("{" + eventData + "}")
    if event.get('new'):
        id = event['id']
        message = id
        if id in notes:
            del notes[id]
        LeafGenerator.clear(id)
    else:
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

### Indicators ###
def dynamic_handler(unused_addr, args, eventData):
    #name='f', *, command=None, direction=None, format_hairpin_stop=None, hide=None, leak=None, name_is_textual=None, ordinal=None, sforzando=None, tweaks=None
    event = eval("{ " + eventData + "}")
    #print(event)
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
        #print("Event has no markup format attribute")
        None

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

def bar_line_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    event['bar_line'] = event['bar_line'].replace("backlash-", "\\") #hack horrible
    id = event['id']
    bar_line = BarLine(event['bar_line'])
    detach( BarLine, select(notes[id].container[id]).leaves()[event['index']])
    attach( bar_line, select(notes[id].container[id]).leaves()[event['index']])

def notehead_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    leaf = select(notes[id].container[id]).leaves()[event['index']]
    if event['notehead'] == 'transparent':
        override(leaf).note_head.transparent = True
    else:
        override(leaf).note_head.style = event['notehead']

### Spanners ###
def slur_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    slur = Slur(direction = event['direction'])
    selection = select(notes[id].container[id]).leaves() #selecciona leaves de Measure. Como hago para seleccionar leaves del Voice dentro de ese Measure?
    default_slice = [0, len(selection), 1]
    slice_params = event['slice']
    for i in range(len(default_slice)):
        try:
            slice_params[i]
        except IndexError:
            slice_params.append(default_slice[i])
    slice_obj = slice(slice_params[0],slice_params[1],slice_params[2]) #reescribir mas pythonico
    detach(Slur, selection[slice_obj])
    attach(slur, selection[slice_obj])

def tie_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    tie = Tie(direction = event['direction'], left_broken = event['left_broken'], repeat = event['repeat'], right_broken = event['right_broken'])
    selection = select(notes[id].container[id]).leaves() #selecciona leaves de Measure. Como hago para seleccionar leaves del Voice dentro de ese Measure?
    default_slice = [0, len(selection), 1]
    slice_params = event['slice']
    for i in range(len(default_slice)):
        try:
            slice_params[i]
        except IndexError:
            slice_params.append(default_slice[i])
    slice_obj = slice(slice_params[0],slice_params[1],slice_params[2]) #reescribir mas pythonico
    detach(Tie, selection[slice_obj])
    attach(tie, selection[slice_obj])

def text_spanner_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    markup_left = Markup(
            event['left_text'],
            #direction=event['direction']
            #tweaks=event['tweaks']
            )

    markup_right = Markup(
            event['right_text'],
            #direction=event['direction']
            #tweaks=event['tweaks']
            )
    """
    try:
        if len(event['markupCommand']) > 0:
            for command in event['markupCommand']:
                string_left = "markup_left."+command+"()"
                string_right = "markup_right."+command+"()"
                markup_left = eval(string_left)
                markup_right = eval(string_right)
    except AttributeError:
        pass
    """
    start_text_span = StartTextSpan(left_text = markup_left, right_text = markup_right, style = event['style'])
    selection = select(notes[id].container[id]).leaves()
    default_slice = [0, len(selection), 1]
    slice_params = event['slice']
    for i in range(len(default_slice)):
        try:
            slice_params[i]
        except IndexError:
            slice_params.append(default_slice[i])
    slice_obj = slice(slice_params[0],slice_params[1],slice_params[2]) #reescribir mas pythonico
    #detach(text_spanner(), selection[slice_obj])
    #text_spanner(selection[slice_obj], start_text_span=start_text_span)
    override(selection[slice_params[0]]).text_spanner.staff_padding = event['staff_padding'] # -dcrop svg de lilypond no tiene en cuenta este override!
    text_spanner(selection[slice_obj], start_text_span=start_text_span, stop_text_span = None)

### Removing items ###
def detach_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    detach( event['attachment'],
            select(notes[id].container[id]).leaves()[event['index']]
            )

def remove_handler(unused_addr, args, eventData):
    event = eval("{ " + eventData + "}")
    id = event['id']
    voice_name = event['voice']
    voice = notes[id].container[id][voice_name] 
    voice.remove(voice[event['index']])

### Display ###
def display_handler(unused_addr, args, id, preview):
    notes[id].display(id, eval(preview))

## OSC Server ##
def main(args):
    LeafGenerator.includes = DEFAULT_INCLUDES + args.include
    dispatcher = Dispatcher()
    dispatcher.map("/remove", remove_handler, "Remove")
    dispatcher.map("/detach", detach_handler, "Detach")
    dispatcher.map("/slur_oneshot", slur_handler, "Slur")
    dispatcher.map("/tie_oneshot", tie_handler, "Tie")
    dispatcher.map("/text_spanner_oneshot", text_spanner_handler, "Text Spanner")
    dispatcher.map("/notehead_oneshot", notehead_handler, "Notehead")
    dispatcher.map("/bar_line_oneshot", bar_line_handler, "BarLine")
    dispatcher.map("/articulation_oneshot", articulation_handler, "Articulation")
    dispatcher.map("/dynamic_oneshot", dynamic_handler, "Dynamic")
    dispatcher.map("/dynamicTrend_oneshot", dynamicTrend_handler, "DynamicTrend")
    dispatcher.map("/literal_oneshot", literal_handler, "Literal")
    dispatcher.map("/markup_oneshot", markup_handler, "Markup")
    dispatcher.map("/note_event", note_handler, "Note")
    dispatcher.map("/display", display_handler, "Display")

    server = osc_server.ThreadingOSCUDPServer((args.host, args.port), dispatcher)

    print("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host",
        default="localhost",
        help="The ip to listen on")
    parser.add_argument("-P", "--port",
        type=int,
        default=5005,
        help="The port to listen on")
    parser.add_argument("-O", "--output",
        default='./static/svg/output',
        help="Location of compiled .ly")
    parser.add_argument("-I", "--include",
        default=[],
        nargs="+",
        help="Include Lilypond file")
    args = parser.parse_args()
    main(args)

    app.run(host="localhost", port=5005) #Flask

## Flask ##
app = Flask(__name__)
@app.route("/tuba")
def html_render():
    #name = request.args.get("name", "World")
    return render_template('output.html', message = message)

@app.route("/preview")
def html_preview():
    #name = request.args.get("name", "World")
    return render_template('output_preview.html', message = message)
