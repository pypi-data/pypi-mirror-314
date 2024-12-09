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

# --------------- nrev ---------------- #
# ;;; NREV (the most popular Samson box reverb)
# 
#   ;; reverb-factor controls the length of the decay -- it should not exceed (/ 1.0 .823)
#   ;; lp-coeff controls the strength of the low pass filter inserted in the feedback loop
#   ;; output-scale can be used to boost the reverb output
@cython.ccall
def is_even(n):
    return bool(n%2==0)

@cython.ccall
def next_prime(n):
    np=[]
    isprime=[]
    for i in range (n+1,n+200):
        np.append(i)
    for j in np:
        val_is_prime = True
        for x in range(2,j-1):
            if j % x == 0:
                val_is_prime = False
                break
        if val_is_prime:
            isprime.append(j)
    return min(isprime)

@clm.clm_reverb
def nrev(reverb_factor=1.09, lp_coeff=.7, volume=1.0, decay_time=1.):
    srscale = clm.get_srate() / 25641
    dly_len = [1433,1601,1867,2053,2251,2399,347,113,37,59,53,43,37,29,19] # TODO: Make this adjust to samplerate

    chans = clm.get_channels(clm.default.output)
    chan2 = chans > 1
    chan4 = chans == 4
    
    for i in range(0,15):
        val = math.floor(srscale * dly_len[i])
        if is_even(val):
            val += 1
        dly_len[i] = next_prime(val)
        
    length: cython.long = math.floor(clm.get_length(clm.default.reverb) + (clm.get_srate()*decay_time))
    comb1 = clm.make_comb(.822 * reverb_factor, dly_len[0])
    comb2 = clm.make_comb(.802 * reverb_factor, dly_len[1])
    comb3 = clm.make_comb(.733 * reverb_factor, dly_len[2])
    comb4 = clm.make_comb(.753 * reverb_factor, dly_len[3])
    comb5 = clm.make_comb(.753 * reverb_factor, dly_len[4])
    comb6 = clm.make_comb(.733 * reverb_factor, dly_len[5])
    low = clm.make_one_pole(lp_coeff, lp_coeff - 1.0)
    allpass1 = clm.make_all_pass(-.7000, .700, dly_len[6])
    allpass2 = clm.make_all_pass(-.7000, .700, dly_len[7])
    allpass3 = clm.make_all_pass(-.7000, .700, dly_len[8])
    allpass4 = clm.make_all_pass(-.7000, .700, dly_len[9])
    allpass5 = clm.make_all_pass(-.7000, .700, dly_len[11])
    allpass6 = clm.make_all_pass(-.7000, .700, dly_len[12]) if chan2 else None
    allpass7 = clm.make_all_pass(-.7000, .700, dly_len[13]) if chan4 else None
    allpass8 = clm.make_all_pass(-.7000, .700, dly_len[14]) if chan4 else None
    
    filts = []

    if not chan2:
        filts.append(allpass5)
    else:
        if not chan4:
            filts.extend([allpass5, allpass6])
        else:
            filts.extend([allpass5, allpass6, allpass7, allpass8])

    combs: clm.mus_any = clm.make_comb_bank([comb1, comb2, comb3, comb4, comb5, comb6])
    allpasses = clm.make_all_pass_bank([allpass1, allpass2, allpass3])
    
    i: cython.long = 0
    
    for i in range(length):
        clm.out_bank(filts, i, clm.all_pass(allpass4, clm.one_pole(low, clm.all_pass_bank(allpasses, clm.comb_bank(combs, volume * clm.ina(i, clm.default.reverb))))))
    
    
