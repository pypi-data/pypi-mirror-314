#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.env as env
if cython.compiled:
    from cython.cimports.pysndlib import clm

# --------------- cellon ---------------- #

@cython.ccall
def cellon(beg, dur, pitch0, amp, ampfun, betafun, beta0, beta1, betaat, betadc, ampat, ampdc, dis, pcrev, deg,
            pitch1, glissfun, glissat, glissdc, pvibfreq, pvibpc, pvibfun=[0,1,100,1], pvibat=0, pvibdc=0, rvibfreq=0, rvibpc=0, rvibfun=[0,1,100,1]):
	
    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    pit1 = pitch0 if pitch1 == 0.0 else pitch1
    loc = clm.make_locsig(deg, dis, pcrev)
    carrier = clm.make_oscil(pitch0)
    low = clm.make_one_zero(.5, -.5)
    fm = 0.0
    fmosc = clm.make_oscil(pitch0)
    pvib = clm.make_triangle_wave(pvibfreq, 1.0)
    rvib = clm.make_rand_interp(rvibfreq, 1.0)
    ampap: cython.double = (100 * (ampat / dur)) if ampat > 0.0 else 25
    ampdp: cython.double = (100 * (1.0 - (ampdc / dur))) if ampdc > 0.0 else 75
    glsap: cython.double = (100 * (glissat / dur)) if glissat > 0.0 else 25
    glsdp: cython.double = (100 * (1.0 - (glissdc / dur))) if glissdc > 0.0 else 75
    betap: cython.double = (100 * (betaat / dur)) if betaat > 0.0 else 25
    betdp: cython.double = (100 * (1.0 - (betadc / dur))) if betadc > 0.0 else 75
    pvbap: cython.double = (100 * (pvibat / dur)) if pvibat > 0.0 else 25
    pvbdp: cython.double = (100 * (1.0 - (pvibdc / dur))) if pvibdc > 0.0 else 75
    
    pvibenv = clm.make_env(env.stretch_envelope(pvibfun, 25, pvbap, 75, pvbdp), duration=dur, scaler=clm.hz2radians(pvibpc * pitch0))
    rvibenv = clm.make_env(rvibfun, duration=dur, scaler=clm.hz2radians(rvibpc * pitch0))
    glisenv = clm.make_env(env.stretch_envelope(pvibfun, 25, pvbap, 75, pvbdp), duration=dur, scaler=clm.hz2radians(pvibpc * pitch0))
    amplenv = clm.make_env(env.stretch_envelope(ampfun, 25, ampap, 75, ampdp), scaler=amp, duration=dur)
    betaenv = clm.make_env(env.stretch_envelope(betafun, 25, betap, 75, betdp), duration=dur, scaler=(beta1 - beta0), offset=beta0)
    
    i: cython.long = 0
    fm: cython.double = 0.0
    vib: cython.double = 0.0
    if (pitch0 == pitch1) and (clm.is_zero(pvibfreq) or clm.is_zero(pvibpc)) and (clm.is_zero(rvibfreq) or clm.is_zero(rvibpc)):
        for i in range(st, nd):
            fm = clm.one_zero(low, clm.env(betaenv) * clm.oscil(fmosc, fm))
            clm.locsig(loc, i, clm.env(amplenv)*clm.oscil(carrier,fm))
    else:
        for i in range(st, nd):
            vib = (clm.env(pvibenv)*clm.triangle_wave(pvib)) + (clm.env(rvibenv)*clm.rand_interp(rvib)) + clm.env(glisenv)
            fm = clm.one_zero(low, clm.env(betaenv) * clm.oscil(fmosc, (fm+vib)))
            clm.locsig(loc, i, clm.env(amplenv)*clm.oscil(carrier,fm+vib))


if __name__ == '__main__': 
    with clm.Sound( play = True, statistics=True):
        cellon(0,1,220,.1,[0,0,25,1,75,1,100,0],[0,0,25,1,75,1,100,0],.75,1.0,0,0,0,0,1,0,0,220,[0,0,25,1,75,1,100,0],0,0,0,0,[0,0,100,0],0,0,0,0,[0,0,100,0])  
