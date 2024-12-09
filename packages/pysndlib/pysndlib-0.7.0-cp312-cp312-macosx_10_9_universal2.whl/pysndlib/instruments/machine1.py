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
# uses fmssb generator

# --------------- machine1 ---------------- #
@cython.ccall
def machine1(start, dur, cfreq, mfreq, amp, index, gliss):
    gen = gens.make_fmssb(cfreq, mfreq/cfreq, index=1.)
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start+dur)
    ampf = clm.make_env([0,0,1,.75,2,1,3,.1,4,.7,5,1,6,.8,100,0], base=32, scaler=amp, duration=dur)
    indf = clm.make_env([0,0,1,1,3,0], duration=dur, base=32, scaler=index)
    frqf = clm.make_env([0,0,1,1] if gliss > 0.0 else [0,1,1,0], duration=dur, scaler=clm.hz2radians((cfreq/mfreq) * math.fabs(gliss)))
    i: cython.long = 0
    for i in range(beg, end):
        gen.index = clm.env(indf)
        clm.outa(i, clm.env(ampf) * gens.fmssb(gen, clm.env(frqf)))


if __name__ == '__main__': 
    with clm.Sound(play=True,statistics=True):
        for i in np.arange(0.0, 2.0, .5):        
            machine1(i, .3, 100, 540, 0.5, 3.0, 0.0)
            machine1(i,.1,100,1200,.5,10.0,200.0)
            machine1(i,.3,100,50,.75,10.0,0.0)
            machine1(i + .1, .1,100,1200,.5,20.0,1200.0)
            machine1(i + .3, .1,100,1200,.5,20.0,1200.0)
            machine1(i + .3, .1,100,200,.5,10.0,200.0)
            machine1(i + .36, .1,100,200,.5,10.0,200.0)
            machine1(i + .4, .1,400,300,.5,10.0,-900.0)
            machine1(i + .4, .21,100,50,.75,10.0,1000.0)

        for i in np.arange(3, 5, .2):
            machine1(i, .3, 100, 540, .5, 4.0, 0.)
            machine1(i+.1, .3, 200, 540, .5, 3.0, 0.0)

        for i in np.arange(5., 7., .6):
            machine1(i, .3, 1000, 540, .5, 6., 0.)
            machine1(i+.1, .1, 2000, 540, .5, 1.0, 0)
