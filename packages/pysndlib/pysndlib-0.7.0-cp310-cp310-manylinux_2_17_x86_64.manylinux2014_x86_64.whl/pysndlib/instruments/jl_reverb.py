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


# --------------- jl_reverb ---------------- #
@cython.ccall
@clm.reverb
def jl_reverb(decay_time: cython.double  =3.0, volume: cython.double =1.0):
    allpass1 = clm.make_all_pass(-.700, .700, 2111)
    allpass2 = clm.make_all_pass(-.700, .700, 673)
    allpass3 = clm.make_all_pass(-.700, .700, 223)
    comb1 = clm.make_comb(.742, 9601)
    comb2 = clm.make_comb(.733, 10007)
    comb3 = clm.make_comb(.715, 10799)
    comb4 = clm.make_comb(.697, 11597)
    outdel1 = clm.make_delay(clm.seconds2samples(.013))
    outdel2 = clm.make_delay(clm.seconds2samples(.011))
    length = math.floor((decay_time * clm.get_srate()) + clm.get_length(clm.default.reverb))
    filts = [outdel1, outdel2]
    combs = clm.make_comb_bank([comb1, comb2, comb3, comb4])
    allpasses = clm.make_all_pass_bank([allpass1, allpass2, allpass3])
    
    i: cython.long = 0
    
    for i in range(length):
        clm.out_bank(filts, i, volume * clm.comb_bank(combs, clm.all_pass_bank(allpasses, clm.ina(i, clm.default.reverb))))
        
