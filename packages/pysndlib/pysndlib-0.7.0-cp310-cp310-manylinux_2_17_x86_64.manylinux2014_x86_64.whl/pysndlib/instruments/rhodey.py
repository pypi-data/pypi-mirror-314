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

# --------------- rhodey ---------------- #
@cython.ccall
#   ;; from Perry Cook's Rhodey.cpp
def rhodey(beg, dur, freq, amp, base=.5):
    osc0 = clm.make_oscil(freq)
    osc1 = clm.make_oscil(freq * .5)
    osc2 = clm.make_oscil(freq)
    osc3 = clm.make_oscil(freq * 15.0)
    ampenv1 = clm.make_env([0,0,.005, 1, dur, 0], base=base, duration=dur, scaler=(amp * .5))
    ampenv2 = clm.make_env([0,0,.001, 1, dur, 0], base=(1.5 * base), duration=dur, scaler=(amp * .5))
    ampenv3 = clm.make_env([0,0,.001, 1, .25, 0, max(dur, .26), 0], base=(4. * base), duration=dur, scaler= .109)
    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    
    i: cython.long = 0
        
    for i in range(st, nd):
        clm.outa(i, ( clm.env(ampenv1)*clm.oscil(osc0, (.535 * clm.oscil(osc1)))) + (clm.env (ampenv2) * clm.oscil(osc2, clm.env(ampenv3) * clm.oscil(osc3))))
