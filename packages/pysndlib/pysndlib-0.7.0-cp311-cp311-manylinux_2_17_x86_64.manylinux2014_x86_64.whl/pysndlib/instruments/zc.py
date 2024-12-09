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


# --------------- zc ---------------- #
@cython.ccall
def zc(time, dur, freq, amp, length1, length2, feedback):
    beg: cython.long = clm.seconds2samples(time)
    end: cython.long = clm.seconds2samples(time + dur)
    s = clm.make_pulse_train(freq, amplitude=amp)
    d0 = clm.make_comb(feedback, size=length1, max_size=(1 + max(length1, length2)))
    zenv = clm.make_env([0,0,1,1], scaler=(length2-length1), duration=dur)
    
    i: cython.long = 0
    
    for i in range(beg, end):
        clm.outa(i, clm.comb(d0, clm.pulse_train(s), clm.env(zenv)))

if __name__ == '__main__': 
    with clm.Sound( play = True, statistics=True):
        zc(0,3,100,.5,20,100,.95) 
        zc(3., 3, 100, .5, 100, 20, .95)
