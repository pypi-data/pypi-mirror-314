r'''#===================================================================================================================
#
# MIDI to Colab AUdio Python Module
#
# Converts any MIDI file to raw audio which is compatible 
# with Google Colab or HUgging Face Gradio
#
# Version 1.0
#
# Includes full source code of MIDI, pyfluidsynth, and midi_synthesizer Python modules
# 
# Original source code for all modules was retrieved on 10/23/2023
#
# Project Los Angeles
# Tegridy Code 2023
#
#===================================================================================================================
#
# Critical dependencies
#
# pip install numpy
# sudo apt install fluidsynth
#
#===================================================================================================================
# 
# Example usage:
#
# from midi_to_colab_audio import midi_to_colab_audio
# from IPython.display import display, Audio
#
# raw_audio = midi_to_colab_audio('/content/input.mid')
#
# display(Audio(raw_audio, rate=16000, normalize=False))
#
#===================================================================================================================
#! /usr/bin/python3
# unsupported 20091104 ...
#     ['set_sequence_number', dtime, sequence]
#     ['raw_data', dtime, raw]

# 20150914   jimbo1qaz   MIDI.py str/bytes bug report
# I found a MIDI file which had Shift-JIS titles. When midi.py decodes it as
# latin-1, it produces a string which cannot even be accessed without raising
# a UnicodeDecodeError.  Maybe, when converting raw byte strings from MIDI,
# you should keep them as bytes, not improperly decode them.  However, this
# would change the API.  (ie: text = a "string" ? of 0 or more bytes).  It
# could break compatiblity, but there's not much else you can do to fix the bug
# https://en.wikipedia.org/wiki/Shift_JIS

This module offers functions:  concatenate_scores(), grep(),
merge_scores(), mix_scores(), midi2opus(), midi2score(), opus2midi(),
opus2score(), play_score(), score2midi(), score2opus(), score2stats(),
score_type(), segment(), timeshift() and to_millisecs(),
where "midi" means the MIDI-file bytes (as can be put in a .mid file,
or piped into aplaymidi), and "opus" and "score" are list-structures
as inspired by Sean Burke's MIDI-Perl CPAN module.

Warning: Version 6.4 is not necessarily backward-compatible with
previous versions, in that text-data is now bytes, not strings.
This reflects the fact that many MIDI files have text data in
encodings other that ISO-8859-1, for example in Shift-JIS.

Download MIDI.py from   http://www.pjb.com.au/midi/free/MIDI.py
and put it in your PYTHONPATH.  MIDI.py depends on Python3.

There is also a call-compatible translation into Lua of this
module: see http://www.pjb.com.au/comp/lua/MIDI.html

Backup web site: https://peterbillam.gitlab.io/miditools/

The "opus" is a direct translation of the midi-file-events, where
the times are delta-times, in ticks, since the previous event.

The "score" is more human-centric; it uses absolute times, and
combines the separate note_on and note_off events into one "note"
event, with a duration:
 ['note', start_time, duration, channel, note, velocity] # in a "score"

  EVENTS (in an "opus" structure)
     ['note_off', dtime, channel, note, velocity]       # in an "opus"
     ['note_on', dtime, channel, note, velocity]        # in an "opus"
     ['key_after_touch', dtime, channel, note, velocity]
     ['control_change', dtime, channel, controller(0-127), value(0-127)]
     ['patch_change', dtime, channel, patch]
     ['channel_after_touch', dtime, channel, velocity]
     ['pitch_wheel_change', dtime, channel, pitch_wheel]
     ['text_event', dtime, text]
     ['copyright_text_event', dtime, text]
     ['track_name', dtime, text]
     ['instrument_name', dtime, text]
     ['lyric', dtime, text]
     ['marker', dtime, text]
     ['cue_point', dtime, text]
     ['text_event_08', dtime, text]
     ['text_event_09', dtime, text]
     ['text_event_0a', dtime, text]
     ['text_event_0b', dtime, text]
     ['text_event_0c', dtime, text]
     ['text_event_0d', dtime, text]
     ['text_event_0e', dtime, text]
     ['text_event_0f', dtime, text]
     ['end_track', dtime]
     ['set_tempo', dtime, tempo]
     ['smpte_offset', dtime, hr, mn, se, fr, ff]
     ['time_signature', dtime, nn, dd, cc, bb]
     ['key_signature', dtime, sf, mi]
     ['sequencer_specific', dtime, raw]
     ['raw_meta_event', dtime, command(0-255), raw]
     ['sysex_f0', dtime, raw]
     ['sysex_f7', dtime, raw]
     ['song_position', dtime, song_pos]
     ['song_select', dtime, song_number]
     ['tune_request', dtime]

  DATA TYPES
     channel = a value 0 to 15
     controller = 0 to 127 (see http://www.pjb.com.au/muscript/gm.html#cc )
     dtime = time measured in "ticks", 0 to 268435455
     velocity = a value 0 (soft) to 127 (loud)
     note = a value 0 to 127  (middle-C is 60)
     patch = 0 to 127 (see http://www.pjb.com.au/muscript/gm.html )
     pitch_wheel = a value -8192 to 8191 (0x1FFF)
     raw = bytes, of length 0 or more  (for sysex events see below)
     sequence_number = a value 0 to 65,535 (0xFFFF)
     song_pos = a value 0 to 16,383 (0x3FFF)
     song_number = a value 0 to 127
     tempo = microseconds per crochet (quarter-note), 0 to 16777215
     text = bytes, of length 0 or more
     ticks = the number of ticks per crochet (quarter-note)

   In sysex_f0 events, the raw data must not start with a \xF0 byte,
   since this gets added automatically;
   but it must end with an explicit \xF7 byte!
   In the very unlikely case that you ever need to split sysex data
   into one sysex_f0 followed by one or more sysex_f7s, then only the
   last of those sysex_f7 events must end with the explicit \xF7 byte
   (again, the raw data of individual sysex_f7 events must not start
   with any \xF7 byte, since this gets added automatically).

   Since version 6.4, text data is in bytes, not in a ISO-8859-1 string.


  GOING THROUGH A SCORE WITHIN A PYTHON PROGRAM
    channels = {2,3,5,8,13}
    itrack = 1   # skip 1st element which is ticks
    while itrack < len(score):
        for event in score[itrack]:
            if event[0] == 'note':   # for example,
                pass  # do something to all notes
            # or, to work on events in only particular channels...
            channel_index = MIDI.Event2channelindex.get(event[0], False)
            if channel_index and (event[channel_index] in channels):
                pass  # do something to channels 2,3,5,8 and 13
        itrack += 1

'''

import sys, struct, copy
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'wb')
Version = '6.7'
VersionDate = '20201120'
# 20201120 6.7 call to bytest() removed, and protect _unshift_ber_int
# 20160702 6.6 to_millisecs() now handles set_tempo across multiple Tracks
# 20150921 6.5 segment restores controllers as well as patch and tempo
# 20150914 6.4 text data is bytes or bytearray, not ISO-8859-1 strings
# 20150628 6.3 absent any set_tempo, default is 120bpm (see MIDI file spec 1.1)
# 20150101 6.2 all text events can be 8-bit; let user get the right encoding
# 20141231 6.1 fix _some_text_event; sequencer_specific data can be 8-bit
# 20141230 6.0 synth_specific data can be 8-bit
# 20120504 5.9 add the contents of mid_opus_tracks()
# 20120208 5.8 fix num_notes_by_channel() ; should be a dict
# 20120129 5.7 _encode handles empty tracks; score2stats num_notes_by_channel
# 20111111 5.6 fix patch 45 and 46 in Number2patch, should be Harp
# 20110129 5.5 add mix_opus_tracks() and event2alsaseq()
# 20110126 5.4 "previous message repeated N times" to save space on stderr
# 20110125 5.2 opus2score terminates unended notes at the end of the track
# 20110124 5.1 the warnings in midi2opus display track_num
# 21110122 5.0 if garbage, midi2opus returns the opus so far
# 21110119 4.9 non-ascii chars stripped out of the text_events
# 21110110 4.8 note_on with velocity=0 treated as a note-off
# 21110108 4.6 unknown F-series event correctly eats just one byte
# 21011010 4.2 segment() uses start_time, end_time named params
# 21011005 4.1 timeshift() must not pad the set_tempo command
# 21011003 4.0 pitch2note_event must be chapitch2note_event
# 21010918 3.9 set_sequence_number supported, FWIW
# 20100913 3.7 many small bugfixes; passes all tests
# 20100910 3.6 concatenate_scores enforce ticks=1000, just like merge_scores
# 20100908 3.5 minor bugs fixed in score2stats
# 20091104 3.4 tune_request now supported
# 20091104 3.3 fixed bug in decoding song_position and song_select
# 20091104 3.2 unsupported: set_sequence_number tune_request raw_data
# 20091101 3.1 document how to traverse a score within Python
# 20091021 3.0 fixed bug in score2stats detecting GM-mode = 0
# 20091020 2.9 score2stats reports GM-mode and bank msb,lsb events
# 20091019 2.8 in merge_scores, channel 9 must remain channel 9 (in GM)
# 20091018 2.7 handles empty tracks gracefully
# 20091015 2.6 grep() selects channels
# 20091010 2.5 merge_scores reassigns channels to avoid conflicts
# 20091010 2.4 fixed bug in to_millisecs which now only does opusses
# 20091010 2.3 score2stats returns channels & patch_changes, by_track & total
# 20091010 2.2 score2stats() returns also pitches and percussion dicts
# 20091010 2.1 bugs: >= not > in segment, to notice patch_change at time 0
# 20091010 2.0 bugs: spurious pop(0) ( in _decode sysex
# 20091008 1.9 bugs: ISO decoding in sysex; str( not int( in note-off warning
# 20091008 1.8 add concatenate_scores()
# 20091006 1.7 score2stats() measures nticks and ticks_per_quarter
# 20091004 1.6 first mix_scores() and merge_scores()
# 20090424 1.5 timeshift() bugfix: earliest only sees events after from_time
# 20090330 1.4 timeshift() has also a from_time argument
# 20090322 1.3 timeshift() has also a start_time argument
# 20090319 1.2 add segment() and timeshift()
# 20090301 1.1 add to_millisecs()

_previous_warning = ''  # 5.4
_previous_times = 0     # 5.4
#------------------------------- Encoding stuff --------------------------

def opus2midi(opus=[]):
    r'''The argument is a list: the first item in the list is the "ticks"
parameter, the others are the tracks. Each track is a list
of midi-events, and each event is itself a list; see above.
opus2midi() returns a bytestring of the MIDI, which can then be
written either to a file opened in binary mode (mode='wb'),
or to stdout by means of:   sys.stdout.buffer.write()

my_opus = [
    96, 
    [   # track 0:
        ['patch_change', 0, 1, 8],   # and these are the events...
        ['note_on',   5, 1, 25, 96],
        ['note_off', 96, 1, 25, 0],
        ['note_on',   0, 1, 29, 96],
        ['note_off', 96, 1, 29, 0],
    ],   # end of track 0
]
my_midi = opus2midi(my_opus)
sys.stdout.buffer.write(my_midi)
'''
    if len(opus) < 2:
        opus=[1000, [],]
    tracks = copy.deepcopy(opus)
    ticks = int(tracks.pop(0))
    ntracks = len(tracks)
    if ntracks == 1:
        format = 0
    else:
        format = 1

    my_midi = b"MThd\x00\x00\x00\x06"+struct.pack('>HHH',format,ntracks,ticks)
    for track in tracks:
        events = _encode(track)
        my_midi += b'MTrk' + struct.pack('>I',len(events)) + events
    _clean_up_warnings()
    return my_midi


def score2opus(score=None):
    r'''
The argument is a list: the first item in the list is the "ticks"
parameter, the others are the tracks. Each track is a list
of score-events, and each event is itself a list.  A score-event
is similar to an opus-event (see above), except that in a score:
 1) the times are expressed as an absolute number of ticks
    from the track's start time
 2) the pairs of 'note_on' and 'note_off' events in an "opus"
    are abstracted into a single 'note' event in a "score":
    ['note', start_time, duration, channel, pitch, velocity]
score2opus() returns a list specifying the equivalent "opus".

my_score = [
    96,
    [   # track 0:
        ['patch_change', 0, 1, 8],
        ['note', 5, 96, 1, 25, 96],
        ['note', 101, 96, 1, 29, 96]
    ],   # end of track 0
]
my_opus = score2opus(my_score)
'''
    if len(score) < 2:
        score=[1000, [],]
    tracks = copy.deepcopy(score)
    ticks = int(tracks.pop(0))
    opus_tracks = []
    for scoretrack in tracks:
        time2events = dict([])
        for scoreevent in scoretrack:
            if scoreevent[0] == 'note':
                note_on_event = ['note_on',scoreevent[1],
                 scoreevent[3],scoreevent[4],scoreevent[5]]
                note_off_event = ['note_off',scoreevent[1]+scoreevent[2],
                 scoreevent[3],scoreevent[4],scoreevent[5]]
                if time2events.get(note_on_event[1]):
                   time2events[note_on_event[1]].append(note_on_event)
                else:
                   time2events[note_on_event[1]] = [note_on_event,]
                if time2events.get(note_off_event[1]):
                   time2events[note_off_event[1]].append(note_off_event)
                else:
                   time2events[note_off_event[1]] = [note_off_event,]
                continue
            if time2events.get(scoreevent[1]):
               time2events[scoreevent[1]].append(scoreevent)
            else:
               time2events[scoreevent[1]] = [scoreevent,]

        sorted_times = []  # list of keys
        for k in time2events.keys():
            sorted_times.append(k)
        sorted_times.sort()

        sorted_events = []  # once-flattened list of values sorted by key
        for time in sorted_times:
            sorted_events.extend(time2events[time])

        abs_time = 0
        for event in sorted_events:  # convert abs times => delta times
            delta_time = event[1] - abs_time
            abs_time = event[1]
            event[1] = delta_time
        opus_tracks.append(sorted_events)
    opus_tracks.insert(0,ticks)
    _clean_up_warnings()
    return opus_tracks

def score2midi(score=None):
    r'''
Translates a "score" into MIDI, using score2opus() then opus2midi()
'''
    return opus2midi(score2opus(score))

#--------------------------- Decoding stuff ------------------------

def midi2opus(midi=b''):
    r'''Translates MIDI into a "opus".  For a description of the
"opus" format, see opus2midi()
'''
    my_midi=bytearray(midi)
    if len(my_midi) < 4:
        _clean_up_warnings()
        return [1000,[],]
    id = bytes(my_midi[0:4])
    if id != b'MThd':
        _warn("midi2opus: midi starts with "+str(id)+" instead of 'MThd'")
        _clean_up_warnings()
        return [1000,[],]
    [length, format, tracks_expected, ticks] = struct.unpack(
     '>IHHH', bytes(my_midi[4:14]))
    if length != 6:
        _warn("midi2opus: midi header length was "+str(length)+" instead of 6")
        _clean_up_warnings()
        return [1000,[],]
    my_opus = [ticks,]
    my_midi = my_midi[14:]
    track_num = 1   # 5.1
    while len(my_midi) >= 8:
        track_type   = bytes(my_midi[0:4])
        if track_type != b'MTrk':
            _warn('midi2opus: Warning: track #'+str(track_num)+' type is '+str(track_type)+" instead of b'MTrk'")
        [track_length] = struct.unpack('>I', my_midi[4:8])
        my_midi = my_midi[8:]
        if track_length > len(my_midi):
            _warn('midi2opus: track #'+str(track_num)+' length '+str(track_length)+' is too large')
            _clean_up_warnings()
            return my_opus   # 5.0
        my_midi_track = my_midi[0:track_length]
        my_track = _decode(my_midi_track)
        my_opus.append(my_track)
        my_midi = my_midi[track_length:]
        track_num += 1   # 5.1
    _clean_up_warnings()
    return my_opus

def opus2score(opus=[]):
    r'''For a description of the "opus" and "score" formats,
see opus2midi() and score2opus().
'''
    if len(opus) < 2:
        _clean_up_warnings()
        return [1000,[],]
    tracks = copy.deepcopy(opus)  # couple of slices probably quicker...
    ticks = int(tracks.pop(0))
    score = [ticks,]
    for opus_track in tracks:
        ticks_so_far = 0
        score_track = []
        chapitch2note_on_events = dict([])   # 4.0
        for opus_event in opus_track:
            ticks_so_far += opus_event[1]
            if opus_event[0] == 'note_off' or (opus_event[0] == 'note_on' and opus_event[4] == 0):  # 4.8
                cha = opus_event[2]
                pitch = opus_event[3]
                key = cha*128 + pitch
                if chapitch2note_on_events.get(key):
                    new_event = chapitch2note_on_events[key].pop(0)
                    new_event[2] = ticks_so_far - new_event[1]
                    score_track.append(new_event)
                elif pitch > 127:
                    pass #_warn('opus2score: note_off with no note_on, bad pitch='+str(pitch))
                else:
                    pass #_warn('opus2score: note_off with no note_on cha='+str(cha)+' pitch='+str(pitch))
            elif opus_event[0] == 'note_on':
                cha = opus_event[2]
                pitch = opus_event[3]
                key = cha*128 + pitch
                new_event = ['note',ticks_so_far,0,cha,pitch, opus_event[4]]
                if chapitch2note_on_events.get(key):
                    chapitch2note_on_events[key].append(new_event)
                else:
                    chapitch2note_on_events[key] = [new_event,]
            else:
                opus_event[1] = ticks_so_far
                score_track.append(opus_event)
        # check for unterminated notes (Oisín) -- 5.2
        for chapitch in chapitch2note_on_events:
            note_on_events = chapitch2note_on_events[chapitch]
            for new_e in note_on_events:
                new_e[2] = ticks_so_far - new_e[1]
                score_track.append(new_e)
                pass #_warn("opus2score: note_on with no note_off cha="+str(new_e[3])+' pitch='+str(new_e[4])+'; adding note_off at end')
        score.append(score_track)
    _clean_up_warnings()
    return score

def midi2score(midi=b''):
    r'''
Translates MIDI into a "score", using midi2opus() then opus2score()
'''
    return opus2score(midi2opus(midi))

def midi2ms_score(midi=b''):
    r'''
Translates MIDI into a "score" with one beat per second and one
tick per millisecond, using midi2opus() then to_millisecs()
then opus2score()
'''
    return opus2score(to_millisecs(midi2opus(midi)))

#------------------------ Other Transformations ---------------------

def to_millisecs(old_opus=None):
    r'''Recallibrates all the times in an "opus" to use one beat
per second and one tick per millisecond.  This makes it
hard to retrieve any information about beats or barlines,
but it does make it easy to mix different scores together.
'''
    if old_opus == None:
        return [1000,[],]
    try:
        old_tpq  = int(old_opus[0])
    except IndexError:   # 5.0
        _warn('to_millisecs: the opus '+str(type(old_opus))+' has no elements')
        return [1000,[],]
    new_opus = [1000,]
    # 6.7 first go through building a table of set_tempos by absolute-tick
    ticks2tempo = {}
    itrack = 1
    while itrack < len(old_opus):
        ticks_so_far = 0
        for old_event in old_opus[itrack]:
            if old_event[0] == 'note':
                raise TypeError('to_millisecs needs an opus, not a score')
            ticks_so_far += old_event[1]
            if old_event[0] == 'set_tempo':
                ticks2tempo[ticks_so_far] = old_event[2]
        itrack += 1
    # then get the sorted-array of their keys
    tempo_ticks = []  # list of keys
    for k in ticks2tempo.keys():
        tempo_ticks.append(k)
    tempo_ticks.sort()
    # then go through converting to millisec, testing if the next
    # set_tempo lies before the next track-event, and using it if so.
    itrack = 1
    while itrack < len(old_opus):
        ms_per_old_tick = 500.0 / old_tpq  # float: will round later 6.3
        i_tempo_ticks = 0
        ticks_so_far = 0
        ms_so_far = 0.0
        previous_ms_so_far = 0.0
        new_track = [['set_tempo',0,1000000],]  # new "crochet" is 1 sec
        for old_event in old_opus[itrack]:
            # detect if ticks2tempo has something before this event
            # 20160702 if ticks2tempo is at the same time, leave it
            event_delta_ticks = old_event[1]
            if (i_tempo_ticks < len(tempo_ticks) and
              tempo_ticks[i_tempo_ticks] < (ticks_so_far + old_event[1])):
                delta_ticks = tempo_ticks[i_tempo_ticks] - ticks_so_far
                ms_so_far += (ms_per_old_tick * delta_ticks)
                ticks_so_far = tempo_ticks[i_tempo_ticks]
                ms_per_old_tick = ticks2tempo[ticks_so_far] / (1000.0*old_tpq)
                i_tempo_ticks += 1
                event_delta_ticks -= delta_ticks
            new_event = copy.deepcopy(old_event)  # now handle the new event
            ms_so_far += (ms_per_old_tick * old_event[1])
            new_event[1] = round(ms_so_far - previous_ms_so_far)
            if old_event[0] != 'set_tempo':
                previous_ms_so_far = ms_so_far
                new_track.append(new_event)
            ticks_so_far += event_delta_ticks
        new_opus.append(new_track)
        itrack += 1
    _clean_up_warnings()
    return new_opus

def event2alsaseq(event=None):   # 5.5
    r'''Converts an event into the format needed by the alsaseq module,
http://pp.com.mx/python/alsaseq
The type of track (opus or score) is autodetected.
'''
    pass

def grep(score=None, channels=None):
    r'''Returns a "score" containing only the channels specified
'''
    if score == None:
        return [1000,[],]
    ticks = score[0]
    new_score = [ticks,]
    if channels == None:
        return new_score
    channels = set(channels)
    global Event2channelindex
    itrack = 1
    while itrack < len(score):
        new_score.append([])
        for event in score[itrack]:
            channel_index = Event2channelindex.get(event[0], False)
            if channel_index:
                if event[channel_index] in channels:
                    new_score[itrack].append(event)
            else:
                new_score[itrack].append(event)
        itrack += 1
    return new_score

def play_score(score=None):
    r'''Converts the "score" to midi, and feeds it into 'aplaymidi -'
'''
    if score == None:
        return
    import subprocess
    pipe = subprocess.Popen(['aplaymidi','-'], stdin=subprocess.PIPE)
    if score_type(score) == 'opus':
        pipe.stdin.write(opus2midi(score))
    else:
        pipe.stdin.write(score2midi(score))
    pipe.stdin.close()

def timeshift(score=None, shift=None, start_time=None, from_time=0, tracks={0,1,2,3,4,5,6,7,8,10,12,13,14,15}):
    r'''Returns a "score" shifted in time by "shift" ticks, or shifted
so that the first event starts at "start_time" ticks.

If "from_time" is specified, only those events in the score
that begin after it are shifted. If "start_time" is less than
"from_time" (or "shift" is negative), then the intermediate
notes are deleted, though patch-change events are preserved.

If "tracks" are specified, then only those tracks get shifted.
"tracks" can be a list, tuple or set; it gets converted to set
internally.

It is deprecated to specify both "shift" and "start_time".
If this does happen, timeshift() will print a warning to
stderr and ignore the "shift" argument.

If "shift" is negative and sufficiently large that it would
leave some event with a negative tick-value, then the score
is shifted so that the first event occurs at time 0. This
also occurs if "start_time" is negative, and is also the
default if neither "shift" nor "start_time" are specified.
'''
    #_warn('tracks='+str(tracks))
    if score == None or len(score) < 2:
        return [1000, [],]
    new_score = [score[0],]
    my_type = score_type(score)
    if my_type == '':
        return new_score
    if my_type == 'opus':
        _warn("timeshift: opus format is not supported\n")
        # _clean_up_scores()  6.2; doesn't exist! what was it supposed to do?
        return new_score
    if not (shift == None) and not (start_time == None):
        _warn("timeshift: shift and start_time specified: ignoring shift\n")
        shift = None
    if shift == None:
        if (start_time == None) or (start_time < 0):
            start_time = 0
        # shift = start_time - from_time

    i = 1   # ignore first element (ticks)
    tracks = set(tracks)  # defend against tuples and lists
    earliest = 1000000000
    if not (start_time == None) or shift < 0:  # first find the earliest event
        while i < len(score):
            if len(tracks) and not ((i-1) in tracks):
                i += 1
                continue
            for event in score[i]:
                 if event[1] < from_time:
                     continue  # just inspect the to_be_shifted events
                 if event[1] < earliest:
                     earliest = event[1]
            i += 1
    if earliest > 999999999:
        earliest = 0
    if shift == None:
        shift = start_time - earliest
    elif (earliest + shift) < 0:
        start_time = 0
        shift = 0 - earliest

    i = 1   # ignore first element (ticks)
    while i < len(score):
        if len(tracks) == 0 or not ((i-1) in tracks):  # 3.8
            new_score.append(score[i])
            i += 1
            continue
        new_track = []
        for event in score[i]:
            new_event = list(event)
            #if new_event[1] == 0 and shift > 0 and new_event[0] != 'note':
            #    pass
            #elif new_event[1] >= from_time:
            if new_event[1] >= from_time:
                # 4.1 must not rightshift set_tempo
                if new_event[0] != 'set_tempo' or shift<0:
                    new_event[1] += shift
            elif (shift < 0) and (new_event[1] >= (from_time+shift)):
                continue
            new_track.append(new_event)
        if len(new_track) > 0:
            new_score.append(new_track)
        i += 1
    _clean_up_warnings()
    return new_score

def segment(score=None, start_time=None, end_time=None, start=0, end=100000000,
 tracks={0,1,2,3,4,5,6,7,8,10,11,12,13,14,15}):
    r'''Returns a "score" which is a segment of the one supplied
as the argument, beginning at "start_time" ticks and ending
at "end_time" ticks (or at the end if "end_time" is not supplied).
If the set "tracks" is specified, only those tracks will
be returned.
'''
    if score == None or len(score) < 2:
        return [1000, [],]
    if start_time == None:  # as of 4.2 start_time is recommended
        start_time = start  # start is legacy usage
    if end_time == None:    # likewise
        end_time = end
    new_score = [score[0],]
    my_type = score_type(score)
    if my_type == '':
        return new_score
    if my_type == 'opus':
        # more difficult (disconnecting note_on's from their note_off's)...
        _warn("segment: opus format is not supported\n")
        _clean_up_warnings()
        return new_score
    i = 1   # ignore first element (ticks); we count in ticks anyway
    tracks = set(tracks)  # defend against tuples and lists
    while i < len(score):
        if len(tracks) and not ((i-1) in tracks):
            i += 1
            continue
        new_track = []
        channel2cc_num  = {}     # most recent controller change before start
        channel2cc_val  = {}
        channel2cc_time = {}
        channel2patch_num  = {}  # keep most recent patch change before start
        channel2patch_time = {}
        set_tempo_num  = 500000 # most recent tempo change before start 6.3
        set_tempo_time = 0
        earliest_note_time = end_time
        for event in score[i]:
            if event[0] == 'control_change':  # 6.5
                cc_time = channel2cc_time.get(event[2]) or 0
                if (event[1] <= start_time) and (event[1] >= cc_time):
                    channel2cc_num[event[2]]  = event[3]
                    channel2cc_val[event[2]]  = event[4]
                    channel2cc_time[event[2]] = event[1]
            elif event[0] == 'patch_change':
                patch_time = channel2patch_time.get(event[2]) or 0
                if (event[1]<=start_time) and (event[1] >= patch_time):  # 2.0
                    channel2patch_num[event[2]]  = event[3]
                    channel2patch_time[event[2]] = event[1]
            elif event[0] == 'set_tempo':
                if (event[1]<=start_time) and (event[1]>=set_tempo_time): #6.4
                    set_tempo_num  = event[2]
                    set_tempo_time = event[1]
            if (event[1] >= start_time) and (event[1] <= end_time):
                new_track.append(event)
                if (event[0] == 'note') and (event[1] < earliest_note_time):
                    earliest_note_time = event[1]
        if len(new_track) > 0:
            new_track.append(['set_tempo', start_time, set_tempo_num])
            for c in channel2patch_num:
                new_track.append(['patch_change',start_time,c,channel2patch_num[c]],)
            for c in channel2cc_num:   # 6.5
                new_track.append(['control_change',start_time,c,channel2cc_num[c],channel2cc_val[c]])
            new_score.append(new_track)
        i += 1
    _clean_up_warnings()
    return new_score

def score_type(opus_or_score=None):
    r'''Returns a string, either 'opus' or 'score' or ''
'''
    if opus_or_score == None or str(type(opus_or_score)).find('list')<0 or len(opus_or_score) < 2:
        return ''
    i = 1   # ignore first element
    while i < len(opus_or_score):
        for event in opus_or_score[i]:
            if event[0] == 'note':
                return 'score'
            elif event[0] == 'note_on':
                return 'opus'
        i += 1
    return ''

def concatenate_scores(scores):
    r'''Concatenates a list of scores into one score.
If the scores differ in their "ticks" parameter,
they will all get converted to millisecond-tick format.
'''
    # the deepcopys are needed if the input_score's are refs to the same obj
    # e.g. if invoked by midisox's repeat()
    input_scores = _consistentise_ticks(scores)  # 3.7
    output_score = copy.deepcopy(input_scores[0])
    for input_score in input_scores[1:]:
        output_stats = score2stats(output_score)
        delta_ticks = output_stats['nticks']
        itrack = 1
        while itrack < len(input_score):
            if itrack >= len(output_score): # new output track if doesn't exist
                output_score.append([])
            for event in input_score[itrack]:
                output_score[itrack].append(copy.deepcopy(event))
                output_score[itrack][-1][1] += delta_ticks
            itrack += 1
    return output_score

def merge_scores(scores):
    r'''Merges a list of scores into one score.  A merged score comprises
all of the tracks from all of the input scores; un-merging is possible
by selecting just some of the tracks.  If the scores differ in their
"ticks" parameter, they will all get converted to millisecond-tick
format.  merge_scores attempts to resolve channel-conflicts,
but there are of course only 15 available channels...
'''
    input_scores = _consistentise_ticks(scores)  # 3.6
    output_score = [1000]
    channels_so_far = set()
    all_channels = {0,1,2,3,4,5,6,7,8,10,11,12,13,14,15}
    global Event2channelindex
    for input_score in input_scores:
        new_channels = set(score2stats(input_score).get('channels_total', []))
        new_channels.discard(9)  # 2.8 cha9 must remain cha9 (in GM)
        for channel in channels_so_far & new_channels:
            # consistently choose lowest avaiable, to ease testing
            free_channels = list(all_channels - (channels_so_far|new_channels))
            if len(free_channels) > 0:
                free_channels.sort()
                free_channel = free_channels[0]
            else:
                free_channel = None
                break
            itrack = 1
            while itrack < len(input_score):
                for input_event in input_score[itrack]:
                    channel_index=Event2channelindex.get(input_event[0],False)
                    if channel_index and input_event[channel_index]==channel:
                        input_event[channel_index] = free_channel
                itrack += 1
            channels_so_far.add(free_channel)

        channels_so_far |= new_channels
        output_score.extend(input_score[1:])
    return output_score

def _ticks(event):
    return event[1]
def mix_opus_tracks(input_tracks):   # 5.5
    r'''Mixes an array of tracks into one track.  A mixed track
cannot be un-mixed.  It is assumed that the tracks share the same
ticks parameter and the same tempo.
Mixing score-tracks is trivial (just insert all events into one array).
Mixing opus-tracks is only slightly harder, but it's common enough
that a dedicated function is useful.
'''
    output_score = [1000, []]
    for input_track in input_tracks:   # 5.8
        input_score = opus2score([1000, input_track])
        for event in input_score[1]:
            output_score[1].append(event)
    output_score[1].sort(key=_ticks) 
    output_opus = score2opus(output_score)
    return output_opus[1]

def mix_scores(scores):
    r'''Mixes a list of scores into one one-track score.
A mixed score cannot be un-mixed.  Hopefully the scores
have no undesirable channel-conflicts between them.
If the scores differ in their "ticks" parameter,
they will all get converted to millisecond-tick format.
'''
    input_scores = _consistentise_ticks(scores)  # 3.6
    output_score = [1000, []]
    for input_score in input_scores:
        for input_track in input_score[1:]:
            output_score[1].extend(input_track)
    return output_score

def score2stats(opus_or_score=None):
    r'''Returns a dict of some basic stats about the score, like
bank_select (list of tuples (msb,lsb)),
channels_by_track (list of lists), channels_total (set),
general_midi_mode (list),
ntracks, nticks, patch_changes_by_track (list of dicts),
num_notes_by_channel (list of numbers),
patch_changes_total (set),
percussion (dict histogram of channel 9 events),
pitches (dict histogram of pitches on channels other than 9),
pitch_range_by_track (list, by track, of two-member-tuples),
pitch_range_sum (sum over tracks of the pitch_ranges),
'''
    bank_select_msb = -1
    bank_select_lsb = -1
    bank_select = []
    channels_by_track = []
    channels_total    = set([])
    general_midi_mode = []
    num_notes_by_channel = dict([])
    patches_used_by_track  = []
    patches_used_total     = set([])
    patch_changes_by_track = []
    patch_changes_total    = set([])
    percussion = dict([]) # histogram of channel 9 "pitches"
    pitches    = dict([]) # histogram of pitch-occurrences channels 0-8,10-15
    pitch_range_sum = 0   # u pitch-ranges of each track
    pitch_range_by_track = []
    is_a_score = True
    if opus_or_score == None:
        return {'bank_select':[], 'channels_by_track':[], 'channels_total':[],
         'general_midi_mode':[], 'ntracks':0, 'nticks':0,
         'num_notes_by_channel':dict([]),
         'patch_changes_by_track':[], 'patch_changes_total':[],
         'percussion':{}, 'pitches':{}, 'pitch_range_by_track':[],
         'ticks_per_quarter':0, 'pitch_range_sum':0}
    ticks_per_quarter = opus_or_score[0]
    i = 1   # ignore first element, which is ticks
    nticks = 0
    while i < len(opus_or_score):
        highest_pitch = 0
        lowest_pitch = 128
        channels_this_track = set([])
        patch_changes_this_track = dict({})
        for event in opus_or_score[i]:
            if event[0] == 'note':
                num_notes_by_channel[event[3]] = num_notes_by_channel.get(event[3],0) + 1
                if event[3] == 9:
                    percussion[event[4]] = percussion.get(event[4],0) + 1
                else:
                    pitches[event[4]]    = pitches.get(event[4],0) + 1
                    if event[4] > highest_pitch:
                        highest_pitch = event[4]
                    if event[4] < lowest_pitch:
                        lowest_pitch = event[4]
                channels_this_track.add(event[3])
                channels_total.add(event[3])
                finish_time = event[1] + event[2]
                if finish_time > nticks:
                    nticks = finish_time
            elif event[0] == 'note_off' or (event[0] == 'note_on' and event[4] == 0):  # 4.8
                finish_time = event[1]
                if finish_time > nticks:
                    nticks = finish_time
            elif event[0] == 'note_on':
                is_a_score = False
                num_notes_by_channel[event[2]] = num_notes_by_channel.get(event[2],0) + 1
                if event[2] == 9:
                    percussion[event[3]] = percussion.get(event[3],0) + 1
                else:
                    pitches[event[3]]    = pitches.get(event[3],0) + 1
                    if event[3] > highest_pitch:
                        highest_pitch = event[3]
                    if event[3] < lowest_pitch:
                        lowest_pitch = event[3]
                channels_this_track.add(event[2])
                channels_total.add(event[2])
            elif event[0] == 'patch_change':
                patch_changes_this_track[event[2]] = event[3]
                patch_changes_total.add(event[3])
            elif event[0] == 'control_change':
                if event[3] == 0:  # bank select MSB
                    bank_select_msb = event[4]
                elif event[3] == 32:  # bank select LSB
                    bank_select_lsb = event[4]
                if bank_select_msb >= 0 and bank_select_lsb >= 0:
                    bank_select.append((bank_select_msb,bank_select_lsb))
                    bank_select_msb = -1
                    bank_select_lsb = -1
            elif event[0] == 'sysex_f0':
                if _sysex2midimode.get(event[2], -1) >= 0:
                    general_midi_mode.append(_sysex2midimode.get(event[2]))
            if is_a_score:
                if event[1] > nticks:
                    nticks = event[1]
            else:
                nticks += event[1]
        if lowest_pitch == 128:
            lowest_pitch = 0
        channels_by_track.append(channels_this_track)
        patch_changes_by_track.append(patch_changes_this_track)
        pitch_range_by_track.append((lowest_pitch,highest_pitch))
        pitch_range_sum += (highest_pitch-lowest_pitch)
        i += 1

    return {'bank_select':bank_select,
            'channels_by_track':channels_by_track,
            'channels_total':channels_total,
            'general_midi_mode':general_midi_mode,
            'ntracks':len(opus_or_score)-1,
            'nticks':nticks,
            'num_notes_by_channel':num_notes_by_channel,
            'patch_changes_by_track':patch_changes_by_track,
            'patch_changes_total':patch_changes_total,
            'percussion':percussion,
            'pitches':pitches,
            'pitch_range_by_track':pitch_range_by_track,
            'pitch_range_sum':pitch_range_sum,
            'ticks_per_quarter':ticks_per_quarter}

#----------------------------- Event stuff --------------------------

_sysex2midimode = {
    "\x7E\x7F\x09\x01\xF7": 1,
    "\x7E\x7F\x09\x02\xF7": 0,
    "\x7E\x7F\x09\x03\xF7": 2,
}

# Some public-access tuples:
MIDI_events = tuple('''note_off note_on key_after_touch
control_change patch_change channel_after_touch
pitch_wheel_change'''.split())

Text_events = tuple('''text_event copyright_text_event
track_name instrument_name lyric marker cue_point text_event_08
text_event_09 text_event_0a text_event_0b text_event_0c
text_event_0d text_event_0e text_event_0f'''.split())

Nontext_meta_events = tuple('''end_track set_tempo
smpte_offset time_signature key_signature sequencer_specific
raw_meta_event sysex_f0 sysex_f7 song_position song_select
tune_request'''.split())
# unsupported: raw_data

# Actually, 'tune_request' is is F-series event, not strictly a meta-event...
Meta_events = Text_events + Nontext_meta_events
All_events  = MIDI_events + Meta_events

# And three dictionaries:
Number2patch = {   # General MIDI patch numbers:
0:'Acoustic Grand',
1:'Bright Acoustic',
2:'Electric Grand',
3:'Honky-Tonk',
4:'Electric Piano 1',
5:'Electric Piano 2',
6:'Harpsichord',
7:'Clav',
8:'Celesta',
9:'Glockenspiel',
10:'Music Box',
11:'Vibraphone',
12:'Marimba',
13:'Xylophone',
14:'Tubular Bells',
15:'Dulcimer',
16:'Drawbar Organ',
17:'Percussive Organ',
18:'Rock Organ',
19:'Church Organ',
20:'Reed Organ',
21:'Accordion',
22:'Harmonica',
23:'Tango Accordion',
24:'Acoustic Guitar(nylon)',
25:'Acoustic Guitar(steel)',
26:'Electric Guitar(jazz)',
27:'Electric Guitar(clean)',
28:'Electric Guitar(muted)',
29:'Overdriven Guitar',
30:'Distortion Guitar',
31:'Guitar Harmonics',
32:'Acoustic Bass',
33:'Electric Bass(finger)',
34:'Electric Bass(pick)',
35:'Fretless Bass',
36:'Slap Bass 1',
37:'Slap Bass 2',
38:'Synth Bass 1',
39:'Synth Bass 2',
40:'Violin',
41:'Viola',
42:'Cello',
43:'Contrabass',
44:'Tremolo Strings',
45:'Pizzicato Strings',
46:'Orchestral Harp',
47:'Timpani',
48:'String Ensemble 1',
49:'String Ensemble 2',
50:'SynthStrings 1',
51:'SynthStrings 2',
52:'Choir Aahs',
53:'Voice Oohs',
54:'Synth Voice',
55:'Orchestra Hit',
56:'Trumpet',
57:'Trombone',
58:'Tuba',
59:'Muted Trumpet',
60:'French Horn',
61:'Brass Section',
62:'SynthBrass 1',
63:'SynthBrass 2',
64:'Soprano Sax',
65:'Alto Sax',
66:'Tenor Sax',
67:'Baritone Sax',
68:'Oboe',
69:'English Horn',
70:'Bassoon',
71:'Clarinet',
72:'Piccolo',
73:'Flute',
74:'Recorder',
75:'Pan Flute',
76:'Blown Bottle',
77:'Skakuhachi',
78:'Whistle',
79:'Ocarina',
80:'Lead 1 (square)',
81:'Lead 2 (sawtooth)',
82:'Lead 3 (calliope)',
83:'Lead 4 (chiff)',
84:'Lead 5 (charang)',
85:'Lead 6 (voice)',
86:'Lead 7 (fifths)',
87:'Lead 8 (bass+lead)',
88:'Pad 1 (new age)',
89:'Pad 2 (warm)',
90:'Pad 3 (polysynth)',
91:'Pad 4 (choir)',
92:'Pad 5 (bowed)',
93:'Pad 6 (metallic)',
94:'Pad 7 (halo)',
95:'Pad 8 (sweep)',
96:'FX 1 (rain)',
97:'FX 2 (soundtrack)',
98:'FX 3 (crystal)',
99:'FX 4 (atmosphere)',
100:'FX 5 (brightness)',
101:'FX 6 (goblins)',
102:'FX 7 (echoes)',
103:'FX 8 (sci-fi)',
104:'Sitar',
105:'Banjo',
106:'Shamisen',
107:'Koto',
108:'Kalimba',
109:'Bagpipe',
110:'Fiddle',
111:'Shanai',
112:'Tinkle Bell',
113:'Agogo',
114:'Steel Drums',
115:'Woodblock',
116:'Taiko Drum',
117:'Melodic Tom',
118:'Synth Drum',
119:'Reverse Cymbal',
120:'Guitar Fret Noise',
121:'Breath Noise',
122:'Seashore',
123:'Bird Tweet',
124:'Telephone Ring',
125:'Helicopter',
126:'Applause',
127:'Gunshot',
}
Notenum2percussion = {   # General MIDI Percussion (on Channel 9):
35:'Acoustic Bass Drum',
36:'Bass Drum 1',
37:'Side Stick',
38:'Acoustic Snare',
39:'Hand Clap',
40:'Electric Snare',
41:'Low Floor Tom',
42:'Closed Hi-Hat',
43:'High Floor Tom',
44:'Pedal Hi-Hat',
45:'Low Tom',
46:'Open Hi-Hat',
47:'Low-Mid Tom',
48:'Hi-Mid Tom',
49:'Crash Cymbal 1',
50:'High Tom',
51:'Ride Cymbal 1',
52:'Chinese Cymbal',
53:'Ride Bell',
54:'Tambourine',
55:'Splash Cymbal',
56:'Cowbell',
57:'Crash Cymbal 2',
58:'Vibraslap',
59:'Ride Cymbal 2',
60:'Hi Bongo',
61:'Low Bongo',
62:'Mute Hi Conga',
63:'Open Hi Conga',
64:'Low Conga',
65:'High Timbale',
66:'Low Timbale',
67:'High Agogo',
68:'Low Agogo',
69:'Cabasa',
70:'Maracas',
71:'Short Whistle',
72:'Long Whistle',
73:'Short Guiro',
74:'Long Guiro',
75:'Claves',
76:'Hi Wood Block',
77:'Low Wood Block',
78:'Mute Cuica',
79:'Open Cuica',
80:'Mute Triangle',
81:'Open Triangle',
}

Event2channelindex = { 'note':3, 'note_off':2, 'note_on':2,
 'key_after_touch':2, 'control_change':2, 'patch_change':2,
 'channel_after_touch':2, 'pitch_wheel_change':2
}

################################################################
# The code below this line is full of frightening things, all to
# do with the actual encoding and decoding of binary MIDI data.

def _twobytes2int(byte_a):
    r'''decode a 16 bit quantity from two bytes,'''
    return (byte_a[1] | (byte_a[0] << 8))

def _int2twobytes(int_16bit):
    r'''encode a 16 bit quantity into two bytes,'''
    return bytes([(int_16bit>>8) & 0xFF, int_16bit & 0xFF])

def _read_14_bit(byte_a):
    r'''decode a 14 bit quantity from two bytes,'''
    return (byte_a[0] | (byte_a[1] << 7))

def _write_14_bit(int_14bit):
    r'''encode a 14 bit quantity into two bytes,'''
    return bytes([int_14bit & 0x7F, (int_14bit>>7) & 0x7F])

def _ber_compressed_int(integer):
    r'''BER compressed integer (not an ASN.1 BER, see perlpacktut for
details).  Its bytes represent an unsigned integer in base 128,
most significant digit first, with as few digits as possible.
Bit eight (the high bit) is set on each byte except the last.
'''
    ber = bytearray(b'')
    seven_bits = 0x7F & integer
    ber.insert(0, seven_bits)  # XXX surely should convert to a char ?
    integer >>= 7
    while integer > 0:
        seven_bits = 0x7F & integer
        ber.insert(0, 0x80|seven_bits)  # XXX surely should convert to a char ?
        integer >>= 7
    return ber

def _unshift_ber_int(ba):
    r'''Given a bytearray, returns a tuple of (the ber-integer at the
start, and the remainder of the bytearray).
'''
    if not len(ba):   # 6.7
        _warn('_unshift_ber_int: no integer found')
        return ((0, b""))
    byte = ba.pop(0)
    integer = 0
    while True:
        integer += (byte & 0x7F)
        if not (byte & 0x80):
            return ((integer, ba))
        if not len(ba):
            _warn('_unshift_ber_int: no end-of-integer found')
            return ((0, ba))
        byte = ba.pop(0)
        integer <<= 7

def _clean_up_warnings():  # 5.4
    # Call this before returning from any publicly callable function
    # whenever there's a possibility that a warning might have been printed
    # by the function, or by any private functions it might have called.
    global _previous_times
    global _previous_warning
    if _previous_times > 1:
        # E:1176, 0: invalid syntax (<string>, line 1176) (syntax-error) ???
        # print('  previous message repeated '+str(_previous_times)+' times', file=sys.stderr)
        # 6.7
        sys.stderr.write('  previous message repeated {0} times\n'.format(_previous_times))
    elif _previous_times > 0:
        sys.stderr.write('  previous message repeated\n')
    _previous_times = 0
    _previous_warning = ''

def _warn(s=''):
    global _previous_times
    global _previous_warning
    if s == _previous_warning:  # 5.4
        _previous_times = _previous_times + 1
    else:
        _clean_up_warnings()
        sys.stderr.write(str(s)+"\n")
        _previous_warning = s

def _some_text_event(which_kind=0x01, text=b'some_text'):
    if str(type(text)).find("'str'") >= 0:   # 6.4 test for back-compatibility
        data = bytes(text, encoding='ISO-8859-1')
    else:
        data = bytes(text)
    return b'\xFF'+bytes((which_kind,))+_ber_compressed_int(len(data))+data

def _consistentise_ticks(scores):  # 3.6
    # used by mix_scores, merge_scores, concatenate_scores
    if len(scores) == 1:
         return copy.deepcopy(scores)
    are_consistent = True
    ticks = scores[0][0]
    iscore = 1
    while iscore < len(scores):
        if scores[iscore][0] != ticks:
            are_consistent = False
            break
        iscore += 1
    if are_consistent:
        return copy.deepcopy(scores)
    new_scores = []
    iscore = 0
    while iscore < len(scores):
        score = scores[iscore]
        new_scores.append(opus2score(to_millisecs(score2opus(score))))
        iscore += 1
    return new_scores


###########################################################################

def _decode(trackdata=b'', exclude=None, include=None,
 event_callback=None, exclusive_event_callback=None, no_eot_magic=False):
    r'''Decodes MIDI track data into an opus-style list of events.
The options:
  'exclude' is a list of event types which will be ignored SHOULD BE A SET
  'include' (and no exclude), makes exclude a list
       of all possible events, /minus/ what include specifies
  'event_callback' is a coderef
  'exclusive_event_callback' is a coderef
'''
    trackdata = bytearray(trackdata)
    if exclude == None:
        exclude = []
    if include == None:
        include = []
    if include and not exclude:
        exclude = All_events
    include = set(include)
    exclude = set(exclude)

    # Pointer = 0;  not used here; we eat through the bytearray instead.
    event_code = -1; # used for running status
    event_count = 0;
    events = []

    while(len(trackdata)):
        # loop while there's anything to analyze ...
        eot = False   # When True, the event registrar aborts this loop
        event_count += 1

        E = []
        # E for events - we'll feed it to the event registrar at the end.

        # Slice off the delta time code, and analyze it
        [time, remainder] = _unshift_ber_int(trackdata)

        # Now let's see what we can make of the command
        first_byte = trackdata.pop(0) & 0xFF

        if (first_byte < 0xF0):  # It's a MIDI event
            if (first_byte & 0x80):
                event_code = first_byte
            else:
                # It wants running status; use last event_code value
                trackdata.insert(0, first_byte)
                if (event_code == -1):
                    _warn("Running status not set; Aborting track.")
                    return []

            command = event_code & 0xF0
            channel = event_code & 0x0F

            if (command == 0xF6):  #  0-byte argument
                pass
            elif (command == 0xC0 or command == 0xD0):  #  1-byte argument
                parameter = trackdata.pop(0)  # could be B
            else: # 2-byte argument could be BB or 14-bit
                parameter = (trackdata.pop(0), trackdata.pop(0))

            #################################################################
            # MIDI events

            if (command      == 0x80):
                if 'note_off' in exclude:
                    continue
                E = ['note_off', time, channel, parameter[0], parameter[1]]
            elif (command == 0x90):
                if 'note_on' in exclude:
                    continue
                E = ['note_on', time, channel, parameter[0], parameter[1]]
            elif (command == 0xA0):
                if 'key_after_touch' in exclude:
                    continue
                E = ['key_after_touch',time,channel,parameter[0],parameter[1]]
            elif (command == 0xB0):
                if 'control_change' in exclude:
                    continue
                E = ['control_change',time,channel,parameter[0],parameter[1]]
            elif (command == 0xC0):
                if 'patch_change' in exclude:
                    continue
                E = ['patch_change', time, channel, parameter]
            elif (command == 0xD0):
                if 'channel_after_touch' in exclude:
                    continue
                E = ['channel_after_touch', time, channel, parameter]
            elif (command == 0xE0):
                if 'pitch_wheel_change' in exclude:
                    continue
                E = ['pitch_wheel_change', time, channel,
                 _read_14_bit(parameter)-0x2000]
            else:
                _warn("Shouldn't get here; command="+hex(command))

        elif (first_byte == 0xFF):  # It's a Meta-Event! ##################
            #[command, length, remainder] =
            #    unpack("xCwa*", substr(trackdata, $Pointer, 6));
            #Pointer += 6 - len(remainder);
            #    # Move past JUST the length-encoded.
            command = trackdata.pop(0) & 0xFF
            [length, trackdata] = _unshift_ber_int(trackdata)
            if (command      == 0x00):
                 if (length == 2):
                     E = ['set_sequence_number',time,_twobytes2int(trackdata)]
                 else:
                     _warn('set_sequence_number: length must be 2, not '+str(length))
                     E = ['set_sequence_number', time, 0]

            elif command >= 0x01 and command <= 0x0f:   # Text events
                # 6.2 take it in bytes; let the user get the right encoding.
                # text_str = trackdata[0:length].decode('ascii','ignore')
                # text_str = trackdata[0:length].decode('ISO-8859-1')
                # 6.4 take it in bytes; let the user get the right encoding.
                text_data = bytes(trackdata[0:length])   # 6.4
                # Defined text events
                if (command == 0x01):
                     E = ['text_event', time, text_data]
                elif (command == 0x02):
                     E = ['copyright_text_event', time, text_data]
                elif (command == 0x03):
                     E = ['track_name', time, text_data]
                elif (command == 0x04):
                     E = ['instrument_name', time, text_data]
                elif (command == 0x05):
                     E = ['lyric', time, text_data]
                elif (command == 0x06):
                     E = ['marker', time, text_data]
                elif (command == 0x07):
                     E = ['cue_point', time, text_data]
                # Reserved but apparently unassigned text events
                elif (command == 0x08):
                     E = ['text_event_08', time, text_data]
                elif (command == 0x09):
                     E = ['text_event_09', time, text_data]
                elif (command == 0x0a):
                     E = ['text_event_0a', time, text_data]
                elif (command == 0x0b):
                     E = ['text_event_0b', time, text_data]
                elif (command == 0x0c):
                     E = ['text_event_0c', time, text_data]
                elif (command == 0x0d):
                     E = ['text_event_0d', time, text_data]
                elif (command == 0x0e):
                     E = ['text_event_0e', time, text_data]
                elif (command == 0x0f):
                     E = ['text_event_0f', time, text_data]

            # Now the sticky events -------------------------------------
            elif (command == 0x2F):
                 E = ['end_track', time]
                     # The code for handling this, oddly, comes LATER,
                     # in the event registrar.
            elif (command == 0x51): # DTime, Microseconds/Crochet
                 if length != 3:
                     _warn('set_tempo event, but length='+str(length))
                 E = ['set_tempo', time,
                      struct.unpack(">I", b'\x00'+trackdata[0:3])[0]]
            elif (command == 0x54):
                 if length != 5:   # DTime, HR, MN, SE, FR, FF
                     _warn('smpte_offset event, but length='+str(length))
                 E = ['smpte_offset',time] + list(struct.unpack(">BBBBB",trackdata[0:5]))
            elif (command == 0x58):
                 if length != 4:   # DTime, NN, DD, CC, BB
                     _warn('time_signature event, but length='+str(length))
                 E = ['time_signature', time]+list(trackdata[0:4])
            elif (command == 0x59):
                 if length != 2:   # DTime, SF(signed), MI
                     _warn('key_signature event, but length='+str(length))
                 E = ['key_signature',time] + list(struct.unpack(">bB",trackdata[0:2]))
            elif (command == 0x7F):   # 6.4
                 E = ['sequencer_specific',time, bytes(trackdata[0:length])]
            else:
                 E = ['raw_meta_event', time, command,
                   bytes(trackdata[0:length])]   # 6.0
                 #"[uninterpretable meta-event command of length length]"
                 # DTime, Command, Binary Data
                 # It's uninterpretable; record it as raw_data.

            # Pointer += length; #  Now move Pointer
            trackdata = trackdata[length:]

        ######################################################################
        elif (first_byte == 0xF0 or first_byte == 0xF7):
            # Note that sysexes in MIDI /files/ are different than sysexes
            # in MIDI transmissions!! The vast majority of system exclusive
            # messages will just use the F0 format. For instance, the
            # transmitted message F0 43 12 00 07 F7 would be stored in a
            # MIDI file as F0 05 43 12 00 07 F7. As mentioned above, it is
            # required to include the F7 at the end so that the reader of the
            # MIDI file knows that it has read the entire message. (But the F7
            # is omitted if this is a non-final block in a multiblock sysex;
            # but the F7 (if there) is counted in the message's declared
            # length, so we don't have to think about it anyway.)
            #command = trackdata.pop(0)
            [length, trackdata] = _unshift_ber_int(trackdata)
            if first_byte == 0xF0:
                # 20091008 added ISO-8859-1 to get an 8-bit str
                # 6.4 return bytes instead
                E = ['sysex_f0', time, bytes(trackdata[0:length])]
            else:
                E = ['sysex_f7', time, bytes(trackdata[0:length])]
            trackdata = trackdata[length:]

        ######################################################################
        # Now, the MIDI file spec says:
        #  <track data> = <MTrk event>+
        #  <MTrk event> = <delta-time> <event>
        #  <event> = <MIDI event> | <sysex event> | <meta-event>
        # I know that, on the wire, <MIDI event> can include note_on,
        # note_off, and all the other 8x to Ex events, AND Fx events
        # other than F0, F7, and FF -- namely, <song position msg>,
        # <song select msg>, and <tune request>.
        #
        # Whether these can occur in MIDI files is not clear specified
        # from the MIDI file spec.  So, I'm going to assume that
        # they CAN, in practice, occur.  I don't know whether it's
        # proper for you to actually emit these into a MIDI file.
        
        elif (first_byte == 0xF2):   # DTime, Beats
            #  <song position msg> ::=     F2 <data pair>
            E = ['song_position', time, _read_14_bit(trackdata[:2])]
            trackdata = trackdata[2:]

        elif (first_byte == 0xF3):   # <song select msg> ::= F3 <data singlet>
            # E = ['song_select', time, struct.unpack('>B',trackdata.pop(0))[0]]
            E = ['song_select', time, trackdata[0]]
            trackdata = trackdata[1:]
            # DTime, Thing (what?! song number?  whatever ...)

        elif (first_byte == 0xF6):   # DTime
            E = ['tune_request', time]
            # What would a tune request be doing in a MIDI /file/?

        #########################################################
        # ADD MORE META-EVENTS HERE.  TODO:
        # f1 -- MTC Quarter Frame Message. One data byte follows
        #     the Status; it's the time code value, from 0 to 127.
        # f8 -- MIDI clock.    no data.
        # fa -- MIDI start.    no data.
        # fb -- MIDI continue. no data.
        # fc -- MIDI stop.     no data.
        # fe -- Active sense.  no data.
        # f4 f5 f9 fd -- unallocated

            r'''
        elif (first_byte > 0xF0) { # Some unknown kinda F-series event ####
            # Here we only produce a one-byte piece of raw data.
            # But the encoder for 'raw_data' accepts any length of it.
            E = [ 'raw_data',
                         time, substr(trackdata,Pointer,1) ]
            # DTime and the Data (in this case, the one Event-byte)
            ++Pointer;  # itself

'''
        elif first_byte > 0xF0:  # Some unknown F-series event
            # Here we only produce a one-byte piece of raw data.
            # E = ['raw_data', time, bytest(trackdata[0])]   # 6.4
            E = ['raw_data', time, trackdata[0]]   # 6.4 6.7
            trackdata = trackdata[1:]
        else:  # Fallthru.
            _warn("Aborting track.  Command-byte first_byte="+hex(first_byte))
            break
        # End of the big if-group


        ######################################################################
        #  THE EVENT REGISTRAR...
        if E and  (E[0] == 'end_track'):
            # This is the code for exceptional handling of the EOT event.
            eot = True
            if not no_eot_magic:
                if E[1] > 0:  # a null text-event to carry the delta-time
                    E = ['text_event', E[1], '']
                else:
                    E = []   # EOT with a delta-time of 0; ignore it.
        
        if E and not (E[0] in exclude):
            #if ( $exclusive_event_callback ):
            #    &{ $exclusive_event_callback }( @E );
            #else:
            #    &{ $event_callback }( @E ) if $event_callback;
                events.append(E)
        if eot:
            break

    # End of the big "Event" while-block

    return events


###########################################################################
def _encode(events_lol, unknown_callback=None, never_add_eot=False,
  no_eot_magic=False, no_running_status=False):
    # encode an event structure, presumably for writing to a file
    # Calling format:
    #   $data_r = MIDI::Event::encode( \@event_lol, { options } );
    # Takes a REFERENCE to an event structure (a LoL)
    # Returns an (unblessed) REFERENCE to track data.

    # If you want to use this to encode a /single/ event,
    # you still have to do it as a reference to an event structure (a LoL)
    # that just happens to have just one event.  I.e.,
    #   encode( [ $event ] ) or encode( [ [ 'note_on', 100, 5, 42, 64] ] )
    # If you're doing this, consider the never_add_eot track option, as in
    #   print MIDI ${ encode( [ $event], { 'never_add_eot' => 1} ) };

    data = [] # what I'll store the chunks of byte-data in

    # This is so my end_track magic won't corrupt the original
    events = copy.deepcopy(events_lol)

    if not never_add_eot:
        # One way or another, tack on an 'end_track'
        if events:
            last = events[-1]
            if not (last[0] == 'end_track'):  # no end_track already
                if (last[0] == 'text_event' and len(last[2]) == 0):
                    # 0-length text event at track-end.
                    if no_eot_magic:
                        # Exceptional case: don't mess with track-final
                        # 0-length text_events; just peg on an end_track
                        events.append(['end_track', 0])
                    else:
                        # NORMAL CASE: replace with an end_track, leaving DTime
                        last[0] = 'end_track'
                else:
                    # last event was neither 0-length text_event nor end_track
                    events.append(['end_track', 0])
        else:  # an eventless track!
            events = [['end_track', 0],]

    # maybe_running_status = not no_running_status # unused? 4.7
    last_status = -1

    for event_r in (events):
        E = copy.deepcopy(event_r)
        # otherwise the shifting'd corrupt the original
        if not E:
            continue

        event = E.pop(0)
        if not len(event):
            continue

        dtime = int(E.pop(0))
        # print('event='+str(event)+' dtime='+str(dtime))

        event_data = ''

        if (   # MIDI events -- eligible for running status
             event    == 'note_on'
             or event == 'note_off'
             or event == 'control_change'
             or event == 'key_after_touch'
             or event == 'patch_change'
             or event == 'channel_after_touch'
             or event == 'pitch_wheel_change'  ):

            # This block is where we spend most of the time.  Gotta be tight.
            if (event == 'note_off'):
                status = 0x80 | (int(E[0]) & 0x0F)
                parameters = struct.pack('>BB', int(E[1])&0x7F, int(E[2])&0x7F)
            elif (event == 'note_on'):
                status = 0x90 | (int(E[0]) & 0x0F)
                parameters = struct.pack('>BB', int(E[1])&0x7F, int(E[2])&0x7F)
            elif (event == 'key_after_touch'):
                status = 0xA0 | (int(E[0]) & 0x0F)
                parameters = struct.pack('>BB', int(E[1])&0x7F, int(E[2])&0x7F)
            elif (event == 'control_change'):
                status = 0xB0 | (int(E[0]) & 0x0F)
                parameters = struct.pack('>BB', int(E[1])&0xFF, int(E[2])&0xFF)
            elif (event == 'patch_change'):
                status = 0xC0 | (int(E[0]) & 0x0F)
                parameters = struct.pack('>B', int(E[1]) & 0xFF)
            elif (event == 'channel_after_touch'):
                status = 0xD0 | (int(E[0]) & 0x0F)
                parameters = struct.pack('>B', int(E[1]) & 0xFF)
            elif (event == 'pitch_wheel_change'):
                status = 0xE0 | (int(E[0]) & 0x0F)
                parameters =  _write_14_bit(int(E[1]) + 0x2000)
            else:
                _warn("BADASS FREAKOUT ERROR 31415!")

            # And now the encoding
            # w = BER compressed integer (not ASN.1 BER, see perlpacktut for
            # details).  Its bytes represent an unsigned integer in base 128,
            # most significant digit first, with as few digits as possible.
            # Bit eight (the high bit) is set on each byte except the last.

            data.append(_ber_compressed_int(dtime))
            if (status != last_status) or no_running_status:
                data.append(struct.pack('>B', status))
            data.append(parameters)
 
            last_status = status
            continue
        else:
            # Not a MIDI event.
            # All the code in this block could be more efficient,
            # but this is not where the code needs to be tight.
            # print "zaz $event\n";
            last_status = -1

            if event == 'raw_meta_event':
                event_data = _some_text_event(int(E[0]), E[1])
            elif (event == 'set_sequence_number'):  # 3.9
                event_data = b'\xFF\x00\x02'+_int2twobytes(E[0])

            # Text meta-events...
            # a case for a dict, I think (pjb) ...
            elif (event == 'text_event'):
                event_data = _some_text_event(0x01, E[0])
            elif (event == 'copyright_text_event'):
                event_data = _some_text_event(0x02, E[0])
            elif (event == 'track_name'):
                event_data = _some_text_event(0x03, E[0])
            elif (event == 'instrument_name'):
                event_data = _some_text_event(0x04, E[0])
            elif (event == 'lyric'):
                event_data = _some_text_event(0x05, E[0])
            elif (event == 'marker'):
                event_data = _some_text_event(0x06, E[0])
            elif (event == 'cue_point'):
                event_data = _some_text_event(0x07, E[0])
            elif (event == 'text_event_08'):
                event_data = _some_text_event(0x08, E[0])
            elif (event == 'text_event_09'):
                event_data = _some_text_event(0x09, E[0])
            elif (event == 'text_event_0a'):
                event_data = _some_text_event(0x0A, E[0])
            elif (event == 'text_event_0b'):
                event_data = _some_text_event(0x0B, E[0])
            elif (event == 'text_event_0c'):
                event_data = _some_text_event(0x0C, E[0])
            elif (event == 'text_event_0d'):
                event_data = _some_text_event(0x0D, E[0])
            elif (event == 'text_event_0e'):
                event_data = _some_text_event(0x0E, E[0])
            elif (event == 'text_event_0f'):
                event_data = _some_text_event(0x0F, E[0])
            # End of text meta-events

            elif (event == 'end_track'):
                event_data = b"\xFF\x2F\x00"

            elif (event == 'set_tempo'):
                #event_data = struct.pack(">BBwa*", 0xFF, 0x51, 3,
                #              substr( struct.pack('>I', E[0]), 1, 3))
                event_data = b'\xFF\x51\x03'+struct.pack('>I',E[0])[1:]
            elif (event == 'smpte_offset'):
                # event_data = struct.pack(">BBwBBBBB", 0xFF, 0x54, 5, E[0:5] )
                event_data = struct.pack(">BBBbBBBB", 0xFF,0x54,0x05,E[0],E[1],E[2],E[3],E[4])
            elif (event == 'time_signature'):
                # event_data = struct.pack(">BBwBBBB",  0xFF, 0x58, 4, E[0:4] )
                event_data = struct.pack(">BBBbBBB", 0xFF, 0x58, 0x04, E[0],E[1],E[2],E[3])
            elif (event == 'key_signature'):
                event_data = struct.pack(">BBBbB", 0xFF, 0x59, 0x02, E[0],E[1])
            elif (event == 'sequencer_specific'):
                # event_data = struct.pack(">BBwa*", 0xFF,0x7F, len(E[0]), E[0])
                event_data = _some_text_event(0x7F, E[0])
            # End of Meta-events

            # Other Things...
            elif (event == 'sysex_f0'):
                 #event_data = struct.pack(">Bwa*", 0xF0, len(E[0]), E[0])
                 #B=bitstring w=BER-compressed-integer a=null-padded-ascii-str
                 event_data = bytearray(b'\xF0')+_ber_compressed_int(len(E[0]))+bytearray(E[0])
            elif (event == 'sysex_f7'):
                 #event_data = struct.pack(">Bwa*", 0xF7, len(E[0]), E[0])
                 event_data = bytearray(b'\xF7')+_ber_compressed_int(len(E[0]))+bytearray(E[0])

            elif (event == 'song_position'):
                 event_data = b"\xF2" + _write_14_bit( E[0] )
            elif (event == 'song_select'):
                 event_data = struct.pack('>BB', 0xF3, E[0] )
            elif (event == 'tune_request'):
                 event_data = b"\xF6"
            elif (event == 'raw_data'):
                _warn("_encode: raw_data event not supported")
                # event_data = E[0]
                continue
            # End of Other Stuff

            else:
                # The Big Fallthru
                if unknown_callback:
                    # push(@data, &{ $unknown_callback }( @$event_r ))
                    pass
                else:
                    _warn("Unknown event: "+str(event))
                    # To surpress complaint here, just set
                    #  'unknown_callback' => sub { return () }
                continue

            #print "Event $event encoded part 2\n"
            if str(type(event_data)).find("'str'") >= 0:
                event_data = bytearray(event_data.encode('Latin1', 'ignore'))
            if len(event_data): # how could $event_data be empty
                # data.append(struct.pack('>wa*', dtime, event_data))
                # print(' event_data='+str(event_data))
                data.append(_ber_compressed_int(dtime)+event_data)

    return b''.join(data)

#===============================================================================

"""
================================================================================

    pyFluidSynth

    Python bindings for FluidSynth

    Copyright 2008, Nathan Whitehead <nwhitehe@gmail.com>


    Released under the LGPL

    This module contains python bindings for FluidSynth.  FluidSynth is a
    software synthesizer for generating music.  It works like a MIDI
    synthesizer.  You load patches, set parameters, then send NOTEON and
    NOTEOFF events to play notes.  Instruments are defined in SoundFonts,
    generally files with the extension SF2.  FluidSynth can either be used
    to play audio itself, or you can call a function that returns chunks
    of audio data and output the data to the soundcard yourself.
    FluidSynth works on all major platforms, so pyFluidSynth should also.

================================================================================
"""

from ctypes import *
from ctypes.util import find_library
import os

# A short circuited or expression to find the FluidSynth library
# (mostly needed for Windows distributions of libfluidsynth supplied with QSynth)

# DLL search method changed in Python 3.8
# https://docs.python.org/3/library/os.html#os.add_dll_directory
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(os.getcwd())

lib = find_library('fluidsynth') or \
    find_library('libfluidsynth') or \
    find_library('libfluidsynth-3') or \
    find_library('libfluidsynth-2') or \
    find_library('libfluidsynth-1')

if lib is None:
    raise ImportError("Couldn't find the FluidSynth library.")

# Dynamically link the FluidSynth library
# Architecture (32-/64-bit) must match your Python version
_fl = CDLL(lib)

# Helper function for declaring function prototypes
def cfunc(name, result, *args):
    """Build and apply a ctypes prototype complete with parameter flags"""
    if hasattr(_fl, name):
        atypes = []
        aflags = []
        for arg in args:
            atypes.append(arg[1])
            aflags.append((arg[2], arg[0]) + arg[3:])
        return CFUNCTYPE(result, *atypes)((name, _fl), tuple(aflags))
    else: # Handle Fluidsynth 1.x, 2.x, etc. API differences
        return None

# Bump this up when changing the interface for users
api_version = '1.3.1'

# Function prototypes for C versions of functions

FLUID_OK = 0
FLUID_FAILED = -1

fluid_version = cfunc('fluid_version', c_void_p,
                        ('major', POINTER(c_int), 1),
                        ('minor', POINTER(c_int), 1),
                        ('micro', POINTER(c_int), 1))

majver = c_int()
fluid_version(majver, c_int(), c_int())
if majver.value > 1:
    FLUIDSETTING_EXISTS = FLUID_OK
else:
    FLUIDSETTING_EXISTS = 1

# fluid settings
new_fluid_settings = cfunc('new_fluid_settings', c_void_p)

fluid_settings_setstr = cfunc('fluid_settings_setstr', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('str', c_char_p, 1))

fluid_settings_setnum = cfunc('fluid_settings_setnum', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', c_double, 1))

fluid_settings_setint = cfunc('fluid_settings_setint', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', c_int, 1))

fluid_settings_copystr = cfunc('fluid_settings_copystr', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('str', c_char_p, 1),
                              ('len', c_int, 1))

fluid_settings_getnum = cfunc('fluid_settings_getnum', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', POINTER(c_double), 1))

fluid_settings_getint = cfunc('fluid_settings_getint', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', POINTER(c_int), 1))

delete_fluid_settings = cfunc('delete_fluid_settings', None,
                              ('settings', c_void_p, 1))

fluid_synth_activate_key_tuning = cfunc('fluid_synth_activate_key_tuning', c_int,
                                        ('synth', c_void_p, 1),
                                        ('bank', c_int, 1),
                                        ('prog', c_int, 1),
                                        ('name', c_char_p, 1),
                                        ('pitch', POINTER(c_double), 1),
                                        ('apply', c_int, 1))

fluid_synth_activate_tuning = cfunc('fluid_synth_activate_tuning', c_int,
                                    ('synth', c_void_p, 1),
                                    ('chan', c_int, 1),
                                    ('bank', c_int, 1),
                                    ('prog', c_int, 1),
                                    ('apply', c_int, 1))

fluid_synth_deactivate_tuning = cfunc('fluid_synth_deactivate_tuning', c_int,
                                      ('synth', c_void_p, 1),
                                      ('chan', c_int, 1),
                                      ('apply', c_int, 1))

fluid_synth_tuning_dump = cfunc('fluid_synth_tuning_dump', c_int,
                                ('synth', c_void_p, 1),
                                ('bank', c_int, 1),
                                ('prog', c_int, 1),
                                ('name', c_char_p, 1),
                                ('length', c_int, 1),
                                ('pitch', POINTER(c_double), 1))

# fluid synth
new_fluid_synth = cfunc('new_fluid_synth', c_void_p,
                        ('settings', c_void_p, 1))

delete_fluid_synth = cfunc('delete_fluid_synth', None,
                           ('synth', c_void_p, 1))

fluid_synth_sfload = cfunc('fluid_synth_sfload', c_int,
                           ('synth', c_void_p, 1),
                           ('filename', c_char_p, 1),
                           ('update_midi_presets', c_int, 1))

fluid_synth_sfunload = cfunc('fluid_synth_sfunload', c_int,
                           ('synth', c_void_p, 1),
                           ('sfid', c_int, 1),
                           ('update_midi_presets', c_int, 1))

fluid_synth_program_select = cfunc('fluid_synth_program_select', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1),
                                   ('sfid', c_int, 1),
                                   ('bank', c_int, 1),
                                   ('preset', c_int, 1))

fluid_synth_noteon = cfunc('fluid_synth_noteon', c_int,
                           ('synth', c_void_p, 1),
                           ('chan', c_int, 1),
                           ('key', c_int, 1),
                           ('vel', c_int, 1))

fluid_synth_noteoff = cfunc('fluid_synth_noteoff', c_int,
                            ('synth', c_void_p, 1),
                            ('chan', c_int, 1),
                            ('key', c_int, 1))

fluid_synth_pitch_bend = cfunc('fluid_synth_pitch_bend', c_int,
                               ('synth', c_void_p, 1),
                               ('chan', c_int, 1),
                               ('val', c_int, 1))

fluid_synth_cc = cfunc('fluid_synth_cc', c_int,
                       ('synth', c_void_p, 1),
                       ('chan', c_int, 1),
                       ('ctrl', c_int, 1),
                       ('val', c_int, 1))

fluid_synth_get_cc = cfunc('fluid_synth_get_cc', c_int,
                       ('synth', c_void_p, 1),
                       ('chan', c_int, 1),
                       ('num', c_int, 1),
                       ('pval', POINTER(c_int), 1))

fluid_synth_program_change = cfunc('fluid_synth_program_change', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1),
                                   ('prg', c_int, 1))

fluid_synth_unset_program = cfunc('fluid_synth_unset_program', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1))

fluid_synth_get_program = cfunc('fluid_synth_get_program', c_int,
                                ('synth', c_void_p, 1),
                                ('chan', c_int, 1),
                                ('sfont_id', POINTER(c_int), 1),
                                ('bank_num', POINTER(c_int), 1),
                                ('preset_num', POINTER(c_int), 1))

fluid_synth_bank_select = cfunc('fluid_synth_bank_select', c_int,
                                ('synth', c_void_p, 1),
                                ('chan', c_int, 1),
                                ('bank', c_int, 1))

fluid_synth_sfont_select = cfunc('fluid_synth_sfont_select', c_int,
                                 ('synth', c_void_p, 1),
                                 ('chan', c_int, 1),
                                 ('sfid', c_int, 1))

fluid_synth_program_reset = cfunc('fluid_synth_program_reset', c_int,
                                  ('synth', c_void_p, 1))

fluid_synth_system_reset = cfunc('fluid_synth_system_reset', c_int,
                                  ('synth', c_void_p, 1))

fluid_synth_write_s16 = cfunc('fluid_synth_write_s16', c_void_p,
                              ('synth', c_void_p, 1),
                              ('len', c_int, 1),
                              ('lbuf', c_void_p, 1),
                              ('loff', c_int, 1),
                              ('lincr', c_int, 1),
                              ('rbuf', c_void_p, 1),
                              ('roff', c_int, 1),
                              ('rincr', c_int, 1))

fluid_synth_all_notes_off = cfunc('fluid_synth_all_notes_off', c_int,
                                  ('synth', c_void_p, 1),
                                  ('chan', c_int, 1))

fluid_synth_all_sounds_off = cfunc('fluid_synth_all_sounds_off', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1))


class fluid_synth_channel_info_t(Structure):
    _fields_ = [
        ('assigned', c_int),
        ('sfont_id', c_int),
        ('bank', c_int),
        ('program', c_int),
        ('name', c_char*32),
        ('reserved', c_char*32)]

fluid_synth_get_channel_info = cfunc('fluid_synth_get_channel_info', c_int,
                                  ('synth', c_void_p, 1),
                                  ('chan', c_int, 1),
                                  ('info', POINTER(fluid_synth_channel_info_t), 1))

fluid_synth_set_reverb_full = cfunc('fluid_synth_set_reverb_full', c_int,
                                    ('synth', c_void_p, 1),
                                    ('set', c_int, 1),
                                    ('roomsize', c_double, 1),
                                    ('damping', c_double, 1),
                                    ('width', c_double, 1),
                                    ('level', c_double, 1))

fluid_synth_set_chorus_full = cfunc('fluid_synth_set_chorus_full', c_int,
                                    ('synth', c_void_p, 1),
                                    ('set', c_int, 1),
                                    ('nr', c_int, 1),
                                    ('level', c_double, 1),
                                    ('speed', c_double, 1),
                                    ('depth_ms', c_double, 1),
                                    ('type', c_int, 1))

fluid_synth_set_reverb = cfunc('fluid_synth_set_reverb', c_int,
                                    ('synth', c_void_p, 1),
                                    ('roomsize', c_double, 1),
                                    ('damping', c_double, 1),
                                    ('width', c_double, 1),
                                    ('level', c_double, 1))

fluid_synth_set_chorus = cfunc('fluid_synth_set_chorus', c_int,
                                    ('synth', c_void_p, 1),
                                    ('nr', c_int, 1),
                                    ('level', c_double, 1),
                                    ('speed', c_double, 1),
                                    ('depth_ms', c_double, 1),
                                    ('type', c_int, 1))

fluid_synth_set_reverb_roomsize = cfunc('fluid_synth_set_reverb_roomsize', c_int,
                                    ('synth', c_void_p, 1),
                                    ('roomsize', c_double, 1))

fluid_synth_set_reverb_damp = cfunc('fluid_synth_set_reverb_damp', c_int,
                                    ('synth', c_void_p, 1),
                                    ('damping', c_double, 1))

fluid_synth_set_reverb_level = cfunc('fluid_synth_set_reverb_level', c_int,
                                    ('synth', c_void_p, 1),
                                    ('level', c_double, 1))

fluid_synth_set_reverb_width = cfunc('fluid_synth_set_reverb_width', c_int,
                                    ('synth', c_void_p, 1),
                                    ('width', c_double, 1))

fluid_synth_set_chorus_nr = cfunc('fluid_synth_set_chorus_nr', c_int,
                                    ('synth', c_void_p, 1),
                                    ('nr', c_int, 1))

fluid_synth_set_chorus_level = cfunc('fluid_synth_set_chorus_level', c_int,
                                    ('synth', c_void_p, 1),
                                    ('level', c_double, 1))

fluid_synth_set_chorus_type = cfunc('fluid_synth_set_chorus_type', c_int,
                                    ('synth', c_void_p, 1),
                                    ('type', c_int, 1))
fluid_synth_get_reverb_roomsize = cfunc('fluid_synth_get_reverb_roomsize', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_reverb_damp = cfunc('fluid_synth_get_reverb_damp', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_reverb_level = cfunc('fluid_synth_get_reverb_level', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_reverb_width = cfunc('fluid_synth_get_reverb_width', c_double,
                                    ('synth', c_void_p, 1))


fluid_synth_get_chorus_nr = cfunc('fluid_synth_get_chorus_nr', c_int,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_level = cfunc('fluid_synth_get_chorus_level', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_speed_Hz = cfunc('fluid_synth_get_chorus_speed_Hz', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_depth_ms = cfunc('fluid_synth_get_chorus_depth_ms', c_double,
                                    ('synth', c_void_p, 1))

fluid_synth_get_chorus_type = cfunc('fluid_synth_get_chorus_type', c_int,
                                    ('synth', c_void_p, 1))

fluid_synth_set_midi_router = cfunc('fluid_synth_set_midi_router', None,
                               ('synth', c_void_p, 1),
                               ('router', c_void_p, 1))

fluid_synth_handle_midi_event = cfunc('fluid_synth_handle_midi_event', c_int,
                               ('data', c_void_p, 1),
                               ('event', c_void_p, 1))

# fluid sequencer
new_fluid_sequencer2 = cfunc('new_fluid_sequencer2', c_void_p,
                             ('use_system_timer', c_int, 1))

fluid_sequencer_process = cfunc('fluid_sequencer_process', None,
                               ('seq', c_void_p, 1),
                               ('msec', c_uint, 1))

fluid_sequencer_register_fluidsynth = cfunc('fluid_sequencer_register_fluidsynth', c_short,
                               ('seq', c_void_p, 1),
                               ('synth', c_void_p, 1))

fluid_sequencer_register_client = cfunc('fluid_sequencer_register_client', c_short,
                              ('seq', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('callback', CFUNCTYPE(None, c_uint, c_void_p, c_void_p, c_void_p), 1),
                              ('data', c_void_p, 1))

fluid_sequencer_get_tick = cfunc('fluid_sequencer_get_tick', c_uint,
                                ('seq', c_void_p, 1))

fluid_sequencer_set_time_scale = cfunc('fluid_sequencer_set_time_scale', None,
                                      ('seq', c_void_p, 1),
                                      ('scale', c_double, 1))

fluid_sequencer_get_time_scale = cfunc('fluid_sequencer_get_time_scale', c_double,
                                      ('seq', c_void_p, 1))

fluid_sequencer_send_at = cfunc('fluid_sequencer_send_at', c_int,
                               ('seq', c_void_p, 1),
                               ('evt', c_void_p, 1),
                               ('time', c_uint, 1),
                               ('absolute', c_int, 1))


delete_fluid_sequencer = cfunc('delete_fluid_sequencer', None,
                              ('seq', c_void_p, 1))

# fluid event
new_fluid_event = cfunc('new_fluid_event', c_void_p)

fluid_event_set_source = cfunc('fluid_event_set_source', None,
                              ('evt', c_void_p, 1),
                              ('src', c_void_p, 1))

fluid_event_set_dest = cfunc('fluid_event_set_dest', None,
                            ('evt', c_void_p, 1),
                            ('dest', c_void_p, 1))

fluid_event_timer = cfunc('fluid_event_timer', None,
                         ('evt', c_void_p, 1),
                         ('data', c_void_p, 1))

fluid_event_note = cfunc('fluid_event_note', None,
                         ('evt', c_void_p, 1),
                         ('channel', c_int, 1),
                         ('key', c_short, 1),
                         ('vel', c_short, 1),
                         ('duration', c_uint, 1))

fluid_event_noteon = cfunc('fluid_event_noteon', None,
                         ('evt', c_void_p, 1),
                         ('channel', c_int, 1),
                         ('key', c_short, 1),
                         ('vel', c_short, 1))

fluid_event_noteoff = cfunc('fluid_event_noteoff', None,
                         ('evt', c_void_p, 1),
                         ('channel', c_int, 1),
                         ('key', c_short, 1))

delete_fluid_event = cfunc('delete_fluid_event', None,
                          ('evt', c_void_p, 1))

fluid_midi_event_get_channel = cfunc('fluid_midi_event_get_channel', c_int,
                                  ('evt', c_void_p, 1))

fluid_midi_event_get_control = cfunc('fluid_midi_event_get_control', c_int,
                                  ('evt', c_void_p, 1))

fluid_midi_event_get_program = cfunc('fluid_midi_event_get_program', c_int,
                                  ('evt', c_void_p, 1))

fluid_midi_event_get_key = cfunc('fluid_midi_event_get_key', c_int,
                                  ('evt', c_void_p, 1))

fluid_midi_event_get_type = cfunc('fluid_midi_event_get_type', c_int,
                                  ('evt', c_void_p, 1))

fluid_midi_event_get_value = cfunc('fluid_midi_event_get_value', c_int,
                                  ('evt', c_void_p, 1))

fluid_midi_event_get_velocity = cfunc('fluid_midi_event_get_velocity', c_int,
                                  ('evt', c_void_p, 1))

# fluid_player_status returned by fluid_player_get_status()
FLUID_PLAYER_READY = 0
FLUID_PLAYER_PLAYING = 1
FLUID_PLAYER_STOPPING = 2
FLUID_PLAYER_DONE = 3

# tempo_type used by fluid_player_set_tempo()
FLUID_PLAYER_TEMPO_INTERNAL = 0
FLUID_PLAYER_TEMPO_EXTERNAL_BPM = 1
FLUID_PLAYER_TEMPO_EXTERNAL_MIDI = 2

new_fluid_player = cfunc('new_fluid_player', c_void_p,
                          ('synth', c_void_p, 1))

delete_fluid_player = cfunc('delete_fluid_player', None,
                             ('player', c_void_p, 1))

fluid_player_add = cfunc('fluid_player_add', c_int,
                         ('player', c_void_p, 1),
                         ('filename', c_char_p, 1))


fluid_player_get_status = cfunc('fluid_player_get_status', c_int,
                                ('player', c_void_p, 1))
fluid_player_join = cfunc('fluid_player_join', c_int,
                          ('player', c_void_p, 1))

fluid_player_play = cfunc('fluid_player_play', c_int,
                          ('player', c_void_p, 1))

fluid_player_set_playback_callback = cfunc('fluid_player_set_playback_callback', c_int,
                                           ('player', c_void_p, 1),
                                           ('handler', CFUNCTYPE(c_int, c_void_p, c_void_p), 1),
                                           ('event_handler_data', c_void_p, 1))

fluid_player_set_tempo = cfunc('fluid_player_set_tempo', c_int,
                               ('player', c_void_p, 1),
                               ('tempo_type', c_int, 1),
                               ('tempo', c_double, 1))

fluid_player_seek = cfunc('fluid_player_seek', c_int,
                          ('player', c_void_p, 1),
                          ('ticks', c_int, 1))

fluid_player_stop = cfunc('fluid_player_stop', c_int,
                          ('player', c_void_p, 1))

# fluid audio driver
new_fluid_audio_driver = cfunc('new_fluid_audio_driver', c_void_p,
                               ('settings', c_void_p, 1),
                               ('synth', c_void_p, 1))

delete_fluid_audio_driver = cfunc('delete_fluid_audio_driver', None,
                                  ('driver', c_void_p, 1))

# fluid midi driver
new_fluid_midi_driver = cfunc('new_fluid_midi_driver', c_void_p,
                               ('settings', c_void_p, 1),
                               ('handler', CFUNCTYPE(c_int, c_void_p, c_void_p), 1),
                               ('event_handler_data', c_void_p, 1))


# fluid midi router rule
class fluid_midi_router_t(Structure):
    _fields_ = [
        ('synth', c_void_p),
        ('rules_mutex', c_void_p),
        ('rules', c_void_p*6),
        ('free_rules', c_void_p),
        ('event_handler', c_void_p),
        ('event_handler_data', c_void_p),
        ('nr_midi_channels', c_int),
        ('cmd_rule', c_void_p),
        ('cmd_rule_type', POINTER(c_int))]

delete_fluid_midi_router_rule = cfunc('delete_fluid_midi_router_rule', c_int,
                                    ('rule', c_void_p, 1))

new_fluid_midi_router_rule = cfunc('new_fluid_midi_router_rule', c_void_p)

fluid_midi_router_rule_set_chan = cfunc('fluid_midi_router_rule_set_chan', None,
                                    ('rule', c_void_p, 1),
                                    ('min', c_int, 1),
                                    ('max', c_int, 1),
                                    ('mul', c_float, 1),
                                    ('add', c_int, 1))

fluid_midi_router_rule_set_param1 = cfunc('fluid_midi_router_rule_set_param1', None,
                                    ('rule', c_void_p, 1),
                                    ('min', c_int, 1),
                                    ('max', c_int, 1),
                                    ('mul', c_float, 1),
                                    ('add', c_int, 1))

fluid_midi_router_rule_set_param2 = cfunc('fluid_midi_router_rule_set_param2', None,
                                    ('rule', c_void_p, 1),
                                    ('min', c_int, 1),
                                    ('max', c_int, 1),
                                    ('mul', c_float, 1),
                                    ('add', c_int, 1))

# fluid midi router
new_fluid_midi_router = cfunc('new_fluid_midi_router', POINTER(fluid_midi_router_t),
                               ('settings', c_void_p, 1),
                               ('handler', CFUNCTYPE(c_int, c_void_p, c_void_p), 1),
                               ('event_handler_data', c_void_p, 1))

fluid_midi_router_handle_midi_event = cfunc('fluid_midi_router_handle_midi_event', c_int,
                               ('data', c_void_p, 1),
                               ('event', c_void_p, 1))

fluid_midi_router_clear_rules = cfunc('fluid_midi_router_clear_rules', c_int,
                                    ('router', POINTER(fluid_midi_router_t), 1))

fluid_midi_router_set_default_rules = cfunc('fluid_midi_router_set_default_rules', c_int,
                                    ('router', POINTER(fluid_midi_router_t), 1))

fluid_midi_router_add_rule = cfunc('fluid_midi_router_add_rule', c_int,
                                    ('router', POINTER(fluid_midi_router_t), 1),
                                    ('rule', c_void_p, 1),
                                    ('type', c_int, 1))

# fluidsynth 2.x
new_fluid_cmd_handler=cfunc('new_fluid_cmd_handler', c_void_p,
                               ('synth', c_void_p, 1),
                               ('router', c_void_p, 1))

fluid_synth_get_sfont_by_id = cfunc('fluid_synth_get_sfont_by_id', c_void_p,
                                    ('synth', c_void_p, 1),
                                    ('id', c_int, 1))

fluid_sfont_get_preset = cfunc('fluid_sfont_get_preset', c_void_p,
                               ('sfont', c_void_p, 1),
                               ('banknum', c_int, 1),
                               ('prenum', c_int, 1))

fluid_preset_get_name = cfunc('fluid_preset_get_name', c_char_p,
                              ('preset', c_void_p, 1))

fluid_synth_set_reverb = cfunc('fluid_synth_set_reverb', c_int,
                                    ('synth', c_void_p, 1),
                                    ('roomsize', c_double, 1),
                                    ('damping', c_double, 1),
                                    ('width', c_double, 1),
                                    ('level', c_double, 1))

fluid_synth_set_chorus = cfunc('fluid_synth_set_chorus', c_int,
                                    ('synth', c_void_p, 1),
                                    ('nr', c_int, 1),
                                    ('level', c_double, 1),
                                    ('speed', c_double, 1),
                                    ('depth_ms', c_double, 1),
                                    ('type', c_int, 1))

fluid_synth_get_chorus_speed = cfunc('fluid_synth_get_chorus_speed', c_double,
                                     ('synth', c_void_p, 1))

fluid_synth_get_chorus_depth = cfunc('fluid_synth_get_chorus_depth', c_double,
                                     ('synth', c_void_p, 1))


def fluid_synth_write_s16_stereo(synth, len):
    """Return generated samples in stereo 16-bit format

    Return value is a Numpy array of samples.

    """
    import numpy
    buf = create_string_buffer(len * 4)
    fluid_synth_write_s16(synth, len, buf, 0, 2, buf, 1, 2)
    return numpy.frombuffer(buf[:], dtype=numpy.int16)


# Object-oriented interface, simplifies access to functions

class Synth:
    """Synth represents a FluidSynth synthesizer"""
    def __init__(self, gain=0.2, samplerate=44100, channels=256, **kwargs):
        """Create new synthesizer object to control sound generation

        Optional keyword arguments:
        gain : scale factor for audio output, default is 0.2
        lower values are quieter, allow more simultaneous notes
        samplerate : output samplerate in Hz, default is 44100 Hz
        added capability for passing arbitrary fluid settings using args
        """
        self.settings = new_fluid_settings()
        self.setting('synth.gain', gain)
        self.setting('synth.sample-rate', float(samplerate))
        self.setting('synth.midi-channels', channels)
        for opt,val in kwargs.items():
            self.setting(opt, val)
        self.synth = new_fluid_synth(self.settings)
        self.audio_driver = None
        self.midi_driver = None
        self.router = None
    def setting(self, opt, val):
        """change an arbitrary synth setting, type-smart"""
        if isinstance(val, (str, bytes)):
            fluid_settings_setstr(self.settings, opt.encode(), val.encode())
        elif isinstance(val, int):
            fluid_settings_setint(self.settings, opt.encode(), val)
        elif isinstance(val, float):
            fluid_settings_setnum(self.settings, opt.encode(), c_double(val))
    def get_setting(self, opt):
        """get current value of an arbitrary synth setting"""
        val = c_int()
        if fluid_settings_getint(self.settings, opt.encode(), byref(val)) == FLUIDSETTING_EXISTS:
            return val.value
        strval = create_string_buffer(32)
        if fluid_settings_copystr(self.settings, opt.encode(), strval, 32) == FLUIDSETTING_EXISTS:
            return strval.value.decode()
        num = c_double()
        if fluid_settings_getnum(self.settings, opt.encode(), byref(num)) == FLUIDSETTING_EXISTS:
            return round(num.value, 6)
        return None

    def start(self, driver=None, device=None, midi_driver=None, midi_router=None):
        """Start audio output driver in separate background thread

        Call this function any time after creating the Synth object.
        If you don't call this function, use get_samples() to generate
        samples.

        Optional keyword argument:
        driver : which audio driver to use for output
        device : the device to use for audio output
        midi_driver : the midi driver to use for communicating with midi devices
        see http://www.fluidsynth.org/api/fluidsettings.xml for allowed values and defaults by platform
        """
        driver = driver or self.get_setting('audio.driver')
        device = device or self.get_setting('audio.%s.device' % driver)
        midi_driver = midi_driver or self.get_setting('midi.driver')

        self.setting('audio.driver', driver)
        self.setting('audio.%s.device' % driver, device)
        self.audio_driver = new_fluid_audio_driver(self.settings, self.synth)
        self.setting('midi.driver', midi_driver)
        self.router = new_fluid_midi_router(self.settings, fluid_synth_handle_midi_event, self.synth)
        if new_fluid_cmd_handler:
            new_fluid_cmd_handler(self.synth, self.router)
        else:
            fluid_synth_set_midi_router(self.synth, self.router)
        if midi_router == None: ## Use fluidsynth to create a MIDI event handler
            self.midi_driver = new_fluid_midi_driver(self.settings, fluid_midi_router_handle_midi_event, self.router)
            self.custom_router_callback = None
        else:                   ## Supply an external MIDI event handler
            self.custom_router_callback = CFUNCTYPE(c_int, c_void_p, c_void_p)(midi_router)
            self.midi_driver = new_fluid_midi_driver(self.settings, self.custom_router_callback, self.router)
        return FLUID_OK

    def delete(self):
        if self.audio_driver:
            delete_fluid_audio_driver(self.audio_driver)
        delete_fluid_synth(self.synth)
        delete_fluid_settings(self.settings)
    def sfload(self, filename, update_midi_preset=0):
        """Load SoundFont and return its ID"""
        return fluid_synth_sfload(self.synth, filename.encode(), update_midi_preset)
    def sfunload(self, sfid, update_midi_preset=0):
        """Unload a SoundFont and free memory it used"""
        return fluid_synth_sfunload(self.synth, sfid, update_midi_preset)
    def program_select(self, chan, sfid, bank, preset):
        """Select a program"""
        return fluid_synth_program_select(self.synth, chan, sfid, bank, preset)
    def program_unset(self, chan):
        """Set the preset of a MIDI channel to an unassigned state"""
        return fluid_synth_unset_program(self.synth, chan)
    def channel_info(self, chan):
        """get soundfont, bank, prog, preset name of channel"""
        if fluid_synth_get_channel_info is not None:
            info=fluid_synth_channel_info_t()
            fluid_synth_get_channel_info(self.synth, chan, byref(info))
            return (info.sfont_id, info.bank, info.program, info.name)
        else:
            (sfontid, banknum, presetnum) = self.program_info(chan)
            presetname = self.sfpreset_name(sfontid, banknum, presetnum)
            return (sfontid, banknum, presetnum, presetname)
    def program_info(self, chan):
        """get active soundfont, bank, prog on a channel"""
        if fluid_synth_get_program is not None:
            sfontid=c_int()
            banknum=c_int()
            presetnum=c_int()
            fluid_synth_get_program(self.synth, chan, byref(sfontid), byref(banknum), byref(presetnum))
            return (sfontid.value, banknum.value, presetnum.value)
        else:
            (sfontid, banknum, prognum, presetname) = self.channel_info(chan)
            return (sfontid, banknum, prognum)
    def sfpreset_name(self, sfid, bank, prenum):
        """Return name of a soundfont preset"""
        if fluid_synth_get_sfont_by_id is not None:
            sfont=fluid_synth_get_sfont_by_id(self.synth, sfid)
            preset=fluid_sfont_get_preset(sfont, bank, prenum)
            if not preset:
                return None
            return fluid_preset_get_name(preset).decode('ascii')
        else:
            (sfontid, banknum, presetnum, presetname) = self.channel_info(chan)
            return presetname
    def router_clear(self):
        if self.router is not None:
            fluid_midi_router_clear_rules(self.router)
    def router_default(self):
        if self.router is not None:
            fluid_midi_router_set_default_rules(self.router)
    def router_begin(self, type):
        """types are [note|cc|prog|pbend|cpress|kpress]"""
        if self.router is not None:
            if type=='note':
                self.router.cmd_rule_type=0
            elif type=='cc':
                self.router.cmd_rule_type=1
            elif type=='prog':
                self.router.cmd_rule_type=2
            elif type=='pbend':
                self.router.cmd_rule_type=3
            elif type=='cpress':
                self.router.cmd_rule_type=4
            elif type=='kpress':
                self.router.cmd_rule_type=5
            if 'self.router.cmd_rule' in globals():
                delete_fluid_midi_router_rule(self.router.cmd_rule)
            self.router.cmd_rule = new_fluid_midi_router_rule()
    def router_end(self):
        if self.router is not None:
            if self.router.cmd_rule is None:
                return
            if fluid_midi_router_add_rule(self.router, self.router.cmd_rule, self.router.cmd_rule_type)<0:
                delete_fluid_midi_router_rule(self.router.cmd_rule)
            self.router.cmd_rule=None
    def router_chan(self, min, max, mul, add):
        if self.router is not None:
            fluid_midi_router_rule_set_chan(self.router.cmd_rule, min, max, mul, add)
    def router_par1(self, min, max, mul, add):
        if self.router is not None:
            fluid_midi_router_rule_set_param1(self.router.cmd_rule, min, max, mul, add)
    def router_par2(self, min, max, mul, add):
        if self.router is not None:
            fluid_midi_router_rule_set_param2(self.router.cmd_rule, min, max, mul, add)
    def set_reverb(self, roomsize=-1.0, damping=-1.0, width=-1.0, level=-1.0):
        """
        roomsize Reverb room size value (0.0-1.0)
        damping Reverb damping value (0.0-1.0)
        width Reverb width value (0.0-100.0)
        level Reverb level value (0.0-1.0)
        """
        if fluid_synth_set_reverb is not None:
            return fluid_synth_set_reverb(self.synth, roomsize, damping, width, level)
        else:
            set=0
            if roomsize>=0:
                set+=0b0001
            if damping>=0:
                set+=0b0010
            if width>=0:
                set+=0b0100
            if level>=0:
                set+=0b1000
            return fluid_synth_set_reverb_full(self.synth, set, roomsize, damping, width, level)
    def set_chorus(self, nr=-1, level=-1.0, speed=-1.0, depth=-1.0, type=-1):
        """
        nr Chorus voice count (0-99, CPU time consumption proportional to this value)
        level Chorus level (0.0-10.0)
        speed Chorus speed in Hz (0.29-5.0)
        depth_ms Chorus depth (max value depends on synth sample rate, 0.0-21.0 is safe for sample rate values up to 96KHz)
        type Chorus waveform type (0=sine, 1=triangle)
        """
        if fluid_synth_set_chorus is not None:
            return fluid_synth_set_chorus(self.synth, nr, level, speed, depth, type)
        else:
            set=0
            if nr>=0:
                set+=0b00001
            if level>=0:
                set+=0b00010
            if speed>=0:
                set+=0b00100
            if depth>=0:
                set+=0b01000
            if type>=0:
                set+=0b10000
            return fluid_synth_set_chorus_full(self.synth, set, nr, level, speed, depth, type)
    def set_reverb_roomsize(self, roomsize):
        if fluid_synth_set_reverb_roomsize is not None:
            return fluid_synth_set_reverb_roomsize(self.synth, roomsize)
        else:
            return self.set_reverb(roomsize=roomsize)
    def set_reverb_damp(self, damping):
        if fluid_synth_set_reverb_damp is not None:
            return fluid_synth_set_reverb_damp(self.synth, damping)
        else:
            return self.set_reverb(damping=damping)
    def set_reverb_level(self, level):
        if fluid_synth_set_reverb_level is not None:
            return fluid_synth_set_reverb_level(self.synth, level)
        else:
            return self.set_reverb(level=level)
    def set_reverb_width(self, width):
        if fluid_synth_set_reverb_width is not None:
            return fluid_synth_set_reverb_width(self.synth, width)
        else:
            return self.set_reverb(width=width)
    def set_chorus_nr(self, nr):
        if fluid_synth_set_chorus_nr is not None:
            return fluid_synth_set_chorus_nr(self.synth, nr)
        else:
            return self.set_chorus(nr=nr)
    def set_chorus_level(self, level):
        if fluid_synth_set_chorus_level is not None:
            return fluid_synth_set_chorus_level(self.synth, level)
        else:
            return self.set_chorus(leve=level)
    def set_chorus_speed(self, speed):
        if fluid_synth_set_chorus_speed is not None:
            return fluid_synth_set_chorus_speed(self.synth, speed)
        else:
            return self.set_chorus(speed=speed)
    def set_chorus_depth(self, depth):
        if fluid_synth_set_chorus_depth is not None:
            return fluid_synth_set_chorus_depth(self.synth, depth)
        else:
            return self.set_chorus(depth=depth)
    def set_chorus_type(self, type):
        if fluid_synth_set_chorus_type is not None:
            return fluid_synth_set_chorus_type(self.synth, type)
        else:
            return self.set_chorus(type=type)
    def get_reverb_roomsize(self):
        return fluid_synth_get_reverb_roomsize(self.synth)
    def get_reverb_damp(self):
        return fluid_synth_get_reverb_damp(self.synth)
    def get_reverb_level(self):
        return fluid_synth_get_reverb_level(self.synth)
    def get_reverb_width(self):
        return fluid_synth_get_reverb_width(self.synth)
    def get_chorus_nr(self):
        return fluid_synth_get_chorus_nr(self.synth)
    def get_chorus_level(self):
        return fluid_synth_get_reverb_level(self.synth)
    def get_chorus_speed(self):
        if fluid_synth_get_chorus_speed is not None:
            return fluid_synth_get_chorus_speed(self.synth)
        else:
            return fluid_synth_get_chorus_speed_Hz(self.synth)
    def get_chorus_depth(self):
        if fluid_synth_get_chorus_depth is not None:
            return fluid_synth_get_chorus_depth(self.synth)
        else:
            return fluid_synth_get_chorus_depth_ms(self.synth)
    def get_chorus_type(self):
        return fluid_synth_get_chorus_type(self.synth)
    def noteon(self, chan, key, vel):
        """Play a note"""
        if key < 0 or key > 127:
            return False
        if chan < 0:
            return False
        if vel < 0 or vel > 127:
            return False
        return fluid_synth_noteon(self.synth, chan, key, vel)
    def noteoff(self, chan, key):
        """Stop a note"""
        if key < 0 or key > 127:
            return False
        if chan < 0:
            return False
        return fluid_synth_noteoff(self.synth, chan, key)
    def pitch_bend(self, chan, val):
        """Adjust pitch of a playing channel by small amounts

        A pitch bend value of 0 is no pitch change from default.
        A value of -2048 is 1 semitone down.
        A value of 2048 is 1 semitone up.
        Maximum values are -8192 to +8192 (transposing by 4 semitones).

        """
        return fluid_synth_pitch_bend(self.synth, chan, val + 8192)
    def cc(self, chan, ctrl, val):
        """Send control change value

        The controls that are recognized are dependent on the
        SoundFont.  Values are always 0 to 127.  Typical controls
        include:
          1 : vibrato
          7 : volume
          10 : pan (left to right)
          11 : expression (soft to loud)
          64 : sustain
          91 : reverb
          93 : chorus
        """
        return fluid_synth_cc(self.synth, chan, ctrl, val)
    def get_cc(self, chan, num):
        i=c_int()
        fluid_synth_get_cc(self.synth, chan, num, byref(i))
        return i.value
    def program_change(self, chan, prg):
        """Change the program"""
        return fluid_synth_program_change(self.synth, chan, prg)
    def bank_select(self, chan, bank):
        """Choose a bank"""
        return fluid_synth_bank_select(self.synth, chan, bank)
    def all_notes_off(self, chan):
        """Turn off all notes on a channel (release all keys)"""
        return fluid_synth_all_notes_off(self.synth, chan)
    def all_sounds_off(self, chan):
        """Turn off all sounds on a channel (equivalent to mute)"""
        return fluid_synth_all_sounds_off(self.synth, chan)
    def sfont_select(self, chan, sfid):
        """Choose a SoundFont"""
        return fluid_synth_sfont_select(self.synth, chan, sfid)
    def program_reset(self):
        """Reset the programs on all channels"""
        return fluid_synth_program_reset(self.synth)
    def system_reset(self):
        """Stop all notes and reset all programs"""
        return fluid_synth_system_reset(self.synth)
    def get_samples(self, len=1024):
        """Generate audio samples

        The return value will be a NumPy array containing the given
        length of audio samples.  If the synth is set to stereo output
        (the default) the array will be size 2 * len.

        """
        return fluid_synth_write_s16_stereo(self.synth, len)
    def tuning_dump(self, bank, prog, pitch):
        return fluid_synth_tuning_dump(self.synth, bank, prog, name.encode(), length(name), pitch)

    def midi_event_get_type(self, event):
        return fluid_midi_event_get_type(event)
    def midi_event_get_velocity(self, event):
        return fluid_midi_event_get_velocity(event)
    def midi_event_get_key(self, event):
        return fluid_midi_event_get_key(event)
    def midi_event_get_channel(self, event):
        return fluid_midi_event_get_channel(event)
    def midi_event_get_control(self, event):
        return fluid_midi_event_get_control(event)
    def midi_event_get_program(self, event):
        return fluid_midi_event_get_program(event)
    def midi_event_get_value(self, event):
        return fluid_midi_event_get_value(event)

    def play_midi_file(self, filename):
        self.player = new_fluid_player(self.synth)
        if self.player == None: return FLUID_FAILED
        if self.custom_router_callback != None:
            fluid_player_set_playback_callback(self.player, self.custom_router_callback, self.synth)
        status = fluid_player_add(self.player, filename.encode())
        if status == FLUID_FAILED: return status
        status = fluid_player_play(self.player)
        return status

    def play_midi_stop(self):
        status = fluid_player_stop(self.player)
        if status == FLUID_FAILED: return status
        status = fluid_player_seek(self.player, 0)
        delete_fluid_player(self.player)
        return status

    def player_set_tempo(self, tempo_type, tempo):
        return fluid_player_set_tempo(self.player, tempo_type, tempo)



class Sequencer:
    def __init__(self, time_scale=1000, use_system_timer=True):
        """Create new sequencer object to control and schedule timing of midi events

        Optional keyword arguments:
        time_scale: ticks per second, defaults to 1000
        use_system_timer: whether the sequencer should advance by itself
        """
        self.client_callbacks = []
        self.sequencer = new_fluid_sequencer2(use_system_timer)
        fluid_sequencer_set_time_scale(self.sequencer, time_scale)

    def register_fluidsynth(self, synth):
        response = fluid_sequencer_register_fluidsynth(self.sequencer, synth.synth)
        if response == FLUID_FAILED:
            raise Error("Registering fluid synth failed")
        return response

    def register_client(self, name, callback, data=None):
        c_callback = CFUNCTYPE(None, c_uint, c_void_p, c_void_p, c_void_p)(callback)
        response = fluid_sequencer_register_client(self.sequencer, name.encode(), c_callback, data)
        if response == FLUID_FAILED:
            raise Error("Registering client failed")

        # store in a list to prevent garbage collection
        self.client_callbacks.append(c_callback)

        return response

    def note(self, time, channel, key, velocity, duration, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_note(evt, channel, key, velocity, duration)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def note_on(self, time, channel, key, velocity=127, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_noteon(evt, channel, key, velocity)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def note_off(self, time, channel, key, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_noteoff(evt, channel, key)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def timer(self, time, data=None, source=-1, dest=-1, absolute=True):
        evt = self._create_event(source, dest)
        fluid_event_timer(evt, data)
        self._schedule_event(evt, time, absolute)
        delete_fluid_event(evt)

    def _create_event(self, source=-1, dest=-1):
        evt = new_fluid_event()
        fluid_event_set_source(evt, source)
        fluid_event_set_dest(evt, dest)
        return evt

    def _schedule_event(self, evt, time, absolute=True):
        response = fluid_sequencer_send_at(self.sequencer, evt, time, absolute)
        if response == FLUID_FAILED:
            raise Error("Scheduling event failed")

    def get_tick(self):
        return fluid_sequencer_get_tick(self.sequencer)

    def process(self, msec):
        fluid_sequencer_process(self.sequencer, msec)

    def delete(self):
        delete_fluid_sequencer(self.sequencer)

def raw_audio_string(data):
    """Return a string of bytes to send to soundcard

    Input is a numpy array of samples.  Default output format
    is 16-bit signed (other formats not currently supported).

    """
    import numpy
    return (data.astype(numpy.int16)).tostring()

#===============================================================================

import numpy as np
import wave

def midi_opus_to_colab_audio(midi_opus, 
                              soundfont_path='/usr/share/sounds/sf2/FluidR3_GM.sf2', 
                              sample_rate=16000, # 44100
                              volume_scale=10,
                              trim_silence=True,
                              silence_threshold=0.1,
                              output_for_gradio=False,
                              write_audio_to_WAV=''
                              ):

    def normalize_volume(matrix, factor=10):
        norm = np.linalg.norm(matrix)
        matrix = matrix/norm  # normalized matrix
        mult_matrix = matrix * factor
        final_matrix = np.clip(mult_matrix, -1.0, 1.0)
        return final_matrix

    if midi_opus[1]:

      ticks_per_beat = midi_opus[0]
      event_list = []
      for track_idx, track in enumerate(midi_opus[1:]):
          abs_t = 0
          for event in track:
              abs_t += event[1]
              event_new = [*event]
              event_new[1] = abs_t
              event_list.append(event_new)
      event_list = sorted(event_list, key=lambda e: e[1])

      tempo = int((60 / 120) * 10 ** 6)  # default 120 bpm
      ss = np.empty((0, 2), dtype=np.int16)
      fl = Synth(samplerate=float(sample_rate))
      sfid = fl.sfload(soundfont_path)
      last_t = 0
      for c in range(16):
          fl.program_select(c, sfid, 128 if c == 9 else 0, 0)
      for event in event_list:
          name = event[0]
          sample_len = int(((event[1] / ticks_per_beat) * tempo / (10 ** 6)) * sample_rate)
          sample_len -= int(((last_t / ticks_per_beat) * tempo / (10 ** 6)) * sample_rate)
          last_t = event[1]
          if sample_len > 0:
              sample = fl.get_samples(sample_len).reshape(sample_len, 2)
              ss = np.concatenate([ss, sample])
          if name == "set_tempo":
              tempo = event[2]
          elif name == "patch_change":
              c, p = event[2:4]
              fl.program_select(c, sfid, 128 if c == 9 else 0, p)
          elif name == "control_change":
              c, cc, v = event[2:5]
              fl.cc(c, cc, v)
          elif name == "note_on" and event[3] > 0:
              c, p, v = event[2:5]
              fl.noteon(c, p, v)
          elif name == "note_off" or (name == "note_on" and event[3] == 0):
              c, p = event[2:4]
              fl.noteoff(c, p)

      fl.delete()
      if ss.shape[0] > 0:
          max_val = np.abs(ss).max()
          if max_val != 0:
              ss = (ss / max_val) * np.iinfo(np.int16).max
      ss = ss.astype(np.int16)

      if trim_silence:
          threshold = np.std(np.abs(ss)) * silence_threshold
          exceeded_thresh = np.abs(ss) > threshold
          if np.any(exceeded_thresh): 
              last_idx = np.where(exceeded_thresh)[0][-1]
              ss = ss[:last_idx+1]

      if output_for_gradio:
        return ss
      
      ss = ss.swapaxes(1, 0)

      raw_audio = normalize_volume(ss, volume_scale)
      
      if write_audio_to_WAV != '':

        r_audio = raw_audio.T

        r_audio = np.int16(r_audio / np.max(np.abs(r_audio)) * 32767)

        with wave.open(write_audio_to_WAV, 'w') as wf:
            wf.setframerate(sample_rate)
            wf.setsampwidth(2)
            wf.setnchannels(r_audio.shape[1])
            wf.writeframes(r_audio)

      return raw_audio
  
    else:
      return None

def midi_to_colab_audio(midi_file, 
                        soundfont_path='/usr/share/sounds/sf2/FluidR3_GM.sf2', 
                        sample_rate=16000, # 44100
                        volume_scale=10,
                        trim_silence=True,
                        silence_threshold=0.1,
                        output_for_gradio=False,
                        write_audio_to_WAV=False
                        ):

    '''
    
    Returns raw audio to pass to IPython.disaply.Audio func

    Example usage:

    from IPython.display import Audio

    display(Audio(raw_audio, rate=16000, normalize=False))
    
    '''

    def normalize_volume(matrix, factor=10):
        norm = np.linalg.norm(matrix)
        matrix = matrix/norm  # normalized matrix
        mult_matrix = matrix * factor
        final_matrix = np.clip(mult_matrix, -1.0, 1.0)
        return final_matrix

    midi_opus = midi2opus(open(midi_file, 'rb').read())

    if midi_opus[1]:

      ticks_per_beat = midi_opus[0]
      event_list = []
      for track_idx, track in enumerate(midi_opus[1:]):
          abs_t = 0
          for event in track:
              abs_t += event[1]
              event_new = [*event]
              event_new[1] = abs_t
              event_list.append(event_new)
      event_list = sorted(event_list, key=lambda e: e[1])

      tempo = int((60 / 120) * 10 ** 6)  # default 120 bpm
      ss = np.empty((0, 2), dtype=np.int16)
      fl = Synth(samplerate=float(sample_rate))
      sfid = fl.sfload(soundfont_path)
      last_t = 0
      for c in range(16):
          fl.program_select(c, sfid, 128 if c == 9 else 0, 0)
      for event in event_list:
          name = event[0]
          sample_len = int(((event[1] / ticks_per_beat) * tempo / (10 ** 6)) * sample_rate)
          sample_len -= int(((last_t / ticks_per_beat) * tempo / (10 ** 6)) * sample_rate)
          last_t = event[1]
          if sample_len > 0:
              sample = fl.get_samples(sample_len).reshape(sample_len, 2)
              ss = np.concatenate([ss, sample])
          if name == "set_tempo":
              tempo = event[2]
          elif name == "patch_change":
              c, p = event[2:4]
              fl.program_select(c, sfid, 128 if c == 9 else 0, p)
          elif name == "control_change":
              c, cc, v = event[2:5]
              fl.cc(c, cc, v)
          elif name == "note_on" and event[3] > 0:
              c, p, v = event[2:5]
              fl.noteon(c, p, v)
          elif name == "note_off" or (name == "note_on" and event[3] == 0):
              c, p = event[2:4]
              fl.noteoff(c, p)

      fl.delete()
      if ss.shape[0] > 0:
          max_val = np.abs(ss).max()
          if max_val != 0:
              ss = (ss / max_val) * np.iinfo(np.int16).max
      ss = ss.astype(np.int16)

      if trim_silence:
          threshold = np.std(np.abs(ss)) * silence_threshold
          exceeded_thresh = np.abs(ss) > threshold
          if np.any(exceeded_thresh): 
              last_idx = np.where(exceeded_thresh)[0][-1]
              ss = ss[:last_idx+1]

      if output_for_gradio:
        return ss

      ss = ss.swapaxes(1, 0)

      raw_audio = normalize_volume(ss, volume_scale)

      if write_audio_to_WAV:

        filename = midi_file.split('.')[-2] + '.wav'

        r_audio = raw_audio.T

        r_audio = np.int16(r_audio / np.max(np.abs(r_audio)) * 32767)

        with wave.open(filename, 'w') as wf:
            wf.setframerate(sample_rate)
            wf.setsampwidth(2)
            wf.setnchannels(r_audio.shape[1])
            wf.writeframes(r_audio)

      return raw_audio
  
    else:
      return None
    
#===================================================================================================================
