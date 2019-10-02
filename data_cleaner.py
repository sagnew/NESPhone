import math, os, subprocess

# from numpy import var
from scipy.stats import variation
from mido import MidiFile


DATA_DIRECTORY = '/home/sam/Code/NESPhone/MIDI_Files'
CLEANED_DATA_DIRECTORY = '/home/sam/Code/NESPhone/CLEANED_DATA'


def note_variation(track):
    return variation([msg.note for msg in track if msg.type == 'note_on'])


def non_meta_tracks(mid):
    not_meta_tracks = []

    for track in mid.tracks:
        meta_msgs = 0
        non_meta_msgs = 0

        for msg in track:
            if msg.is_meta:
                meta_msgs += 1
            else:
                non_meta_msgs += 1
        if non_meta_msgs > meta_msgs:
            not_meta_tracks.append(track)
    return not_meta_tracks


def remove_meta_tracks(mid):
    non_meta = non_meta_tracks(mid)
    for track in meta_tracks:
        if not track in non_meta:
            mid.tracks.remove(track)


def remove_empty_tracks(mid):
    empty_tracks = []

    for track in mid.tracks:
        if math.isnan(note_variation(track)):
            empty_tracks.append(track)

    for track in empty_tracks:
        mid.tracks.remove(track)


def remove_duplicate_tracks(mid):
    message_numbers = []
    duplicates = []

    for track in mid.tracks:

        if len(track) in message_numbers:
            duplicates.append(track)
        else:
            message_numbers.append(len(track))

    for track in duplicates:
        # It's probably a harmony track at this point.
        if len(non_meta_tracks(mid)) <= 3:
            return
        mid.tracks.remove(track)


def remove_drum_tracks(mid):
    # Go through and delete the track with the lowest variance.
    drum_tracks = []

    # Check to see if any tracks have titles like "drums" or "percussion"
    # or if the notes are on channel "9" because channel 10 on MIDI files
    # is for percussion, and channels are zero-indexed in mido.
    for track in mid.tracks:
        if (any(x in track.name.lower() for x in ['drum', 'perc']) or
               9 in [note.channel for note in track if not note.is_meta]):
            drum_tracks.append(track)

    for track in drum_tracks:
        mid.tracks.remove(track)


def reduce_to_three_tracks(mid):
    # Remove every track except for the 3 with the highest note variation.
    if len(mid.tracks) <= 3:
        return mid
    sorted_tracks = sorted(mid.tracks, key=note_variation)

    for track in sorted_tracks:
        if len(mid.tracks) > 3:
            mid.tracks.remove(track)


def clean_midi_file(mid):
    remove_drum_tracks(mid)
    remove_duplicate_tracks(mid)


if __name__ == '__main__':
    # Run through the cleaner functions and save the final track.
    for filename in os.listdir(DATA_DIRECTORY):
        try:
            mid = MidiFile('{}/{}'.format(DATA_DIRECTORY, filename), clip=True)
            clean_midi_file(mid)

            if len(non_meta_tracks(mid)) <= 3:
                # Assume that if these filters didn't reduce the tracks to two
                # square waves and a triangle wave, that they aren't usable.
                mid.save('{}/{}'.format(CLEANED_DATA_DIRECTORY, filename))
            else:
                # Print out all the tracks that have problems for inspection.
                print('\n{} - {}\n'.format(filename, str(mid)))
        except Exception as e:
            print(filename)
            print(e)

