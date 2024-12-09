#==================================================================================
# The code is an attempt at translation of Bill Schottstedaet's 'clm-ins.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

# TODO: Instruments not translated yet - mlbvoi, pins, grm, expfil, graphEq, anoi, bes_fm, sbfm, fm2, rmsg, rms, cnvrev
# There are various fixes needed for items translated details in code

# Comments with hash and semicolons (# ;;;) are from original source

# ;;; CLM instruments translated to Snd/Scheme

import functools
import math

import numpy as np
import numpy.typing as npt
cimport numpy as np
import cython
cimport cython
import pysndlib.clm as clm
cimport pysndlib.clm as clm
from .env import stretch_envelope, interleave, max_envelope, min_envelope

np.import_array()
ctypedef np.double_t DTYPE




# TODO: more complex case --------------- mlbvoi ---------------- #

# ;;; translation from MUS10 of Marc LeBrun's waveshaping voice instrument (using FM here)
# ;;; this version translated (and simplified slightly) from CLM's mlbvoi.ins

@cython.ccall
def vox_fun(phonemes, forms):
    formants = {'I' : (390, 1990, 2550),
                'E' : ( 530, 1840, 2480),
                'AE' : ( 660, 1720, 2410),
                'UH' : ( 520, 1190, 2390),
                'A' : ( 730, 1090, 2440),
                'OW' : ( 570, 840, 2410),
                'U' : ( 440, 1020, 2240),
                'OO' : ( 300, 870, 2240),
                'ER' : ( 490, 1350, 1690),
                'W' : ( 300, 610, 2200),
                'LL' : ( 380, 880, 2575),
                'R' : ( 420, 1300, 1600),
                'Y' : ( 300, 2200, 3065),
                'EE' : ( 260, 3500, 3800),
                'LH' : ( 280, 1450, 1600),
                'L' : ( 300, 1300, 3000),
                'I2' : ( 350, 2300, 3340),
                'B' : ( 200, 800, 1750),
                'D' : ( 300, 1700, 2600),
                'G' : ( 250, 1350, 2000),
                'M' : ( 280, 900, 2200),
                'N' : ( 280, 1700, 2600),
                'NG' : ( 280, 2300, 2750),
                'P' : ( 300, 800, 1750),
                'T' : ( 200, 1700, 2600),
                'K' : ( 350, 1350, 2000),
                'F' : ( 175, 900, 4400),
                'TH' : ( 200, 1400, 2200),
                'S' : ( 200, 1300, 2500),
                'SH' : ( 200, 1800, 2000),
                'V' : ( 175, 1100, 2400),
                'THE' : ( 200, 1600, 2200),
                'Z' : ( 200, 1300, 2500),
                'ZH' : ( 175, 1800, 2000),
                'ZZ' : ( 900, 2400, 3800),
                'VV' : ( 565, 1045, 2400)}
    x = phonemes[0::2]
    y = phonemes[1::2]
    f = list([formants[i][forms] for i in y])
    return [item for first in zip(x,f) for item in first]



@cython.ccall
def vox(beg, dur, freq, amp, ampfun, freqfun, freqscl, phonemes, formant_amps, formant_indices,vibscl=.1, deg=0, pcrev=0):
    start: cython.long = clm.seconds2samples(beg)
    end: cython.long = clm.seconds2samples(beg + dur)
    car_os = clm.make_oscil(0)
    fs = len(formant_amps)
    per_vib = clm.make_triangle_wave(6, amplitude=clm.hz2radians(freq * vibscl))
    ran_vib = clm.make_rand(20, amplitude=clm.hz2radians(freq * .5 * vibscl))
    freqf = clm.make_env(freqfun, duration=dur, scaler=clm.hz2radians(freqscl * freq), offset=clm.hz2radians(freq))
    
    i: cython.long = 0
    
    if fs == 3 and clm.get_channels(clm.default.output):
        a0 = clm.make_env(ampfun, scaler=amp*formant_amps[0], duration=dur)
        a1 = clm.make_env(ampfun, scaler=amp*formant_amps[1], duration=dur)
        a2 = clm.make_env(ampfun, scaler=amp*formant_amps[2], duration=dur)
        o0 = clm.make_oscil(0.0)
        o1 = clm.make_oscil(0.0)
        o2 = clm.make_oscil(0.0)
        e0 = clm.make_oscil(0.0)
        e1 = clm.make_oscil(0.0)
        e2 = clm.make_oscil(0.0)
        ind0 = formant_indices[0]
        ind1 = formant_indices[1]
        ind2 = formant_indices[2]
        f0 = clm.make_env(vox_fun(phonemes,0),scaler=clm.hz2radians(1.0), duration=dur)
        f1 = clm.make_env(vox_fun(phonemes,1),scaler=clm.hz2radians(1.0), duration=dur)
        f2 = clm.make_env(vox_fun(phonemes,2),scaler=clm.hz2radians(1.0), duration=dur)
        
        for i in range(start, end):
            frq: cython.double = clm.env(freqf) + clm.triangle_wave(per_vib) + clm.rand_interp(ran_vib)
            carg: cython.double = clm.oscil(car_os, frq)
            frm0: cython.double = clm.env(f0) / frq
            frm1: cython.double = clm.env(f1) / frq
            frm2: cython.double = clm.env(f2) / frq
            
            rx: cython.double = clm.even_weight(frm0) * clm.oscil(e0, ((ind0*carg) + clm.even_multiple(frm0, frq)))
            rx += clm.odd_weight(frm0) * clm.oscil(o0, ((ind0*carg) + clm.odd_multiple(frm0, frq)))
            rx *= clm.env(a0)
            
            ry: cython.double = clm.even_weight(frm1) * clm.oscil(e1, ((ind1*carg) + clm.even_multiple(frm1, frq)))
            ry += clm.odd_weight(frm1) * clm.oscil(o1, ((ind1*carg) + clm.odd_multiple(frm1, frq)))
            ry *= clm.env(a1)
            
            rz: cython.double = clm.even_weight(frm2) * clm.oscil(e2, ((ind2*carg) + clm.even_multiple(frm2, frq)))
            rz += clm.odd_weight(frm2) * clm.oscil(o2, ((ind2*carg) + clm.odd_multiple(frm2, frq)))
            rz *= clm.env(a2)
            clm.outa(i, rx+ry+rz)
#         else:
#             evens = [None] * fs
#             odds = [None] * fs
#             ampfs = [None] * fs
#             indices = [None] * fs
#             frmfs = [None] * fs
#             carrier = frm_int = rfrq = frm0 = frac = fracf = 0.0
#             loc = clm.make_locsig(deg, 1.0, pcrev)
#             
#             for i in range(fs):
#                 evens[i] = clm.make_oscil(0)
#                 odds[i] = clm.make_oscil(0)
#                 ampfs[i] = clm.make_env(ampfun, scaler=(amp * formant_amps[i]), duration=dur)
#                 indices[i] = formant_indices[i]
#                 frmfs[i] = clm.make_env(vox_fun(phonemes, i), scaler=clm.hz2radians(1.0), duration=dur)
#                 
#                 
#             if fs == 3:
#                 frmfs0 = frmfs[0]; frmfs1 = frmfs[1]; frmfs2 = frmfs[2]
#                 index0 = indices[0]; index1 = indices[1]; index2 = indices[2]
#                 ampfs0 = ampfs[0]; ampfs1 = ampfs[1]; ampfs2 = ampfs[2]
#                 evens0 = evens[0]; evens1 = evens[1]; evens2 = evens[2]
#                 odds0 = odds[0]; odds1 = odds[1]; odds2 = odds[2]
#                 
#                 for i in range(start, end):
#                     rfrq = clm.env(freqf) + clm.triangle_wave(per_vib) + clm.rand_interp(ran_vib)
#                     carrier = clm.oscil(car_os, rfrq)
#                     frm0 = clm.env(frmfs0) / rfrq
#                     frm_int = int(math.floor(frm0))
#                     frac = frm0 - frm_int
#                     fracf = (index0 * carrier) + (frm_int * rfrq)
#                     
#                     clm.locsig(i, clm.env(ampfs0), clm.is_even(frm_int))
            
# with clm.Sound(play=True, statistics=True):
#     vox(0,2,170,.4, [0,0,25,1,75,1,100,0], [0,0,5,.5,10,0,100,1], .1, [0,'E',25,'AE',35,'ER',65,'ER',75,'I',100,'UH'], [.8, .15, .05], [.005, .0125, .025], .05, .1)


# TODO: --------------- pqwvox ---------------- #

        














                    
                    
# --------------- drone ---------------- #
@cython.ccall
def drone(startime, dur, frequency, amp, ampfun, synth, ampat, ampdc, amtrev, deg, dis, rvibamt, rvibfreq):
    beg: cython.long = clm.seconds2samples(startime)
    end: cython.long = clm.seconds2samples(startime + dur)
    waveform: np.ndarray = clm.partials2wave(synth)
    amplitude: cython.double = amp * .25
    freq: cython.double = clm.hz2radians(frequency)
    s = clm.make_table_lookup(frequency, wave=waveform)
    ampe = stretch_envelope(ampfun, 25, (100 * (ampat / dur)), 75, (100 - (100 * (ampdc / dur))))
    amp_env = clm.make_env(ampe, scaler=amplitude, duration=dur)
    ran_vib = clm.make_rand(rvibfreq, rvibamt*freq)
    loc = clm.make_locsig(deg, dis, amtrev)
    
    i: cython.long = 0
        
    for i in range(beg, end):
        clm.locsig(loc, i, clm.env(amp_env) * clm.table_lookup(s, clm.rand(ran_vib)))


# --------------- canter ---------------- #
@cython.ccall
def canter(beg, dur, pitch, amp_1, deg, dis, pcrev, ampfun, ranfun, skewfun, skewpc, ranpc, ranfreq, indexfun, atdr, dcdr, 
            ampfun1, indfun1, fmtfun1, 
            ampfun2, indfun2, fmtfun2, 
            ampfun3, indfun3, fmtfun3, 
            ampfun4, indfun4, fmtfun4):

    amp = amp_1 * .25
    rangetop = 910.0
    rangebot = 400.0
    k = math.floor(100 * math.log(pitch / rangebot, rangetop / rangebot))
    atpt = 100 * (atdr / dur)
    dcpt = 100 - ( 100 * (dcdr / dur))
    lfmt1 = clm.env_interp(k, fmtfun1)
    lfmt2 = clm.env_interp(k, fmtfun2)
    lfmt3 = clm.env_interp(k, fmtfun3)
    lfmt4 = clm.env_interp(k, fmtfun4)
    
    dev11 = clm.hz2radians(clm.envelope_interp(k, indfun1) * pitch)
    dev12 = clm.hz2radians(clm.envelope_interp(k, indfun2) * pitch)
    dev13 = clm.hz2radians(clm.envelope_interp(k, indfun3) * pitch)
    dev14 = clm.hz2radians(clm.envelope_interp(k, indfun4) * pitch)
    start = clm.seconds2samples(beg)
    end = clm.seconds2samples(beg + dur)
    dev01 = dev11 * .5
    dev02 = dev12 * .5
    dev03 = dev13 * .5
    dev04 = dev14 * .5
    
    harm1 = math.floor(.5 + (lfmt1 / pitch))
    harm2 = math.floor(.5 + (lfmt2 / pitch))
    harm3 = math.floor(.5 + (lfmt3 / pitch))
    harm4 = math.floor(.5 + (lfmt4 / pitch))

    lamp1 = clm.envelope_interp(k, ampfun1) * amp * (1 - math.fabs(harm1 - (lfmt1 / pitch)))
    lamp2 = clm.envelope_interp(k, ampfun2) * amp * (1 - math.fabs(harm2 - (lfmt2 / pitch)))
    lamp3 = clm.envelope_interp(k, ampfun3) * amp * (1 - math.fabs(harm3 - (lfmt3 / pitch)))
    lamp4 = clm.envelope_interp(k, ampfun4) * amp * (1 - math.fabs(harm4 - (lfmt4 / pitch)))
    
    tidx_stretched = stretch_envelope(indexfun, 25, atpt, 75, dcpt)
    tampfun = clm.make_env(stretch_envelope(ampfun, 25, atpt, 75, dcpt), duration=dur)
    tskwfun = clm.make_env(stretch_envelope(skewfun, 25, atpt, 75, dcpt), scaler=clm.hz2radians(pitch * skewpc), duration=dur)
    tranfun = clm.make_env(stretch_envelope(ranfun, 25, atpt, 75, dcpt), duration=dur)    
    d1env = clm.make_env(tidx_stretched, offset=dev01, scaler=dev11, duration=dur)
    d2env = clm.make_env(tidx_stretched, offset=dev02, scaler=dev12, duration=dur)
    d3env = clm.make_env(tidx_stretched, offset=dev03, scaler=dev13, duration=dur)
    d4env = clm.make_env(tidx_stretched, offset=dev04, scaler=dev14, duration=dur)
    modgen = clm.make_oscil(pitch)
    ranvib = clm.make_rand(ranfreq, clm.hz2radians(ranpc * pitch))
    loc = clm.make_locsig(deg, dis, pcrev)
    gen1 = clm.make_oscil(pitch * harm1)
    gen2 = clm.make_oscil(pitch * harm2)
    gen3 = clm.make_oscil(pitch * harm3)
    gen4 = clm.make_oscil(pitch * harm4)
    
    frqval: cython.double = 0.0
    modval: cython.double = 0.0
    
    for i in range(start, end):
        frqval = clm.env(tskwfun) + (clm.env(tranfun) * clm.rand(ranvib))
        modval = clm.oscil(modgen, frqval)
        
        clm.locsig(loc, i, clm.env(tampfun) * 
                (lamp1 * clm.oscil(gen1, (((clm.env(d1env)*modval) + frqval) * harm1))) +
                (lamp2 * clm.oscil(gen2, (((clm.env(d2env)*modval) + frqval) * harm2))) +
                (lamp3 * clm.oscil(gen3, (((clm.env(d3env)*modval) + frqval) * harm3))) +
                (lamp4 * clm.oscil(gen4, (((clm.env(d4env)*modval) + frqval) * harm4))))
    




        


    







# TODO: --------------- pins ---------------- #

# def pins(beg, dur, file, amp, transposition=1.0, time_scaler=1.0, fftsize=256, highest_bin=128, max_peaks=16, attack=False):
#     fdr = np.zeros(fftsize-1)   
#     fdi = np.zeros(fftsize-1) 
#     start = seconds2samples(beg)    






# TODO: --------------- grm ---------------- #

# TODO: --------------- expfil ---------------- #

# TODO: --------------- graphEq ---------------- #

# TODO: --------------- anoi ---------------- #

# TODO: --------------- bes_fm ---------------- #

# TODO: --------------- sbfm ---------------- #

# TODO: --------------- fm2 ---------------- #

# TODO: --------------- rmsg ---------------- #

# TODO: --------------- rms ---------------- #

# TODO: --------------- cnvrev ---------------- #



