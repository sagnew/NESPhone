import os

from flask import Flask, request, send_from_directory
from redis import Redis
from rq import Queue
from twilio.twiml.voice_response import VoiceResponse

import midi_converter

# Temporary values for local development.
UPLOAD_FOLDER = '/home/sam/Code/NESPhone/uploads'

q = Queue(connection=Redis())
app = Flask(__name__)


@app.route('/call', methods=['POST'])
def call():
    call_sid = request.form['CallSid']

    output_file = '{}/{}.wav'.format(UPLOAD_FOLDER, call_sid)
    q.enqueue(midi_converter.generate_nes_music, call_sid, output_file)

    resp = VoiceResponse()
    resp.pause()
    resp.say('Please wait while we generate some new Nintendo music for you.')
    resp.redirect('/waiting_room')

    return str(resp)


@app.route('/waiting_room', methods=['POST'])
def wait():
    call_sid = request.form['CallSid']
    output_file = '{}/{}.wav'.format(UPLOAD_FOLDER, call_sid)

    resp = VoiceResponse()

    if os.path.isfile(output_file):
        resp.play('/uploads/{}.wav'.format(call_sid))
    else:
        resp.pause(length=2)
        resp.redirect('/waiting_room')
    return str(resp)


@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
