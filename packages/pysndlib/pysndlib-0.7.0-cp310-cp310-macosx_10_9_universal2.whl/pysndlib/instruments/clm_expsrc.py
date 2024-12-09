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



# --------------- clm_expsrc ---------------- #

def clm_expsrc(beg, dur, input_file, exp_ratio, src_ratio, amp: cython.double, rev=False, start_in_file=False):
    stf = math.floor((start_in_file or 0)*clm.get_srate(input_file))
    two_chans = clm.get_channels(input_file) == 2 and clm.get_channels(clm.default.output) == 2
    revit = clm.default.reverb and rev
    st: cython.long = clm.seconds2samples(beg)
    exA = clm.make_granulate(clm.make_readin(input_file, chan=0, start=stf), expansion=exp_ratio)
    if two_chans:
        exB = clm.make_granulate(clm.make_readin(input_file, chan=1, start=stf), expansion=exp_ratio)
    srcA = clm.make_src(lambda d : clm.granulate(exA), srate=src_ratio)
    
    rev_amp: cython.double = 0
    
    if two_chans:
        srcB: clm.mus_any = clm.make_src(lambda d : clm.granulate(exB),srate=src_ratio)
        
    if revit:
        if two_chans:
            rev_amp = rev * .5
        else:
            rev_amp = rev 
    else:
        rev_amp = 0.0
        
    nd: cython.long = clm.seconds2samples(beg + dur)
    
    if revit:
        
        valA: cython.double = 0.0
        valB: cython.double = 0.0
        
        if two_chans:
            for i in range(st, nd):
                valA = amp * clm.src(srcA)
                valB = amp * clm.src(srcB)
                clm.outa(i, valA)
                clm.outb(i, valB)
                clm.outa(i, rev_amp * (valA + valB), clm.default.reverb)
        else:
            
            for i in range(st, nd):
                valA = amp * clm.src(srcA)
                clm.outa(i, valA)
                clm.outb(i, rev_amp * valA, clm.default.reverb)
    else:
        if two_chans:
            for i in range(st, nd):
                clm.outa(i, amp*clm.src(srcA))
                clm.outb(i, amp*clm.src(srcB))
        else:
            for i in range(st, nd):
                clm.outa(i, amp * clm.src(srcA))

if __name__ == '__main__': 
    with clm.Sound(play=True,statistics=True):
        clm_expsrc(0, 2.5, '../examples/oboe.snd', 2.0, 1.0, 1.0)
