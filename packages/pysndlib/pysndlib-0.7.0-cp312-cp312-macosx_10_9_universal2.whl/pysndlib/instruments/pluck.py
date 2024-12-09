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
# from pysndlib.env import stretch_envelope
# --------------- pluck ---------------- #

# ;;; The Karplus-Strong algorithm as extended by David Jaffe and Julius Smith -- see 
# ;;;  Jaffe and Smith, "Extensions of the Karplus-Strong Plucked-String Algorithm"
# ;;;  CMJ vol 7 no 2 Summer 1983, reprinted in "The Music Machine".
# ;;;  translated from CLM's pluck.ins


def tuneIt(f, s1):
    def getOptimumC(S,o,p):
        pa = (1.0 / o) * math.atan2((S * math.sin(o)), (1.0 + (S * math.cos(o))) - S)
        tmpInt = math.floor(p - pa)
        pc = p - pa - tmpInt
        
        if pc < .1:
            while pc >= .1:
                tmpInt = tmpInt - 1
                pc += 1.0
        return [tmpInt, (math.sin(o) - math.sin(o * pc)) / math.sin(o + (o * pc))]
        
    p = clm.get_srate() / f
    s = .5 if s1 == 0.0 else s1
    o = clm.hz2radians(f)
    vals = getOptimumC(s,o,p)
    vals1 = getOptimumC((1.0 - s), o, p)
    
    if s != 1/2 and math.fabs(vals[1]) < math.fabs(vals1[1]):
        return [(1.0 - s), vals[1], vals[0]]
    else:
        return [s, vals1[1], vals1[0]]


@cython.ccall
def pluck(start, dur, freq, amp, weighting=.5, lossfact=.9):
    vals = tuneIt(freq, weighting)
    wt0 = vals[0]
    c = vals[1]
    dlen = vals[2]
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start + dur)
    lf = 1.0 if (lossfact == 0.0) else min(1.0, lossfact)
    wt = .5 if (wt0 == 0.0) else min(1.0, wt0)
    tab: np.ndarray  = np.zeros(dlen, dtype=np.double)
    allp = clm.make_one_zero(lf * (1.0 - wt), (lf * wt))
    feedb = clm.make_one_zero(c, 1.0)
    c1: cython.double = 1.0 - c
    
    k: cython.long = 0
    
    for k in range(0,dlen):
        tab[k] = clm.random(1.0) # could replace with python random
        
    ctr: cython.long = 0

    i: cython.long = 0
    val: cython.double = 0.
    
    for i in range(beg, end):
        ctr = (ctr + 1) % dlen
        val = (c1 * (clm.one_zero(feedb, clm.one_zero(allp, tab[ctr]))))
        tab[ctr] = val
        clm.outa(i, amp * val)
