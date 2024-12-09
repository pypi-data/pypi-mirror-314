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

# --------------- attract ---------------- #
#   ;; by James McCartney, from CMJ vol 21 no 3 p 6
@cython.ccall
def attract(beg, dur, amp, c):
    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    a: cython.double = .2
    b: cython.double = .2
    dt: cython.double = .04
    scale: cython.double = (.5 * amp) / c
    x: cython.double = -1.0
    y: cython.double = 0.0
    z: cython.double = 0.0
    x1: cython.double = 0.0
    
    i: cython.long = 0
    
    for i in range(st,nd):
        x1 = x - (dt * (y + z))
        y  += (dt * (x + (a * y)))
        z  += (dt * ((b + (x * z)) - (c * z)))
        x = x1
        clm.outa(i, scale * x)


if __name__ == '__main__': 
    with clm.Sound(play=True, statistics=True):
        attract(0, 2, .5, 4)
