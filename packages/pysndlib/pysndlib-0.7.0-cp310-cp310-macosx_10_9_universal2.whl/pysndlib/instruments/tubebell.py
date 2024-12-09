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

# --------------- tubebell ---------------- #
# ;;; taken from Perry Cook's stkv1.tar.Z (Synthesis Toolkit), but I was
# ;;; in a bit of a hurry and may not have made slavishly accurate translations.
# ;;; Please let me know of any errors.

@cython.ccall
def tubebell(beg, dur, freq, amp, base=32.0):
    osc0 = clm.make_oscil(freq * .995)
    osc1 = clm.make_oscil(freq * 1.414 * 0.995)
    osc2 = clm.make_oscil(freq * 1.005)
    osc3 = clm.make_oscil(freq * 1.414)
    ampenv1 = clm.make_env([0,0,.005, 1, dur, 0], base=base, duration=dur, scaler=(amp * .5 * .707))
    ampenv2 = clm.make_env([0,0,.001, 1, dur, 0], base=(2 * base), duration=dur, scaler=(amp * .5))
    ampmod = clm.make_oscil(2.0)
    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    
    i: cython.long = 0
    
    for i in range(st, nd):
        clm.outa(i, ((.007 * clm.oscil(ampmod)) + .993) *
                ((clm.env(ampenv1) * clm.oscil(osc0, (.203 * clm.oscil(osc1)))) +
                 (clm.env(ampenv2) * clm.oscil(osc2, (.144 * clm.oscil(osc3))))))

if __name__ == '__main__':  
    import random

    with clm.Sound( play = True, statistics=True):
        freqs = [1174.659, 1318.510, 1396.913, 1567.982, 2093.005]
        for t in np.arange(0, 10, .4):
            tubebell(t, 1, random.choice(freqs), .5)    

