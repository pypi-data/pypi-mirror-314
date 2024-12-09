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


# --------------- wurley ---------------- #
#   ;; from Perry Cook's Rhodey.cpp
@cython.ccall
def wurley(beg, dur, freq, amp):
    osc0 = clm.make_oscil(freq)
    osc1 = clm.make_oscil(freq * 4.0)
    osc2 = clm.make_oscil(510.0)
    osc3 = clm.make_oscil(510.0)
    ampmod = clm.make_oscil(8.0)
    g0: cython.double = .5 * amp
    ampenv = clm.make_env([0,0,1,1,9,1,10,0], duration=dur)
    indenv = clm.make_env([0,0,.001,1,.15,0,max(dur, .16),0], duration=dur, scaler=.117)
    resenv = clm.make_env([0,0,.001,1,.25,0,max(dur, .26),0], duration=dur, scaler=(.5 * .307 * amp))
    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    
    i: cython.long = 0
    
    for i in range(st, nd):
        clm.outa(i, clm.env(ampenv) * 
            (1.0 + (.007 * clm.oscil(ampmod))) * 
            ((g0 * clm.oscil(osc0, (.307 * clm.oscil(osc1)))) + (clm.env(resenv) * clm.oscil(osc2, (clm.env(indenv) * clm.oscil(osc3))))))
            
