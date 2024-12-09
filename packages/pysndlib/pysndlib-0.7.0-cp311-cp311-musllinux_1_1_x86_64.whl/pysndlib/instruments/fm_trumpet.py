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

# --------------- fm_trumpet ---------------- #

# ;;; Dexter Morrill's FM-trumpet:
# ;;; from CMJ feb 77 p51

@cython.ccall
def fm_trumpet(startime, dur, frq1=250, frq2=1500, amp1=.5, amp2=.1, 
    ampatt1=.03, ampdec1=.35,
    ampatt2=.03, ampdec2=.3,
    modfrq1=250,
    modind11=0.0,
    modind12=2.66,
    modfrq2=250.,
    modind21=0.0,
    modind22=1.8,
    rvibamp=.007,
    rvibfrq=125.0,
    vibamp=.007,
    vibfrq=7.0,
    vibatt=.6,
    vibdec=.2,
    frqskw=.03,
    frqatt=.06,
    ampenv1=[0,0,25,1,75,.9,100,0],
    ampenv2=[0,0,25,1,75,.9,100,0],
    indenv1=[0,0,25,1,75,.9,100,0],
    indenv2=[0,0,25,1,75,.9,100,0],
    degree=0.0,
    distance=1.0,
    reverb_amount=.005):
    
    dec_01 = max(75, (100 * (1.0 - (.01 / dur))))
    beg: cython.long = clm.seconds2samples(startime)
    end: cython.long = clm.seconds2samples(startime + dur)
    loc = clm.make_locsig(degree, distance, reverb_amount)
    vibe = env.stretch_envelope([0,1,25,.1, 75, 0, 100, 0], 25, min((100 * (vibatt / dur)), 45), 75, max((100 * (1.0 - (vibdec / dur)), 55)))

    per_vib_f = clm.make_env(vibe, scaler=vibamp, duration=dur)
    ran_vib = clm.make_rand_interp(rvibfrq, rvibamp)
    per_vib = clm.make_oscil(vibfrq)
    frqe = env.stretch_envelope([0,0,25,1,75,1,100,0], 25, min(25, (100 * (frqatt / dur))), 75, dec_01)
    frq_f = clm.make_env(frqe, scaler=frqskw, offset=1.0, duration=dur)
    ampattpt1 = min(25, (100 * (ampatt1 / dur)))
    ampdecpt1 = max(75, (100 * (1.0 - (ampdec1 / dur))))
    ampattpt2 = min(25, (100 * (ampatt2 / dur)))
    ampdecpt2 = max(75, (100 * (1.0 - (ampdec2 / dur))))
    
    mod1_f = clm.make_env(env.stretch_envelope(indenv1, 25, ampattpt1, 75, dec_01), scaler=(modfrq1 * (modind12 - modind11)), duration=dur)
    mod1 = clm.make_oscil(0.0)
    car1 = clm.make_oscil(0.0)
    car1_f = clm.make_env(env.stretch_envelope(ampenv1, 25, ampattpt1, 75, ampdecpt1), scaler=amp1, duration=dur)
    
    mod2_f = clm.make_env(env.stretch_envelope(indenv2, 25, ampattpt2, 75, dec_01), scaler=(modfrq2 * (modind22 - modind21)), duration=dur)

    mod2 = clm.make_oscil(0.0)
    car2 = clm.make_oscil(0.0)
    car2_f = clm.make_env(env.stretch_envelope(ampenv2, 25, ampattpt2, 75, ampdecpt2), scaler=amp2, duration=dur)
    
    i: cython.long = 0
    frq_change: cython.double = 0.0
    
    for i in range(beg, end):
        frq_change = clm.hz2radians((1.0 + clm.rand_interp(ran_vib)) * 
                            (1.0 + (clm.env(per_vib_f) * clm.oscil(per_vib))) *
                            clm.env(frq_f))
                            
                            
        clm.locsig(loc, i, clm.env(car1_f) * clm.oscil(car1, frq_change * (frq1 + clm.env(mod1_f) * clm.oscil(mod1, modfrq1 * frq_change))) +
                        clm.env(car2_f) * clm.oscil(car2, frq_change * (frq2 + clm.env(mod2_f) * clm.oscil(mod2, modfrq2 * frq_change))))
if __name__ == '__main__': 
    with clm.Sound(play=True, statistics=True):
        fm_trumpet(0, 3, 250, 1500, .5, .1, degree=45)
        fm_trumpet(2.9, 3, 350, 1500, .5, .1, degree=45)    

