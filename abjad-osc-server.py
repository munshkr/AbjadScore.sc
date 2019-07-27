"""
Minimum Abjad & OSC server

"""
from abjad import *
import argparse

from pythonosc import dispatcher
from pythonosc import osc_server

class Note:

  def __init__(self, pitch, duration, id):
        self.pitch = pitch
        self.duration = duration
        self.id = id

  def makeAndDisplay(self):
        note = abjad.Note(self.pitch, Duration(self.duration))
        abjad.show(note)

def show_note_handler(unused_addr, args, eventData):
  event = eval("{" + eventData + "}")
  note = Note(event['note'], event['dur'], "idCualunque")
  note.makeAndDisplay()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/note_event", show_note_handler, "Note")

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
