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
# uses r2k!cos generator

# --------------- pianoy2 ---------------- #
@cython.ccall
def pianoy2(start, dur, freq, amp, bounce_freq=5, bounce_amp=20):
    gen = gens.make_r2kfcos(freq, r=.5, k=3)
    ampf = clm.make_env([0,0,.01,1,.03,1,1,.15, max(2,dur), 0.0], base=32, scaler=amp, duration=dur)
    knock = gens.make_fmssb(10., 20., index=1.0)
    kmpf = clm.make_env([0,0,1,1,3,1,100,0], base=3, scaler=.05, length=30000)
    indf = clm.make_env([0,1,1,0], length=30000, base=3, scaler=10)
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start+dur)
    
    for i in range(beg, end):
        knock.index = clm.env(indf)
        clm.outa(i, (clm.env(ampf) * gens.r2kfcos(gen)) + (clm.env(kmpf) * gens.fmssb(knock, 0.0)))

    
if __name__ == '__main__': 
    with clm.Sound(statistics=True, play=True):
        pianoy2(0,1,100,.5)
