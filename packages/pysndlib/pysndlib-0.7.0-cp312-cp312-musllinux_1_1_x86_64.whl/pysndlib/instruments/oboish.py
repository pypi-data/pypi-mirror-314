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
# uses nrssb generator


# --------------- oboish ---------------- #
@cython.ccall
def oboish(beg, dur, freq, amp, aenv):
    res1: cython.double = max(1, round(1400.0 / max(1.0, min(1400.0, freq))))
    mod1 = clm.make_oscil(5.)
    res2: cython.double = max(1, round(2400.0 / max(1.0, min(2400.0, freq))))
    gen3 = clm.make_oscil(freq)
    start: cython.long = clm.seconds2samples(beg)
    amplitude = clm.make_env(aenv, duration=dur, base=4, scaler=amp)
    skenv = clm.make_env([0.0,0.0,1,1,2.0,clm.random(1.), 3.0, 0.0, max(4.0, dur*20.0), 0.0], duration=dur, scaler=clm.hz2radians(random.uniform(0.,freq*.05)))
    relamp: cython.double = .85 + random.uniform(0, .1)
    avib = clm.make_rand_interp(5, .2)
    hfreq = clm.hz2radians(freq)
    h3freq = clm.hz2radians(.003 * freq)
    
    scl: cython.double = .05 / amp
    gen = gens.make_nrssb(frequency=freq*res1, ratio=1/res1, n=res1, r=.75)
    gen2 = clm.make_oscil(freq*res2)
    stop: cython.long = start + clm.seconds2samples(dur)
    i: cython.long = 0
    for i in range(start, stop):
        vol: cython.double = (.8 + clm.rand_interp(avib)) * clm.env(amplitude)
        vola: cython.double = scl * vol
        vib: cython.double = (h3freq * clm.oscil(mod1)) + clm.env(skenv)
        result: cython.double = vol * (((relamp - vola) * gens.nrssb_interp(gen, (res1*vib), -1.0)) +
                         (((1 + vola) - relamp)  * clm.oscil(gen2, ((vib*res2)+(hfreq*clm.oscil(gen3, vib))))))
        clm.outa(i, result)
        if clm.default.reverb :
            clm.outa(i, (.01*result), clm.default.reverb)
