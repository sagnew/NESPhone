import os, re, subprocess


GENERATION_DIR = '/home/sam/Code/NESPhone/tmp/polyphony_rnn/generated'
soundfont = '/home/sam/Code/NESPhone/Famicom.sf2'
rnn_model = '/home/sam/Code/NESPhone/backup_rnn.mag'


def to_audio(midi_file, output_file):
    subprocess.call(['fluidsynth', '-T', 'wav', '-F',
                    output_file, '-ni', soundfont, midi_file])


def generate_midi(call_sid):
    output_dir = '{}/{}'.format(GENERATION_DIR, call_sid)

    # Using the model I trained. Change --run_dir to change the model used.
    args = ['polyphony_rnn_generate',
            '--run_dir', 'tmp/polyphony_rnn/logdir/run1/',
            '--output_dir', output_dir,
            '--num_outputs', '1',
            '--num_steps', '256']
            # '--hparams', '"batch_size=128,rnn_layer_sizes=[256,256,256]"',
            # '--primer_pitches', '[67,64,60]',
            # '--condition_on_primer', 'true',
            # '--inject_primer_during_generation', 'true']
    # args = ['polyphony_rnn_generate',
    #         '--bundle_file', rnn_model,
    #         '--output_dir', output_dir,
    #         '--num_outputs', '1',
    #         '--num_steps', '256',
    #         '--primer_pitches', '[67,64,60]',
    #         '--condition_on_primer', 'true',
    #         '--inject_primer_during_generation', 'true']
    subprocess.call(args)
    midi_file = os.listdir(output_dir)[0]

    return '{}/{}'.format(output_dir, midi_file)
