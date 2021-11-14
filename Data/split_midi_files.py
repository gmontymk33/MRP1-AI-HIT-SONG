from mido import MidiFile
import mido
import os
from os.path import join

def split():
    dir = "./Songs/"
    files = os.listdir(dir)
    for midifilename in files:
        if midifilename.endswith(".midi"):
            midi = MidiFile(join(dir, midifilename), clip=True)
            if len(midi.tracks[1:]) >= 4:
                #Perform splitting
                note_on_times = []
                acc_time = 0
                for note in midi.tracks[4]:
                    if note.type == "note_on":
                        note_on_times.append([acc_time, note.note])
                    
                    acc_time += note.time

                #tracks without the meta channel and the fourth channel
                tracks = midi.tracks[1:]
                del tracks[3]
                splits = {note: [mido.MidiTrack() for _ in range(len(tracks))] for [_, note] in note_on_times}

                #Check if any note is being played on the other channels before the first split
                #If so, set the first split to be identical in time as the first note being played
                if note_on_times[0][0] > 0:
                    for track in tracks:
                        for note in track:
                            if note.type == "note_on" and note.velocity > 0:
                                    note_on_times[0][0] = min(note_on_times[0][0], note.time)
                                    continue

                #Go through all channels and split according to the fourth channel note times
                for idx,track in enumerate(tracks):
                    curr_time = 0
                    
                    j = 0
                    for time_idx, [_, note_split] in enumerate(note_on_times):
                        if time_idx < len(note_on_times)-1:
                            stop_time = note_on_times[time_idx+1][0]
                        else:
                            stop_time = float("inf")
                        while j < len(track) and curr_time < stop_time:
                            note = track[j]
                            curr_time += note.time
                            splits[note_split][idx].append(note)
                            j += 1
                            if j < len(track) and (curr_time + track[j].time) > stop_time:
                                break

                #Save new midi file with split sections
                for (split, tracks) in splits.items():
                    new_midi = MidiFile()
                    new_midi.tracks.append(midi.tracks[0])
                    for track in tracks:
                        new_midi.tracks.append(track)
                    path_dir = f"./Songs/Split_songs"
                    if not os.path.exists(path_dir):
                        os.mkdir(path_dir)
                    path_dir += f"/{split}"
                    if not os.path.exists(path_dir):
                        os.mkdir(path_dir)
                    path_file = path_dir + f"/{midifilename}"
                    new_midi.save(path_file)
                    
                print(f"Split and saved {midifilename}")


split()