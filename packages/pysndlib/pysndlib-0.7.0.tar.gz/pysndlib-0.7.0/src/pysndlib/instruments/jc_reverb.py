#==================================================================================
# The code is ported from Bill Schottstedaet's 'jcrev.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================
import math
import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.env as env
if cython.compiled:
    from cython.cimports.pysndlib import clm

@clm.clm_reverb
def jc_reverb(lowpass=False, volume=1., amp_env = None, decay_time=1.0):
   
    allpass1 = clm.make_all_pass(-.7, .7, 1051)
    allpass2 = clm.make_all_pass(-.7, .7, 337)
    allpass3 = clm.make_all_pass(-.7, .7, 113)
    comb1 = clm.make_comb(.742, 4799)
    comb2 = clm.make_comb(.733, 4999)
    comb3 = clm.make_comb(.715, 5399)
    comb4 = clm.make_comb(.697, 5801)
    chans = clm.get_channels(clm.default.output)
    
    length: cython.long = math.floor(clm.get_length(clm.default.reverb) + (clm.get_srate()*decay_time)) # in for loop
    filts = [clm.make_delay(clm.seconds2samples(.013))] if chans == 1 else [clm.make_delay(clm.seconds2samples(.013)),clm.make_delay(clm.seconds2samples(.011)) ]
    combs = clm.make_comb_bank([comb1, comb2, comb3, comb4])
    allpasses = clm.make_all_pass_bank([allpass1,allpass2,allpass3])
    
    i: cython.long = 0 # in for loop
    
    if lowpass or amp_env:
        flt = clm.make_fir_filter(3, [.25, .5, .25]) if lowpass else None
        envA = clm.make_env(amp_env, scaler=volume, duration = length / clm.get_srate())
        
        if lowpass:
            for i in range(length):
                clm.out_bank(filts, i, (clm.env(envA) * clm.fir_filter(flt, clm.comb_bank(combs, clm.all_pass_bank(allpasses, clm.ina(i, clm.default.reverb))))))
        else:
            for i in range(length):
                clm.out_bank(filts, i, (clm.env(envA) * clm.comb_bank(combs, clm.all_pass_bank(allpasses, clm.ina(i, clm.default.reverb)))))
    else:
        if chans == 1:
            
            gen = filts[0]
            for i in range(length):
                clm.outa(i, clm.delay(gen, volume * clm.comb_bank(combs, clm.all_pass_bank(allpasses, clm.ina(i, clm.default.reverb)))))
        else:    
            gen1: clm.mus_any = filts[0]
            gen2: clm.mus_any = filts[1]
            for i in range(length):
                val: cython.double = volume * clm.comb_bank(combs, clm.all_pass_bank(allpasses, clm.ina(i, clm.default.reverb))) 
                clm.outa(i, clm.delay(gen1, val))
                clm.outb(i, clm.delay(gen2, val))
