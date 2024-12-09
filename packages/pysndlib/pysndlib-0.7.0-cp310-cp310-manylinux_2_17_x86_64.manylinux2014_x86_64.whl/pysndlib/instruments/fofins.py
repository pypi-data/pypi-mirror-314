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

# --------------- fof ---------------- #

@cython.ccall
def fofins(beg, dur, frq, amp, vib, f0, a0, f1, a1, f2, a2, ae=[0, 0, 25, 1, 75, 1, 100,0], ve=[0,1,100,1]):
    foflen = math.floor(clm.get_srate() / 220.5)
    start: cython.long = clm.seconds2samples(beg)
    end: cython.long = clm.seconds2samples(beg + dur)
    ampf= clm.make_env(ae, scaler=amp, duration=dur)
    vibf = clm.make_env(ve, scaler=vib, duration=dur)
    frq0 = clm.hz2radians(f0)
    frq1 = clm.hz2radians(f1)
    frq2 = clm.hz2radians(f2)
    vibr = clm.make_oscil(0)
    foftab: np.ndarray = np.zeros(foflen)
    win_freq = ((2.0 * math.pi) / foflen)
    
    k: cython.long = 0

    for k in range(foflen):
        v = (a0 * math.sin(k * frq0)) + (a1 * math.sin(k * frq1)) + (a2 * math.sin(k * frq2))
        foftab[k] = v * .5 * (1.0 - math.cos(k * win_freq))
    wt0 = clm.make_wave_train(frq, foftab)
    
    i: cython.long = 0
    
    for i in range(start, end):
        clm.outa(i, clm.env(ampf) * clm.wave_train(wt0, (clm.env(vibf) * clm.oscil(vibr))))


if __name__ == '__main__': 
    with clm.Sound( play = True ):
        fofins(0,4,270,.2,0.005,730,.6,1090,.3,2440,.1,[0,0,40,0,75,.2,100,1],
                [0,0,.5,1,3,.5,10,.2,20,.1,50,.1,60,.2,85,1,100,0])
        fofins(0,4,(6/5 * 540),.2,0.005,730,.6,1090,.3,2440,.1,[0,0,40,0,75,.2,100,1],
                [0,0,.5,.5,3,.25,6,.1,10,.1,50,.1,60,.2,85,1,100,0])
        fofins(0,4,135,.2,0.005,730,.6,1090,.3,2440,.1,[0,0,40,0,75,.2,100,1],
                [0,0,1,3,3,1,6,.2,10,.1,50,.1,60,.2,85,1,100,0])
      
