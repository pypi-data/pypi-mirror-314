#==================================================================================
# The code is an attempt at translation of Bill Schottstedaet's 'dsp.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

# TODO: 'easy case '  

import math
import cython
import pysndlib.clm as clm
import numpy as np
if cython.compiled:
    from cython.cimports.pysndlib import clm


#not sure typing any of the args are worth it.
@cython.ccall
def fm_violin(beg, dur, frequency, amplitude, fm_index=1, 
            amp_env = [ 0, 0,  25, 1,  75, 1,  100, 0],
            periodic_vibrato_rate = 5.0,
            random_vibrato_rate = 16.0,
            periodic_vibrato_amplitude = 0.0025,
            random_vibrato_amplitude = 0.005,
            fm1_index=None,
            fm2_index=None,
            fm3_index=None,
            fm1_rat: cython.double = 1.0, # in for loop
            fm2_rat: cython.double = 3.0, # in for loop
            fm3_rat: cython.double = 4.0, # in for loop
            fm1_env = [0., 1., 25., .4, 75., .6, 100., 0.],
            fm2_env = [0., 1., 25., .4, 75., .6, 100., 0.],
            fm3_env = [0., 1., 25., .4, 75., .6, 100., 0.],
            gliss_env = [0,0,100,0],
            glissando_amount = 0.0,
            noise_amount = 0.0,
            noise_freq = 1000.,
            ind_noise_freq = 10.,
            ind_noise_amount = 0.0,
            amp_noise_freq = 20.0,
            amp_noise_amount = 0.0,
            degree=45,
            distance=1.0,
            reverb_amount = .01,
            base=1):   
    start: cython.long = clm.seconds2samples(beg) # in for loop
    end: cython.long = start + clm.seconds2samples(dur) # in for loop
    
    frq_scl = clm.hz2radians(frequency)
    maxdev = frq_scl * fm_index
    index1 = fm1_index if fm1_index else min(math.pi, maxdev * (5.0 / math.log(frequency)))
    index2 = fm2_index if fm2_index else min(math.pi, maxdev * 3.0 * ((8.5 - math.log(frequency)) / (3.0 + (frequency / 1000.))))
    index3 = fm3_index if fm3_index else min(math.pi, maxdev * (4.0 / math.sqrt(frequency)))
    carrier = clm.make_oscil(frequency)
    fmosc1 = clm.make_oscil(frequency)
    fmosc2 = clm.make_oscil(frequency * fm2_rat)
    fmosc3 = clm.make_oscil(frequency * fm3_rat)
    ampf = clm.make_env(amp_env, scaler = amplitude, duration = dur, base=base)
    indf1 = clm.make_env(fm1_env, scaler = index1, duration = dur)
    indf2 = clm.make_env(fm2_env, scaler = index2, duration = dur)
    indf3 = clm.make_env(fm3_env, scaler = index3, duration = dur)
    frqf = clm.make_env(gliss_env,scaler = (glissando_amount * frq_scl), duration=dur)
    pervib = clm.make_triangle_wave(periodic_vibrato_rate,periodic_vibrato_amplitude * frq_scl)
    ranvib = clm.make_rand_interp(random_vibrato_rate, random_vibrato_amplitude * frq_scl)
    fm_noi = clm.make_rand(noise_freq, math.pi * noise_amount)
    ind_noi = clm.make_rand_interp(ind_noise_freq, ind_noise_amount)
    amp_noi = clm.make_rand_interp(amp_noise_freq, amp_noise_amount)
    loc = clm.make_locsig(degree, distance, reverb_amount)
    
    i: cython.int = 0 # in for loop
    
    for i in range(start, end):
        vib: cython.double = clm.triangle_wave(pervib) + clm.rand_interp(ranvib) + clm.env(frqf)
        fuzz: cython.double = clm.rand(fm_noi)
        inoi: cython.double = 1.0 + clm.rand_interp(ind_noi)
        anoi: cython.double  = clm.env(ampf) * (1.0 + clm.rand_interp(amp_noi))
        clm.locsig(loc, i, anoi * clm.oscil(carrier, 
                        vib + 
                        inoi * 
                        ((clm.env(indf1) * clm.oscil(fmosc1, (vib * fm1_rat) + fuzz)) +
                        (clm.env(indf2) * clm.oscil(fmosc2, ((vib * fm2_rat) + fuzz))) +
                        (clm.env(indf3) * clm.oscil(fmosc3, ((vib * fm3_rat) + fuzz))))))



