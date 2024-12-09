#==================================================================================
# The code is ported from Bill Schottstedaet's 'clm-ins.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import math
import random
import cython
import numpy as np
import pysndlib.clm as clm
if cython.compiled:
    from cython.cimports.pysndlib import clm

# --------------- two_tab ---------------- #
# ;;; interpolate between two waveforms (this could be extended to implement all the various
# ;;; wavetable-based synthesis techniques).
@cython.ccall
def two_tab(startime, duration, frequency, amplitude, partial_1=[1.0,1.0,2.0,0.5], partial_2=[1.0,0.0,3.0,1.0], 
                    amp_envelope=[0,0,50,1,100,0], interp_func=[0,1,100,0], 
                    vibrato_amplitude=.005, vibrato_speed=5.0, 
                    degree=0.0, distance=1.0, reverb_amount=.005):

    beg = clm.seconds2samples(startime)
    end = clm.seconds2samples(startime + duration)
    waveform_1 = clm.partials2wave(partial_1)
    waveform_2 = clm.partials2wave(partial_2)
    freq = clm.hz2radians(frequency)
    s_1 = clm.make_table_lookup(frequency, wave=waveform_1)
    s_2 = clm.make_table_lookup(frequency, wave=waveform_2)
    amp_env = clm.make_env(amp_envelope, scaler=amplitude, duration=duration)
    interp_env = clm.make_env(interp_func, duration=duration)
    interp_env_1 = clm.make_env(interp_func, duration=duration, offset=1.0, scaler=-1.0)
    loc = clm.make_locsig(degree, distance, reverb_amount)
    per_vib = clm.make_triangle_wave(vibrato_speed, vibrato_amplitude * freq)
    ran_vib = clm.make_rand_interp(vibrato_speed+1.0, vibrato_amplitude * freq)
    
    i: cython.long = 0
    vib: cython.double = 0.
    
    for i in range(beg, end):
        vib = clm.triangle_wave(per_vib) + clm.rand_interp(ran_vib)
        clm.locsig(loc, i, clm.env(amp_env) * ((clm.env(interp_env)*clm.table_lookup(s_1, vib)) + (clm.env(interp_env_1)*clm.table_lookup(s_2, vib))))
    
