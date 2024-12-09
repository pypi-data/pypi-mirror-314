#==================================================================================
# The code is ported from Bill Schottstedaet's 'generators.scm' 
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
# uses nrssb generator

# --------------- organish ---------------- #
@cython.ccall
def organish(beg, dur, freq, amp, fm_index, amp_env=None):
    start: cython.long = clm.seconds2samples(beg)
    i: cython.long = 0
    carriers = [None] * 3
    fmoscs = [None] * 3
    ampfs = [None] * 3
    pervib = clm.make_triangle_wave(5, clm.hz2radians(freq * .003))
    ranvib = clm.make_rand_interp(6, clm.hz2radians(freq * .002))
    resc = gens.make_nrssb(340, 1.0, 5, .5)
    resf = clm.make_env([0,0,.05,1,.1,0,dur,0], scaler=(amp * .05), duration=dur)
    stop: cython.long = start + clm.seconds2samples(dur)
    for i in range(3):
        frq = freq * 2**i
        index1 = clm.hz2radians((fm_index * frq * 5.0) / math.log(frq))
        index2 = clm.hz2radians((fm_index * frq * 3.0 * (8.5 - math.log(frq)) / (3.0 + (frq * 0.001))))
        index3 = clm.hz2radians((fm_index * frq * 4.0) / math.sqrt(frq))
        carriers[i] = clm.make_oscil(frq)

        fmoscs[i] = clm.make_polywave(frq, partials=[1, index1, 3, index2, 4, index3])
    if not amp_env:
        amp_env = [0,0,1,1,2,1,3,0]
    ampfs[0] = clm.make_env(amp_env, scaler=amp, duration=dur)
    ampfs[1] = clm.make_env([0,0,.04,1,.075, 0,dur,0], scaler=amp*.0125, duration=dur)
    ampfs[2] = clm.make_env([0,0,.02,1,.05,0,dur,0], scaler=amp*.025, duration=dur)
    
    for i in range(start, stop):
        vib = clm.triangle_wave(pervib) + clm.rand_interp(ranvib)
        res: cython.double = 0.0
        res += clm.env(resf) * gens.nrssb(resc, 0.0)
        res += clm.oscil(carriers[0], (vib+clm.polywave(fmoscs[0], vib)))
        res += clm.env(ampfs[0]) * clm.oscil(carriers[0], ((vib*2)+clm.polywave(fmoscs[0], (vib*2))))
        res += clm.env(ampfs[1]) * clm.oscil(carriers[1], ((vib*4)+clm.polywave(fmoscs[1], (vib*4))))
        clm.outa(i, res)


if __name__ == '__main__': 
    with clm.Sound(play=True,statistics=True):
        for i in range(10):
            organish(i*.3, .4, (100 + (50 * i)), .5, 1.0, [0,0,1,1,2,.5,3,.25,4,.125,10,0])
