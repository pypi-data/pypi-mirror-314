import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.generators as gens
if cython.compiled:
    from cython.cimports.pysndlib import clm
    from cython.cimports.pysndlib import generators as gens

# uses nrcos generator


# --------------- lutish ---------------- #
@cython.ccall
def lutish(beg, dur, freq, amp):
    res1: cython.double = max(1, round(1000.0 / max(1.0, min(1000., freq))))
    maxind: cython.double = max(.01, min(.3, ((math.log(freq) - 3.5) / 8.0)))
    gen = gens.make_nrcos(frequency=freq*res1,n=max(1, (res1 - 2)))
    mod = clm.make_oscil(freq)
    start: cython.long = clm.seconds2samples(beg)
    stop: cython.long = clm.seconds2samples(beg + dur)
    indx = clm.make_env([0,maxind, 1, maxind*.25, max(dur, 2.0), 0.0], duration=dur)
    amplitude = clm.make_env([0,0,.01,1,.2,1,.5,.5,1,.25, max(dur, 2.0), 0.0], duration=dur, scaler =amp)
    i: cython.long = 0
    for i in range(start, stop):
        ind: cython.double = clm.env(indx)
        gen.mus_scaler = ind
        clm.outa(i, clm.env(amplitude) * gens.nrcos(gen, (ind * clm.oscil(mod))))



if __name__ == '__main__':   
    with clm.Sound(clipped=False, statistics=True, play=True):
        for i in range(10):
            lutish(i*.1, 2, (100 * (i+1)), .05)
