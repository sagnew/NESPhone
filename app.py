import os

from flask import Flask, request, send_from_directory
from redis import Redis
from rq import Queue
from twilio.twiml.voice_response import VoiceResponse

import music_generator

# Temporary values for local development.
UPLOAD_FOLDER = '/home/sam/Code/NESPhone/uploads'

q = Queue(connection=Redis())
app = Flask(__name__)


@app.route('/call', methods=['POST'])
def call():
    call_sid = request.form['CallSid']

    output_file = '{}/{}.wav'.format(UPLOAD_FOLDER, call_sid)
    q.enqueue(music_generator.generate_nes_music, call_sid, output_file)

    resp = VoiceResponse()
    resp.pause()
    resp.say('Please wait while we generate some new Nintendo music for you.')

    # Wait until we asynchronously update the call after music is generated.
    resp.pause(length=100)

    return str(resp)


@app.route('/play_music', methods=['POST'])
def play():
    call_sid = request.form['CallSid']
    output_file = '{}/{}.wav'.format(UPLOAD_FOLDER, call_sid)

    resp = VoiceResponse()
    resp.play('/uploads/{}.wav'.format(call_sid))
    return str(resp)


@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
