#==================================================================================
# The code is an attempt at translation of Bill Schottstedaet's 'dsp.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

# TODO: things not translated yet - down_oct , Dolph-Chebyshev window, differentiator, IIR filters
# There are various fixes needed for items translated details in code

import math
from pathlib import Path
import cython
import pysndlib.clm as clm
# TODO: Figure out why I need to do this. 
from pysndlib.clm import ndarray2file

import numpy as np
from .env import scale_envelope
"hello there"

NEARLY_ZERO = 1.0e-10

# @cython.ccall
# def binomial(n, k):
#     if 0 <= k <= n:
#         a= 1
#         b=1
#         for t in range(1, min(k, n - k) + 1):
#             a *= n
#             b *= t
#             n -= 1
#         return a // b
#     else:
#         return 0

# --------------- src_duration ---------------- #


@cython.ccall
def src_duration(e) -> cython.double:
    """
      returns the new duration of a sound after using 'envelope' for time-varying sampling-rate conversion
    """
    length = len(e) - 2
    dur = 0.0
    all_x = e[length] - e[0]
    area = 0
    for i in range(0,length, 2):
        x0 = e[i]
        x1 = e[i+2]
        y0 = e[i+1]
        y1 = e[i+3]
        if abs(y0-y1) < .0001:
            area = (x1 - x0) / (y0 * all_x)
        else:
            if y0 == 0:
                raise ValueError("src can't use an evelope that has 0 as a y value")
            area = (math.log(y1 / y0) * (x1 - x0)) / ((y1-y0)*all_x)
        dur += abs(area)
    return dur
    
# --------------- src_fit_envelope ---------------- #

@cython.ccall
def src_fit_envelope(e, target_dur):
    return scale_envelope(e, src_duration(e) / target_dur)
    
    
    
# --------------- Dolph-Chebyshev window ---------------- #
# already in sndlib

    
    
# --------------- down_oct ---------------- #
# TODO: make this able to work with multi channel files
def down_oct(n, snd, chn, outname=None):
    if not clm.is_power_of_2(n):
        raise ValueError(f'n must be power of 2 not {n}')
    length = clm.get_length(snd)
    fftlen = int(math.floor(2**math.ceil(math.log(length, 2))))
    
    fftlen2 = fftlen // 2
    fft_1 = (n * fftlen) - 1
    fftscale = (1.0 / fftlen)
    rl1, sr = clm.file2ndarray(snd, chn, 0, fftlen )
    rl1 = rl1[0]
    im1 = np.zeros(fftlen)
    clm.mus_fft(rl1, im1, fftlen, 1)
    rl1 *= fftscale
    im1 *= fftscale
    rl2 = np.zeros(n * fftlen)
    im2 = np.zeros(n * fftlen)
    np.copyto(rl2[0:fftlen2], rl1[0:fftlen2])
    np.copyto(im2[0:fftlen2], im1[0:fftlen2])

    i: cython.long = 0
    j: cython.long = 0
    
    j = fft_1
    for k in range(fftlen-1, fftlen2):
        rl2[j] = rl1[k]
        im2[j] = im1[k]
        j -= 1
    clm.mus_fft(rl2, im2, (n * fftlen), -1)
    
    if outname is not None:
        ndarray2file(outname, rl2[:n*length], sr=sr)
        return outname
    else:
        ndarray2file(Path(snd).stem +'down_oct.wav', rl2[:n*length], sr=sr) 
        return Path(snd).stem +'_down_oct.wav'
    
    
# --------------- stretch-sound-via-dft ---------------- #
# Too slow

# def stretch_sound_via_dft(factor, snd, chn, outname=None):
#     n = clm.length(snd)
#     out_n = round(n*factor)
#     out_data = np.zeros(out_n)
#     fr = np.zeros(out_n)
#     freq = (np.pi*2) / n
#     in_data, sr = clm.file2ndarray(snd, chn, 0, n )
#     n2 = n // 2
#     in_data = in_data[0]
#     for i in range(n):
#         fr = i if i < n2 else ((out_n + i) - n - 1)
#         clm.edot_product(freq * (complex(0, -1) * i), in_data)
#     freq = ((np.pi*2) / out_n)
#     for i in range(out_n):
#         out_data[i] = clm.edot_product(freq * (complex(0, 1) * i), fr, n)   
#     if outname is not None:
#         ndarray2file(outname, out_data, sr=sr)
#         return outname
#     else:
#         ndarray2file(Path(snd).stem +'stretch_sound_via_dft.wav', out_data, sr=sr) 
#         return Path(snd).stem +'stretch_sound_via_dft.wav'


# --------------- freqdiv ---------------- #
@cython.ccall
def freqdiv(n, snd, chn, outname=None):
    data, sr = clm.file2ndarray(snd, chn, 0)
    size = clm.get_length(data)
    i: cython.long = 0
    k: cython.long = 0
    
    if n > 1:
        for i in range(0,size,n):
            val = data[0][i]
            stop = min(size, i+n)
            for k in range(i+1, stop):
                data[0][k] = val
        if outname is None:
            raise ValueError('missing outfile name')
    clm.ndarray2file(outname, data, size=size, sr=sr)


# -------- "adaptive saturation" -- an effect from sed_sed@my-dejanews.com

#-------- spike

#;;; -------- easily-fooled autocorrelation-based pitch tracker 

#;;; -------- chorus (doesn't always work and needs speedup)

# --------------- highpass ---------------- #

#-------- chordalize (comb filters to make a chord using chordalize-amount and chordalize-base)

# -------- zero-phase, rotate-phase

# -------- brighten-slightly

# ---FIR 

# -------- Hilbert transform


# freq in radians
@cython.ccall
def make_highpass(fc, length: cython.int =30):
    """makes an FIR highpass filter."""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = -math.sin(fc * i)
        if i == 0:
            arr[k] = fc / math.pi
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))
    return clm.make_fir_filter(arrlen, arr)
    
    
@cython.ccall
def highpass(gen: clm.mus_any, insig: cython.double) -> cython.double:
    return clm.fir_filter(gen, insig)
# 
# --------------- lowpass ---------------- #
# freq in radians
@cython.ccall
def make_lowpass(fc, length: cython.int=30):
    """makes an FIR lowpass filter."""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = math.sin(fc * i)
        if i == 0:
            arr[k] = fc / math.pi
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))
    return clm.make_fir_filter(arrlen, arr)

@cython.ccall
def lowpass(gen: clm.mus_any, insig: cython.double) -> cython.double:
    return clm.fir_filter(gen, insig)




# --------------- bandpass ---------------- #
# freq in radians
@cython.ccall
def make_bandpass(flo, fhi, length: cython.int =30):
    """makes an FIR bandpass filter."""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = math.sin(fhi * i) - math.sin(flo * i)
        if i == 0:
            arr[k] = (fhi - flo) / math.pi
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))
    return clm.make_fir_filter(arrlen, arr)

@cython.ccall
def bandpass(gen: clm.mus_any, insig: cython.double) -> cython.double:
    return clm.fir_filter(gen, insig)

# --------------- bandstop ---------------- #
# freq in radians
@cython.ccall
def make_bandstop(flo, fhi, length: cython.int =30):
    """makes an FIR bandstop filter"""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = math.sin(flo * i) - math.sin(fhi * i)
        if i == 0:
            arr[k] = (1.0 - (fhi - flo) / math.pi)
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))  
    return clm.make_fir_filter(arrlen, arr)
    
@cython.ccall
def bandstop(gen: clm.mus_any, insig: cython.double) -> cython.double:
    return clm.fir_filter(gen, insig)
# 
# 
# # --------------- TODO: differentiator ---------------- #
# 
# # --------------- IIR filters ---------------- #
# 
# --------------- Butterworth filters ---------------- #

@cython.ccall
def make_butter_high_pass(fq):
    """makes a Butterworth filter with high pass cutoff at 'freq'"""
    r = math.tan((math.pi * fq) / clm.get_srate())
    r2 = r * r
    c1 = 1.0 / (1.0 + (r * math.sqrt(2.0)) + r2)
    return clm.make_filter(3, [c1, (-2.0 * c1), c1], [0.0, 2.0*(r2-1.0)*c1, ((1.0 + r2 ) - (r * math.sqrt(2.0))) * c1])
#     
@cython.ccall
def make_butter_low_pass(fq):
    """makes a Butterworth filter with low pass cutoff at 'freq'"""
    r = 1.0 / math.tan((math.pi * fq) / clm.get_srate())
    r2 = r * r
    c1 = 1.0 / (1.0 + (r * math.sqrt(2.0)) + r2)
    return clm.make_filter(3, [c1, (2.0 * c1), c1], [0.0, 2.0*(1.0-r2)*c1, ((1.0 + r2 ) - (r * math.sqrt(2.0))) * c1])
    
@cython.ccall
def make_butter_band_pass(fq, bw):
    """makes a bandpass Butterworth filter with low edge at 'freq' and width 'band'"""
    c = 1.0 / math.tan((math.pi*bw) / clm.get_srate())
    d = 2.0 * math.cos((2.0 * math.pi * fq) / clm.get_srate())
    c1 = 1.0 / (1.0 + c)
    return clm.make_filter(3, [c1,0.0,-c1], [0., -c * d * c1, (c - 1.0) * c1])
 
@cython.ccall
def make_butter_band_reject(fq, bw):
    """makes a band-reject Butterworth filter with low edge at 'freq' and width 'band'"""
    c = 1.0 / math.tan((math.pi*bw) / clm.get_srate())
    c1 = 1.0 / (1.0 + c)
    c2 = c1 * -2.0 * math.cos((2.0*math.pi*fq) / clm.get_srate())
    return clm.make_filter(3, [c1,c2,c1], [0.0, c2, ((1.0 - c) * c1)])
    
@cython.ccall
def butter(gen: clm.mus_any, insig: cython.double) -> cython.double:
    return clm.filter(gen, insig) 
      

# --------------- Biquads ---------------- #

@cython.ccall
def make_biquad(a0,a1,a2,b1,b2):
    """returns a biquad filter (use with the CLM filter gen)"""
    return clm.make_filter(3, [a0,a1,a2], [0.0,b1,b2])

@cython.ccall
def make_local_biquad(a0, a1, a2, gamma, beta):
    return make_biquad(a0, a1, a2, (-2.0 * gamma), (2.0 * beta))

@cython.ccall
def make_iir_low_pass_2(fc, din):
    theta = (2 * math.pi * fc) / clm.get_srate()
    d = math.sin(theta) * ( (din or math.sqrt(2.0)) / 2.0)
    beta = .5 * ((1.0 - d) / (1.0 + d))
    gamma = (.5 + beta) * math.cos(theta)
    alpha = (.5 * ((.5 + beta) - gamma))
    return make_local_biquad(alpha, 2.0*alpha, alpha, gamma, beta)

@cython.ccall
def make_iir_band_pass_2(f1, f2):
    theta = (2 * math.pi * math.sqrt(f1*f2)) / clm.get_srate()
    t2 = math.tan(theta / (2 * (math.sqrt(f1*f2) / (f2-f1))))
    beta = .5 * ((1.0-t2)/(1.0+t2))
    gamma = (.5 * beta) * math.cos(theta)
    alpha = .5 - beta
    return make_local_biquad(alpha, 0.0, -alpha, gamma, beta)

@cython.ccall
def make_iir_band_stop_2(f1, f2):
    theta = (2 * math.pi * math.sqrt(f1*f2)) / clm.get_srate()
    t2 = math.tan(theta / (2 * (math.sqrt(f1*f2) / (f2-f1))))
    beta = .5 * ((1.0-t2)/(1.0+t2))
    gamma = (.5 * beta) * math.cos(theta)
    alpha = .5 + beta
    return make_local_biquad(alpha, -2.0*gamma, alpha, gamma, beta)

@cython.ccall
def biquad(gen: clm.mus_any, insig: cython.double) -> cython.double:
    clm.filter(gen, insig)

