from flask import Flask, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse

import midi_converter

# Temporary values for local development.
UPLOAD_FOLDER = '/home/sam/Code/NESPhone/uploads'
HOSTING_URL='http//*server_url*/uploads'
app = Flask(__name__)


@app.route('/call', methods=['POST'])
def call():
    call_sid = request.form['CallSid']

    midi_file_path = midi_converter.generate_midi(call_sid)
    midi_converter.to_audio(midi_file_path, '{}/{}.wav'.format(UPLOAD_FOLDER, call_sid))

    resp = VoiceResponse()
    resp.play('{}/{}.wav'.format(HOSTING_URL, call_sid))
    return str(resp)


@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
