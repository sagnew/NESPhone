import asyncio
import os

from quart import Quart, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse

from music_generator import generate_nes_music


# Folder where the generated music will be.
UPLOAD_FOLDER = 'output/'

app = Quart(__name__)


@app.route('/call', methods=['POST'])
async def call():
    form_data = await request.form
    call_sid = form_data['CallSid']

    # The file we want the final .wav file to be saved to.
    output_file = '{}/{}.wav'.format(UPLOAD_FOLDER, call_sid)

    # Spin up an async task to generate the music.
    # After this task is completed, the phone call will be updated.
    # asyncio.get_running_loop().run_in_executor(None, generate_nes_music(call_sid, output_file))
    asyncio.ensure_future(generate_nes_music(call_sid, output_file))

    resp = VoiceResponse()
    resp.pause()
    resp.say('Please wait while we generate some new Nintendo music for you.')

    # Wait until we asynchronously update the call after music is generated.
    resp.pause(length=100)

    return str(resp)


@app.route('/play_music', methods=['POST'])
async def play():
    # call_sid = await request.form['CallSid']
    form_data = await request.form
    call_sid = form_data['CallSid']

    output_file = '{}/{}.wav'.format(UPLOAD_FOLDER, call_sid)

    resp = VoiceResponse()
    resp.play('/uploads/{}.wav'.format(call_sid))
    return str(resp)


@app.route('/uploads/<filename>', methods=['GET', 'POST'])
async def uploaded_file(filename):
    return await send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

