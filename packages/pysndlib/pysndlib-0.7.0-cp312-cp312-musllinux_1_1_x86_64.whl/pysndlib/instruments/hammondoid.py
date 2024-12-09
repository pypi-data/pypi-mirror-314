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
# --------------- hammondoid ---------------- #
#   ;; from Perry Cook's BeeThree.cpp
@cython.ccall
def hammondoid(beg, dur, freq, amp):
    osc0  = clm.make_oscil(freq * .999)
    osc1  = clm.make_oscil(freq * 1.997)
    osc2  = clm.make_oscil(freq * 3.006)
    osc3  = clm.make_oscil(freq * 6.009)
    ampenv1  = clm.make_env([0,0,.005, 1, dur-.008, 1, dur, 0], duration=dur)
    ampenv2  = clm.make_env([0,0,.005, 1, dur, 0], duration=dur, scaler=(.5 * .75 * amp))
    g0: cython.double = .25 * .75 * amp
    g1: cython.double = .25 * .75 * amp
    g2: cython.double = .5 * amp
    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    
    i: cython.long = 0
        
    for i in range(st, nd):
        clm.outa(i, (clm.env(ampenv1) * ((g0 * clm.oscil(osc0)) + (g1 * clm.oscil(osc1)) + (g2 * clm.oscil(osc2)))) +
                    (clm.env(ampenv2)*clm.oscil(osc3)))
