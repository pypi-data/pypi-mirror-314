#==================================================================================
# The code is ported from Bill Schottstedaet's 'generators.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.generators as gens
if cython.compiled:
    from cython.cimports.pysndlib import clm
    from cython.cimports.pysndlib import generators as gens

# from generators.scm 
# uses make_rxykcos generator

# --------------- brassy ---------------- #
@cython.ccall
def brassy(start, dur, freq, amp, ampf, freqf, gliss):
    gen = clm.make_rxykcos(freq, 1, 0.0)
    beg = clm.seconds2samples(start)
    end = clm.seconds2samples(start+dur)
    amp_env = clm.make_env(ampf, duration=dur, scaler=amp)
    pitch_env = clm.make_env(freqf, scaler=gliss / freq, duration=dur)
    slant = clm.make_moving_average(clm.seconds2samples(.05))
    vib = clm.make_polywave(5, [1, clm.hz2radians(4.0)], clm.Polynomial.SECOND_KIND)
    harmfrq: cython.double = 0.0
    harmonic: cython.double = 0.0
    dist: cython.double = 0.0
    slant.mus_increment = clm.hz2radians(freq) * slant.mus_increment
    for i in range(beg, end):
        harmfrq = clm.env(pitch_env)
        harmonic = math.floor(harmfrq)
        dist = abs(harmfrq - harmonic)
        gen.mus_scaler = 20.0 * min(.1, dist, (1.0 - dist))
        clm.outa(i, clm.env(amp_env) * clm.rxykcos(gen, clm.moving_average(slant, harmonic) + clm.polywave(vib)))


if __name__ == '__main__': 

    with clm.Sound(clipped=False, statistics=True, play=True):
        brassy(0,4,50,.05,[0,0,1,1,10,1,11,0], [0,1,1,0], 1000)
