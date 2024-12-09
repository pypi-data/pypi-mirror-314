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
# uses nkssb generator


# --------------- nkssber ---------------- #
@cython.ccall
def nkssber(beg, dur, freq, mfreq, n, vibfreq, amp):
    start: cython.long = clm.seconds2samples(beg)
    stop: cython.long = clm.seconds2samples(beg + dur)
    gen = gens.make_nkssb(freq, (mfreq / freq), n)
    move = clm.make_env([0,1,1,-1], duration=dur)
    vib = clm.make_polywave(vibfreq, [1,clm.hz2radians((freq / mfreq) * 5.)], clm.Polynomial.SECOND_KIND)
    ampf = clm.make_env([0,0,1,1,5,1,6,0], scaler=amp, duration=dur)
    i: cython.long = 0
    for i in range(start, stop):
        clm.outa(i, clm.env(ampf) * gens.nkssb_interp(gen, clm.polywave(vib), clm.env(move)))

if __name__ == '__main__':  
    with clm.Sound(play=True, statistics=True, scaled_to=.5):
        nkssber(0,1,1000,100,5,5,.5)
        nkssber(1,2,600,100,4,1,.5)
        nkssber(3,2,1000,540,3,3,.5)
        nkssber(5,4,300,120,2,.25,.5)
        nkssber(9,1,30,4,40,.5,.5)
        nkssber(10,1,20,6,80,.5,.5)
