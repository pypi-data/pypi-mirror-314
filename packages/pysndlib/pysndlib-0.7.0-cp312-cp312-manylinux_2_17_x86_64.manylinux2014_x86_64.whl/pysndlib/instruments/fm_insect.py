import math
import random
import cython
#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import numpy as np
import pysndlib.clm as clm
if cython.compiled:
    from cython.cimports.pysndlib import clm
# --------------- fm_insect ---------------- #
@cython.ccall
def fm_insect(startime, dur, frequency, 
                amplitude, 
                amp_env, 
                mod_freq, 
                mod_skew, 
                mod_freq_env, 
                mod_index, 
                mod_index_env, 
                fm_index, 
                fm_ratio, 
                degree=0.0, 
                distance=1.0,
                reverb_amount=.005):
                
    beg: cython.long = clm.seconds2samples(startime)
    end:cython.long  = clm.seconds2samples(startime + dur)
    loc = clm.make_locsig(degree, distance, reverb_amount)
    carrier = clm.make_oscil(frequency)
    fm1_osc = clm.make_oscil(mod_freq)
    fm2_osc = clm.make_oscil((fm_ratio * frequency))
    ampf = clm.make_env(amp_env, scaler=amplitude, duration=dur)
    indf = clm.make_env(mod_index_env, scaler=clm.hz2radians(mod_index), duration=dur)
    modfrqf = clm.make_env(mod_freq_env, scaler=clm.hz2radians(mod_skew), duration=dur)
    fm2_amp: cython.double = clm.hz2radians(fm_index * fm_ratio * frequency)
    
    i: cython.long = 0
    garble_in: cython.double = 0.
    
    for i in range(beg, end):
        garble_in = (clm.env(modfrqf) * clm.oscil(fm1_osc, clm.env(modfrqf)))
        clm.locsig(loc, i, (clm.env(ampf) * clm.oscil(carrier, (fm2_amp * clm.oscil(fm2_osc, garble_in)) + garble_in)))
        
        
if __name__ == '__main__': 
    LOCUST = [0,0,40,1,95,1,100,.5]
    BUG_HI = [0,1,25,.7,75,.78,100,1]
    AMP = [0,0,25,1,75,.7,100,0]

    with clm.Sound(play=True, statistics=True, channels=1):
        fm_insect(0,1.699,4142.627,.015,AMP,60,-16.707,LOCUST,500.866,BUG_HI,.346,.500)
        fm_insect(0.195,.233,4126.284,.030,AMP,60,-12.142,LOCUST,649.490,BUG_HI,.407,.500)
        fm_insect(0.217,2.057,3930.258,.045,AMP,60,-3.011,LOCUST,562.087,BUG_HI,.591,.500)
        fm_insect(2.100,1.500,900.627,.06,AMP,40,-16.707,LOCUST,300.866,BUG_HI,.346,.500)
        fm_insect(3.000,1.500,900.627,.06,AMP,40,-16.707,LOCUST,300.866,BUG_HI,.046,.500)
        fm_insect(3.450,1.500,900.627,.09,AMP,40,-16.707,LOCUST,300.866,BUG_HI,.006,.500)
        fm_insect(3.950,1.500,900.627,.12,AMP,40,-10.707,LOCUST,300.866,BUG_HI,.346,.500)
        fm_insect(4.300,1.500,900.627,.09,AMP,40,-20.707,LOCUST,300.866,BUG_HI,.246,.500)
