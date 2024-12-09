#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.generators as gens
if cython.compiled:
    from cython.cimports.pysndlib import clm
    from cython.cimports.pysndlib import generators as gens

# from generators.scm 
# uses rcos and rkoddssb generators

# --------------- stringy ---------------- #
@cython.ccall
def stringy(beg, dur, freq, amp):
    n: cython.double = math.floor(clm.get_srate() / (3 * freq))
    start: cython.long = clm.seconds2samples(beg)
    stop: cython.long = clm.seconds2samples(beg+dur)
    r: cython.double = pow(.001,1/n)
    carrier = gens.make_rcos(freq, .5*r)
    clang = gens.make_rkoddssb(freq * 2, 1.618 / 2, r)
    ampf = clm.make_env([0,0,1,1,2,.5,4,.25,10,0], scaler=amp, duration=dur)
    clangf = clm.make_env([0,0,.1,1,.2,.1,.3,0], scaler=amp*.5, duration=.1)
    rf = clm.make_env([0,1,1,0], scaler=.5*r, duration=dur)
    crf = clm.make_env([0,1,1,0], scaler=r, duration=.1)
    i: cython.long = 0
    for i in range(start,stop):
        clang.mus_scaler = clm.env(crf)
        carrier.r: cython.double = clm.env(rf)
        clm.outa(i, (clm.env(clangf) * gens.rkoddssb(clang, 0.0) + (clm.env(ampf)*gens.rcos(carrier, 0.))))
        
                    
if __name__ == '__main__':  
    with clm.Sound(play=True, statistics=True):
        stringy(0, 1, 1000, .5)       
        for i in range(1, 11):
            stringy(i*.3, .3, 200+(100*i), .5)    

