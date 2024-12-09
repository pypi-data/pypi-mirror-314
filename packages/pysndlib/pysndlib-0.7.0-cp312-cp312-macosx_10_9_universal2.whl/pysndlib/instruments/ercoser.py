#==================================================================================
# The code is ported from Bill Schottstedaet's 'generators.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
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
# uses ercos generators

# --------------- ercoser ---------------- #
@cython.ccall
def ercoser(start, dur, freq, amp, r):
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start + dur)
    gen = gens.make_ercos(freq, r)
    ampf = clm.make_env([0.0,0.0,.001, 1, .7, .5, 1.0, 0], duration=dur)
    t_env = clm.make_env([0,.1,1,2], duration=dur)
    
    for i in range(beg, end):
        r: cython.double  = clm.env(t_env)
        gen.cosh_t: cython.double = math.cosh(r)
        gen.osc.mus_data[0] = gen.cosh_t
        exp_t: cython.double = math.exp(-r)
        gen.offset = ((1.0 - exp_t) / (2.0 * exp_t))
        gen.scaler = (math.sinh(r) * gen.offset)
        clm.outa(i, amp*gens.ercos(gen)*clm.env(ampf))
#         
if __name__ == '__main__':          
    with clm.Sound(clipped=False, statistics=True, play=True):
        ercoser(0,1,100,.5,.1)  
        ercoser(.5,1,200,.5,.1)  
        ercoser(1,1,300,.5,.1)  
        ercoser(1.5,1,400,.5,.1)  
