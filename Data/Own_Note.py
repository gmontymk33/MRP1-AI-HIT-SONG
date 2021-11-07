from os import times


class Own_Note():
    def __init__(self, channel, is_meta, is_realtime, note, time, type, velocity):
        self.channel = channel
        self.is_meta = is_meta
        self.is_realtime = is_realtime
        self.note = note
        self.time = time
        self.type = type
        self.velocity = velocity