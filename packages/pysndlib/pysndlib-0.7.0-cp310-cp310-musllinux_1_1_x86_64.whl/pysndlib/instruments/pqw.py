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

# --------------- pqw ---------------- #
#   ;; phase-quadrature waveshaping used to create asymmetric (i.e. single side-band) spectra.
#   ;; The basic idea here is a variant of sin x sin y - cos x cos y = cos (x + y)

def clip_env(e):
    xs = e[0::2]
    ys = [min(x,1.0) for x in e[1::2]]
    return env.interleave(xs, ys)
    
    
@cython.ccall
def pqw(start, dur, spacing_freq, carrier_freq, amplitude, 
        ampfun, indexfun, partials, degree=0.0, distance=1.0, reverb_amount=.005):
    normalized_partials = clm.normalize_partials(partials)
    spacing_cos = clm.make_oscil(spacing_freq, initial_phase=math.pi/2.0)
    spacing_sin = clm.make_oscil(spacing_freq)
    carrier_cos = clm.make_oscil(carrier_freq, initial_phase=math.pi/2.0)
    carrier_sin = clm.make_oscil(carrier_freq)
    sin_coeffs: np.ndarray = clm.partials2polynomial(normalized_partials, clm.Polynomial.SECOND_KIND)
    cos_coeffs: np.ndarray = clm.partials2polynomial(normalized_partials, clm.Polynomial.FIRST_KIND)
    amp_env = clm.make_env(ampfun, scaler=amplitude, duration=dur)
    ind_env = clm.make_env(clip_env(indexfun), duration=dur)
    loc = clm.make_locsig(degree, distance, reverb_amount)
    r: cython.double = carrier_freq / spacing_freq
    tr = clm.make_triangle_wave(5, clm.hz2radians(.005 * spacing_freq))
    rn = clm.make_rand_interp(12, clm.hz2radians(.005 * spacing_freq))
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start + dur)
    
    i: cython.long = 0
    vib: cython.double = 0.0
    
    for i in range(beg, end):
        vib = clm.triangle_wave(tr) + clm.rand_interp(rn)
        ax = clm.env(ind_env) * clm.oscil(spacing_cos, vib)
        clm.locsig(loc, i, clm.env(amp_env) * 
            ((clm.oscil(carrier_sin, (vib * r)) * clm.oscil(spacing_sin, vib) * clm.polynomial(sin_coeffs, ax)) -
                (clm.oscil(carrier_cos, (vib * r)) * clm.polynomial(cos_coeffs, ax))))

if __name__ == '__main__': 
    with clm.Sound( play = True, statistics=True):
        pqw(0, .5, 200, 1000, .2, [0,0,25,1,100,0], [0, 1, 100, 0], [2, .1, 3, .3, 6, .5])
