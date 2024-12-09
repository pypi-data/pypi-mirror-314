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

# --------------- reson ---------------- #
@cython.ccall
def reson(startime, dur, pitch, amp, numformants, indxfun, skewfun, pcskew, skewat, skewdc,
		      vibfreq, vibpc, ranvibfreq, ranvibpc, degree, distance, reverb_amount, data):
		      
    beg: cython.long = clm.seconds2samples(startime)
    end: cython.long = clm.seconds2samples(startime + dur)
    carriers = [None] * numformants
    modulator = clm.make_oscil(pitch)
    ampfs = [None] * numformants
    indfs = [None] * numformants
    c_rats = [None] * numformants
    totalamp = 0.0
    loc = clm.make_locsig(degree, distance, reverb_amount)
    pervib = clm.make_triangle_wave(vibfreq, clm.hz2radians(vibpc * pitch))
    ranvib = clm.make_rand_interp(ranvibfreq, clm.hz2radians(ranvibpc * pitch))
    frqe = clm.stretch_envelope(skewfun, 25, 100 * (skewat / dur), 75, 100 - (100 * (skewdc / dur)))
    frqf = clm.make_env(frqe, scaler=clm.hz2radians(pcskew * pitch), duration=dur)

    for k in range(0,numformants):
        totalamp += data[k][2]
        
    for k in range(0, numformants):
        frmdat = data[k]
        freq = frmdat[k]
        harm = round(freq / pitch)
        rfamp = frmdat[2]
        ampat = 100 * (frmdat[3] / dur)
        ampdc = 100 - (100 * (frmdat[4] / dur))
        dev0 = clm.hz2radians(frmdat[5] * freq)
        dev1 = clm.hz2radians(frmdat[6] * freq)
        indxat = 100 * (frmdat[7] / dur)
        indxdc = 100 - (100 * (frmdat[8] / dur))
        ampf = frmdat[0]
        rsamp = 1.0 - math.fabs(harm - (freq / pitch))
        cfq = pitch * harm
        if ampat == 0:
            ampat = 25
        if ampdc == 0:
            ampdc = 75
        if indxat == 0:
            indxat = 25
        if indxdc == 0:
            indxdc = 75
        indfs[k] = clm.make_env(env.stretch_envelope(indxfun, 25, indxat, 75, indxdc), duration=dur, scaler=(dev1 - dev0), offset=dev0)
        ampfs[k] = clm.make_env(env.stretch_envelope(ampf, 25, ampat, 75, ampdc), duration=dur, scaler=(rsamp * amp * rfamp) / totalamp)
        c_rats[k] = harm
        carriers[k] = clm.make_oscil(cfq)
        
    i: cython.long = 0
    j: cython.long = 0
    vib: cython.double = 0.0
    modsig: cython.double = 0.0
    outsum: cython.double
    
    if numformants == 2:
        e1: clm.mus_any = ampfs[0]
        e2: clm.mus_any = ampfs[1]
        c1: clm.mus_any = carriers[0]
        c2: clm.mus_any = carriers[1]
        i1: clm.mus_any = indfs[0]
        i2: clm.mus_any = indfs[1]
        r1: cython.double = c_rats[0]
        r2: cython.double = c_rats[1]
        
        for i in range(beg, end):
            vib = clm.env(frqf) + clm.triangle_wave(pervib) + clm.rand_interp(ranvib)
            modsig = clm.oscil(modulator, vib)
            clm.locsig(loc, i, (clm.env(e1) * clm.oscil(c1, (vib * r1) + (clm.env(i1) * modsig))) + (clm.env(e2) * clm.oscil(c2, (vib * r2) + (clm.env(i2) * modsig))))
        
    else:
        for i in range(beg, end):
            outsum = 0.0
            vib = clm.env(frqf) + clm.triangle_wave(pervib) + clm.rand_interp(ranvib)
            modsig = clm.oscil(modulator, vib)
            
            for j in range(0,numformants):
                outsum += clm.env(ampfs[j]) * clm.oscil(carriers[j], (vib * c_rats[j]) + (clm.env(indfs[j]) * modsig))
            
            clm.locsig(loc, i, outsum)       
