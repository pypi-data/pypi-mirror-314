# cython: c_string_type=unicode
# cython: c_string_encoding=utf8

#==================================================================================
# The code is part of an attempt at translation of Bill Schottstedaet's sndlib 
# available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

#==================================================================================
# In Bill's original he has a nice mechanism for defining generators that I initially
# attempted to replicate but it did not really work well with compiled code 
# so I used a cdef class approach 
#==================================================================================



cimport cython
import numpy as np
cimport numpy as np
#cimport pysndlib.cclm as cclm
cimport pysndlib.clm as clm
from pysndlib.sndlib cimport Sample, Header

np.import_array()

cdef class CLMGenerator:
    cpdef cython.double next(self, cython.double  fm=*)

# --------------- nssb ---------------- #
cdef class Nssb(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double ratio
    cdef public cython.int n
    cdef public cython.double angle

    
cpdef cython.double nssb (Nssb gen, cython.double fm=*)
cpdef cython.bint is_nssb(gen)
    
# --------------- nxysin ---------------- #
cdef class Nxysin(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double ratio
    cdef public cython.int n
    cdef public cython.double angle
    cdef public cython.double norm

cpdef cython.double nxysin(Nxysin gen, cython.double fm=*)
cpdef cython.bint is_nxysin(gen)

# --------------- nxycos ---------------- #
cdef class Nxycos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio 
    cdef public cython.int n 
    cdef public cython.double angle 

cpdef cython.double nxycos(Nxycos gen, cython.double fm =*)
cpdef cython.bint is_nxycos(gen)
   
# --------------- nxy1cos ---------------- #
cdef class Nxy1cos(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double ratio
    cdef public cython.int n
    cdef public cython.double angle 

cpdef cython.double nxy1cos(Nxy1cos gen, cython.double fm =*)
cpdef cython.bint is_nxy1cos(gen)

# --------------- nxy1sin ---------------- #
cdef class Nxy1sin(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double ratio
    cdef public cython.int n
    cdef public cython.double angle

cpdef cython.double nxy1sin(Nxy1sin gen, cython.double fm =*)
cpdef cython.bint is_nxy1sin(gen)

# --------------- Noddcos ---------------- #
cdef class Noddcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio 
    cdef public cython.int n 
    cdef public cython.double angle 


cpdef cython.double noddcos(Noddcos gen, cython.double fm=*)
cpdef cython.bint is_noddcos(gen)

# --------------- noddssb ---------------- #
cdef class Noddssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio 
    cdef public cython.double n
    cdef public cython.double angle 

cpdef cython.double noddssb(Noddssb gen, cython.double fm=*)
cpdef cython.bint is_noddssb(gen)

# --------------- ncos2 ---------------- #
cdef class Ncos2(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.int n
    cdef public cython.double angle 
    
cpdef cython.double ncos2(Ncos2 gen, cython.double fm=*)
cpdef cython.bint is_ncos2(gen)

# --------------- ncos4 ---------------- #
cdef class Ncos4(Ncos2):
    pass

cpdef cython.double ncos4(Ncos4 gen, cython.double fm=*)
cpdef cython.bint is_ncos4(gen)

# --------------- npcos ---------------- #      
cdef class Npcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double angle 

cpdef cython.double npcos(Npcos gen, cython.double fm=*)
cpdef cython.bint is_npcos(gen)

# --------------- ncos5 ---------------- #  
cdef class Ncos5(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double angle 

cpdef cython.double ncos5(Ncos5 gen, cython.double fm=*)
cpdef cython.bint is_ncos5(gen)


# --------------- nsin5 ---------------- #  

cdef class Nsin5(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double angle 
    cdef public cython.double norm 

cpdef cython.double nsin5(Nsin5 gen, cython.double fm=*)
cpdef cython.bint is_nsin5(gen)

# --------------- nrsin ---------------- #  
    
cpdef cython.double nrsin(clm.mus_any gen, cython.double fm=*)
cpdef cython.bint is_nrsin(gen)

# 
# --------------- nrcos ---------------- #  
cdef class Nrcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double r
    cdef public cython.double angle 
    cdef public cython.double rr
    cdef public cython.double r1 
    cdef public cython.double e1 
    cdef public cython.double e2 
    cdef public cython.double norm 
    cdef public cython.bint trouble

cpdef cython.double nrcos(Nrcos gen, cython.double fm=*)
cpdef cython.bint is_nrcos(gen)

# --------------- nrssb ---------------- #
cdef class Nrssb(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double ratio 
    cdef public cython.double n
    cdef public cython.double r 
    cdef public cython.double angle
    cdef public cython.double interp
    cdef public cython.double rn
    cdef public cython.double rn1
    cdef public cython.double norm
    cpdef call_interp(self, cython.double fm =*, cython.double interp=*)

cpdef cython.double nrssb(Nrssb gen, cython.double fm=*)
cpdef cython.double nrssb_interp(Nrssb gen, cython.double fm=*,cython.double interp =* )
cpdef cython.bint is_nrssb(gen)

# --------------- nkssb ---------------- #  
cdef class Nkssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double n
    cdef public cython.double angle
    cdef public cython.double norm
    cdef public cython.double interp
    cpdef cython.double call_interp(self, cython.double fm=*, cython.double interp=*)
    
cpdef cython.double nkssb(Nkssb gen, cython.double fm=*)
cpdef cython.double nkssb_interp(Nkssb gen, cython.double fm=*, cython.double interp=*)
cpdef cython.bint is_nkssb(gen)

# --------------- nsincos ---------------- #  
cdef class Nsincos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double angle
    cdef public cython.double n2
    cdef public cython.double cosn
    cdef public cython.double norm
    
cpdef cython.double nsincos(Nsincos gen, cython.double fm=*)
cpdef cython.bint is_nsincos(gen)

# --------------- n1cos ---------------- #  

cdef class N1cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double angle
    
cpdef cython.double n1cos(N1cos gen, cython.double fm=*)
cpdef cython.bint is_n1cos(gen)

# TODO: --------------- npos1cos ---------------- #  

cdef class Npos1cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double angle

cpdef cython.double npos1cos(Npos1cos gen, cython.double fm=*)
cpdef cython.bint is_npos1cos(gen)

# --------------- npos3cos ---------------- #  
cdef class Npos3cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double angle
cpdef cython.double npos3cos(Npos3cos gen, cython.double fm=*)
cpdef cython.bint is_npos3cos(gen)
# --------------- rcos ---------------- #

cdef class Rcos(CLMGenerator):
    cdef public clm.mus_any osc
    cdef public cython.double r
    cdef public cython.double rr
    cdef public cython.double rrp1
    cdef public cython.double rrm1
    cdef public cython.double r2
    cdef public cython.double norm 

cpdef cython.double rcos(Rcos gen, cython.double fm=*)
cpdef cython.bint is_rcos(gen)


# --------------- rssb ---------------- #  

cdef class Rssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double angle


    cpdef cython.double call_interp(self, cython.double fm=*, cython.double interp=*)
    
cpdef cython.double rssb(Rssb gen, cython.double fm=*)
cpdef cython.double rssb_interp(Rssb gen, cython.double fm=*, cython.double interp=*)
cpdef cython.bint is_rssb(gen)

# --------------- rxysin ---------------- #  

cdef class Rxysin(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double angle
    cdef public cython.double rr
    cdef public cython.double r2    
 
cpdef cython.double rxysin(Rxysin gen, cython.double fm=*)
cpdef cython.bint is_rxysin(gen)   

# --------------- rxycos ---------------- #  

cdef class Rxycos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double angle
    cdef public cython.double rr
    cdef public cython.double r2
    cdef public cython.double norm
    
cpdef cython.double rxycos(Rxycos gen, cython.double fm=*)
cpdef cython.bint is_rxycos(gen)   


#  --------------- safe-rxycos ---------------- #  

cdef class SafeRxycos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double angle
    cdef public cython.double cutoff
    cpdef clamp_rxycos_r(self, cython.double fm=*)
    
cpdef cython.double safe_rxycos(SafeRxycos gen, cython.double fm=*)
cpdef cython.bint is_safe_rxycos(gen)

# --------------- ercos ---------------- #  
cdef class Ercos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double angle
    cdef public cython.double cosh_t
    cdef public cython.double offset
    cdef public cython.double scaler
    cdef public clm.mus_any osc
    
cpdef cython.double ercos(Ercos gen, cython.double fm=*)
cpdef cython.bint is_ercos(gen)

# --------------- erssb ---------------- #  
cdef class Erssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double angle

cpdef cython.double erssb(Erssb gen, cython.double fm=*)
cpdef cython.bint is_erssb(gen)


# --------------- r2sin ---------------- #  
# removed


# --------------- r2cos ---------------- #  
cdef class R2cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double angle

cpdef cython.double r2cos(R2cos gen, cython.double fm=*)
cpdef cython.bint is_r2cos(gen)

# --------------- r2ssb ---------------- #  

cdef class R2ssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double angle
    cdef public clm.mus_any osc

cpdef cython.double r2ssb(R2ssb gen, cython.double fm=*)
cpdef cython.bint is_r2ssb(gen)

# --------------- eoddcos ---------------- #  

cdef class Eoddcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public clm.mus_any osc

cpdef cython.double eoddcos(Eoddcos gen, cython.double fm=*)
cpdef cython.bint is_eoddcos(gen)


# --------------- rkcos ---------------- #  

cdef class Rkcos(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double r
    cdef public cython.double norm
    cdef public clm.mus_any osc

cpdef cython.double rkcos(Rkcos gen, cython.double fm=*)
cpdef cython.bint is_rkcos(gen)

# --------------- rksin ---------------- #  

cdef class Rksin(CLMGenerator):

    cdef public cython.double frequency
    cdef public cython.double r
    cdef public cython.double angle
    
cpdef cython.double rksin(Rksin gen, cython.double fm=*)
cpdef cython.bint is_rksin(gen)

# --------------- rkssb ---------------- #  

cdef class Rkssb(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double r
    cdef public cython.double norm
    cdef public clm.mus_any osc

cpdef cython.double rkcos(Rkcos gen, cython.double fm=*)
cpdef cython.bint is_rkcos(gen)


# --------------- rk!cos ---------------- #  
cdef class Rkfcos(CLMGenerator):

    cdef public cython.double frequency
    cdef public cython.double r
    cdef public cython.double angle
    cdef public cython.double norm
    
cpdef cython.double rkfcos(Rkfcos gen, cython.double fm=*)
cpdef cython.bint is_rkfcos(gen)


# --------------- rk!ssb ---------------- #  

cdef class Rkfssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double angle

cpdef cython.double rkfssb(Rkfssb gen, cython.double fm=*)
cpdef cython.bint is_rkfssb(gen)

# TODO: --------------- rxyk!sin ---------------- # 
# remove rxyksin in clm

# TODO: --------------- rxyk!cos ---------------- # 
# remove rxykcos in clm

# --------------- r2k!cos ---------------- # 

cdef class R2kfcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double k 
    cdef public cython.double rr1
    cdef public cython.double r2
    cdef public clm.mus_any osc
    cdef public cython.double norm
    
cpdef cython.double r2kfcos(R2kfcos gen, cython.double fm=*)
cpdef cython.bint is_r2kfcos(gen)

# --------------- k2sin ---------------- # 

cdef class K2sin(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double angle
    
cpdef cython.double k2sin(K2sin gen, cython.double fm=*)
cpdef cython.bint is_k2sin(gen)

# --------------- k2cos ---------------- # 

cdef class K2cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double angle
    
cpdef cython.double k2cos(K2cos gen, cython.double fm=*)
cpdef cython.bint is_k2cos(gen)

# --------------- k2ssb ---------------- # 

cdef class K2ssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double angle
    
cpdef cython.double k2ssb(K2ssb gen, cython.double fm=*)
cpdef cython.bint is_k2ssb(gen)

# --------------- dblsum ---------------- # 

cdef class Dblsum(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double angle
    
cpdef cython.double dblsum(Dblsum gen, cython.double fm=*)
cpdef cython.bint is_dblsum(gen)


# --------------- rkoddssb ---------------- #
cdef class Rkoddssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio 
    cdef public cython.double r
    cdef public cython.double rr1
    cdef public cython.double angle 
    cdef public cython.double norm 
    
cpdef cython.double rkoddssb(Rkoddssb gen, cython.double fm=*)
cpdef cython.bint is_rkoddssb(gen)

# --------------- krksin ---------------- # 

cdef class Krksin(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double angle
    
cpdef cython.double krksin(Krksin gen, cython.double fm=*)
cpdef cython.bint is_krksin(gen)

# --------------- abssin ---------------- # 

cdef class Absin(CLMGenerator):
    cdef public cython.double frequency 
    cdef public clm.mus_any osc
    
cpdef cython.double absin(Absin gen, cython.double fm=*)
cpdef cython.bint is_absin(gen)

# --------------- abscos ---------------- # 

cdef class Abcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double a
    cdef public cython.double b
    cdef public cython.double angle
    cdef public cython.double ab
    cdef public cython.double norm
    
cpdef cython.double abcos(Abcos gen, cython.double fm=*)
cpdef cython.bint is_abcos(gen)

# --------------- r2k2cos ---------------- # 

cdef class R2k2cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double angle
    cdef cython.double r2k2cos_norm(self, cython.double a)
    
cpdef cython.double r2k2cos(R2k2cos gen, cython.double fm=*)
cpdef cython.bint is_r2k2cos(gen)

# --------------- blsaw ---------------- # 

cdef class Blsaw(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double n
    cdef public cython.double r
    cdef public cython.double angle
    
cpdef cython.double blsaw(Blsaw gen, cython.double fm=*)
cpdef cython.bint is_blsaw(gen)


# TODO: add I variant--------------- asyfm ---------------- # 

cdef class Asyfm(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double r
    cdef public cython.double index
    cdef public cython.double angle
    cpdef cython.double next_i(self, cython.double fm =*)
    cpdef cython.double next_j(self, cython.double fm =*)
    
cpdef cython.double asyfm(Asyfm gen, cython.double fm=*)
cpdef cython.double asyfm_i(Asyfm gen, cython.double fm=*)
cpdef cython.double asyfm_j(Asyfm gen, cython.double fm=*)
cpdef cython.bint is_asyfm(gen)
# 
# --------------- bess ---------------- # 

cdef class Bess(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.int n
    cdef public cython.double angle
    cdef public cython.double norm
    
cpdef cython.double bess(Bess gen, cython.double fm=*)
cpdef cython.bint is_bess(gen)


# --------------- jjcos ---------------- # 
cdef class Jjcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double a
    cdef public cython.double k
    cdef public cython.double angle
    
cpdef cython.double jjcos(Jjcos gen, cython.double fm=*)
cpdef cython.bint is_jjcos(gen)

# --------------- j0evencos ---------------- # 
cdef class J0evencos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double index
    cdef public cython.double angle
    
cpdef cython.double j0evencos(J0evencos gen, cython.double fm=*)
cpdef cython.bint is_j0evencos(gen)

# --------------- j2cos ---------------- # 


cdef class J2cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.int n
    cdef public cython.double r
    cdef public cython.double angle
    cdef public cython.double norm
    
cpdef cython.double j2cos(J2cos gen, cython.double fm=*)
cpdef cython.bint is_j2cos(gen)


# --------------- jpcos ---------------- # 

cdef class Jpcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double a
    cdef public cython.double k
    cdef public cython.double angle
    
cpdef cython.double jpcos(Jpcos gen, cython.double fm=*)
cpdef cython.bint is_jpcos(gen)
# 


# --------------- jncos ---------------- # 
cdef class Jncos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double a
    cdef public cython.int n
    cdef public cython.double angle
    cdef public cython.double ra
    
cpdef cython.double jncos(Jncos gen, cython.double fm=*)
cpdef cython.bint is_jncos(gen)

# --------------- j0j1cos  ---------------- # 

cdef class J0j1cos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double index
    cdef public cython.double angle
    
cpdef cython.double j0j1cos(J0j1cos gen, cython.double fm=*)
cpdef cython.bint is_j0j1cos(gen)

# --------------- jycos  ---------------- # 

cdef class Jycos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double a
    cdef cython.double angle
    
cpdef cython.double jycos(Jycos gen, cython.double fm=*)
cpdef cython.bint is_jycos(gen)

# --------------- jcos  ---------------- # 
cdef class Jcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.int n
    cdef public cython.double r
    cdef public cython.double a
    
cpdef cython.double jcos(Jcos gen, cython.double fm=*)
cpdef cython.bint is_jcos(gen)
 
# --------------- blackman  ---------------- # 
cdef class Blackman(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.int n
    cdef public clm.mus_any osc
    cpdef mus_reset(self)
    
cpdef cython.double blackman(Blackman gen, cython.double fm=*)
cpdef cython.bint is_blackman(gen)

# --------------- fmssb ---------------- #

cdef class Fmssb(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.double idx
    cdef public cython.double angle 

cpdef cython.double fmssb(Fmssb gen, cython.double fm=*)
cpdef cython.bint is_fmssb(gen)

# --------------- k3sin  ---------------- # 

cdef class K3sin(CLMGenerator):
    cdef public cython.double frequency 
    cdef public np.ndarray coeffs
    cdef public cython.double angle 
    
cpdef cython.double k3sin(K3sin gen, cython.double fm=*)
cpdef cython.bint is_k3sin(gen)


# --------------- izcos  ---------------- # # 
cdef class Izcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public cython.double angle 
    cdef public cython.double dc
    cdef public cython.double norm
    cdef public cython.double inorm

cpdef cython.double izcos(Izcos gen, cython.double fm=*)
cpdef cython.bint is_izcos(gen)
# 
# --------------- adjustable-square-wave ---------------- # 
# Note: modulating the duty factor will not work
cdef class AdjustableSquareWave(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double duty_factor
    cdef public cython.double amplitude
    cdef public cython.double sum
    cdef public clm.mus_any p1
    cdef public clm.mus_any p2
    
cpdef cython.double adjustable_square_wave(AdjustableSquareWave gen, cython.double fm=*)
cpdef cython.bint is_adjustable_square_wave(gen)
# # 
# --------------- adjustable-triangle-wave ---------------- # 
# 
cdef class AdjustableTriangleWave(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double duty_factor
    cdef public cython.double amplitude
    cdef public clm.mus_any gen
    cdef public cython.double top
    cdef public cython.double mtop
    cdef public cython.double scl
    cdef public cython.double val
    
cpdef cython.double adjustable_triangle_wave(AdjustableTriangleWave gen, cython.double fm=*)
cpdef cython.bint is_adjustable_triangle_wave(gen)
# 
# # 
# --------------- adjustable-sawtooth-wave ---------------- # 

cdef class AdjustableSawtoothWave(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double duty_factor
    cdef public cython.double amplitude
    cdef public clm.mus_any gen
    cdef public cython.double top
    cdef public cython.double mtop
    cdef public cython.double scl
    cdef public cython.double val
    
cpdef cython.double adjustable_sawtooth_wave(AdjustableSawtoothWave gen, cython.double fm=*)
cpdef cython.bint is_adjustable_sawtooth_wave(gen)
# # 
# TODO: --------------- adjustable-oscil-wave ---------------- # 

cdef class AdjustableOscil(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double duty_factor
    cdef public cython.double amplitude
    cdef public clm.mus_any gen
    cdef public cython.double top
    cdef public cython.double mtop
    cdef public cython.double scl
    cdef public cython.double val
    
cpdef cython.double adjustable_oscil(AdjustableOscil gen, cython.double fm=*)
cpdef cython.bint is_adjustable_oscil(gen)


# --------------- make-table-lookup-with-env ---------------- # 
cpdef make_table_lookup_with_env(frequency, pulse_env, size=*)

# --------------- make-wave-train-with-env ---------------- # 
cpdef make_wave_train_with_env(frequency, pulse_env, size=*)

# --------------- round-interp ---------------- # 
cdef class RoundInterp(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.int n
    cdef public cython.double amplitude
    cdef public clm.mus_any rnd
    cdef public clm.mus_any flt
    
cpdef cython.double round_interp(RoundInterp gen, cython.double fm=*)
cpdef cython.bint is_round_interp(gen)


# --------------- env-any functions ---------------- # 

# --------------- sine-env ---------------- # 
cpdef cython.double sine_env(e)

# --------------- square-env ---------------- # 
cpdef cython.double square_env(e)

# --------------- blackman4-env ---------------- # 
cpdef cython.double blackman4_env(e)

# --------------- multi-expt-env ---------------- # 
# going to be slow
#def multi_expt_env(e, expts):

# --------------- run-with-fm-and-pm ---------------- # 
# skip for now

# TODO: This is not working correctly --------------- nchoosekcos ---------------- # 
cdef class Nchoosekcos(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double ratio
    cdef public cython.int n
    cdef public cython.double angle
    
cpdef cython.double nchoosekcos(Nchoosekcos gen, cython.double fm=*)
cpdef cython.bint is_nchoosekcos(gen)
# 
# 
# # 
# TODO: --------------- sinc-train ---------------- # 

cdef class SincTrain(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.int n
    cdef public cython.double angle
    cdef public cython.double original_n
    cdef public cython.double original_frequency
    
cpdef cython.double sinc_train(SincTrain gen, cython.double fm=*)
cpdef cython.bint is_sinc_train(gen)

# --------------- pink-noise ---------------- # 
cdef class PinkNoise(CLMGenerator):
    cdef public cython.int n
    cdef public np.ndarray data 

cpdef cython.double pink_noise(PinkNoise gen, cython.double fm=*)
cpdef cython.bint is_pink_noise(gen)

# --------------- brown-noise ---------------- # 
cdef class BrownNoise(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double amplitude
    cdef public cython.double prev
    cdef public cython.double sum
    cdef public clm.mus_any gr
    
cpdef cython.double brown_noise(BrownNoise gen, cython.double fm=*)
cpdef cython.bint is_brown_noise(gen)
# 
# 
# --------------- green-noise ---------------- # 
cdef class GreenNoise(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double amplitude
    cdef public cython.double prev
    cdef public cython.double sum
    cdef public clm.mus_any gr
    cdef public cython.double low
    cdef public cython.double high
#     
# TODO: This is not working properly--------------- green-noise-interp ---------------- # 
cdef class GreenNoiseInterp(CLMGenerator):
    cdef public cython.double frequency
    cdef public cython.double amplitude
    cdef public cython.double sum
    cdef public cython.double low
    cdef public cython.double high
    cdef public cython.double dv
    cdef public cython.double incr
    cdef public cython.double angle
# 
# 
# 
# --------------- moving-sum ---------------- # 

cdef class MovingSum(CLMGenerator):
    cdef public cython.int n
    cdef public clm.mus_any gen

cpdef cython.double moving_sum(MovingSum gen, cython.double insig=*)
cpdef cython.bint is_moving_sum(gen)

# --------------- moving-variance ---------------- # 

cdef class MovingVariance(CLMGenerator):
    cdef public cython.int n
    cdef public clm.mus_any gen1
    cdef public clm.mus_any gen2

cpdef cython.double moving_variance(MovingVariance gen, cython.double insig=*)
cpdef cython.bint is_moving_variance(gen)

# --------------- moving-rms ---------------- # 

cdef class MovingRMS(CLMGenerator):
    cdef public cython.int n
    cdef public clm.mus_any gen

cpdef cython.double moving_rms(MovingRMS gen, cython.double insig=*)
cpdef cython.bint is_moving_rms(gen)

# --------------- moving-length ---------------- # 

cdef class MovingLength(MovingRMS):
    pass
    
cpdef cython.double moving_length(MovingLength gen, cython.double insig=*)
cpdef cython.bint is_moving_length(gen)

# --------------- weighted-moving-average---------------- # 

cdef class WeightedMovingAverage(CLMGenerator):
    cdef public cython.int n
    cdef public clm.mus_any dly
    cdef public cython.double num
    cdef public cython.double sum
    cdef public cython.double y
    cdef public cython.double den

cpdef cython.double weighted_moving_average(WeightedMovingAverage gen, cython.double insig=*)
cpdef cython.bint is_weighted_moving_average(gen)

# --------------- exponentially-weighted-moving-average---------------- # 

cdef class ExponentiallyWeightedMovingAverage(CLMGenerator):
    cdef public cython.int n
    cdef public clm.mus_any gen

cpdef cython.double exponentially_weighted_moving_average(ExponentiallyWeightedMovingAverage gen, cython.double insig=*)
cpdef cython.bint is_exponentially_weighted_moving_average(gen)

# --------------- polyoid ---------------- # 

cpdef cython.double polyoid(clm.mus_any gen, cython.double fm=*)
cpdef cython.bint is_polyoid(gen)


# # # TODO: these require potentially loading a file so
# # # wondering good way to do this. using maybe binary numpy files

# TODO: --------------- noid ---------------- # 
# TODO: --------------- knoid ---------------- # 
# TODO: --------------- roid ---------------- # 


# Removed --------------- waveshape ---------------- # 


# --------------- tanhsin ---------------- # 
cdef class Tanhsin(CLMGenerator):
    cdef public cython.double frequency 
    cdef public cython.double r
    cdef public clm.mus_any osc 

cpdef cython.double tanhsin(Tanhsin gen, cython.double fm=*)
cpdef cython.bint is_tanhsin(gen)   
# 
# --------------- moving-fft ---------------- # 

# cdef class MovingFFT(CLMGenerator):
#     cdef public clm.mus_any reader
#     cdef public cython.int n 
#     cdef public cython.int hop
#     cdef public cython.int outctr
#     cdef public np.ndarray rl
#     cdef public np.ndarray im
#     cdef public np.ndarray data
#     cdef public np.ndarray window
#     cdef last_moving_fft_window
#     cpdef mus_run(self, arg1, arg1)
# 
# cpdef cython.double moving_fft(MovingFFT gen)
# cpdef cython.bint is_moving_fft(gen)
# 
# # --------------- moving-spectrum ---------------- # 
# 
# 
# cdef class MovingSpectrum(CLMGenerator):
#     cdef public cython.int n 
#     cdef public cython.int hop
#     cdef public cython.int outctr
#     cdef public np.ndarray amps
#     cdef public np.ndarray phases
#     cdef public np.ndarray amp_incs
#     cdef public np.ndarray freqs
#     cdef public np.ndarray freq_incs
#     cdef public np.ndarray new_freq_incs
#     cdef public np.ndarray window
#     cdef public np.ndarray data
#     cdef public cython.long dataloc
# 
# cpdef cython.double moving_spectrum(MovingSpectrum gen)
# cpdef cython.bint is_moving_spectrum(gen)
# 
# 
# --------------- moving-scentroid ---------------- # 
# cdef class MovingScentroid(CLMGenerator):
#     cdef public cython.double dbfloor
#     cdef public cython.double rfreq
#     cdef public cython.int size
#     cdef public cython.int hop
#     cdef public cython.int outctr
#     cdef public cython.double curval
#     cdef public cython.double binwidth
#     cdef public np.ndarray rl
#     cdef public np.ndarray im
#     cdef public clm.mus_any dly
#     cdef public clm.mus_any rms
#     cdef public cython.double x
#     
# cpdef cython.double moving_scentroid(MovingScentroid gen, cython.double x=*)
# cpdef cython.bint is_moving_scentroid(gen)

# # --------------- moving-autocorrelation ---------------- # 
# 
# cdef class MovingAutocorrelation(CLMGenerator):
#     cdef public cython.int n 
#     cdef public cython.int hop
#     cdef public cython.int outctr
#     cdef public np.ndarray rl
#     cdef public np.ndarray im
#     cdef public np.ndarray data
# 
# cpdef cython.double moving_autocorrelation(MovingAutocorrelation gen)
# cpdef cython.bint is_moving_autocorrelationt(gen)
# 
# # --------------- moving-pitch ---------------- # 
# 
# cdef class MovingPitch(CLMGenerator):
#     cdef public cython.int n 
#     cdef public cython.int hop
#     cdef public clm.mus_any ac
#     cdef public cython.double val
# 
# cpdef cython.double moving_pitch(MovingPitch gen)
# cpdef cython.bint is_moving_pitch(gen)
# 
# # --------------- flocsig ---------------- # 
# 
# cdef class Flocsig(CLMGenerator):
#     cdef public cython.double reverb_amount
#     cdef public cython.double frequency
#     cdef public cython.double amplitude
#     cdef public cython.double offset
#     cdef public cython.int maxd
#     cdef public np.ndarray out1
#     cdef public np.ndarray out2
#     cdef public cython.long outloc
#     cdef public clm.mus_any ri
#     cdef public cython.long samp
#     cdef public cython.double insig
#     
# 
# cpdef cython.double flocsig(Flocsig gen, cython.long samp, cython.double insig)
# cpdef cython.bint is_flocsig(gen)
# """
