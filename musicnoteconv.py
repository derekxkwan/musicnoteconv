note_dict = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
# (sharp, flat) tuples
step_dict = {0: ('c','c'),
             1: ('cs', 'df'),
             2: ('d', 'd'),
             3: ('ds', 'ef'),
             4: ('e', 'e'),
             5: ('f', 'f'),
             6: ('fs', 'gf'),
             7: ('g', 'g'),
             8: ('gs', 'af'),
             9: ('a','a'),
             10: ('as', 'bf'),
             11: ('b', 'b')}
sign_dict = {"n": 0, "f": -1, "s": 1}

def note_to_midi(nstr):
    nlower = nstr.lower()
    note = ""
    nsign = "n"
    octave = 0
    if len(nlower) == 2:
        note = nlower[0]
        octave = int(nlower[1])
    else:
        note = nlower[0]
        nsign = nlower[1]
        octave = int(nlower[2])
    midi = note_dict.get(note, 0) + sign_dict.get(nsign, 0) + (octave+1)*12
    return midi


def midi_to_note(midinote, sharp = True):
    octave = midinote//12 - 1
    offset_from_c = int(midinote) % 12
    cur_note = None
    if sharp == True:
        cur_note = step_dict[offset_from_c][0]
    else:
        cur_note = step_dict[offset_from_c][1]
    ret = f'{cur_note}{octave}'
    return ret

def midi_to_hz(mnote):
    freq = 440.*(2.**(float(mnote-69.)/12.))
    return freq

def note_to_hz(nstr):
    mnote = note_to_midi(nstr)
    freq = midi_to_hz(mnote)
    return freq

def ms_to_bpm(ms):
    return 60000./ms

def bpm_to_ms(bpm):
    return 60000./bpm

def dur_to_ms(ndur, bpm):
    ms = bpm_to_ms(bpm)
    first_dot_idx = -1
    if "." in ndur:
        first_dot_idx = ndur.index(".")
    reldur = 4.
    if first_dot_idx >= 1:
        reldur = 4./int(ndur[:first_dot_idx])
        num_dots = len(ndur[first_dot_idx:])
        add_dur = reldur * 0.5
        for _ in range(num_dots):
            reldur += add_dur
            add_dur *= 0.5
    else:
        reldur = 4./int(ndur)
    reldur *= ms
    return reldur

def ndur_to_hz_ms(nstr2, bpm):
    dur = "4"
    nstr = "a4"
    if ":" in nstr2:
        nstr, dur = nstr2.split("|")
    hz = note_to_hz(nstr)
    ms = dur_to_ms(dur,bpm)
    return (hz,ms)

def ndurstr_to_hz_ms(ndurstr, bpm):
    return [ndur_to_hz_ms(x,bpm) for x in ndurstr.split(" ")]

def ndurstr_to_hz_ms2(ndurstr, bpm):
    hzarr = []
    darr = []
    for x in ndurstr.split(" "):
        hz,ms = ndur_to_hz_ms(x, bpm)
        hzarr.append(hz)
        darr.append(ms)
    return hzarr, darr
