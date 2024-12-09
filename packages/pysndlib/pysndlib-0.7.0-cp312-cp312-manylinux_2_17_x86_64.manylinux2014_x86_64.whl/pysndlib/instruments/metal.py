#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
if cython.compiled:
    from cython.cimports.pysndlib import clm


# --------------- metal ---------------- #
#   ;; from Perry Cook's HeavyMtl.cpp
@cython.ccall
def metal(beg, dur, freq, amp):
    osc0 = clm.make_oscil(freq)
    osc1 = clm.make_oscil(freq * 4.0 * 0.999)
    osc2 = clm.make_oscil(freq * 3.0 * 1.001)
    osc3 = clm.make_oscil(freq * 0.50 * 1.002)
    ampenv0 = clm.make_env([0,0,.001,1, (dur-.002),1,dur,0], duration=dur, scaler=(amp * .615))
    ampenv1 = clm.make_env([0,0,.001,1,(dur-.011),1,dur,0], duration=dur, scaler=.202)
    ampenv2 = clm.make_env([0,0,.01,1,(dur-.015),1,dur,0], duration=dur, scaler=.574)
    ampenv3 = clm.make_env([0,0,.03,1,(dur-.040),1,dur,0], duration=dur, scaler=.116)
    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    
    i: cython.long = 0
    
    for i in range(st, nd):
        clm.outa(i, (clm.env(ampenv0) * (clm.oscil(osc0, ((clm.env(ampenv1) * clm.oscil(osc1, clm.env(ampenv2) * clm.oscil(osc2))))) +
                    (clm.env(ampenv3) * clm.oscil(osc3)))))
