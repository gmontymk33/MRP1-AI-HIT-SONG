import random
from melody_input import notes2index
from melody_input import intlist2onehot
from melody_input import midi_to_int_melody

# TODO Once range of notes we will used has been decided, change this in all methods and test!

def note_distribution(melodies):
    # Finds a distribution of the different notes over all of the training songs
    freq = [0] * 38  # TODO Change if number of notes is not 36
    note_total = 0
    for s,m in melodies.items():
        mel_idx = notes2index(m)
        note_total += len(mel_idx)
        for idx in mel_idx:
            freq[idx] += 1
    distribution = [num/note_total for num in freq]
    return distribution


def rand_input_melody(length):
    # Generates a random melody input for the network based on the distribution of the notes in the training data
    notes = [-1, -2, range(36, 72)]  # TODO Change if range of notes is not 36-71
    # Probability distribution found from note_distribution
    probs = [] # TODO Find distribution using note_distribution, then add it in here
    # Generate a list of note values
    mel = random.choices(notes, weights=probs, k=length)
    # Turn this into onehot for melody input
    return intlist2onehot(mel)


if __name__ == "__main__":
    pass


