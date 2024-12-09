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


# --------------- spectra ---------------- #
@cython.ccall
def spectra(startime, duration, frequency, amplitude, partials=[1,1,2,0.5], amp_envelope=[0,0,50,1,100,0], 
                vibrato_amplitude=0.005, vibrato_speed=5.0,degree=0.0, distance=1.0, reverb_amount=0.005):

    beg: cython.long  = clm.seconds2samples(startime)
    end:  cython.long = clm.seconds2samples(startime + duration)
    waveform: np.ndarray = clm.partials2wave(partials)
    freq: cython.double = clm.hz2radians(frequency)
    s = clm.make_table_lookup(frequency=frequency, wave=waveform)
    amp_env = clm.make_env(amp_envelope, scaler=amplitude, duration=duration)
    per_vib = clm.make_triangle_wave(vibrato_speed, vibrato_amplitude * freq)
    loc = clm.make_locsig(degree, distance, reverb_amount)
    ran_vib = clm.make_rand_interp(vibrato_speed + 1.0, vibrato_amplitude * freq)
    
    i: cython.long = beg
    
    for i in range(beg, end):
        clm.locsig(loc, i, clm.env(amp_env) * clm.table_lookup(s, clm.triangle_wave(per_vib) + clm.rand_interp(ran_vib)))

if __name__ == '__main__': 
    with clm.Sound( play = True, statistics=True):
        spectra(0, 4, 440.0, .1, [1.0,.4,2.0,.2,3.0,.2,4.0,.1,6.0,.1], [0.0,0.0,1.0,1.0,5.0,0.9,12.0,0.5,25.0,0.25,100.0,0.0])
