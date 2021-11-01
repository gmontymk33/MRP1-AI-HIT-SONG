from mido import MidiFile
import os
from os.path import join
from Own_MidiFile import Own_MidiFile

def get_all_midi_files():
    midi_files = []
    dir = "./Data/Songs"
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
                            note.time += curr_tick
                            curr_tick = note.time
                            new_track.append(note)
                    tracks[i] = new_track

                midi_file = Own_MidiFile(midi.length, midi.ticks_per_beat, midi.tracks[0][1].numerator, midi.tracks[0][1].denominator, midi.tracks[0][2].key, midi.tracks[0][3].tempo, midi.tracks[0][4].time, tracks)
                midi_files.append(midi_file)

    return midi_files

# midi_files = get_all_midi_files()
# print(len(midi_files))