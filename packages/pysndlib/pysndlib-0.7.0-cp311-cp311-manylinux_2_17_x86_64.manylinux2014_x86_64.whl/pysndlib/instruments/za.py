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

# --------------- za ---------------- #
@cython.ccall
def za(time, dur, freq, amp, length1, length2, feedback, feedforward):
    beg: cython.long = clm.seconds2samples(time)
    end: cython.long = clm.seconds2samples(time + dur)
    s: clm.mus_any = clm.make_pulse_train(freq, amplitude=amp)
    d0: clm.mus_any = clm.make_all_pass(feedback, feedforward, size=length1, max_size=(1 + max(length1, length2)))
    zenv: clm.mus_any = clm.make_env([0,0,1,1], scaler=(length2-length1), duration=dur)
    i: cython.long = 0
    for i in range(beg, end):
        clm.outa(i, clm.all_pass(d0, clm.pulse_train(s), clm.env(zenv)))

if __name__ == '__main__': 
    with clm.Sound(play=True,statistics=True):
        za(0,1,100,.5, 20, 100, .95, .95)
        za(1.5, 1, 100, .5, 100, 20, .95, .95)
