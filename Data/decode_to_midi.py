from midiutil.MidiFile import MIDIFile


def export_midi(melody):

    # create your MIDI object
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 0
    volume = 100

    duration = 0.25  # Starting 16th note time value

    if melody[0] == -1:
        pitch = -1
    elif melody[0] == -2:
        pitch = 1
    else:
        pitch = melody[0]

    for note in melody[1:]:
        if note == -2:
            duration = duration + 0.25
            continue
        else:
            if pitch != -1:
                mf.addNote(track, channel, pitch, time, duration, volume)

            time = time + duration
            duration = 0.25
            if note == -1:
                pitch = -1
            else:
                pitch = note

    if melody[len(melody)-1] != -1:
        mf.addNote(track, channel, pitch, time, duration, volume)

    # write it to disk
    with open("output.mid", 'wb') as outf:
        mf.writeFile(outf)
