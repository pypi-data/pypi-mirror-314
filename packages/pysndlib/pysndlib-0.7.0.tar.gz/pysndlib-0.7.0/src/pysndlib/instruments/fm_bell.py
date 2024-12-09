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



# --------------- fm_bell ---------------- #
@cython.ccall
def fm_bell(startime, dur, frequency, amplitude, 
        amp_env=[0, 0, .1, 1, 10, .6, 25, .3, 50, .15, 90, .1, 100, 0], 
        index_env=[0, 1, 2, 1.1, 25, .75, 75, .5, 100, .2], index=1.):
    fmInd2: cython.double = clm.hz2radians( (8.0 - (frequency / 50.)) * 4)
    beg: cython.long = clm.seconds2samples(startime)
    end: cython.long = clm.seconds2samples(startime + dur)
    fmInd1: cython.double = clm.hz2radians(32.0 * frequency)
    fmInd3: cython.double = fmInd2 * .705 * (1.4 - (frequency / 250.))
    fmInd4: cython.double = clm.hz2radians(32.0 * (20  - (frequency / 20)))
    mod1 = clm.make_oscil(frequency * 2)
    mod2 = clm.make_oscil(frequency * 1.41)
    mod3 = clm.make_oscil(frequency * 2.82)
    mod4 = clm.make_oscil(frequency * 2.4)
    car1 = clm.make_oscil(frequency)
    car2 = clm.make_oscil(frequency)
    car3 = clm.make_oscil(frequency * 2.4)
    indf = clm.make_env(index_env, scaler=index, duration=dur)
    ampf = clm.make_env(amp_env, scaler=amplitude, duration=dur)
    
    i: cython.long = 0
    fmenv: cython.double = 0.0
    
    for i in range(beg, end):
        fmenv = clm.env(indf)
        clm.outa(i, clm.env(ampf) * (clm.oscil(car1, fm=(fmenv * fmInd1 * clm.oscil(mod1))) +
                             (.15 * clm.oscil(car2, fm=(fmenv * ( (fmInd2 * clm.oscil(mod2)) + (fmInd3 * clm.oscil(mod3)) )))) +
                             (.15 * clm.oscil(car3, fm=(fmenv * fmInd4 * clm.oscil(mod4)))) ))
  
if __name__ == '__main__':                             
    with clm.Sound( play = True, statistics=True, channels=1 ):
        fbell = [0,1,2,1.1,25,.75,75,.5,100,.2]
        abell = [0,0,.1,1,10,.6,25,.3,50,.15,90,.1,100,0]
        fm_bell( 0,5.000,233.046,.028,abell,fbell,.750)
        fm_bell( 5.912,2.000,205.641,.019,abell,fbell,.650)
        fm_bell( 6.085,5.000,207.152,.017,abell,fbell,.750)
        fm_bell( 6.785,7.000,205.641,.010,abell,fbell,.650)
        fm_bell( 15.000,.500,880,.060,abell,fbell,.500)
        fm_bell( 15.006,6.500,293.66,.1,abell,fbell,0.500)
        fm_bell( 15.007,7.000,146.5,.1,abell,fbell,1.000)
        fm_bell( 15.008,6.000,110,.1,abell,fbell,1.000)
        fm_bell( 15.010,10.00,73.415,.028,abell,fbell,0.500)
        fm_bell( 15.014,4.000,698.46,.068,abell,fbell,0.500)
        
