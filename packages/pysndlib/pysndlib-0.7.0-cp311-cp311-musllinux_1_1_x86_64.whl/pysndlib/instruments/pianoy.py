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
# uses r2k!co generator

# --------------- pianoy ---------------- #
@cython.ccall
def pianoy(start, dur, freq, amp):
    gen = gens.make_r2kfcos(freq, r=.5, k=3)
    ampf = clm.make_env([0,0,.01,1,.03,1,1,.15, max(2,dur), 0.0], base=32, scaler=amp, duration=dur)
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start+dur)
    i:  cython.long = 0
    for i in range(beg, end):
        clm.outa(i, clm.env(ampf) *gens.r2kfcos(gen))


if __name__ == '__main__': 
    with clm.Sound(statistics=True, play=True):
        pianoy(0,3,400,.5)
