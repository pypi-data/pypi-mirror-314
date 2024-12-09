# cython: c_string_type=unicode
# cython: c_string_encoding=utf8

#==================================================================================
# The code is an attempt at translation of Bill Schottstedaet's 'dsp.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================


cimport cython
import numpy as np
import pysndlib.clm as clm
 
cimport pysndlib.clm as clm
from pysndlib.sndlib cimport Sample, Header
cpdef freqdiv(n, snd, chn, outname=*)
cpdef cython.double src_duration(e)
cpdef src_fit_envelope(e, target_dur)
cpdef cython.double highpass(clm.mus_any gen, cython.double insig)
cpdef cython.double lowpass(clm.mus_any gen, cython.double insig)
cpdef cython.double bandpass(clm.mus_any gen, cython.double insig)
cpdef cython.double bandstop(clm.mus_any gen, cython.double insig)
cpdef cython.double butter(clm.mus_any gen, cython.double insig)
cpdef cython.double biquad(clm.mus_any gen, cython.double insig)
