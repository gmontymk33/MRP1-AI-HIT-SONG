class Own_MidiFile():
    def __init__(self, length, ticks_per_beat, numerator, denominator, key, tempo, end_track_time, channels):
        self.length = length
        self.ticks_per_beat = ticks_per_beat
        self.numerator = numerator
        self.denominator = denominator
        self.key = key
        self.tempo = tempo
        self.end_track_time = end_track_time
        self.channels = channels
        self.number_of_notes = 127
        #Add one to number of nodes so that index starts from 1
        self.channels_without_note_off = [[] for i in range(len(channels))]
        self.flatten_tracks_without_duplicates()

    def flatten_tracks_without_duplicates(self):
        notes_played_at_same_time = [[0]*(self.number_of_notes + 1), 0]
        for idx,track in enumerate(self.channels):
            for note in track:
                if note.type == 'note_on':
                    notes_played_at_same_time[1] = note.time
                    notes_played_at_same_time[0][note.note] = 1
                elif note.type == 'note_off':
                    self.channels_without_note_off[idx].append(notes_played_at_same_time)
                    notes_played_at_same_time = [[0]*(self.number_of_notes + 1), 0]