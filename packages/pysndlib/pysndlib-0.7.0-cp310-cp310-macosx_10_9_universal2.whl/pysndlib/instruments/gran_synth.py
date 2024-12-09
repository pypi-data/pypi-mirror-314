#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
if cython.compiled:
    from cython.cimports.pysndlib import clm

# --------------- gran_synth ---------------- #
@cython.ccall
def gran_synth(startime, duration, audio_freq, grain_dur, grain_interval, amp: cython.double):
    grain_size = math.ceil(max(grain_dur, grain_interval) * clm.get_srate())
    beg: cython.long = clm.seconds2samples(startime)
    end: cython.long = clm.seconds2samples(startime + duration)
    grain_env = clm.make_env([0,0,25,1,75,1,100,0], duration=grain_dur)
    carrier = clm.make_oscil(audio_freq)
    grain = [(clm.env(grain_env) * clm.oscil(carrier)) for i in range(grain_size)]
    grains = clm.make_wave_train(1.0 / grain_interval, grain)

    i: cython.long = 0

    for i in range(beg, end):
        clm.outa(i, amp * clm.wave_train(grains))

if __name__ == '__main__':   
    with clm.Sound( play = True, statistics=True):
        gran_synth(0, 2, 100, .0189, .02, .4)
