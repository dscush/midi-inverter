import mido, tempfile

def invert_around_middle(note, middle_note):
    return note - ((note - middle_note) * 2)

def invert_midi(infile, invert_drums=False):
    mid = mido.MidiFile(file = infile)

    # Get highest and lowest notes
    highest_note = -1
    lowest_note = 1000
    first_note = None
    for track_num, track in enumerate(mid.tracks):
        if invert_drums or track_num != 10:
            for message in track:
                if message.type in ('note_on', 'note_off'):
                    if first_note is None:
                        first_note = message.note
                    lowest_note = min(lowest_note, message.note)
                    highest_note = max(highest_note, message.note)
    middle_note = (highest_note + lowest_note) / 2

    # Invert all the notes
    for track_num, track in enumerate(mid.tracks):
        if invert_drums or track_num != 10:
            for message in track:
                if message.type in ('note_on', 'note_off'):
                    message.note = message.note - ((message.note - middle_note) * 2)
    outfile = tempfile.TemporaryFile()
    mid.save(file = outfile)
    outfile.seek(0)
    return outfile
