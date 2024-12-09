#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================


import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
import pysndlib.env as env
if cython.compiled:
    from cython.cimports.pysndlib import clm

# --------------- exp_snd ---------------- #
# moved file arg from 1st arg
#   ;; granulate with envelopes on the expansion amount, segment envelope shape,
#   ;; segment length, hop length, and input file resampling rate

@cython.ccall
def is_pair(x): #seems only useful in this instrument
    return isinstance(x, list)

@cython.ccall
def exp_snd(beg, dur, file, amp, exp_amt=1.0, ramp=.4, seglen=.15, sr=1.0, hop=.05, ampenv=[0,0,.5,1,1,0]):

    max_seg_len = env.max_envelope(seglen) if is_pair(seglen) else seglen
    initial_seg_len = seglen[1] if is_pair(seglen) else seglen
    rampdata = ramp if is_pair(ramp) else [0, ramp, 1, ramp]
    max_out_hop = env.max_envelope(hop) if is_pair(hop) else hop
    initial_out_hop = hop[1] if is_pair(hop) else hop
    min_exp_amt = env.min_envelope(exp_amt) if is_pair(exp_amt) else exp_amt
    initial_exp_amt = exp_amt[1] if is_pair(exp_amt) else exp_amt

    if (env.min_envelope(rampdata) <= 0.0) or (env.max_envelope(rampdata) >= .5):
        raise RuntimeError(f'ramp argument to exp_snd must always be between 0.0 and .5: {ramp}.')

    st: cython.long = clm.seconds2samples(beg)
    nd: cython.long = clm.seconds2samples(beg + dur)
    f0 = clm.make_readin(file)

    expenv = clm.make_env( exp_amt if is_pair(exp_amt) else [0, exp_amt, 1, exp_amt], duration=dur)
    lenenv = clm.make_env( seglen if is_pair(seglen) else [0, seglen, 1, seglen], scaler=clm.default.srate, duration=dur)
    scaler_amp = ((.6 * .15) / max_seg_len) if max_seg_len > .15 else .6
    srenv = clm.make_env(sr if is_pair(sr) else [0, sr, 1, sr], duration=dur)
    rampenv = clm.make_env(rampdata, duration=dur)
    initial_ramp_time = ramp[1] if is_pair(ramp) else ramp
    max_in_hop = max_out_hop / min_exp_amt
    max_len = clm.seconds2samples(max(max_out_hop, max_in_hop) + max_seg_len)
    hopenv = clm.make_env( hop if is_pair(hop) else [0, hop, 1, hop], duration=dur)
    ampe = clm.make_env(ampenv, scaler= amp, duration=dur)
    exA = clm.make_granulate(f0, expansion=initial_exp_amt, max_size=max_len, ramp=initial_ramp_time, hop=initial_out_hop, length=initial_seg_len, scaler=scaler_amp)
    vol = clm.env(ampe)
    
    valA0: cython.double = vol * clm.granulate(exA)
    valA1: cython.double = vol * clm.granulate(exA)
    ex_samp: cython.double = 0.0
    next_samp: cython.double = 0.0
    
    i: cython.long = 0
    k: cython.long = 0
    
    for i in range(st, nd):
        sl: cython.double = clm.env(lenenv)
        vol: cython.double = clm.env(ampe)
        exA.mus_length = round(sl)
        exA.mus_ramp = math.floor(sl * clm.env(rampenv))
        exA.mus_frequency = clm.env(hopenv)
        exA.mus_increment = clm.env(expenv)
        next_samp += clm.env(srenv)
        
        if next_samp > (ex_samp + 1):
            samps = math.floor(next_samp - ex_samp)
            if samps > 2:
                for k in range(samps-2):
                    clm.granulate(exA)
            valA0 = (vol * clm.granulate(exA)) if samps >= 2 else valA1
            valA1 = vol * clm.granulate(exA)
            ex_samp += samps
            
            clm.outa(i, valA0 if next_samp == ex_samp else (valA0 + ((next_samp - ex_samp) * (valA1 - valA0)))) 

if __name__ == '__main__':       
    with clm.Sound(play=True,statistics=True):
        exp_snd(0, 3, '../examples/fyow.snd', 1, [0,1,1,3],   .4, .15, [0,2,1,.5], .05)

