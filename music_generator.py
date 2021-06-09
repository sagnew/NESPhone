import asyncio, re, subprocess, os

from twilio.rest import Client


APP_URL = 'https://sagnew.ngrok.io'
GENERATION_DIR = 'midi/'

soundfont = 'Famicom.sf2'
rnn_model = 'nes_rnn.mag'

# Create a Twilio Client object.
# Don't forget! Set environment variables with your Account SID and auth token.
client = Client()


# Takes a path to a midi and creates a .wav file with the Famicom soundfont.
async def to_audio(midi_file, output_file):
    args = ['fluidsynth', '-T',
            'wav', '-F', output_file,
            '-ni', soundfont, midi_file]

    process = await asyncio.create_subprocess_exec(*args)
    await process.communicate()


# Uses the NES RNN model to generate a new MIDI file for a phone call.
async def generate_midi(call_sid):
    output_dir = '{}/{}'.format(GENERATION_DIR, call_sid)
    args = ['polyphony_rnn_generate',
            '--bundle_file', rnn_model,
            '--output_dir', output_dir,
            '--num_outputs', '1',
            '--num_steps', '256']

    process = await asyncio.create_subprocess_exec(*args)
    await process.communicate()

    midi_file = os.listdir(output_dir)[0]

    return '{}/{}'.format(output_dir, midi_file)


async def generate_nes_music(call_sid, output_file):
    midi_file_path = await generate_midi(call_sid)
    await to_audio(midi_file_path, output_file)

    # After the music is generated. Update the phone call to play it.
    client.calls(call_sid).update(url='{}/play_music'.format(APP_URL))

