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
# uses rkoddssb!cos generator

# --------------- glassy ---------------- #
@cython.ccall
def glassy(beg, dur, freq, amp, r=.5):
    r: cython.double = .001**(1.0 / math.floor(clm.get_srate() / (3 * freq)))
    start: cython.long = clm.seconds2samples(beg)
    stop: cython.int  = clm.seconds2samples(beg+dur)
    clang = gens.make_rkoddssb(freq * 2, 1.618 / 2, r)
    clangf = clm.make_env([0,0,.01,1,.1,1,.2,.4,max(.3,dur),0], scaler=amp, duration=dur)
    crf = clm.make_env([0,1,1,0], scaler=r, duration=dur)
    i: cython.long = 0
    for i in range(start, stop):
        clang.r = clm.env(crf)
        clm.outa(i, clm.env(clangf) * gens.rkoddssb(clang, 0.))


if __name__ == '__main__': 
    with clm.Sound(clipped=False, statistics=True, play=True):
        for i in range(10):
            glassy(i*.3, .1, 400. + (100. * i), .5)
