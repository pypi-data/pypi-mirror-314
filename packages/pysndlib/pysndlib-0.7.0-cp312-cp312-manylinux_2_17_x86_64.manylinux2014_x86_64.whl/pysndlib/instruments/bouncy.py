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
# uses rkfssb generators 

# --------------- bouncy ---------------- #
@cython.ccall
def bouncy(start, dur, freq, amp, bounce_freq=5, bounce_amp=20):
    lng: cython.long = clm.seconds2samples(dur)
    start: cython.long = clm.seconds2samples(start)
    gen = gens.make_rkfssb(freq*4, 1/4, r=1.0)
    gen1 = clm.make_oscil(bounce_freq)
    bouncef = clm.make_env([0,1,1,0], base=32, scaler=bounce_amp, duration=1.)
    rf = clm.make_env([0,0,1,1,max(2.0, dur), 0], base=32, scaler=3, duration=dur)
    ampf = clm.make_env([0,0,.01,1,.03,1,1,.15, max(2.,dur), 0.0], base=32, scaler=amp, duration=dur)
    stop: cython.long = start+ lng
    fv = np.zeros(lng)
    
    i: cython.long = 0
    for i in range(lng):
        fv[i] = clm.env(rf) + math.fabs(clm.env(bouncef) * clm.oscil(gen1))

    j: cython.long = 0
    
    for i in range(start, stop):
        gen.r = fv[j]
        clm.outa(i, clm.env(ampf) * gens.rkfssb(gen))
        j+=1
        
if __name__ == '__main__': 
        
    with clm.Sound(clipped=False, statistics=True, play=True):
        bouncy(0,2,300,.5, 5, 10)
        bouncy(2.5,2,200,.5, 3, 2)
        
