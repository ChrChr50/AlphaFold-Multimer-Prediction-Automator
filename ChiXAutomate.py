from tempfile import tempdir
import gspread
import time
from datetime import date
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, DirMovedEvent
from chimerax.core.commands import run
import os
import bottle
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from boxsdk import Client, OAuth2

# INPUT THE FOLLOWING INFORMATION:
Google_Sheet = ''
AlphaFold_Directory = ''
CLIENT_ID = ''
CLIENT_SECRET = ''
Box_VideoFolder_ID = ''
Box_ModelFolder_ID = ''
VideoFile_Path = ''
ModelFolder_Path = ''

# Open spreadsheet and worksheets
gs = gspread.service_account()
sh = gs.open(Google_Sheet)
notes = sh.worksheet("Notes")
inter = sh.worksheet("Interaction")
seq = sh.worksheet("Protein Sequence")

# Compile protein sequence pairs
def protlist(proteins, sequences):
   for target in proteins:
      i = seq.col_values(1).index(target)
      temp = seq.col_values(2)[i]
      sequences.append(temp)

csix = inter.col_values(6)
csev = inter.col_values(7)
acc = []
acc2 = []
seqacc = []
seqacc2 = []
if len(csix) > len(csev):
   for x in range(len(csev) + 1, len(csix) + 1):
      val = inter.acell('B' + str(x)).value
      acc.append(val)
      val2 = inter.acell('C' + str(x)).value
      acc2.append(val2)
#     inter.update('G' + str(x), str(date.month) + '/' + str(date.day))
protlist(acc, seqacc)
protlist(acc2, seqacc2)

# Run AlphaFold predictions on ChimeraX
def iterate(num):
    time.sleep(3)
    run(session, 'alphafold predict ' + str(seqacc[num]) + ',' + str(seqacc2[num]))
    global first
    first = acc[num]
    global second
    second = acc2[num]

class DirHandler(FileSystemEventHandler):
    accum = 0
    def __init__(self):
        super(DirHandler, self).__init__()

    def on_created(self, event: DirCreatedEvent):
        time.sleep(3)
        run(session, 'select /A')
        run(session, 'color sel red')
        run(session, 'select clear')
        run(session, 'movie record')
        run(session, 'turn y 2 180')
        run(session, 'wait 180')
        run(session, 'movie encode')
        newfile = first + ' - ' + second + ' ' + str(date.today())
        newdir = os.path.join(AlphaFold_Directory, newfile)
        os.rename(event.src_path, newdir)

    def on_moved(self, event: DirMovedEvent):
        if DirHandler.accum < len(seqacc) - 1:
            DirHandler.accum += 1
            iterate(DirHandler.accum)
        else:
            print('Finished!')

scan = Observer()
actor = DirHandler()
scan.schedule(actor, path = AlphaFold_Directory)
scan.start()
iterate(0)

# Upload model folder and movie to Box
# The authenticate function definition was acquired from https://github.com/box/box-python-sdk/blob/main/demo/auth.py
def authenticate(oauth_class = OAuth2):
    class StoppableWSGIServer(bottle.ServerAdapter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._server = None

        def run(self, app):
            server_cls = self.options.get('server_class', WSGIServer)
            handler_cls = self.options.get('handler_class', WSGIRequestHandler)
            self._server = make_server(self.host, self.port, app, server_cls, handler_cls)
            self._server.serve_forever()

        def stop(self):
            self._server.shutdown()

    auth_code = {}
    auth_code_is_available = Event()

    local_oauth_redirect = bottle.Bottle()

    @local_oauth_redirect.get('/')
    def get_token():
        auth_code['auth_code'] = bottle.request.query.code
        auth_code['state'] = bottle.request.query.state
        auth_code_is_available.set()

    local_server = StoppableWSGIServer(host = 'localhost', port = 8080)
    server_thread = Thread(target=lambda: local_oauth_redirect.run(server = local_server))
    server_thread.start()

    oauth = oauth_class(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
    )
    auth_url, csrf_token = oauth.get_authorization_url('http://0.0.0.0')
    webbrowser.open(auth_url)

    auth_code_is_available.wait()
    local_server.stop()
    assert auth_code['state'] == csrf_token
    access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])

    print('access_token: ' + access_token)
    print('refresh_token: ' + refresh_token)

    return oauth, access_token, refresh_token

client = Client(authenticate()[0])

new_video = client.folder(Box_VideoFolder_ID).upload(VideoFile_Path)
new_folder = client.folder(Box_ModelFolder_ID).upload(ModelFolder_Path)