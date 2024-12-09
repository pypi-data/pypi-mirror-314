#==================================================================================
# The code is ported from Bill Schottstedaet's 'generators.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
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
# uses r2k!cos generator

# --------------- pianoy1 ---------------- #

@cython.ccall
def pianoy1(start, dur, freq, amp, bounce_freq=5, bounce_amp=20):
    gen = gens.make_r2kfcos(freq, r=.5, k=3)
    gen1 = clm.make_oscil(bounce_freq)
    bouncef = clm.make_env([0,1,1,0], base=32, scaler=bounce_amp, duration=1.0)
    rf = clm.make_env([0,0,1,1,max(2.0,dur), 0], base=32, scaler=.1, offset=.25, duration=dur)
    ampf = clm.make_env([0,0,.01,1,.03,1,1,.15, max(2,dur), 0.0], base=32, scaler=amp, duration=dur)
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start+dur)
    ln = clm.seconds2samples(dur)
    fv: np.ndarray = np.zeros(ln)
    i: cython.long = 0
    j: cython.long = 0
    for i in range(ln):
        fv[i] = clm.env(rf) + abs(clm.env(bouncef) * clm.oscil(gen1))
    
    for i in range(beg, end):
        gen.r = fv[j]
        clm.outa(i, clm.env(ampf) * gens.r2kfcos(gen))
        j += 1

if __name__ == '__main__': 
    with clm.Sound(statistics=True, play=True):
        pianoy1(0,4,200,.5, 1, .1)
