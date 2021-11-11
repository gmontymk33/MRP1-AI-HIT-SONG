from mido import MidiFile, Message
import os
from os.path import join
from Own_Note import Own_Note
from Own_MidiFile import Own_MidiFile
import music21
import glob

# Ryan:
# Slightly adjusted preprocess_midi the get_all_midi_files() method. Before, if no note was being played, it placed a
# copy of the previous note but with note.type = "rest". Now, it treats a rest more like a note; it adds a note with
# note.note = -1 and note.type = "note_on" when the rest starts and with note.type = "note_off" when it ends. I am not
# sure if the use of -1 as a note value causes trouble in the other methods. Most likely some small adjustments need to
# be made to those to accomodate for this special note value.


def get_all_midi_files():
    midi_files = []
    dir = "./Songs/" # If we are going to use different midi files (i.e. split verse/chorus), change to proper directory
    files = os.listdir(dir)
    print(len(files))
    for midifilename in files:
        if midifilename.endswith(".midi"):
            midi = MidiFile(join(dir, midifilename), clip=True)
            # if len(midi.tracks[1:]) == 1:
            #     print(midifilename)
            if len(midi.tracks[1:]) > 2:
                tracks = midi.tracks[1:]
                for i in range(len(tracks)):
                    new_track = []
                    curr_tick = 0
                    for note in tracks[i]:
                        if note.type == 'note_on' or note.type == 'note_off':
                            new_note = Own_Note(note.channel, note.is_meta, note.is_realtime, note.note, note.time, note.type, note.velocity)
                            if note.type == "note_on" and note.time > 0: # note.note == -1 represents a rest
                                hold_note_on = Own_Note(note.channel, note.is_meta, note.is_realtime, -1, note.time, "note_on", note.velocity)
                                hold_note_on.time += curr_tick-note.time
                                new_track.append(hold_note_on)
                                hold_note_off = Own_Note(note.channel, note.is_meta, note.is_realtime, -1, note.time, "note_off", note.velocity)
                                hold_note_off.time += curr_tick
                                new_track.append(hold_note_off)

                            new_note.time += curr_tick
                            curr_tick = new_note.time
                            new_track.append(new_note)
                    tracks[i] = new_track

                midi_file = Own_MidiFile(midi.length, midi.ticks_per_beat, midi.tracks[0][1].numerator, midi.tracks[0][1].denominator, midi.tracks[0][2].key, midi.tracks[0][3].tempo, midi.tracks[0][4].time, tracks)
                midi_files.append(midi_file)

    return midi_files

# midi_files = get_all_midi_files()
# print(len(midi_files))


"""
This code transposes the keys of all midi files to C major if it's a major key or C minor if it's a minor key and it saves
the output songs in the same file. Run transpose_key function once in order to produce the midi files in C key.
"""


def transpose_key():
    os.chdir("C:/Users/fib0/PycharmProjects/MRP1-AI-HIT-SONG/Data/Songs")

    majors = dict(
        [("A-", 4), ("A", 3), ("B-", 2), ("B", 1), ("C", 0), ("D-", -1), ("D", -2), ("E-", -3), ("E", -4), ("F", -5),
         ("G-", 6), ("G", 5), ("G#", 4), ("F#", 6), ("D#", -3), ("C#", -1), ("A#", 2)])
    minors = dict(
        [("A-", 4), ("A", 3), ("B-", 2), ("B", 1), ("C", 0), ("D-", -1), ("D", -2), ("E-", -3), ("E", -4), ("F", -5),
         ("G-", 6), ("G", 5), ("C#", -1), ("D#", -3), ("F#", 6), ("G#", 4), ("A#", 2)])

    # Store the total number of midi files
    total_size = len(glob.glob("*.midi"))

    # The number of songs scanned so far
    number_of_songs = 0

    for file in glob.glob("*.midi"):
        score = music21.converter.parse(file)
        key = score.analyze('key')

        print("For song " + str(number_of_songs) + " The key tonic name before = " + str(
            key.tonic.name) + " and the key mode = " + str(key.mode))

        if key.mode == "major":
            halfSteps = majors[key.tonic.name]

        elif key.mode == "minor":
            halfSteps = minors[key.tonic.name]

        newscore = score.transpose(halfSteps)
        key = newscore.analyze('key')
        print(key.tonic.name, key.mode + "\n")

        # Check if the output key is correct

        if key.tonic.name != "C":
            print("Not A minor or C major")
            break

        newFileName = "C_" + file
        newscore.write('midi', newFileName)

        number_of_songs += 1

        # Termination of the function when every song has been transposed

        if number_of_songs > total_size:
            break