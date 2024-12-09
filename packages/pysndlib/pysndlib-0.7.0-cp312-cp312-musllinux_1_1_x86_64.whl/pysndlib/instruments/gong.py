#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.env as env
if cython.compiled:
    from cython.cimports.pysndlib import clm

# --------------- gong ---------------- #
# ;;; Paul Weineke's gong.
@cython.ccall
def gong(start_time, duration, frequency, amplitude, degree=0.0, distance=1.0, reverb_amount=.005):
    mfq1 = frequency * 1.16
    mfq2 = frequency * 3.14
    mfq3 = frequency * 1.005    
    indx01 = clm.hz2radians(.01 * mfq1)
    indx11 = clm.hz2radians(.30 * mfq1)
    indx02 = clm.hz2radians(.01 * mfq2)
    indx12 = clm.hz2radians(.38 * mfq2)
    indx03 = clm.hz2radians(.01 * mfq3)
    indx13 = clm.hz2radians(.50 * mfq3)
    atpt = 5
    atdur = 100 * (.002 / duration)
    expf = [0,0,3,1,15,.5,27,.25,50,.1,100,0]
    rise = [0,0,15,.3,30,1.0,75,.5,100,0]
    fmup = [0,0,75,1.0,98,1.0,100,0]
    fmdwn = [0,0,2,1.0,100,0]
    ampfun = clm.make_env(env.stretch_envelope(expf, atpt, atdur, None, None), scaler=amplitude, duration=duration)
    indxfun1 = clm.make_env(fmup, duration=duration, scaler=indx11-indx01, offset=indx01)
    indxfun2 = clm.make_env(fmup, duration=duration, scaler=indx12-indx02, offset=indx02)
    indxfun3 = clm.make_env(fmup, duration=duration, scaler=indx13-indx03, offset=indx03)
    loc = clm.make_locsig(degree, distance, reverb_amount)
    carrier = clm.make_oscil(frequency)
    mod1 = clm.make_oscil(mfq1)
    mod2 = clm.make_oscil(mfq2)
    mod3 = clm.make_oscil(mfq3)
    beg: cython.long = clm.seconds2samples(start_time)
    end: cython.long = clm.seconds2samples(start_time + duration)
    
    i: cython.long = 0
    
    for i in range(beg, end):
        clm.locsig(loc, i, clm.env(ampfun) * clm.oscil(carrier, (clm.env(indxfun1) * clm.oscil(mod1)) + (clm.env(indxfun2) * clm.oscil(mod2)) + (clm.env(indxfun3) * clm.oscil(mod3))))
    
if __name__ == '__main__':     
    with clm.Sound(play=True, statistics=True):
        gong(0, 3, 261.61, .6)
    
