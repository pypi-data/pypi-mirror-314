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
#     
# --------------- zn ---------------- #
#   ;; notches are spaced at srate/len, feedforward sets depth thereof
#   ;; so sweep of len from 20 to 100 sweeps the notches down from 1000 Hz to ca 200 Hz 
#   ;; so we hear our downward glissando beneath the pulses.
@cython.ccall
def zn(time, dur, freq, amp, length1, length2, feedforward):
    beg: cython.long = clm.seconds2samples(time)
    end: cython.long = clm.seconds2samples(time + dur)
    s = clm.make_pulse_train(freq, amplitude=amp)
    d0 = clm.make_notch(feedforward, size=length1, max_size=(1 + max(length1, length2)))
    zenv = clm.make_env([0,0,1,1], scaler=(length2-length1), duration=dur)
    
    i: cython.long
    
    for i in range(beg, end):
        clm.outa(i, clm.notch(d0, clm.pulse_train(s), clm.env(zenv)))

if __name__ == '__main__': 
    with clm.Sound(play=True,statistics=True):
        zn(0,1,100,.5,20,100,.995) 
        zn(1.5, 1, 100, .5, 100, 20, .995)
