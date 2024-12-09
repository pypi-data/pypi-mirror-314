import math
import random
#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.env as env
if cython.compiled:
    from cython.cimports.pysndlib import clm


# --------------- fm_drum ---------------- #
# ;;; Jan Mattox's fm drum:

@cython.ccall
def fm_drum(start_time, duration, frequency, amplitude, index, high=True, degree=0.0, distance=1.0, reverb_amount=.01):
    indxfun = [0,0,5,.014,10,.033,15,.061,20,.099,
            	25,.153,30,.228,35,.332,40,.477,
		        45,.681,50,.964,55,.681,60,.478,65,.332,
		        70,.228,75,.153,80,.099,85,.061,
		        90,.033,95,.0141,100,0]

    indxpt: cython.double = 100 - (100 * ((duration - .1) / duration))
    atdrpt: cython.double = 100 * ((.01 if high else .015) / duration)
    divindxf = env.stretch_envelope(indxfun, 50, atdrpt, 65, indxpt)
    ampfun = [0,0,3,.05,5,.2,7,.8,8,.95,10,1.0,12,.95,20,.3,30,.1,100,0]
    casrat: cython.double = 8.525 if high else 3.515    
    fmrat: cython.double = 3.414 if high else 1.414
    glsfun = [0,0,25,0,75,1,100,1]
    beg: cython.long = clm.seconds2samples(start_time)
    end: cython.long = clm.seconds2samples(start_time + duration)
    glsf = clm.make_env(glsfun, scaler=(clm.hz2radians(66) if high else 0.0), duration=duration)
    ampe = env.stretch_envelope(ampfun, 10, atdrpt, 15, max((atdrpt + 1), 100 - (100 * ((duration - .05) / duration))))
    ampf  = clm.make_env(ampe, scaler=amplitude, duration=duration)
    indxf  = clm.make_env(divindxf, scaler=min(clm.hz2radians(index * fmrat * frequency), math.pi), duration=duration)
    mindxf  = clm.make_env(divindxf, scaler=min(clm.hz2radians(index * casrat * frequency), math.pi), duration=duration)
    deve = env.stretch_envelope(ampfun, 10, atdrpt, 90, max((atdrpt + 1), (100 - (100 * ((duration - .05) / duration)))))
    devf  = clm.make_env(deve, scaler=min(math.pi, clm.hz2radians(7000)), duration=duration)
    loc  = clm.make_locsig(degree, distance, reverb_amount)
    rn  = clm.make_rand(7000., 1.0)
    carrier  = clm.make_oscil(frequency)
    fmosc  = clm.make_oscil(frequency*fmrat)
    cascade = clm.make_oscil(frequency*casrat)
    
    i: cython.long = 0
    gls: cython.double = 0.0
    
    for i in range(beg, end):
        gls = clm.env(glsf)
        clm.locsig(loc, i, (clm.env(ampf) * clm.oscil(carrier, (gls + (clm.env(indxf) * 
                                        clm.oscil(fmosc, ((gls*fmrat)+(clm.env(mindxf)*
                                            clm.oscil(cascade, ((gls*casrat)+(clm.env(devf)*clm.rand(rn))))))))))))
if __name__ == '__main__':  
    with clm.Sound(play=True, statistics=True):
        fm_drum(0, 1.5, 55, .3, 5, False)
        fm_drum(2, 1.5, 66, .3, 5, True)
