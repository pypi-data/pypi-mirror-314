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

# --------------- resflt ---------------- #
@cython.ccall
def resflt(start, dur, driver, ranfreq, noiamp, noifun, cosamp, cosfreq1, cosfreq0, cosnum, 
                ampcosfun, freqcosfun, frq1, r1, g1, frq2, r2, g2, frq3, r3, g3, 
                degree=0.0,distance=1.0,reverb_amount=0.005):
   
    with_noise = driver == 1
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(dur) + beg
    f1 = clm.make_two_pole(frq1, r1) # fix when these have kw args
    f2 = clm.make_two_pole(frq2, r2)
    f3 = clm.make_two_pole(frq3, r3)
    loc = clm.make_locsig(degree, distance, reverb_amount)

    if with_noise:
        ampf = clm.make_env(noifun, scaler=noiamp, duration=dur)
        rn = clm.make_rand(frequency=ranfreq)
    else:
        frqf = clm.make_env(freqcosfun, duration=dur, scaler=clm.hz2radians(cosfreq1 - cosfreq0))             
        cn = clm.make_ncos(cosfreq0, cosnum)
        ampf = clm.make_env(ampcosfun, scaler=cosamp, duration=dur)
        
    f1.mus_xcoeffs[0] = g1
    f2.mus_xcoeffs[0] = g2
    f3.mus_xcoeffs[0] = g3
    
    i: cython.long = 0
    input1: cython.double = 0.0
    
    if with_noise:
        for i in range(beg, end):   
            input1 = clm.env(ampf) * clm.rand(rn)
            clm.locsig(loc, i, clm.two_pole(f1, input1) + clm.two_pole(f2, input1) + clm.two_pole(f3, input1))
    else:
        for i in range(beg, end):   
            input1 = clm.env(ampf) * clm.ncos(cn, clm.env(frqf))
            clm.locsig(loc, i, clm.two_pole(f1, input1) + clm.two_pole(f2, input1) + clm.two_pole(f3, input1))

if __name__ == '__main__':          
    with clm.Sound( play = True, statistics=True):
        resflt(0,1.0,0,0,0,False,.1,200,230,10,[0,0,50,1,100,0],[0,0,100,1],500,.995,.1,1000,.995,.1,2000,.995,.1)  


