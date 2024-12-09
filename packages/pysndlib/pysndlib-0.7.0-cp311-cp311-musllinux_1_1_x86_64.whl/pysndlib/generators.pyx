#==================================================================================
# The code is part of an attempt at translation of Bill Schottstedaet's sndlib 
# available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

import cython
import random
import pysndlib.clm as clm
cimport pysndlib.clm as clm
import numpy as np
cimport numpy as np

import math
## TODO: Look into using cimports for c math for c . as here - https://cython.readthedocs.io/en/latest/src/tutorial/pure.html?highlight=math#calling-c-functions
from math import sin, fabs, cos, tan, pow, fabs, floor, cosh, exp, sinh, atan2, log, acos, sqrt, ceil, tanh

cdef cython.double NEARLY_ZERO = 1.0e-10
cdef cython.double TWO_PI = math.pi * 2
cdef cython.double PI = math.pi

cdef class CLMGenerator:
    cpdef cython.double next(self, cython.double fm =0.0):
        pass

# --------------- nssb ---------------- #
cdef class Nssb(CLMGenerator):

    def __init__(self, frequency, ratio=1., n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.angle = 0.0
           
    cpdef cython.double next(self, cython.double fm =0.0) :
        cdef cython.double cx  = self.angle
        cdef cython.double mx  = cx * self.ratio
        cdef cython.double den  = sin(.5 * mx)
        cdef cython.double n  = self.n
        self.angle += fm + self.frequency
        if fabs(den) <  NEARLY_ZERO:
            # return -1.0 in original but seems to cause weird inconsistencies
            den = NEARLY_ZERO
        
        return ((sin(cx) * sin(mx * ((n + 1.) / 2.)) * sin((n * mx) / 2.)) - 
                (cos(cx) * .5 * (den + sin(mx * (n + .5))))) /  ((n + 1.) * den)
    
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)

 
cpdef Nssb make_nssb(frequency=0, ratio=1., n=1):
    """
    Creates an nssb generator. nssb is the single side-band version of ncos and nsin. It is very similar to nxysin and nxycos.
    
    :param frequency: frequency in hz
    :param ratio: 
    :return: Nssb gen
    """
    return Nssb(frequency, ratio, n)
    
     
cpdef cython.double nssb(Nssb gen, cython.double fm = 0.):
    """
    returns n sinusoids from frequency spaced by frequency * ratio.
    
    :param gen: nssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
     
cpdef cython.bint is_nssb(gen):
    """
    returns True if gen is an nssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nssb)

# --------------- nxysin ---------------- #
 
def nodds(x, n):
    den = sin(x)
    num = sin(n * x)
    if den == 0.0:
        return 0.0
    else:
        return (num*num) / den
        
def find_nxysin_max(n, ratio):
    def ns(x, n):
        a2 = x / 2
        den = sin(a2)
        if den == 0.0:
            return 0.0
        else:
            return (sin(n*a2) * sin((1 + n) * a2)) / den
            
    def find_mid_max(n, lo, hi):
        mid = (lo + hi) / 2
        ylo = ns(lo, n)
        yhi = ns(hi, n)
        if fabs(ylo - yhi) < NEARLY_ZERO:
            return ns(mid,n)
        else:
            if ylo > yhi:
                return find_mid_max(n, lo, mid)   
            else:
                return find_mid_max(n, mid, hi)    
    
    def find_nodds_mid_max(n, lo, hi):
        mid = (lo + hi) / 2
        ylo = nodds(lo, n)
        yhi = nodds(hi, n)
        if fabs(ylo - yhi) < NEARLY_ZERO:
            return nodds(mid,n)
        else:
            if ylo > yhi:
                return find_nodds_mid_max(n, lo, mid)   
            else:
                return find_nodds_mid_max(n, mid, hi)    
            
    if ratio == 1:
        return find_mid_max(n, 0.0, PI / (n + .5))
    elif ratio == 2:
        return find_nodds_mid_max(n, 0.0, PI / ((2 * n) + .5))
    else:
        return n   


cdef class Nxysin(CLMGenerator):
    
    def __init__(self, frequency, ratio=1.0, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.angle = 0.0
        self.norm = 1.0 / find_nxysin_max(self.n, self.ratio)


    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x  = self.angle
        cdef cython.double y  = x * self.ratio
        cdef cython.double den  = sin(y * .5)
        cdef cython.double n  = self.n
        cdef cython.double norm  = self.norm
        self.angle += fm + self.frequency
        if fabs(den) <  NEARLY_ZERO:
            return 0.0
        return ((sin(x + (0.5 * (n - 1) * y)) * sin(0.5 * n * y) * norm) / den)
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
 

cpdef Nxysin make_nxysin(frequency=0, ratio=1., n=1):
    """
    Creates an nxysin generator that produces a sum of 'n' sinsoids starting at 'frequency', spaced by 'frequency'.
    
    :param frequency: frequency in hz
    :param ratio: 
    :param n: 
    :return: nssb gen
    
    """
    return Nxysin(frequency, ratio, n)

cpdef cython.double nxysin(Nxysin gen, cython.double fm=0.):
    """
    returns n sines from frequency spaced by frequency * ratio.
    
    :param gen: nxysin gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)

cpdef cython.bint is_nxysin(gen):
    """
    returns True if gen is an nxysin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nxysin)        

# --------------- nxycos ---------------- #

cdef class Nxycos(CLMGenerator):
    
    def __init__(self, frequency, ratio=1., n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.angle = 0.0
    
  
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x  = self.angle
        cdef cython.double y  = x * self.ratio
        cdef cython.double den  = sin(y * .5)
        cdef cython.double n = self.n
        self.angle += fm + self.frequency
        if fabs(den) <  NEARLY_ZERO:
            return 1.
        return (cos(x + (0.5 * (n - 1) * y)) * sin(.5 * n * y)) / (n * den)
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Nxycos make_nxycos(frequency=0, ratio=1., n=1):
    """Creates an nxycos generator that produces a sum of 'n' sinsoids starting at 'frequency', spaced by 'frequency'."""
    return Nxycos(frequency, ratio, n)

cpdef cython.double nxycos(Nxycos gen, cython.double fm =0.):
    """
    returns n cosines from frequency spaced by frequency * ratio.

    :param gen: nxycos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)

cpdef cython.bint is_nxycos(gen):
    """
    returns True if gen is an nxycos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nxycos)        

      
# --------------- nxy1cos ---------------- #

cdef class Nxy1cos(CLMGenerator):
    
    def __init__(self, frequency, ratio=1.0, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double y = x * self.ratio
        cdef cython.double den = cos(y * .5)
        cdef cython.double n = self.n
        self.angle += self.frequency + fm
        if fabs(den) < NEARLY_ZERO:
            return -1.0
        else:
            return max(-1., min(1.0, (sin(n * y) * sin(x + ((n - .5) * y))) / (2 * n * den)))
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Nxy1cos make_nxy1cos(frequency=0, ratio=1., n=1):
    """
    Creates an nxy1co generator that produces a sum of 'n' sinsoids starting at 'frequency', spaced by 'frequency'. 
        nxy1cos is the same as nxycos, but every other component is multiplied by -1, and "n" produces 2n components.
    
    """
    return Nxy1cos(frequency, ratio, n)
    

cpdef cython.double nxy1cos(Nxy1cos gen, cython.double fm =0.):
    """
    
    :param gen: nxy1cos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    

cpdef cython.bint is_nxy1cos(gen):
    """
    returns True if gen is an nxy1cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nxy1cos)  


# --------------- nxy1sin ---------------- #

cdef class Nxy1sin(CLMGenerator):

    def __init__(self, frequency, ratio=1., n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.angle = 0.0
    

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x  = self.angle
        cdef cython.double y  = x * self.ratio
        cdef cython.double den  = cos(y * .5)
        cdef cython.double n = self.n
        self.angle += fm + self.frequency
        cdef cython.double res = (sin(x + (.5 * (n - 1) * (y + PI))) * sin(.5 * n * (y + PI))) / (n * den)
        return res
        
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Nxy1sin make_nxy1sin(frequency=0, ratio=1., n=1):
    """
    Creates an nxy1sin generator hat produces a sum of 'n' sinsoids starting at 'frequency', spaced by 'frequency'. 
    nxy1sin is the same as nxysin, but every other component is multiplied by -1, and "n" produces 2n components. 
    """
    return Nxy1sin(frequency, ratio, n)


cpdef cython.double nxy1sin(Nxy1sin gen, cython.double fm =0.):
    """
    
    :param gen: nxy1sin gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    

cpdef cython.bint is_nxy1sin(gen):
    """
    returns True if gen is an nxy1sin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nxy1sin)        


# --------------- noddsin ---------------- #

def find_noddsin_max(n):    
    def find_mid_max(n=n, lo=0.0, hi= PI / ((2 * n) + 0.5)):
        mid = (lo + hi) / 2
        ylo = nodds(lo, n)
        yhi = nodds(hi, n)
        if fabs(ylo - yhi) < 1.0e-9:
            return nodds(mid,n)
        else:
            if ylo > yhi:
                return find_mid_max(n, lo, mid)   
            else:
                return find_mid_max(n, mid, hi)
    return find_mid_max(n)
    

@cython.cclass
cdef class Noddsin(CLMGenerator):
    
    def __init__(self, frequency, ratio=1., n=1):
        noddsin_maxes = np.zeros(100, dtype=np.double) # temporary
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = max(n, 1)
        self.norm = 1.
        if not (self.n < 100 and noddsin_maxes[self.n] > 0.0) :
            noddsin_maxes[self.n] = find_noddsin_max(self.n)
        else:
            self.norm = 1.0 / noddsin_maxes[self.n]
        self.angle = 0.0


    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double n = <cython.double>self.n
        cdef cython.double snx = sin(n * self.angle)
        cdef cython.double den = sin(self.angle)
        self.angle += fm + self.frequency
        if fabs(den) < NEARLY_ZERO:
            return 0.0
        else:
            return (self.norm * snx * snx) / den
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Noddsin make_noddsin(frequency=0, ratio=1., n=1):
    """
    Creates an noddsin generator that produces 'n' odd-numbered sines spaced by 'frequency'.
    """
    return Noddsin(frequency, ratio, n)


cpdef cython.double noddsin(Noddsin gen, cython.double fm =0.):
    """
    returns n odd-numbered sines spaced by ratio.
    
    :param gen: noddsin gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)


cpdef cython.bint is_noddsin(gen):
    """
    returns True if gen is an noddsin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Noddsin) 


# --------------- noddcos ---------------- #

cdef class Noddcos(CLMGenerator):
    
    def __init__(self, frequency, ratio=1., n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.angle = 0.0


    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double cx = self.angle
        cdef cython.double n = self.n
        cdef cython.double den = 2 * self.n * sin(self.angle)
        cdef cython.double fang = 0.
        self.angle += fm + self.frequency
        
        if fabs(den) < NEARLY_ZERO:
            fang = cx % TWO_PI
            if (fang < .001) or (fabs(fang - (2 * PI)) < .001):
                return 1.0
            else: 
                return -1.0
        else:
            return sin(2 * n * cx) / den
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)


cpdef Noddcos make_noddcos(frequency=0, ratio=1., n=1):
    """
    Creates an noddcos generator that produces 'n' odd-numbered cosines spaced by 'frequency'.
    """
    return Noddcos(frequency, ratio, n)

cpdef cython.double noddcos(Noddcos gen, cython.double fm =0.):
    """
    returns n odd-numbered sines spaced by ratio.
    
    :param gen: noddcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
   
cpdef cython.bint is_noddcos(gen):
    """
    returns True if gen is an noddcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Noddcos)        
    

# --------------- noddssb ---------------- #

cdef class Noddssb(CLMGenerator):
    
    def __init__(self, frequency, ratio, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.angle = 0.0

  
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double cx = self.angle
        cdef cython.double mx = cx * self.ratio
        cdef cython.double x = cx - mx
        cdef cython.double n = self.n
        cdef cython.double sinnx = sin(n * mx)
        cdef cython.double den = n * sin(mx)
        self.angle += fm + self.frequency
        if fabs(den) <  NEARLY_ZERO:
            if (mx % TWO_PI) < .1: #TODO something is wrong here
                return -1
#             else: # removed seemed like it causing large spikes
#                 return 1
        return (sin(x) * ((sinnx*sinnx) / den)) - ((cos(x) * (sin(2 * n * mx) / (2 * den))))
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Noddssb make_noddssb(frequency=0, ratio=1., n=1):
    """
    Creates an noddssb generator that produces 'n' sinusoids from frequency spaced by 2 * 'ratio' * 'frequency'.
    """
    return Noddssb(frequency, ratio, n)
    

cpdef cython.double noddssb(Noddssb gen, cython.double fm =0.):
    """
    Returns n sinusoids from frequency spaced by 2 * ratio * frequency.
    
    :param gen: noddssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    

cpdef cython.bint is_noddssb(gen):
    """
    returns True if gen is an noddssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Noddssb)   

# --------------- ncos2 ---------------- #


cdef class Ncos2(CLMGenerator):
    
    def __init__(self, frequency, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.angle = 0.0
    

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double den = sin(.5 * x)
        cdef cython.double n = self.n
        self.angle += fm + self.frequency
        if fabs(den) < NEARLY_ZERO:
            return 1.0
        else:
            val: cython.double = sin(0.5 * (n + 1) * x) / ((n + 1) * den)
            return val * val
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Ncos2 make_ncos2(frequency=0, n=1):
    """
    Creates an ncos2 (Fejer kernel) generator that will produce n sinusoids spaced by frequency scaled by (n-k)/(n+1)
    """
    return Ncos2(frequency, n)
    

cpdef cython.double ncos2(Ncos2 gen, cython.double fm =0.):
    """
    returns n cosines from frequency spaced by frequency * ratio.
        
    :param gen: ncos2 gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)


cpdef cython.bint is_ncos2(gen):
    """
    returns True if gen is an ncos2

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Ncos2)        
       
# --------------- ncos4 ---------------- #

cdef class Ncos4(Ncos2):

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double val = super(Ncos4, self).next(fm)
        return val * val
                

cpdef Ncos4 make_ncos4(frequency=0, n=1):
    """
    Creates an ncos4 (Jackson kernel) generator that produces 'n' sinusoids spaced by 'frequency' scaled by ((n-k)/(n+1))^2
    """
    return Ncos4(frequency, n)
    

cpdef cython.double ncos4(Ncos4 gen, cython.double fm =0.):
    """
    returns n cosines from frequency spaced by frequency * ratio.
    
    :param gen: ncos4 gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)


cpdef cython.bint is_ncos4(gen):
    """
    returns True if gen is an ncos4

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Ncos4)      
 
# --------------- npcos ---------------- #      

cdef class Npcos(CLMGenerator):
    
    def __init__(self, frequency, n):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double result  = 0.0
        cdef cython.double result1  = 0.0
        cdef cython.double result2  = 0.0
        cdef cython.double den  = sin(.5 * self.angle)
        cdef cython.double n = self.n
        if fabs(den) < NEARLY_ZERO:
            result = 1.0
        else:
            n1 = n + 1
            val = sin(.5 * n1 * self.angle) / (n1 * den)
            result1 = val * val
            p2n2 = (2 * n) + 2
            val = sin(.5 * p2n2 * self.angle) / (p2n2 * den)
            result2 = val * val
            result = (2 * result2) - result1
        self.angle += fm + self.frequency
        return result
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Npcos make_npcos(frequency=0, n=1):
    """
    Creates an npcos (Poussin kernel) generator that produces 
    n*2+1 sinusoids spaced by frequency with amplitudes in a sort of tent shape.
    """
    return Npcos(frequency, n)


cpdef cython.double npcos(Npcos gen, cython.double fm =0.):
    """
    returns n*2+1 sinusoids spaced by frequency with amplitudes in a sort of tent shape.
    
    :param gen: npcos gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)

cpdef cython.bint is_npcos(gen):
    """
    returns True if gen is an npcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Npcos)        


# --------------- ncos5 ---------------- #  


cdef class Ncos5(CLMGenerator):
    
    def __init__(self, frequency, n):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.angle = 0.0
    

    cpdef cython.double next(self, cython.double fm =0.0):
        x: cython.double = self.angle
        den: cython.double = tan(.5 * x)
        n: cython.double = self.n
        self.angle += fm + self.frequency
        if fabs(den) < NEARLY_ZERO:
            return 1.0
        else:
            return ((sin(n*x) / (2 * den)) - .5) / (n - .5)
               
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Ncos5 make_ncos5(frequency=0, n=1):
    """
    Creates an ncos5 generator that produces 'n' cosines spaced by 'frequency'. 
    All are equal amplitude except the first and last at half amp.
    """
    return Ncos5(frequency, n)


cpdef cython.double ncos5(gen: Ncos5, cython.double fm =0.):
    """
    returns n cosines spaced by frequency. All are equal amplitude except the first and last at half amp
    
    :param gen: ncos5 gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
  
cpdef cython.bint is_ncos5(gen):
    """
    returns True if gen is an ncos5

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Ncos5) 
    
                  
# --------------- nsin5 ---------------- #  

def find_nsin5_max(n):
    def ns(x, n):
            den = tan(.5 * x)
            if fabs(den) < NEARLY_ZERO:
                return 0.0
            else:
                return (1.0 - cos(n * x)) / den
                
    def find_mid_max(n, lo, hi):
        mid = (lo + hi) / 2
        ylo = ns(lo, n)
        yhi = ns(hi, n)
        if fabs(ylo - yhi) < 1e-9:
            return ns(mid,n)
        else:
            if ylo > yhi:
                return find_mid_max(n, lo, mid)   
            else:
                return find_mid_max(n, mid, hi)
                
    return find_mid_max(n, 0.0, PI / (n + .5))


cdef class Nsin5(CLMGenerator):
    
    def __init__(self, frequency, n):
        self.frequency = clm.hz2radians(frequency)
        self.n = max(2, n)
        self.angle = 0.0
        self.norm = find_nsin5_max(self.n)
    

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double den = tan(.5 * x)
        cdef cython.double n = self.n
        self.angle += fm + self.frequency
        if fabs(den) < NEARLY_ZERO:
            return 0.0
        else:
            return (1.0 - cos(n*x)) / (den * self.norm)

                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

cpdef Nsin5 make_nsin5(frequency=0, n=1):
    """
    Creates an nsin5 generator that produces 'n' sines spaced by 'frequency'. 
    All are equal amplitude except last at half amp.
    """
    return Nsin5(frequency, n)
    
cpdef cython.double nsin5(Nsin5 gen, cython.double fm =0.):
    """
    :param gen: noddssb gen
    :param fm: fm input
    :rtype: float
    """

    return gen.next(fm)
    
cpdef cython.bint is_nsin5(gen):
    """
    returns True if gen is an nsin5

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nsin5)  


# --------------- nrsin ---------------- #  
    
cpdef clm.mus_any make_nrsin(frequency=0, n=1, r=.5):
    return clm.make_nrxysin(frequency, 1., n, r)
    
cpdef cython.double nrsin(clm.mus_any gen, cython.double fm=0.):
    """
    :param gen: nrsin gen
    :param fm: fm input
    :rtype: float
    """
    return clm.nrxysin(gen, fm)
    
cpdef cython.bint is_nrsin(gen):
    return clm.is_nrxysin(gen)   
# --------------- nrcos ---------------- #  

cdef class Nrcos(CLMGenerator):
    
    def __init__(self, frequency, n=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.n = 1 + n
        self.r = clm.clamp(r, -.999999, .999999)
        self.angle = 0.0
        self.rr = self.r * self.r
        self.r1 = 1.0 + self.rr
        self.e1 = pow(self.r, self.n)
        self.e2 = pow(self.r, self.n + 1)
        self.norm = ((pow(fabs(self.r), self.n) - 1.0) / (fabs(self.r) - 1.)) - 1.0
        self.trouble = (self.n == 1) or (fabs(self.r) < NEARLY_ZERO)

    

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double rcos = self.r * cos(self.angle)
        self.angle += fm + self.frequency
        if self.trouble:
            return 0.0
        else: 
            return ((rcos + (self.e2 * cos((self.n - 1) * x))) - (self.e1 * cos(self.n * x)) - self.rr) / (self.norm * (self.r1 + (-2.0 * rcos)))
                
    def __call__(self, fm: cython.double=0.):
        return self.next(fm)
        
        
    @property
    def mus_order(self) -> cython.double:
        return self.n -1

    @mus_order.setter
    def mus_order(self, val: cython.double):
        self.n = 1 + val
        self.e1 = pow(self.r, self.n)
        self.e2 = pow(self.r, (self.n + 1))
        self.norm = ((pow(fabs(self.r), self.n) - 1.0) / (fabs(self.r) - 1.)) - 1.0
        self.trouble = (self.n == 1) or (abs(self.r) < NEARLY_ZERO)
 
    @property
    def mus_frequency(self) -> cython.double:
        return clm.radians2hz(self.frequency)
    
    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.frequency = clm.hz2radians(val)
    
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = min(.999999, max(-.999999, val))
        absr: cython.double = fabs(self.r)
        self.rr = self.r * self.r
        self.r1 = 1.0 + self.rr
        self.norm = ((pow(absr, self.n) - 1) / (absr - 1)) - 1.0
        self.trouble = ((self.n == 1) or (absr < NEARLY_ZERO))

        

cpdef Nrcos make_nrcos(frequency=0, n=1, r=.5):
    """
    Creates an nrcos generator that produces 'n' cosines 
    spaced by 'frequency' with amplitudes scaled by r^k.
    """
    return Nrcos(frequency, n, r)
    
cpdef cython.double nrcos(Nrcos gen, cython.double fm =0.):
    """
    returns n cosines spaced by frequency with amplitudes scaled by r^k.
        
    :param gen: nrcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_nrcos(gen):
    """
    returns True if gen is an nrcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nrcos)         
 
# --------------- nrssb ---------------- #

cdef class Nrssb(CLMGenerator):

    def __init__(self, frequency, ratio=1.0, n=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n
        self.r = clm.clamp(r, 0.0, .999999)
        self.rn = -pow(self.r, self.n)
        self.rn1 = pow(self.r, (self.n + 1))
        self.norm = (self.rn - 1) / (self.r - 1)
        self.angle = 0.0
#         print(self.frequency,  self.ratio , self.n, self.r , self.rn , self.rn1,self.norm )
    

    cpdef cython.double next(self, fm: cython.double =0.0):
        cdef cython.double cx = self.angle
        cdef cython.double mx = cx * self.ratio
        cdef cython.double nmx = self.n * mx
        cdef cython.double n1mx = (self.n - 1) * mx
        cdef cython.double den = self.norm * (1.0 + (-2.0 * self.r * cos(mx)) + (self.r * self.r))
        self.angle += fm + self.frequency
        cdef cython.double a = (sin(cx) * ((self.r * sin(mx)) + (self.rn * sin(nmx)) + (self.rn1 * sin(n1mx))))
        cdef cython.double b = (cos(cx) * (1.0 + (-1. * self.r * cos(mx)) + (self.rn * cos(nmx)) + (self.rn1 * cos(n1mx))))
        return (a - b) / den

    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        

    cpdef call_interp(self, cython.double fm =0.0, cython.double interp=0.0):
        cdef cython.double cx = self.angle
        cdef cython.double mx = cx * self.ratio
        cdef cython.double nmx = self.n * mx
        cdef cython.double n1mx = (self.n - 1) * mx
        cdef cython.double den = self.norm * (1.0 + (-2.0 * self.r * cos(mx)) + (self.r * self.r))
        self.angle += fm + self.frequency
        cdef cython.double a = interp * (sin(cx) * ((self.r * sin(mx)) + (self.rn * sin(nmx)) + (self.rn1 * sin(n1mx))))
        cdef cython.double b = (cos(cx) * (1.0 + (-1. * self.r * cos(mx)) + (self.rn * cos(nmx)) + (self.rn1 * cos(n1mx))))
        return (a - b) / den
      
        
        
cpdef Nrssb make_nrssb(frequency=0, ratio=1.0, n=1, r=.5) :
    """
    Creates an nrssb generator that produces returns n sinusoids from 
    frequency spaced by frequency * ratio with amplitudes scaled by r^k.
    """
    return Nrssb(frequency, ratio, n, r)
    
cpdef cython.double nrssb(Nrssb gen, cython.double fm =0.):
    """returns n sinusoids from frequency spaced by frequency * ratio with amplitudes scaled by r^k.
    
    :param gen: nrssb gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.double nrssb_interp(Nrssb gen, cython.double fm=0.,cython.double interp =0. ):
    """
    returns n sinusoids from frequency spaced by frequency * ratio with amplitudes scaled by r^k.
        
    :param gen: nrssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.call_interp(fm)
    
cpdef cython.bint is_nrssb(gen):
    """
    returns True if gen is an nrssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nrssb)                   

# --------------- nkssb ---------------- #  

cdef class Nkssb(CLMGenerator):

    
    def __init__(self, frequency, ratio=1.0, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.n = n + 1
        self.norm = 1.0 / (.5 * self.n * (self.n - 1.))
        self.angle = 0.0
        self.interp = 0.0

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle * self.ratio
        cdef cython.double cxx = self.angle - x
        cdef cython.double sx2 = sin(.5 * x)
        cdef cython.double nx = self.n * x
        cdef cython.double nx2 = .5 * ((2*self.n) - 1) * x
        cdef cython.double sx22 = 2.0 * sx2
        cdef cython.double sxsx = 4 * sx2 * sx2
        cdef cython.double s1
        cdef cython.double c1
        self.angle += fm + self.frequency
        if fabs(sx2) < NEARLY_ZERO:
             return -1. # TODO original has -1 but that seems wrong
        
        s1 = (sin(nx) / sxsx) - ((self.n * cos(nx2)) / sx22)
        c1 = (sin(nx2) / sx22) - ((1.0 - cos(nx)) / sxsx)
        return ((s1 * sin(cxx)) - (c1 * cos(cxx))) * self.norm
    
    cpdef cython.double call_interp(self, cython.double fm=0.0, cython.double interp=0.0):
        cdef cython.double x = self.angle * self.ratio
        cdef cython.double cxx = self.angle - x
        cdef cython.double sx2 = sin(.5 * x)
        cdef cython.double nx = self.n * x
        cdef cython.double nx2 = .5 * ((2*self.n) - 1) * x
        cdef cython.double sx22 = 2.0 * sx2
        cdef cython.double sxsx = 4 * sx2 * sx2
        cdef cython.double s1
        cdef cython.double c1
        self.angle += fm + self.frequency
        if fabs(sx2) < NEARLY_ZERO:
            return 1. 
        else:
            s1 = (sin(nx) / sxsx) - ((self.n * cos(nx2)) / sx22)
            c1 = (sin(nx2) / sx22) - ((1.0 - cos(nx))/ sxsx)
            return ((c1 * cos(cxx)) - (interp * sin(cxx) * s1)) * self.norm
    
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        
    @property
    def mus_order(self) -> cython.double:
        return self.n -1

    @mus_order.setter
    def mus_order(self, val: cython.double):
        self.n = 1 + val
        self.norm = 1.0 / (.5 * val * (val - 1.))

cpdef Nkssb make_nkssb(frequency=0, ratio=1.0, n=1):
    """
    Creates an nkssb generator that produces n sinusoids from 
    frequency spaced by frequency * ratio with amplitude k.
    """
    return Nkssb(frequency, ratio, n)
    
cpdef cython.double nkssb(Nkssb gen, cython.double fm=0.):
    """
    produces n sinusoids from frequency spaced by frequency * ratio with amplitude k
    
        
    :param gen: nkssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.double nkssb_interp(Nkssb gen, cython.double fm=0., cython.double interp=0.0):
    """
    returns n sinusoids from frequency spaced by frequency * ratio 
    with amplitude k. The 'interp' argument determines whether the 
    sidebands are above (1.0) or below (-1.0) frequency.
    """
    return gen.call_interp(fm, interp)
    
cpdef cython.bint is_nkssb(gen):
    """
    returns True if gen is an nkssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nkssb)    



# --------------- nsincos ---------------- #  

cdef class Nsincos(CLMGenerator):
    
    def __init__(self, frequency, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.n2 = (n + 1) / 2
        self.cosn = cos(PI / (n + 1))
        self.norm = 0.0
        for k in range(1,n):
            self.norm += sin((k*PI) / (n + 1)) / sin(PI / (n + 1))
        self.angle = 0.0
    

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double num = cos(self.n2 * x)
        self.angle += fm + self.frequency
        return (num*num) / (self.norm * (cos(x) - self.cosn))

                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        

cpdef Nsincos make_nsincos(frequency=0, n=1):
    return Nsincos(frequency, n)
    
cpdef cython.double nsincos(Nsincos gen, cython.double fm=0.):
    """
    :param gen: nsincos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_nsincos(gen):
    """
    returns True if gen is an nsincos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nsincos)    
     
    
# 
# --------------- n1cos ---------------- #  

cdef class N1cos(CLMGenerator):

    def __init__(self, frequency, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.angle = 0.0
        
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double tn = tan(.5 * x)
        self.angle += fm + self.frequency
        if fabs(tn) < 1.0e-6:
            return 1.
        else:
            return (1.0 - cos(self.n * x)) / (tn * tn * self.n * self.n * 2)
            
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)    

cpdef N1cos make_n1cos(frequency=0, n=1):
    """
    Creates an n1cos generator that produces a spikey waveform similar to ncos2
    """
    return N1cos(frequency, n)
    
cpdef cython.double n1cos(N1cos gen, cython.double fm=0.):
    """
    :param gen: n1cos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_n1cos(gen):
    """
    returns True if gen is an n1cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, N1cos)    
     

# --------------- npos1cos ---------------- #  

cdef class Npos1cos(CLMGenerator):

    def __init__(self, frequency, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double num = ((self.n + 2) * sin((self.n * x) / 2)) - (self.n * sin(((self.n + 2) * x) / 2))
        #cdef cython.double num = ((self.n + 2) * math.sin((self.n*x) / 2)) - (self.n * math.sin(1.0 / ((self.n + 2) * 2)))
        cdef cython.double sx = sin(x / 2.)
        cdef cython.double den = 4 * self.n * (self.n + 1) * (self.n + 2) * sx * sx * sx * sx
        self.angle += fm + self.frequency
        if fabs(den) < NEARLY_ZERO:
            return 0.0
        else:
            return (3 * num * num) / den
                                
            
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)    

cpdef Npos1cos make_npos1cos(frequency=0, n=1):
    """
    Creates an nsincos generator that produces n cosines spaced 
    by frequency with amplitude sin(k*pi/(n+1))/sin(pi/(n+1))
    """
    return Npos1cos(frequency, n)
    
cpdef cython.double npos1cos(Npos1cos gen, cython.double fm=0.):
    """
    produces n cosines spaced by frequency with amplitude sin(k*pi/(n+1))/sin(pi/(n+1))
    
    :param gen: npos1cos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_npos1cos(gen):
    """
    returns True if gen is an npos1cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Npos1cos)    
     

# --------------- npos3cos ---------------- #  

cdef class Npos3cos(CLMGenerator):

    def __init__(self, frequency, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double sx = sin(x / 2.)
        cdef cython.double den = ((4*self.n) + 2) * sx * sx
        self.angle += fm + self.frequency
        if fabs(den) < NEARLY_ZERO:
            return 1.0 * self.n
        else:
            return (2 - cos(self.n * x) - cos((self.n + 1) * x)) / den
                                
            
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)    

cpdef Npos3cos make_npos3cos(frequency=0, n=1):
    """
    creates an npos3cos generator that produces n cosines spaced by frequency.
    """
    return Npos3cos(frequency, n)
    
cpdef cython.double npos3cos(Npos3cos gen, cython.double fm=0.):
    """
    produces n cosines spaced by frequency
        
    :param gen: npos3cos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_npos3cos(gen):
    """
    returns True if gen is an npos3cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Npos3cos)    

# --------------- rcos ---------------- #

cdef class Rcos(CLMGenerator):
    
    def __init__(self, frequency, r):
        self.osc = clm.make_oscil(frequency, .5 * PI)
        self.r = clm.clamp(r, -.999999, .999999)
        self.rr = self.r * self.r
        self.rrp1 = 1.0 + self.rr
        self.rrm1 = 1.0 - self.rr
        self.r2 = 2. * self.r
        cdef cython.double absr = fabs(self.r)
        self.norm = 0.0 if absr < NEARLY_ZERO else (1.0 - absr) /  ( 2.0 * absr)
    

    cpdef cython.double next(self, cython.double fm =0.0):
        return ((self.rrm1 / (self.rrp1 - (self.r2 * clm.oscil(self.osc, fm)))) - 1.0) * self.norm

                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
    @property
    def mus_frequency(self) -> cython.double:
        return clm.osc.mus_frequency
    
    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        clm.osc.mus_frequency = val
        
    @property
    def mus_scale(self) -> cython.double:
        return self.r
    
    @mus_scale.setter
    def mus_scale(self, val: cython.double):
        self.r = clm.clamp(val, -.999999, .999999)
        self.rr = self.r*self.r
        self.rrp1 = 1.0 + self.rr
        self.rrm1 = 1.0 - self.rr
        self.r2 = 2.0 * self.r
        absr: cython.double = fabs(self.r)
        self.norm = 0.0 if absr < NEARLY_ZERO else (1.0 - absr) /  ( 2.0 * absr)


cpdef Rcos make_rcos(frequency=0, r=1):
    """
    Creates an rcos generator that produces many cosines spaced by frequency with amplitude r^k.
    """
    return Rcos(frequency, r)
    
cpdef cython.double rcos(Rcos gen, cython.double fm =0.):
    """
    returns many cosines spaced by frequency with amplitude r^k
        
    :param gen: rcos gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_rcos(gen):
    """
    returns True if gen is an rcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rcos)    


# --------------- rssb ---------------- #  

cdef class Rssb(CLMGenerator):

    def __init__(self, frequency, ratio=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = r
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double angle1 = self.angle
        cdef cython.double angle2 = angle1 * self.ratio
        cdef cython.double carsin = sin(angle1)
        cdef cython.double canrcos = sin(angle1)
        cdef cython.double den = 1.0 + (self.r * self.r) + (-2.0 * self.r * cos(angle2))
        cdef cython.double sumsin = self.r * sin(angle2)
        cdef cython.double sumcos = 1.0 - (self.r * cos(angle2))
        self.angle += fm + self.frequency
        return (carsin * sumsin) - (canrcos * sumcos) / (2.0 * den)

    cpdef cython.double call_interp(self, cython.double fm=0.0, cython.double interp=0.0):
        
        cdef cython.double angle1 = self.angle
        cdef cython.double angle2 = angle1 * self.ratio
        cdef cython.double carsin = sin(angle1)
        cdef cython.double canrcos = sin(angle1)
        cdef cython.double den = 1.0 + (self.r * self.r) + (-2.0 * self.r * cos(angle2))
        cdef cython.double sumsin = self.r * sin(angle2)
        cdef cython.double sumcos = 1.0 - (self.r * cos(angle2))
        self.angle += fm + self.frequency
        return (carsin * sumsin) - (interp * canrcos * sumcos) / (2.0 * den)
                          
            
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)    
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = clm.clamp(val, -.99999, .99999)
    

cpdef Rssb make_rssb(frequency, ratio=1,r=.5):
    """
    creates an rssb generator that produces many cosines from frequency spaced by frequency * ratio with amplitude r^k."
    """
    return Rssb(frequency, ratio, r)
    
cpdef cython.double rssb(Rssb gen, cython.double fm=0.):
    """returns many cosines from frequency spaced by frequency * ratio with amplitude r^k."""
    return gen.next(fm)
    
cpdef cython.double rssb_interp(Rssb gen, cython.double fm=0., cython.double interp=0.):
    """returns many cosines from frequency spaced by frequency * ratio 
    with amplitude r^k. The 'interp' argument determines whether the sidebands 
    are above (1.0) or below (-1.0) frequency
    
        
    :param gen: rssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.call_interp(fm)
    
cpdef cython.bint is_rssb(gen):
    """
    returns True if gen is an rssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rssb) 
    
    
# 
# --------------- rxysin ---------------- #  

cdef class Rxysin(CLMGenerator):  
    
    def __init__(self, frequency, ratio=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = clm.clamp(r, -.99999,.99999)
        self.r2 = -2.0 * self.r
        self.rr = 1.0 + (self.r*self.r)
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double y = x * self.ratio
        self.angle += fm + self.frequency
        return (sin(x) - (self.r * sin(x - y))) / (self.rr + (self.r2 * cos(y)))

                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = clm.clamp(val, -.99999,.99999)
        self.r2 = -2.0 * self.r
        self.rr = 1.0 + (self.r*self.r)

cpdef Rxysin make_rxysin(frequency=0, ratio=1, r=.5):
    """
    creates an rxysin generator (similar to rssb) that produces many sines from frequency spaced by frequency * ratio with amplitude r^k."
    """
    return Rxysin(frequency, ratio, r)
    
cpdef cython.double rxysin(Rxysin gen, cython.double fm=0.):
    """
    returns many sines from frequency spaced by frequency * ratio with amplitude r^k.
    
        
    :param gen: rxysin gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_rxysin(gen):
    """
    returns True if gen is an rxysin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rxysin)  


 
# --------------- rxycos ---------------- #  

cdef class Rxycos(CLMGenerator):
    
    def __init__(self, frequency, ratio=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = clm.clamp(r, -.99999,.99999)
        self.r2 = -2.0 * self.r
        self.rr = 1.0 + (self.r*self.r)
        self.norm = 1.0 - fabs(self.r)
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double y = x * self.ratio
        self.angle += fm + self.frequency
        return ((cos(x) - (self.r * cos(x - y))) / (self.rr + (self.r2 * cos(y)))) * self.norm

                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    @property
    def mus_frequency(self) -> cython.double:
        return clm.radians2hz(self.frequency)
    
    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.frequency = clm.hz2radians(val)
    
    

cpdef Rxycos make_rxycos(frequency=0, ratio=1, r=.5):
    """
    creates an rxycos generator that produces many cosines 
    from frequency spaced by frequency * ratio with amplitude r^k.
    """
    return Rxycos(frequency, ratio, r)
    
cpdef cython.double rxycos(Rxycos gen, cython.double fm=0.):    
    """
    returns many cosines from frequency spaced by frequency * ratio with amplitude r^k.
        
    :param gen: rxycos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_rxycos(gen):
    """
    returns True if gen is an rxycos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rxycos)     
    
      
# 
# --------------- safe-rxycos ---------------- #    

cdef class SafeRxycos(CLMGenerator):

    def __init__(self, frequency, ratio=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = self.clamp_rxycos_r(0.0)
        self.angle = 0.0
        self.cutoff = .001

        
    cpdef clamp_rxycos_r(self, cython.double fm=0.0):
        cdef maxr = self.cutoff**( 1.0 /  floor((TWO_PI / (3.0 * self.ratio * (fm + self.frequency))) - (1.0 / self.ratio)))
        if self.r >= 0.0:
            return min(self.r, maxr)
        else:
            return max(self.r, -maxr)
        
        
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double y = x * self.ratio
        cdef maxr = 0.0
        self.angle += fm + self.frequency
        
        if fm != 0.0:
            self.r = self.clamp_rxycos_r(fm)
        return ((cos(x) - (self.r * cos(x - y))) /  (1.0 + (-2.0 * self.r * cos(y)) + (self.r*self.r))) * (1.0 - fabs(self.r))

                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = val
        self.r = self.clamp_rxycos_r(0.0)
         
    @property
    def mus_frequency(self) -> cython.double:
        return clm.radians2hz(self.frequency)

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.frequency = clm.hz2radians(val)
        self.r = self.clamp_rxycos_r(0.0)  
        
    @property
    def mus_offset(self) -> cython.double:
        return self.ratio

    @mus_offset.setter
    def mus_offset(self, val: cython.double):
        self.ratio = val
        self.r = self.clamp_rxycos_r(0.0)    
        

cpdef SafeRxycos make_safe_rxycos(frequency=0, ratio=1, r=.5):
    """
    creates a safe-rxycos generator that produces many cosines from 
    frequency spaced by frequency * ratio with amplitude r^k where 'r' is restricted to a safe value.
    """
    return SafeRxycos(frequency, ratio, r)
    
cpdef cython.double safe_rxycos(SafeRxycos gen, cython.double fm=0.):
    """
    returns many cosines from frequency spaced by frequency * ratio with amplitude r^k where 'r' is restricted to a safe value.
        
    :param gen: safe_rxycos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_safe_rxycos(gen):
    """
    returns True if gen is an safe_rxycos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, SafeRxycos)     



# --------------- ercos ---------------- #  

cdef class Ercos(CLMGenerator):

    def __init__(self, frequency, r=.5):
        self.frequency = frequency
        self.r = max(r, .00001)
        self.cosh_t = cosh(self.r)
        self.osc = clm.make_polywave(self.frequency, [0,self.cosh_t, 1, -1.], clm.Polynomial.SECOND_KIND)
        expt_t = exp(-self.r)
        self.offset = (1.0 - expt_t) / (2.0 * expt_t)
        self.scaler = sinh(self.r) * self.offset

    cpdef cython.double next(self, cython.double fm=0.0):
        return (self.scaler / clm.polywave(self.osc, fm) - self.offset)
                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.osc.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.osc.mus_phase = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.frequency = val
        

cpdef Ercos make_ercos(frequency=0, r=.5):
    """
    creates an ercos generator (a special case of rcos) that produces 
    many cosines from frequency with amplitude e^(-kr).
    """
    return Ercos(frequency, r)
    
cpdef cython.double ercos(Ercos gen, cython.double fm=0.):
    """
    returns many cosines from frequency with amplitude e^(-kr).
        
    :param gen: ercos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_ercos(gen):
    """
    returns True if gen is an ercos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Ercos)     

# 
# --------------- erssb ---------------- #  

cdef class Erssb(CLMGenerator):
      
    def __init__(self, frequency, ratio=1.0, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = r
        self.angle = 0.0
    

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double cx = self.angle
        cdef cython.double mx = cx * self.ratio
        cdef cython.double cxx = cx - mx
        cdef cython.double ccmx = cosh(self.r) - cos(mx)
        
        self.angle += fm + self.frequency
        if fabs(ccmx) < NEARLY_ZERO:
            return 1.
        else:
            return ((cos(cxx)*((sinh(self.r) / ccmx) - 1.0)) - (sin(cxx)*(sin(mx) / ccmx))) / (2.0 * (1.0 / (1.0 - exp(-self.r))) - 1.0)
                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        

cpdef Erssb make_erssb(frequency=0, ratio=1.0, r=.5):
    """
    creates an erssb generator (a special case of rssb) the produces 
    many sinusoids from frequency spaced by frequency * ratio with amplitude e^(-kr).
    """
    return Erssb(frequency, ratio, r)
    
cpdef cython.double erssb(Erssb gen, cython.double fm=0.):
    """
    returns many sinusoids from frequency spaced by frequency * ratio with amplitude e^(-kr).
     
    :param gen: erssb gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_erssb(gen):
    """
    returns True if gen is an erssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Erssb)    
     



# --------------- r2sin ---------------- #  
# bil removed 



# --------------- r2cos ---------------- #  
cdef class R2cos(CLMGenerator):

    def __init__(self, frequency, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        if (self.r*self.r) >= 1.0:
            self.r = 0.9999999
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        self.angle += self.frequency + fm
        return ((cosh(self.r * cos(x)) * cos(self.r * sin(x))) - 1.0) / (cosh(self.r) - 1.0)

    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        
cpdef R2cos make_r2cos(frequency=0, r=.5):
    """
    creates an r2sin generator that produces many even-numbered 
    sines from frequency with amplitude r^(2k)/(2k)!.
    """
    return R2cos(frequency, r)
    
cpdef cython.double r2cos(R2cos gen, cython.double fm=0.):
    """
    returns many even-numbered sines from frequency with amplitude r^(2k)/(2k)!.
    
        
    :param gen: r2cos gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_r2cos(gen):
    """
    returns True if gen is an r2cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, R2cos)  

# --------------- r2ssb ---------------- #  

cdef class R2ssb(CLMGenerator):

    def __init__(self, frequency, ratio=1., r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = r
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double cx = self.angle
        cdef cython.double mx = cx * self.ratio
        cdef cython.double a = self.r
        cdef cython.double asinx = a * sin(mx)
        cdef cython.double acosx = a * cos(mx)
        
        self.angle += self.frequency + fm
        return ((cos(cx) * cosh(acosx) * cos(asinx)) - (sin(cx) * sinh(acosx) * sin(asinx))) / cosh(a)

    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        
cpdef R2ssb make_r2ssb(frequency=0, ratio=1., r=.5):
    """
    creates an r2ssb generator that produces many even-numbered sinusoids 
    from frequency spaced by frequency * ratio, if that makes any sense, with amplitude r^(2k)/(2k)!.
    """
    return R2ssb(frequency, ratio, r)
    
cpdef cython.double r2ssb(R2ssb gen, cython.double fm=0.):
    """
    returns many even-numbered sinusoids from frequency spaced by frequency * ratio, if that makes any sense, with amplitude r^(2k)/(2k)!.
    
    :param gen: r2ssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_r2ssb(gen):
    """
    returns True if gen is an r2ssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, R2ssb)  


# --------------- eoddcos ---------------- #  

cdef class Eoddcos(CLMGenerator):

    def __init__(self, frequency, r=1.):
        self.frequency = frequency
        self.r = r
        self.osc = clm.make_oscil(self.frequency, .5*PI)


    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double sinha = sinh(self.r)
        if clm.is_zero(sinha):
            return 0.0
        return atan2(clm.oscil(self.osc, fm), sinha) / atan2(1.0, sinha)
        
                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.osc.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.osc.mus_phase = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.osc.mus_frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.osc.mus_frequency = val
        

cpdef Eoddcos make_eoddcos(frequency=0, r=1.):
    """
    creates an eoddcos generator that produces many cosines 
    from spaced by frequency with amplitude e^(-r).
    """
    return Eoddcos(frequency, r)
    
cpdef cython.double eoddcos(Eoddcos gen, cython.double fm=0.):
    """
    returns many cosines from spaced by frequency with amplitude e^(-r).
        
    :param gen: eoddcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_eoddcos(gen):
    """
    returns True if gen is an eoddcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Eoddcos)    

# --------------- koddcos ---------------- #  
# removed by bill

# --------------- rkcos ---------------- #  

cdef class Rkcos(CLMGenerator):
    
    def __init__(self, frequency, r=.5):
        self.frequency = frequency
        self.osc = clm.make_oscil(self.frequency)
        self.r = clm.clamp(r, -.99999, .99999)
        self.norm = log(1.0 - fabs(self.r))

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double cs = clm.oscil(self.osc, fm)
        return (.5 * log(1.0 + (-2.0 * self.r * cs) + (self.r*self.r))) / self.norm
                
    def __call__(self, fm: cython.double=0.):
        return self.next(fm)
        
    @property
    def mus_phase(self) -> cython.double:
        return self.osc.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.osc.mus_phase = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.osc.mus_frequency
    
    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.osc.mus_frequency = val
    
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = clm.clamp(val, -.99999, .99999)


cpdef Rkcos make_rkcos(frequency=0, r=.5):
    """
    creates an rkcos generator that produces many cosines 
    from spaced by frequency with amplitude (r^k)/k.
    """
    return Rkcos(frequency, r)
    
cpdef cython.double rkcos(Rkcos gen, cython.double fm =0.):
    """
    returns many cosines from spaced by frequency with amplitude (r^k)/k.
        
    :param gen: rkcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_rkcos(gen):
    """
    returns True if gen is an rkcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rkcos)     


# --------------- rksin ---------------- #  
cdef class Rksin(CLMGenerator):
    
    def __init__(self, frequency, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.r = clm.clamp(r, .00001, .99999)
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        self.angle += fm + self.frequency
        return  atan2(self.r*sin(x), 1.0 - (self.r * cos(x))) / atan2(self.r*sin(acos(self.r)), (1.0 - (self.r * self.r)))
    
    def __call__(self, fm: cython.double=0.):
        return self.next(fm)
    
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = clm.clamp(val, .00001, .99999)


cpdef Rksin make_rksin(frequency=0, r=.5):
    """
    creates an rksin generator that produces many sines from spaced by frequency with amplitude (r^k)/k.
    """
    return Rksin(frequency, r)
    
cpdef cython.double rksin(Rksin gen, cython.double fm =0.):
    """
    returns many sines from spaced by frequency with amplitude (r^k)/k.
    
    :param gen: rksin gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_rksin(gen):
    """
    returns True if gen is an rksin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rksin)     



# --------------- rkssb ---------------- #  

cdef class Rkssb(CLMGenerator):

    def __init__(self, frequency, ratio=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = r
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double angle1 = self.angle
        cdef cython.double angle2 = angle1 * self.ratio
        cdef cython.double carsin = sin(angle1)
        cdef cython.double canrcos = sin(angle1)
        cdef cython.double den = 1.0 + (self.r * self.r) + (-2.0 * self.r * cos(angle2))
        cdef cython.double sumsin = self.r * sin(angle2)
        cdef cython.double sumcos = 1.0 - (self.r * cos(angle2))
        self.angle += fm + self.frequency
        return (carsin * sumsin) - (canrcos * sumcos) / (2.0 * den)
                                     
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)    
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = clm.clamp(val, -.99999, .99999)
    

cpdef Rkssb make_rkssb(frequency, ratio=1,r=.5):
    """
    creates an rkssb generator that produces many sinusoids from 
    frequency from spaced by frequency * ratio with amplitude (r^k)/k.
    """
    return Rkssb(frequency, ratio, r)
    
cpdef cython.double rkssb(Rkssb gen, cython.double fm=0.):
    """
    returns many sinusoids from frequency from spaced by frequency * ratio with amplitude (r^k)/k.
        
    :param gen: rkssb gen
    :param fm: fm input
    :rtype: float

    """
    return gen.next(fm)
    
cpdef cython.bint is_rkssb(gen):
    """
    returns True if gen is an rkssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rkssb) 
 
# --------------- rk!cos ---------------- #  

cdef class Rkfcos(CLMGenerator):
    
    def __init__(self, frequency, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.norm = 1.0 / (exp(fabs(self.r)) - 1.0 )
        self.angle = 0.0

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        self.angle += fm + self.frequency
        return ((exp(self.r*cos(x)) * cos(self.r*sin(x))) - 1.0) * self.norm
    
    def __call__(self, fm: cython.double=0.):
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.angle

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.angle = val
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = val
        self.norm = 1.0 / (exp(fabs(self.r)) - 1.0 )

cpdef Rkfcos make_rkfcos(frequency=0, r=.5):
    """
    creates an rkfcos (rkf!os) generator that produces many 
    cosines spaced by frequency with amplitude (r^k)/k!.
    """
    return Rkfcos(frequency, r)
    
cpdef cython.double rkfcos(Rkfcos gen, cython.double fm = 0.):
    """
    returns many cosines spaced by frequency with amplitude (r^k)/k!.
       
    :param gen: rkfcos gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_rkfcos(gen):
    """
    returns True if gen is an rkfcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rkfcos)     




# 
# --------------- rk!ssb ---------------- #  

cdef class Rkfssb(CLMGenerator):
      
    def __init__(self, frequency, ratio=1.0, r=1.0):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = r
        self.angle = 0.0
    

    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double cx = self.angle
        cdef cython.double mx = cx * self.ratio
        cdef cython.double ercosmx = exp(self.r*cos(mx))
        cdef cython.double rsinmx = self.r * sin(mx)
        self.angle += fm + self.frequency

        return (cos(cx) * ercosmx * cos(rsinmx) - sin(cx) * ercosmx * sin(rsinmx)) / exp(fabs(self.r))

    
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = val
        

cpdef Rkfssb make_rkfssb(frequency=0, ratio=1.0, r=.5):
    """
    creates an rkfssb (rk!ssb) generator that produces many sinusoids from frequency spaced by frequency * ratio with amplitude (r^k)/k!.
    """
    return Rkfssb(frequency, ratio, r)
    
cpdef cython.double rkfssb(Rkfssb gen, cython.double fm=0.):
    """
    returns many sinusoids from frequency spaced by frequency * ratio with amplitude (r^k)/k!.
    
    :param gen: rkfssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_rkfssb(gen):
    """
    returns True if gen is an rkfssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rkfssb)    
     



# 
# --------------- rxyk!cos---------------- # 

cdef class R2kfcos(CLMGenerator):

    def __init__(self, frequency, r=.5, k=0.0):
        self.frequency = frequency
        self.r = r
        self.k = k
        self.rr1 = 1.0 + (self.r*self.r)
        self.r2 = 2.0 * fabs(self.r)
        self.norm = (self.rr1 - self.r2)**(self.k)
        self.osc = clm.make_polywave(self.frequency, [0,self.rr1, 1, -self.r2], clm.Polynomial.SECOND_KIND)
        self.k = -self.k
       # print(f'self.frequency: {self.frequency} self.k: {self.k}, self.rr1: {self.rr1}, self.r2: {self.r2}, self.norm: {self.norm}, self.osc: {self.osc}')
    

    cpdef cython.double next(self, cython.double fm =0.0):
        return (clm.polywave(self.osc, fm)**self.k) * self.norm

    def __call__(self, fm=0.) -> cython.double:
        return self.next(fm)
        
    @property
    def mus_phase(self) -> cython.double:
        return self.osc.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.osc.mus_phase = val
    
    @property
    def mus_frequency(self) -> cython.double:
        return self.osc.mus_frequency
    
    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.osc.mus_frequency = val

    
cpdef R2kfcos make_r2kfcos(frequency=0, r=.5, k=.0):
    """
    creates an r2kfcos (r2k!cos) generator that produces many cosines 
    spaced by frequency with amplitude too messy to write down.
    """
    return R2kfcos(frequency, r, k)
    
cpdef cython.double r2kfcos(R2kfcos gen, cython.double fm =0.):
    """
    returns many cosines spaced by frequency with amplitude too messy to write down.
        
    :param gen: r2kfcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_r2kfcos(gen):
    """
    returns True if gen is an r2kfcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, R2kfcos)   

# 
# # TODO: --------------- rxyk!cos ---------------- # 
# 
# # TODO: --------------- r2k!cos ---------------- # 
# 
# --------------- k2sin ---------------- # 

cdef class K2sin(CLMGenerator):
    
    def __init__(self, frequency):
        self.frequency = clm.hz2radians(frequency)
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        self.angle += fm + self.frequency
        return (3.0 * sin(x) / (5.0 - (4.0 * cos(x))))
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef K2sin make_k2sin(frequency=0):
    """
    creates a k2sin generator that produces many sines 
    spaced by frequency with amplitude 1/(2^k).
    """
    return K2sin(frequency)
    
cpdef cython.double k2sin(K2sin gen, cython.double fm =0.):
    """
    returns many sines spaced by frequency with amplitude 1/(2^k).
        
    :param gen: k2sin gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_k2sin(gen):
    """
    returns True if gen is an k2sin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, K2sin)      



# 
# --------------- k2cos ---------------- # 

cdef class K2cos(CLMGenerator):
    
    def __init__(self, frequency):
        self.frequency = clm.hz2radians(frequency)
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        self.angle += fm + self.frequency
        return  ((3.0 / (5.0 - (4.0 * cos(x)))) - 1.0) * .5
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef K2cos make_k2cos(frequency=0):
    """
     creates a k2cos generator that produces many cosines 
     spaced by frequency with amplitude 1/(2^k).
    """
    return K2cos(frequency)
    
cpdef cython.double k2cos(K2cos gen, cython.double fm =0.):
    """
    returns many cosines spaced by frequency with amplitude 1/(2^k).

    :param gen: noddssb k2cos
    :param fm: fm input
    :rtype: float    
    """
    return gen.next(fm)
    
cpdef cython.bint is_k2cos(gen):
    """
    returns True if gen is an k2cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, K2cos) 

# --------------- k2ssb ---------------- # 
cdef class K2ssb(CLMGenerator):

    def __init__(self, frequency, ratio=1.):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.angle = 0.0
           
    cpdef cython.double next(self, cython.double fm =0.0) :
        cdef cython.double cx  = self.angle
        cdef cython.double mx  = cx * self.ratio

        self.angle += fm + self.frequency
        return ((3. * cos(cx))-(sin(cx) * 4.0 * sin(mx))) / (3.0 * (5.0 - (4.0 * cos(mx))))
    
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)

 
cpdef K2ssb make_k2ssb(frequency=0, ratio=1.):
    """
     creates a k2ssb generator that produces many sinusoids from 
     frequency spaced by frequency * ratio with amplitude 1/(2^k).
    """
    return K2ssb(frequency, ratio)
    
cpdef cython.double k2ssb(gen: K2ssb, fm: cython.double = 0.):
    """
    returns many sinusoids from frequency spaced by frequency * ratio with amplitude 1/(2^k).
        
    :param gen: k2ssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_k2ssb(gen):
    """
    returns True if gen is an k2ssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, K2ssb)



# --------------- dblsum ---------------- # 
cdef class Dblsum(CLMGenerator):
    
    def __init__(self, frequency, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        self.angle += fm + self.frequency
        cdef cython.double a = ((1 + self.r) * sin(.5 * x))
        cdef cython.double b = (1.0 + (-2.0 * self.r * cos(x)) + (self.r*self.r))
        return a / b
                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        
    @property
    def mus_frequency(self) -> cython.double:
        return clm.radians2hz(self.frequency * .5)
    
    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.frequency = clm.hz2radians(2*val)
        
cpdef Dblsum make_dblsum(frequency=0, r=.5):
    """
     creates a dblsum generator that produces many sines from frequency 
     spaced by frequency * (2k -1) with amplitude r^k (this is buggy)
    """
    return Dblsum(frequency, r)
    
cpdef cython.double dblsum(Dblsum gen, cython.double fm=0.):
    """
    returns many sines from frequency spaced by frequency * (2k -1) with amplitude r^k (this is buggy)
       
    :param gen: dblsum gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_dblsum(gen):
    """
    returns True if gen is an dblsum

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Dblsum)  
 
# --------------- rkoddssb ---------------- #

cdef class Rkoddssb(CLMGenerator):
    
    def __init__(self, frequency, ratio=1., r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = clm.clamp(r, -.999999, .999999)
        self.rr1 = 1.0 + (self.r*self.r)
        self.norm = 1.0 / (log(1.0 + self.r) - log(1.0 - self.r))
        self.angle = 0.0
    

    cpdef cython.double next(self, cython.double fm =0.0):
        cx: cython.double = self.angle
        mx: cython.double = cx * self.ratio
        cxx: cython.double = cx - mx
        cmx: cython.double = 2.0 * self.r * cos(mx)
        self.angle += fm + self.frequency
        return (((cos(cxx) * .5 * log((self.rr1+cmx) / (self.rr1-cmx))) - (sin(cxx) * (atan2((2.0 * self.r * sin(mx)), (1.0 - (self.r*self.r)))))) * self.norm)

                
    def __call__(self, fm=0.) -> cython.double:
        return self.next(fm)
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.r
    
    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = clm.clamp(val, -.999999, .9999999)
        self.rr1 = 1.0 + (self.r * self.r)
        self.norm = 1.0 / (log(1.0 + self.r) - log(1.0 - self.r))

cpdef Rkoddssb make_rkoddssb(frequency=0, ratio=1., r=.5):
    """
    creates an rkoddssb generator that produces many sinusoids from 
    frequency spaced by frequency * 2 * ratio with amplitude (r^(2k-1))/(2k-1).
    """
    return Rkoddssb(frequency, ratio, r)
    
cpdef cython.double rkoddssb(Rkoddssb gen, cython.double fm =0.):
    """
    returns many sinusoids from frequency spaced by frequency * 2 * ratio with amplitude (r^(2k-1))/(2k-1).

    :param gen: rkoddssb gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_rkoddssb(gen):
    """
    returns True if gen is an rkoddssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Rkoddssb)            
       
# --------------- krksin ---------------- #     
cdef class Krksin(CLMGenerator):

    def __init__(self, frequency, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double r1 = 1.0 - self.r
        cdef cython.double r3 = r1 if self.r > .9 else 1.0
        cdef cython.double den = 1.0 + (-2.0 * self.r * cos(x)) + (self.r*self.r)
        self.angle += self.frequency + fm
        return (r1 * r1 * r3 * sin(x)) / (den * den)

    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        
cpdef Krksin make_krksin(frequency=0, r=.5):
    """
    creates a krksin generator that produces many sines spaced by frequency with amplitude kr^k.
    """
    return Krksin(frequency, r)
    
cpdef cython.double krksin(Krksin gen, cython.double fm=0.):
    """
    returns many sines spaced by frequency with amplitude kr^k.
        
    :param gen: krksin gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_krksin(gen):
    """
    returns True if gen is an krksin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Krksin)  
    

# --------------- absin ---------------- # 
# In generators.scm this is called abssin but in docs it is absin
cdef class Absin(CLMGenerator):
    
    def __init__(self, frequency):
        self.frequency = frequency
        self.osc = clm.make_oscil(self.frequency)
        
    cpdef cython.double next(self, cython.double fm=0.0):
        return (fabs(clm.oscil(self.osc, fm)) - (2.0 / PI)) / (2.0 / PI)

                
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        
    @property
    def mus_frequency(self) -> cython.double:
        return self.osc.mus_frequency
    
    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.osc.mus_frequency = val
        
    @property
    def mus_phase(self) -> cython.double:
        return self.osc.mus_phase
    
    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.osc.mus_phase = val
    
    

cpdef Absin make_absin(frequency=0):
    """creates an absin generator (abs oscil)."""
    return Absin(frequency)
    
cpdef cython.double absin(Absin gen, cython.double fm=0.):
    """(abs oscil)
        
    :param gen: absin gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_absin(gen):
    """
    returns True if gen is an absin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Absin)     

# --------------- abcos ---------------- # 


cdef class Abcos(CLMGenerator):
    
    def __init__(self, frequency, a=.5, b=.25):
        self.frequency = clm.hz2radians(frequency)
        self.a = a
        self.b = b
        self.ab = sqrt((self.a*self.a) - (self.b*self.b))
        self.norm = .5 / ((1.0 - (fabs(self.ab - self.a) / self.b)) - 1.0)

    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        self.angle += fm + self.frequency
        return self.norm * ((self.ab / (self.a + ( self.b * cos(x)))) - 1.0)
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Abcos make_abcos(frequency=0, a=.5, b=.25):
    """
    creates an abcos generator that produces many cosines spaced 
    by frequency with amplitude (-a+sqrt(a^2-b^2))^k/b^k.
    """
    return Abcos(frequency, a, b)
    
cpdef cython.double abcos(Abcos gen, cython.double fm=0.):
    """
    returns many cosines spaced by frequency with amplitude (-a+sqrt(a^2-b^2))^k/b^k.
        
    :param gen: abcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_abcos(gen):
    """
    returns True if gen is an abcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Abcos) 

# --------------- r2k2cos ---------------- # 

cdef class R2k2cos(CLMGenerator):
    
    def __init__(self, frequency, r=1.0):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.angle = 0.0
        
    cdef cython.double r2k2cos_norm(self, cython.double a):
       return ((PI * cosh(PI * a)) / (2 * a * sinh(PI*a))) - (1.0 / (2 * a * a))
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        if x > TWO_PI:
            x = x % TWO_PI
        self.angle += fm + self.frequency
        return ((PI * (cosh(self.r*(PI-x))) / (sinh(self.r*PI))) - (1.0 / self.r)) / (2 * self.r * self.r2k2cos_norm(self.r))
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef R2k2cos make_r2k2cos(frequency=0, r=1.):
    """
    creates an r2k2cos generator that produces many cosines spaced by frequency with amplitude 1/(r^2+k^2).
    """
    return R2k2cos(frequency, r)
    
cpdef cython.double r2k2cos(R2k2cos gen, cython.double fm=0.):
    """
    returns many cosines spaced by frequency with amplitude 1/(r^2+k^2).
        
    :param gen: r2k2cos gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_r2k2cos(gen):
    """
    returns True if gen is an r2k2cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, R2k2cos) 



# # 
# --------------- blsaw ---------------- # 

cdef class Blsaw(CLMGenerator):
    
    def __init__(self, frequency, n=1, r=.5):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.r = r
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double a = self.r
        cdef cython.double N = self.n
        cdef cython.double x = self.angle
        cdef cython.double incr = self.frequency
        cdef cython.double den = 1.0 + (-2.0 * a * cos(x)) + (a*a)
        self.angle += fm + incr
        if fabs(den) < NEARLY_ZERO:
            return 0.0
        
        cdef cython.double s1 = (a**(N-1.)) * sin(((N-1.0)*x) + incr)
        cdef cython.double s2 = (a**N) * sin((N*x) + incr)
        cdef cython.double s3 = (a * sin(x + incr))
        
        return (sin(incr) + (-s3) + (-s2) + s1) / den
        
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Blsaw make_blsaw(frequency=0, n=1, r=.5):
    """ creates a blsaw generator that produces a band-limited sawtooth wave."""
    return Blsaw(frequency, r, n)
    
cpdef cython.double blsaw(Blsaw gen, cython.double fm=0.):
    """
    returns a band-limited sawtooth wave.

    :param gen: blsaw gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_blsaw(gen):
    """
    returns True if gen is an blsaw

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Blsaw) 


# # 
# --------------- asyfm ---------------- # 

cdef class Asyfm(CLMGenerator):
    
    def __init__(self, frequency, ratio=1., r=1., index=1.0):
        self.frequency = clm.hz2radians(frequency)
        self.ratio = ratio
        self.r = r
        self.index = index
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double r1 = 1 / self.r
        cdef cython.double one = -1.0 if self.r > 1.0 or (-1.0 < self.r < 0.0) else 1.0
        cdef cython.double modphase = self.ratio * self.angle
        cdef cython.double result = exp(.5 * self.index * (self.r - r1) * (one + cos(modphase))) * (cos(self.angle + (.5 * self.index * (self.r+r1) * sin(modphase))))
        self.angle += fm + self.frequency
        return result
        
    cpdef cython.double next_i(self, cython.double fm =0.0):
        self.next(fm)
        
    cpdef cython.double next_j(self, cython.double fm =0.0):
        cdef cython.double r1 = 1 / self.r
        cdef cython.double modphase = self.ratio * self.angle
        cdef cython.double result = exp(.5 * self.index * (self.r + r1) * (cos(modphase) - 1.0)) * (cos(self.angle + (.5 * self.index * (self.r-r1) * sin(modphase))))
        self.angle += fm + self.frequency
        return result
        
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Asyfm make_asyfm(frequency=0, ratio=1., r=1., index=1.0):
    """
    create an asymmetric fm gens. can produce same as asymmetric-fm generator or can use is the I0 case set r != 1.0 to get the asymmetric spectra
    """
    return Asyfm(frequency, ratio, r, index)
    
cpdef cython.double asyfm(Asyfm gen, cython.double fm=0.):
    """
    same as asyfum_i. the I0 case of the asymmetric-fm generator
    
        
    :param gen: asyfm gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.double asyfm_i(Asyfm gen, cython.double fm=0.):
    """
    the I0 case of the asymmetric-fm generator
        
    :param gen: asyfm gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.double asyfm_j(Asyfm gen, cython.double fm=0.):
    """
    is the same as the CLM asymmetric-fm generator
        
    :param gen: asyfm gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next_j(fm)
    
cpdef cython.bint is_asyfm(gen):
    """
    returns True if gen is an asyfm

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Asyfm) 


# --------------- bess ---------------- # 
cdef class Bess(CLMGenerator):
    bessel_peaks = [1.000,0.582,0.487,0.435,0.400,0.375,0.355,0.338,0.325,0.313,0.303,0.294,0.286,0.279,0.273,0.267,0.262,0.257,0.252,0.248]
    
    def __init__(self, frequency, n=0):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.angle = 0.0
        if self.n >= len(Bess.bessel_peaks):
            self.norm = (.67 / self.n**(1/3))
        else:
            self.norm = Bess.bessel_peaks[self.n]
        
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double result = clm.bes_jn(self.n, self.angle) / self.norm
        self.angle += self.frequency + fm
        return result
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Bess make_bess(frequency=0, n=0):
    """creates a bessel function (Jn) generator"""
    return Bess(frequency, n)
    
cpdef cython.double bess(Bess gen, cython.double fm=0.):
    """
    returns Jn
        
    :param gen: bess gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_bess(gen):
    """
    returns True if gen is an bess

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Bess) 

# --------------- jjcos ---------------- # 

cdef class Jjcos(CLMGenerator):

    def __init__(self, frequency, r=.5, a=1., k=1.):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.a = a
        self.k = k
        self.angle = 0.0
        
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double dc = clm.bes_j0(self.k*self.a) * clm.bes_j0(self.k*self.r)
        cdef cython.double norm = clm.bes_j0(self.k * sqrt((self.a*self.a) + (self.r*self.r) + (-2. * self.a * self.r))) - dc
        self.angle += self.frequency + fm
        return (clm.bes_j0(self.k * sqrt((self.r*self.r) + (self.a*self.a) + (self.a * -2.0 * self.r * cos(x)))) - dc) / norm
                
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Jjcos make_jjcos(frequency=0, r=.5, a=1., k=1.):
    """creates a jjcos generator that produces a sum of cosines scaled by a product of Bessel functions.
    """
    return Jjcos(frequency, r, a, k)
    
cpdef cython.double jjcos(Jjcos gen, cython.double fm=0.):
    """
    returns a sum of cosines scaled by a product of Bessel functions.
        
    :param gen: jjcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_jjcos(gen):
    """
    returns True if gen is an jjcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Jjcos) 


# --------------- j0evencos ---------------- # 

cdef class J0evencos(CLMGenerator):

    def __init__(self, frequency, index=1.):
        self.frequency = clm.hz2radians(frequency)
        self.index = index
        self.angle = 0.0
        
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double j0 = clm.bes_j0(.5 * self.index)
        cdef cython.double dc = j0*j0
        self.angle += self.frequency + fm
        if dc == 1.0:
            return 1.
        return (clm.bes_j0(self.index * math.sin(x)) - dc) / (1.0 - dc)
       

    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef J0evencos make_j0evencos(frequency=0,index=1):
    """
    creates a j0evencos generator that produces a sum of cosines scaled Jk^2(index/2).
    """
    return J0evencos(frequency, index)
    
cpdef cython.double j0evencos(J0evencos gen, cython.double fm=0.):
    """returns a sum of cosines scaled Jk^2(index/2).
        
    :param gen: j0evencos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_j0evencos(gen):
    """
    returns True if gen is an j0evencos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, J0evencos) 



# --------------- j2cos ---------------- # 

cdef class J2cos(CLMGenerator):

    def __init__(self, frequency, r=.5, n=1):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.n = max(n, 1)
        self.angle = 0.0
        
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double rsinx2  = 2.0 * self.r  * sin(0.5 * self.angle)
        self.angle += self.frequency + fm
        if fabs(rsinx2) < NEARLY_ZERO:
            return 1
        return clm.bes_jn(self.n, rsinx2) / rsinx2

    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef J2cos make_j2cos(frequency=0, r=.5, n=1):
    """
    creates a j2cos generator that produces a sum of cosines scaled in a very complicated way.
    """
    return J2cos(frequency, r, n)
    
cpdef cython.double j2cos(J2cos gen, cython.double fm=0.):
    """
    returns a sum of cosines scaled in a very complicated way.
    
    :param gen: j2cos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_j2cos(gen):
    """
    returns True if gen is an j2cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, J2cos) 



# --------------- jpcos ---------------- # 

cdef class Jpcos(CLMGenerator):
    
    def __init__(self, frequency, r=.5, a=0.0, k=1.0):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.a = a
        self.k = k
        if self.r == self.a:
            raise ValueError("Jpcos: r and a can't have same value")
        self.angle = 0.0
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double arg = (self.r*self.r) + (self.a*self.a) + (self.a * -2. * self.r * cos(self.angle))
        self.angle += self.frequency + fm
        if fabs(arg) < NEARLY_ZERO:
            return 1.0
        
        return sin(self.k * sqrt(arg))
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Jpcos make_jpcos(frequency=0, r=.5, a=0.0, k=1.0):
    """
    creates a jpcos generator that produces a sum of cosines scaled in a very complicated way.
    """
    return Jpcos(frequency, r, a, k)
    
cpdef cython.double jpcos(Jpcos gen, cython.double fm=0.):
    """
    returns a sum of cosines scaled in a very complicated way.
    
    :param gen: jpcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_jpcos(gen):
    """
    returns True if gen is an jpcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Jpcos) 

# --------------- jncos ---------------- # 

cdef class Jncos(CLMGenerator):

    def __init__(self, frequency, r=.5, a=1.0, n=0):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.a = a
        self.n = n
        self.angle = 0.0
        self.ra = (self.a*self.a) + (self.r * self.r)
        
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double arg = sqrt(self.ra + (self.a * -2. * self.r * cos(self.angle)))
        self.angle += self.frequency + fm
        if arg < NEARLY_ZERO:
            return 1.0
        return clm.bes_jn(self.n, arg) / arg**self.n

    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Jncos make_jncos(frequency=0,  r=.5, a=1.0, n=0):
    """
    creates a jncos generator that produces a sum of cosines scaled in a very complicated way.
    """
    return Jncos(frequency, r, a, n)
    
cpdef cython.double jncos(Jncos gen, cython.double fm=0.):
    """
    returns a sum of cosines scaled in a very complicated way.
      
    :param gen: jncos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_jncos(gen):
    """
    returns True if gen is an jncos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Jncos) 


# --------------- j0j1cos  ---------------- # 

cdef class J0j1cos(CLMGenerator):

    def __init__(self, frequency,index=1):
        self.frequency = clm.hz2radians(frequency)
        self.index = index
        self.angle = 0.0
        
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double j0 = clm.bes_j0(.5 * self.index)
        cdef cython.double dc = j0 * j0
        cdef cython.double arg = self.index * cos(self.angle)
        self.angle += self.frequency + fm
        return ((clm.bes_j0(arg) + clm.bes_j1(arg)) - dc) / 1.215

    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef J0j1cos make_j0j1cos(frequency=0, index=1):
    """
    creates a j0j1cos generator that produces a sum of cosines scaled in a very complicated way.
    """
    return J0j1cos(frequency, index)
    
cpdef cython.double j0j1cos(J0j1cos gen, cython.double fm=0.):
    """
    returns a sum of cosines scaled in a very complicated way.
         
    :param gen: j0j1cos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_j0j1cos(gen):
    """
    returns True if gen is an j0j1cos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, J0j1cos) 


 
# --------------- jycos  ---------------- # 

cdef class Jycos(CLMGenerator):

    def __init__(self, frequency,r=1.0, a=.5):
        self.frequency = clm.hz2radians(frequency)
        self.r = max(.0001, r)
        self.a = a
        if self.r < self.a:
            raise ValueError(f'a: {self.a} must be < r: {self.r}')
        if (self.a*self.a + self.r*self.r) <= (2 * self.a * self.r):
            raise ValueError(f'a: {self.a}, r: {self.r} will cause bes_y0 to return -inf')
        
        self.angle = 0.0
        
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double b2c2 = (self.r*self.r) + (self.a*self.a)
        cdef cython.double dc = clm.bes_y0(self.r) * clm.bes_j0(self.a)
        cdef cython.double norm = fabs(clm.bes_y0( sqrt(b2c2 + (-2 * self.r * self.a))) - dc)
#         print(self.r, self.a, dc,norm, b2c2, sqrt(b2c2 + (-2 * self.r * self.a)), clm.bes_y0(sqrt(b2c2 + (-2 * self.r * self.a))))
#         #3.0 0.0 0.37685001001279034 0.0 9.0 3.0 0.37685001001279034
        self.angle += self.frequency + fm
        return ((clm.bes_y0(sqrt(b2c2 + (-2. * self.r * self.a * cos(x))))) - dc) / norm
        
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Jycos make_jycos(frequency=0, r=1.0, a=.5):
    """
    creates a jycos generator that produces a sum of cosines scaled by Yn(r)*Jn(r).
    """
    return Jycos(frequency, r,a)
    
cpdef cython.double jycos(Jycos gen, cython.double fm=0.): 
    """
    returns a sum of cosines scaled by Yn(r)*Jn(r).
        
    :param gen: jycos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_jycos(gen):
    """
    returns True if gen is an jycos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Jycos) 


# --------------- jcos  ---------------- # 
cdef class Jcos(CLMGenerator):

    def __init__(self, frequency,n=0, r=1.0, a=.5):
        self.frequency = clm.hz2radians(frequency)
        self.n = n
        self.r = r
        self.a = a
        
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        cdef cython.double b = self.r
        cdef cython.double c = self.a
        cdef cython.double nf = self.n
        cdef cython.double dc = clm.bes_j0(b) * clm.bes_j0(c)
        self.angle += self.frequency + fm
        return clm.bes_jn(self.n, ((nf + 1) * (sqrt((b*b) + (c*c) + (-2.0 * b * c * cos(x)))))) - dc
        
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef Jcos make_jcos(frequency=0, r=1.0, a=.5):
    """
    creates a jcos generator. (jcos gen (fm 0.0)) that produces a sum of cosines scaled in some complex manner.
    """
    return Jcos(frequency, r,a)
    
cpdef cython.double jcos(Jcos gen, cython.double fm=0.):
    """
    returns a sum of cosines scaled in some complex manner.
        
    :param gen: jcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_jcos(gen):
    """
    returns True if gen is an jcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Jcos) 
    
# --------------- blackman  ---------------- # 

cdef class Blackman(CLMGenerator):
    blackman_coeffs = [[0,0], [0,0.54,1,-0.46], [0,0.42323,1,-0.49755,2,0.078279],[0,0.35875,1,0.48829,2,0.14128,3,-0.01168],
                        [0,0.287333,1,-0.44716,2,0.20844,3,-0.05190,4,0.005149], [0,.293557,1,-.451935,2,.201416,3,-.047926,4,.00502619,5,-.000137555],
                        [0,.2712203,1,-.4334446,2,.2180041,3,-.0657853,4,.010761867,5,-.0007700127,6,.00001368088],
                        [0,.2533176,1,-.4163269,2,.2288396,3,-.08157508,4,.017735924,5,-.0020967027,6,.00010677413,7,-.0000012807],
                        [0,.2384331,1,-.4005545,2,.2358242,3,-.09527918,4,.025373955,5,-.0041524329,6,.00036856041,7,-.00001384355,8,.0000001161808],
                        [0,.2257345,1,-.3860122,2,.2401294,3,-.1070542,4,.03325916,5,-.00687337,6,.0008751673,7,-.0000600859,8,.000001710716,9,-.00000001027272],
                        [0,.2151527,1,-.3731348,2,.2424243,3,-.1166907,4,.04077422,5,-.01000904,6,.0016398069,7,-.0001651660,8,.000008884663,9,-.000000193817,10,.00000000084824]]
    def __init__(self, frequency, cython.int n=1):
        self.frequency = frequency
        self.n = n
        self.osc = clm.make_polywave(self.frequency, Blackman.blackman_coeffs[self.n])
    
    cpdef cython.double next(self, cython.double fm =0.0):
        return clm.polywave(self.osc, fm)
    
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
    
    cpdef mus_reset(self):
        self.frequency = 0.
        self.angle = 0.
        
cpdef Blackman make_blackman(frequency=0, n=1):
    """
    creates a blackman generator that produces the nth Blackman-Harris fft data window as a periodic waveform. (n <= 10)"""
    return Blackman(frequency, n)
    
cpdef cython.double blackman(Blackman gen, cython.double fm=0.):
    """returns the nth Blackman-Harris fft data window as a periodic waveform. (n <= 10)
    
    :param gen: blackman gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_blackman(gen):
    """
    returns True if gen is an blackman

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Blackman) 


# --------------- fmssb ---------------- #

@cython.cclass
cdef class Fmssb(CLMGenerator):

    def __init__(self, frequency, ratio=1.0, index=1.):
        self.frequency = clm.hz2radians(frequency)# added because this did not seem righ. was generating octave higher
        self.ratio = ratio
        self.idx = index
    

    cpdef cython.double next(self, fm: cython.double =0.0):
        cdef cython.double cx = self.angle
        cdef cython.double mx = cx * self.ratio
        self.angle += fm + self.frequency
        return (cos(cx)*sin(self.idx * cos(mx))) - (sin(cx)*sin(self.idx * sin(mx)))
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
       
    @property
    def index(self) -> cython.double:
        return self.idx
    
    @index.setter
    def index(self, val: cython.double): 
        self.idx = val
        

cpdef Fmssb make_fmssb(frequency=0, ratio=1.0, index=1.):
    """
    creates an fmssb generator that produces single-sideband FM.
    """
    return Fmssb(frequency, ratio, index)
    
cpdef cython.double fmssb(Fmssb gen, cython.double fm =0.):
    """
    returns single-sideband FM.
    
    :param gen: fmssb gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_fmssb(gen):
    """
    returns True if gen is an fmssb

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Fmssb)           
         
# --------------- k3sin  ---------------- # 
cdef class K3sin(CLMGenerator):

    def __init__(self, frequency):
        self.frequency = clm.hz2radians(frequency)
        self.coeffs = np.array([0.0, (PI*PI) / 6.0, PI / -4.0, .08333])
        self.angle = 0.0
 
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        if not 0.0 <= x <= TWO_PI:
            x = x % TWO_PI*2
        self.angle = x + fm + self.frequency
        return clm.polynomial(self.coeffs, x)
                
    def __call__(self, fm: cython.double =0.) -> cython.double:
        return self.next(fm)
        
    def mus_reset(self):
        self.frequency = 0.
        self.angle = 0.
        

cpdef K3sin make_k3sin(frequency=0, n=1):
    """creates a k3sin generator that produces a sum of sines scaled by k^3."""
    return K3sin(frequency)
    
cpdef cython.double k3sin(K3sin gen, cython.double fm =0.):
    """
    returns a sum of sines scaled by k^3.
    
    :param gen: k3sin gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_k3sin(gen):
    """
    returns True if gen is an k3sin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, K3sin)       
    

# --------------- izcos  ---------------- # 

cdef class Izcos(CLMGenerator):

    def __init__(self, frequency, r=1.0):
        self.frequency = clm.hz2radians(frequency)
        self.r = r
        self.angle = 0.0
        self.dc = clm.bes_i0(self.r)
        self.norm = exp(self.r) - self.dc
        self.inorm = 1.0 / self.norm
    
    cpdef cython.double next(self, cython.double fm =0.0):
        cdef cython.double x = self.angle
        self.angle = x + fm + self.frequency
        if abs(self.norm) < NEARLY_ZERO:
            return 1.
        return (exp(self.r * math.cos(x)) - self.dc) * self.inorm
                
    def __call__(self, fm: cython.double =0.) -> cython.double:
        return self.next(fm)
        
    def mus_reset(self):
        self.frequency = 0.
        self.angle = 0.
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.r

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.r = val
        self.dc = clm.bes_i0(val)
        self.norm = exp(self.r) - self.dc
        self.inorm = 1.0 / self.norm

cpdef Izcos make_izcos(frequency=0,r=1.):
    """
    creates an izcos generator that produces a sum of sines scaled by In(r).
    """
    return Izcos(frequency, r)
    
cpdef cython.double izcos(Izcos gen, cython.double fm =0.):
    """
    returns a sum of sines scaled by In(r)
    :param gen: izcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_izcos(gen):
    """
    returns True if gen is an izcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Izcos)   
    
    
# # 
# --------------- adjustable-square-wave ---------------- # 

cdef class AdjustableSquareWave(CLMGenerator):

    def __init__(self, frequency, duty_factor=.5, amplitude=1.0):
        self.frequency = frequency
        self.duty_factor = duty_factor
        self.amplitude = amplitude
        self.sum = 0.0
        self.p1 = clm.make_pulse_train(self.frequency, self.amplitude)
        self.p2 = clm.make_pulse_train(self.frequency, -self.amplitude, (TWO_PI * (1.0 - self.duty_factor)))
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double a = clm.pulse_train(self.p1, fm)
        cdef cython.double b = clm.pulse_train(self.p2, fm)
        self.sum += a + b

        return self.sum
                     
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.p1.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.p1.mus_phase = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.p1.mus_frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.p1.mus_frequency = val
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.duty_factor

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.duty_factor = val
        self.p2.mus_phase = TWO_PI * (1.0 - self.duty_factor)
        

cpdef AdjustableSquareWave make_adjustable_square_wave(frequency=0, duty_factor=.5, amplitude=1.0):
    """
    creates an adjustable-square-wave generator that produces square-wave 
    where the duty-factor sets the ratio of pulse duration to pulse period."""
    return AdjustableSquareWave(frequency, duty_factor, amplitude)
    
cpdef cython.double adjustable_square_wave(AdjustableSquareWave gen, cython.double fm=0.):
    """
    returns a square-wave where the duty-factor sets the ratio of pulse duration to pulse period.
    
    :param gen: adjustable_square_wave gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_adjustable_square_wave(gen):
    """
    returns True if gen is an adjustable_square_wave

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, AdjustableSquareWave)   
    
    
# --------------- adjustable-triangle-wave ---------------- # 

cdef class AdjustableTriangleWave(CLMGenerator):     
    def __init__(self, frequency, duty_factor=.5, amplitude=1.0):
        self.frequency = frequency
        self.duty_factor = duty_factor
        self.amplitude = amplitude
        self.gen = clm.make_triangle_wave(self.frequency)
        self.top = 1.0 - self.duty_factor
        self.mtop = - self.top
        self.scl = 0.0
        self.val = 0.0
        if self.duty_factor != 0.0:
            self.scl = self.amplitude / self.duty_factor
    
    cpdef cython.double next(self, cython.double fm=0.0):
        self.val = clm.triangle_wave(self.gen, fm)
        return self.scl * (self.val - max(self.mtop, min(self.top, self.val)))
                     
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.gen.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.gen.mus_phase = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.gen.mus_frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.gen.mus_frequency = val
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.duty_factor

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.duty_factor = val
        self.top = 1.0 - val
        if val != 0.0:
            self.scl = self.amplitude / val

cpdef AdjustableTriangleWave make_adjustable_triangle_wave(frequency=0, duty_factor=.5, amplitude=1.0):
    """
    creates an adjustable-triangle-wave generator that produces a triangle-wave where the 
    duty-factor sets the ratio of pulse duration to pulse period.
    """
    return AdjustableTriangleWave(frequency, duty_factor, amplitude)
    
cpdef cython.double adjustable_triangle_wave(AdjustableTriangleWave gen, cython.double fm=0.):
    """
    returns a triangle-wave where the duty-factor sets the ratio of pulse duration to pulse period.
    
    :param gen: adjustable_triangle_wave gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_adjustable_triangle_wave(gen):
    """
    returns True if gen is an adjustable_triangle_wave

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, AdjustableTriangleWave)   
    
# --------------- adjustable-sawtooth-wave ---------------- # 
cdef class AdjustableSawtoothWave(CLMGenerator): 
 
    def __init__(self, frequency, duty_factor=.5, amplitude=1.0):
        self.frequency = frequency
        self.duty_factor = duty_factor
        self.amplitude = amplitude
        self.gen = clm.make_sawtooth_wave(self.frequency)
        self.top = 1.0 - self.duty_factor
        self.mtop = self.duty_factor - 1.0
        self.scl = 0.0
        self.val = 0.0
        if self.duty_factor != 0.0:
            self.scl = self.amplitude / self.duty_factor
    
    cpdef cython.double next(self, cython.double fm=0.0):
        self.val = clm.sawtooth_wave(self.gen, fm)
        return self.scl * (self.val - max(self.mtop, min(self.top, self.val)))
                     
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.gen.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.gen.mus_phase = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.gen.mus_frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.gen.mus_frequency = val
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.duty_factor

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.duty_factor = val
        self.top = 1.0 - val
        self.mtop = val - 1.0
        if val != 0.0:
            self.scl = self.amplitude / val

cpdef AdjustableSawtoothWave make_adjustable_sawtooth_wave(frequency=0, duty_factor=.5, amplitude=1.0):
    """
    creates an adjustable-sawtooth-wave generator that produces a sawtooth-wave where the duty-factor sets the ratio of pulse duration to pulse period.
    """
    return AdjustableSawtoothWave(frequency, duty_factor, amplitude)
    
cpdef cython.double adjustable_sawtooth_wave(AdjustableSawtoothWave gen, cython.double fm=0.):
    """
    returns a sawtooth-wave where the duty-factor sets the ratio of pulse duration to pulse period.
        
    :param gen: adjustable_sawtooth_wave gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_adjustable_sawtooth_wave(gen):
    """
    returns True if gen is an adjustable_sawtooth_wave

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, AdjustableSawtoothWave)   



# # 
# --------------- adjustable-oscil-wave ---------------- # 
cdef class AdjustableOscil(CLMGenerator): 
 
    def __init__(self, frequency, duty_factor=.5):
        self.frequency = frequency
        self.duty_factor = duty_factor
        self.gen = clm.make_oscil(self.frequency)
        self.top = 1.0 - self.duty_factor
        self.mtop = self.duty_factor - 1.0
        self.scl = 0.0
        self.val = 0.0
        if self.duty_factor != 0.0:
            self.scl = 1. / self.duty_factor
    
    cpdef cython.double next(self, cython.double fm=0.0):
        self.val = clm.oscil(self.gen, fm)
        return self.scl * (self.val - max(self.mtop, min(self.top, self.val)))
                     
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.gen.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.gen.mus_phase = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.gen.mus_frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.gen.mus_frequency = val
        
    @property
    def mus_scaler(self) -> cython.double:
        return self.duty_factor

    @mus_scaler.setter
    def mus_scaler(self, val: cython.double):
        self.duty_factor = val
        self.top = 1.0 - val
        self.mtop = val - 1.0
        if val != 0.0:
            self.scl = 1. / val

cpdef AdjustableOscil make_adjustable_oscil(frequency=0, duty_factor=.5):
    """
    creates an adjustable-oscil generator that produces a sinusoid where the duty-factor sets the ratio of pulse duration to pulse period.
    """
    return AdjustableOscil(frequency, duty_factor)
    
cpdef cython.double adjustable_oscil(AdjustableOscil gen, cython.double fm=0.):
    """
    returns a sinusoid where the duty-factor sets the ratio of pulse duration to pulse period.
            
    :param gen: adjustable_oscil gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_adjustable_oscil(gen):
    """
    returns True if gen is an adjustable_oscil_wave

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, AdjustableOscil)   

# --------------- make-table-lookup-with-env ---------------- # 

cpdef make_table_lookup_with_env(frequency, pulse_env, size=clm.default.table_size): 
    """
    creates a table lookup generator from an envelope
    """
    ve = np.zeros(size)
    e = clm.make_env(pulse_env, length=size)
    for i in range(size):
        ve[i] = clm.env(e)
    return clm.make_table_lookup(frequency, 0.0, ve, size)


# --------------- make-wave-train-with-env ---------------- # 

cpdef make_wave_train_with_env(frequency, pulse_env, size=clm.default.table_size): 
    """
    creates a wave train generator from an envelope
    """
    ve = np.zeros(size)
    e = clm.make_env(pulse_env, length=size)
    for i in range(size):
        ve[i] = clm.env(e)
    return clm.make_wave_train(frequency, 0.0, ve, size)



# --------------- round-interp ---------------- # 
cdef class RoundInterp(CLMGenerator):
 
    def __init__(self, frequency, n=1, amplitude=1.0):
        self.frequency = frequency
        self.n = n
        self.amplitude = amplitude
        self.rnd = clm.make_rand_interp(self.frequency, self.amplitude)
        self.flt = clm.make_moving_average(self.n)

    
    cpdef cython.double next(self, cython.double fm=0.0):
        return clm.moving_average(self.flt, clm.rand_interp(self.rnd, fm))
                     
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
    
    @property
    def mus_phase(self) -> cython.double:
        return self.rnd.mus_phase

    @mus_phase.setter
    def mus_phase(self, val: cython.double):
        self.gen.rnd = val

    @property
    def mus_frequency(self) -> cython.double:
        return self.rnd.mus_frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.rnd.mus_frequency = val
        

cpdef RoundInterp make_round_interp(frequency=0, n=1, amplitude=1.0):
    """
    creates a round-interp generator that produces a rand-interp sequence low-pass filtered by a moving-average generator of length n.
    """
    return RoundInterp(frequency, n, amplitude)
    
cpdef cython.double round_interp(RoundInterp gen, cython.double fm=0.):
    """returns a rand-interp sequence low-pass filtered by a moving-average generator of length n.
    
            
    :param gen: round_interp gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_round_interp(gen):
    """
    returns True if gen is an round

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, RoundInterp)   

# # 
# --------------- env-any functions ---------------- # 

# --------------- sine-env ---------------- # 
cdef cython.double sin_env_fun(y):
    return (0.5 * (1.0 + (sin (PI * (y - 0.5)))))
    
cpdef cython.double sine_env(e):
    """connects envelope points using sin function"""
    return clm.env_any(e, sin_env_fun)
    
cdef cython.double square_env_fun(y):
    return y*y
    
cpdef cython.double square_env(e):
    """connects envelope points using square wave function"""
    return clm.env_any(e, square_env_fun)

cdef cython.double blackman4_env_fun(y):
    cx = math.cos(math.pi * y)
    return 0.084037 + (cx * ((cx * (0.375696 + (cx * ((cx * 0.041194) - 0.20762)))) - 0.29145))
    
cpdef cython.double blackman4_env(e):
    """connects envelope points using blackman function"""
    return clm.env_any(e, blackman4_env_fun)
 
    
def multi_expt_env(e, expts):
    def fun(y):
        b = expts[clm.channels(e) % len(expts)]
        return ((b**y) - 1.0) / (b - 1.0)
    return clm.env_any(e, fun)

# --------------- run-with-fm-and-pm ---------------- # 

# TODO: This is not working correctly--------------- nchoosekcos ---------------- # 
cdef class Nchoosekcos(CLMGenerator):
    
    def __init__(self, frequency, ratio=1.0, n=1):
        self.frequency = frequency
        self.ratio = ratio
        self.n = n
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double y = x * self.ratio
        self.angle += self.frequency + fm

        return np.real(math.cos(x) * math.pow(math.cos(y), self.n))
               
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)


cpdef Nchoosekcos make_nchoosekcos(frequency=0, n=1, amplitude=1.0):
    """creates an nchoosekcos generator that produces a sum of cosines scaled by the binomial coefficients"""
    return Nchoosekcos(frequency, n, amplitude)
    
cpdef cython.double nchoosekcos(Nchoosekcos gen, cython.double fm=0.):
    """
    returns a sum of cosines scaled by the binomial coefficients
         
    :param gen: nchoosekcos gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_nchoosekcos(gen):
    """
    returns True if gen is an nchoosekcos

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Nchoosekcos)   

# --------------- sinc-train ---------------- # 

cdef class SincTrain(CLMGenerator):
    
    def __init__(self, frequency, n=1):
        self.frequency = frequency
        self.n = n
        if self.n <= 0:
            self.original_n = 1
            self.n = 3
        else:
            self.original_n = self.n
            self.n = 1 + (2 * self.n)
        self.original_frequency = self.frequency
        self.frequency = .5 * self.n * clm.hz2radians(self.frequency)
        self.angle = 0.0
        self.n = n
    
    cpdef cython.double next(self, cython.double fm=0.0):
        cdef cython.double x = self.angle
        cdef cython.double max_angle = PI * .5 * self.n
        cdef cython.double new_angle = x + fm + self.frequency
        cdef cython.double DC = 1.0 / self.n
        cdef cython.double norm = self.n / (self.n - 1)
        if new_angle > max_angle:
            new_angle = new_angle - (PI * self.n)
        self.angle = new_angle
        if fabs(x) < NEARLY_ZERO:
            return 1.0
        return norm * ((sin(x) / x) - DC)
               
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)

    @property
    def mus_frequency(self) -> cython.double:
        return self.original_frequency

    @mus_frequency.setter
    def mus_frequency(self, val: cython.double):
        self.original_frequency = val
        self.frequency = .5 * self.n * clm.hz2radians(val)
        
    @property
    def mus_order(self) -> cython.int:
        return self.original_n

    @mus_order.setter
    def mus_order(self, val: cython.int):
        if val <= 0:
            self.original_n = 1
            self.n = 3
        else:
            self.original_n = val
            self.n = 1 + (2 * val)
            
cpdef SincTrain make_sinc_train(frequency=0, n=1):
    """
    creates a sinc-train generator with n components
    """
    return SincTrain(frequency, n)
    
cpdef cython.double sinc_train(SincTrain gen, cython.double fm=0.):
    """
    returns a sinc-train
    
    :param gen: sinc_train gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_sinc_train(gen):
    """
    returns True if gen is an sinc_train

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, SincTrain)   


# --------------- pink-noise ---------------- # 
 
cdef class PinkNoise(CLMGenerator):

    def __init__(self, n):
        self.n = n
        self.data = np.zeros(self.n*2, dtype=np.double)
        amp: cython.double = 1.0 / (2.5 * sqrt(self.n))
        self.data[0] = amp
        for i in range(2,2*self.n,2):
            self.data[i] =  clm.random(amp)
            self.data[i+1] = random.random()
    
    cpdef cython.double next(self, fm: cython.double =0.0):
        cdef cython.double x = 0.5 
        cdef cython.double s = 0.0
        cdef cython.double amp = self.data[0]
        cdef cython.int size = self.n*2

        cdef cython.long i = 0

        for i in range(2,size,2):
            s += self.data[i]
            self.data[i+1] -= x
        
            if self.data[i+1] < 0.0:
                self.data[i] = clm.random(amp)
                self.data[i+1] += 1.0
            x *= .5
        return s + clm.random(amp)
                
    def __call__(self, fm: cython.double =0.) -> cython.double:
        return self.next(fm)

cpdef PinkNoise make_pink_noise(n=1):
    """Creates a pink-noise generator with n octaves of rand (12 is recommended)."""
    return PinkNoise( n)
    
cpdef cython.double pink_noise(PinkNoise gen, cython.double fm=0.):
    """
    Returns the next random value in the 1/f stream produced by gen.
    
    :param gen: pink_noise gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_pink_noise(gen):
    """
    returns True if gen is an pink_noise

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, PinkNoise)           

# --------------- brown-noise ---------------- # 
cdef class BrownNoise(CLMGenerator):
    
    def __init__(self, frequency, amplitude=1.0):
        self.gr = clm.make_rand(frequency, amplitude)
        self.prev = 0
        self.sum = 0
    
    cpdef cython.double next(self, fm: cython.double =0.0):
        val: cython.double = clm.rand(self.gr, fm)
        if val != self.prev:
            self.prev = val
            self.sum += val
        return self.sum
                
    def __call__(self, fm: cython.double=0.) ->  cython.double:
        return self.next(fm)
        

cpdef BrownNoise make_brown_noise(frequency, amplitude=1.0):
    """Returns a generator that produces brownian noise."""
    return BrownNoise(frequency, amplitude=1.0)
    
cpdef cython.double brown_noise(BrownNoise gen, cython.double fm=0.):
    """
    returns the next brownian noise sample
        
    :param gen: brown_noise gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_brown_noise(gen):
    """
    returns True if gen is an brown_noise

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, BrownNoise)           

# --------------- green-noise ---------------- # 

cdef class GreenNoise(CLMGenerator):
    
    def __init__(self, frequency, amplitude=1.0, low=-1, high=1):
        self.gr = clm.make_rand(frequency, amplitude)
        self.low = low
        self.high = high
        self.sum = .5 * (self.low + self.high)
        self.prev = 0.
        self.sum = 0.
    

    cpdef cython.double next(self, cython.double fm =0.0) :
        val: cython.double = clm.rand(self.gr, fm)
        if val != self.prev:
            self.prev = val
            self.sum += val
            if not (self.low <= self.sum <= self.high):
                self.sum -= 2*val
        return self.sum
                
    def __call__(self, fm: cython.double=0.) -> cython.double:
        return self.next(fm)
        
cpdef GreenNoise make_green_noise(frequency, amplitude=1.0, low=-1.0, high=1.0):
    """Returns a new green-noise (bounded brownian noise) generator."""
    return GreenNoise(frequency, amplitude=1.0)
    
cpdef cython.double  green_noise(GreenNoise gen, cython.double fm=0.):
    """
    returns the next sample in a sequence of bounded brownian noise samples.
            
    :param gen: green_noise gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(fm)
    
cpdef cython.bint is_green_noise(gen):
    """
    returns True if gen is an green_noise

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, GreenNoise)           

# TODO: This is not working properly --------------- green-noise-interp ---------------- # 
cdef class GreenNoiseInterp(CLMGenerator):    
    def __init__(self, frequency, amplitude=1.0, low=-1, high=1):
        self.low = low
        self.high = high
        self.amplitude = amplitude
        self.sum = .5 * (self.low + self.high)
        self.dv = 1.0 / (ceil(clm.get_srate() / max(1.0, self.frequency)))
        self.frequency = clm.hz2radians(frequency)
        self.incr = clm.random(self.amplitude) * self.dv
        self.angle = 0.0
       # print(f'dv: {self.dv} incr: {self.incr}')

    cpdef cython.double next(self, cython.double fm = 0.0):
        cdef cython.double val 
        if not (0.0 <= self.angle <= TWO_PI):
            val = clm.random(self.amplitude)
            self.angle = self.angle % TWO_PI
            if self.angle < 0.0:
                self.angle += TWO_PI
            if not (self.low <= (self.sum+val) <= self.high):
                val = min(self.high-self.sum, max(self.low-self.sum, -val))
            self.incr = self.dv * val

        self.angle += fm + self.frequency
        self.sum += self.incr
        return self.sum
                
    def __call__(self, fm: cython.double =0.) -> cython.double:
        return self.next(fm)
        

cpdef GreenNoiseInterp make_green_noise_interp(frequency, amplitude=1.0, low=-1.0, high=1.0):
    """Returns a new green-noise (bounded brownian noise) generator."""
    return GreenNoiseInterp(frequency, amplitude=1.0)
    
cpdef green_noise_interp(GreenNoiseInterp gen, cython.double fm=0.):
    """
    Returns the next sample in a sequence of interpolated bounded brownian noise samples.
    
    :param gen: green_noise_interp gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_green_noise_interp(gen):
    """
    returns True if gen is an green_noise_interp

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, GreenNoiseInterp)          

# --------------- moving-sum ---------------- # 

cdef class MovingSum(CLMGenerator):

    def __init__(self, n=128):
        self.n = n
        self.gen = clm.make_moving_average(self.n)
        
    cpdef cython.double next(self, cython.double insig=0.0):
        return clm.moving_average(self.gen, fabs(insig))

    def __call__(self, cython.double insig=0.) -> cython.double:
        return self.next(insig)
        

cpdef MovingSum make_moving_sum(n=128):
    """ 
    returns a moving-sum generator that produces the sum of the absolute values in a moving window over the last n inputs.
    """
    return MovingSum(n)
    
cpdef cython.double moving_sum(MovingSum gen, cython.double insig=0.):
    """
    returns the sum of the absolute values in a moving window over the last n inputs.
    :param gen: moving_sum gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(insig)
    
cpdef cython.bint is_moving_sum(gen):
    """
    returns True if gen is an moving_sum

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, MovingSum)    
#      
# --------------- moving-variance ---------------- # 

cdef class MovingVariance(CLMGenerator):
    def __init__(self, n=128):
        self.n = n
        self.gen1 = clm.make_moving_average(self.n)
        self.gen1.mus_increment = 1.0
        self.gen2 = clm.make_moving_average(self.n)
        self.gen2.mus_increment = 1.0
        
        
    cpdef cython.double next(self, cython.double insig=0.0):
        cdef cython.double x1 = clm.moving_average(self.gen1, insig)
        cdef cython.double x2 = clm.moving_average(self.gen2, insig*insig)
        return ((self.n*x2) - (x1*x1)) / (self.n * (self.n - 1))

    def __call__(self, cython.double insig=0.) -> cython.double:
        return self.next(insig)
        

cpdef MovingVariance make_moving_variance(n=128):
    """ 
    returns a moving-variance generator that produces the variance of the values in a moving window over the last n inputs.
    """
    return MovingVariance(n)
    
cpdef cython.double moving_variance(MovingVariance gen, cython.double insig=0.):
    """
    returns the variance of the values in a moving window over the last n inputs.
    :param gen: moving_variance gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(insig)
    
cpdef cython.bint is_moving_variance(gen):
    """
    returns True if gen is an moving_variance

    :param gen: gen
    :rtype: bool
    """

    return isinstance(gen, MovingVariance)    



# --------------- moving-rms ---------------- # 

cdef class MovingRMS(CLMGenerator):

    def __init__(self, n=128):
        self.n = n
        self.gen = clm.make_moving_average(self.n)
       
    cpdef cython.double next(self, cython.double insig=0.0):  
        return sqrt(clm.moving_average(self.gen, insig*insig))
        
    def __call__(self, cython.double insig=0.) -> cython.double:
        return self.next(insig)
        

cpdef MovingRMS make_moving_rms(n=128):
    """
    returns a moving-rms generator that produces
    the rms of the values in a window over the last n inputs.
    """
    return MovingRMS(n)
    
cpdef cython.double moving_rms(MovingRMS gen, cython.double insig=0.):
    """
    returns the rms of the values in a window over the last n inputs.
    :param gen: moving_rms gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(insig)
    
cpdef cython.bint is_moving_rms(gen):
    """
    returns True if gen is an moving_rms

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, MovingRMS)    


# --------------- moving-length ---------------- # 
cdef class MovingLength(MovingRMS):

    def __init__(self, n=128):
        super().__init__(n)
        self.gen.mus_increment = 1.0
        
cpdef MovingLength make_moving_length(n=128):
    """returns a moving-length generator that produces the length 
    of the values in a window over the last few inputs.
    """
    return MovingLength(n)
    
cpdef cython.double moving_length(MovingLength gen, cython.double insig=0.):
    """
    returns the length of the values in a window over the last few inputs.
    
    :param gen: moving_length gen
    :param fm: fm input
    :rtype: float
    """

    return gen.next(insig)
    
cpdef cython.bint is_moving_length(gen):
    """
    returns True if gen is an moving_length

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, MovingLength)    
    
# --------------- weighted-moving-average ---------------- # 
cdef class WeightedMovingAverage(CLMGenerator):

    def __init__(self, n=128):
        self.n = n
        self.dly = clm.make_moving_average(self.n)
        self.dly.mus_increment = 1.0
        self.den = .5 * (self.n + 1) * n
        self.num = 0.0
        self.sum = 0.0
       
    cpdef cython.double next(self, cython.double insig=0.0):  
        self.num = (self.num + (self.n*insig)) - self.sum
        self.sum = clm.moving_average(self.dly, insig)
        return self.num / self.den
        
    def __call__(self, cython.double insig=0.) -> cython.double:
        return self.next(insig)
        

cpdef WeightedMovingAverage make_weighted_moving_average(n=128):
    """returns a weighted-moving-average generator that produces the sum of the last n inputs weighted by 1/n"""
    return WeightedMovingAverage(n)
    
cpdef cython.double weighted_moving_average(WeightedMovingAverage gen, cython.double insig=0.):
    """
    returns the sum of the last n inputs weighted by 1/n
    :param gen: weighted_moving_average gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(insig)
    
cpdef cython.bint is_weighted_moving_average(gen):
    """
    returns True if gen is an weighted_moving_average

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, WeightedMovingAverage)   


# --------------- exponentially-weighted-moving-average ---------------- #
cdef class ExponentiallyWeightedMovingAverage(CLMGenerator):

    def __init__(self, n=128):
        self.n = n
        self.gen = clm.make_one_pole(1.0 / self.n, -self.n / (1.0 + self.n))
       
    cpdef cython.double next(self, cython.double insig=0.0):  
        return clm.one_pole(self.gen, insig)
        
    def __call__(self, cython.double insig=0.) -> cython.double:
        return self.next(insig)
        

cpdef ExponentiallyWeightedMovingAverage make_exponentially_weighted_moving_average(n=128):
    """returns an exponentially-weighted-moving-average generator that produces the sum of the last n inputs weighted by (-n/(n+1))^k"""
    return ExponentiallyWeightedMovingAverage(n)
    
cpdef cython.double exponentially_weighted_moving_average(ExponentiallyWeightedMovingAverage gen, cython.double insig=0.):
    """
    returns the sum of the last n inputs weighted by (-n/(n+1))^k
    :param gen: exponentially_weighted_moving_average gen
    :param fm: fm input
    :rtype: float
    
    """
    return gen.next(insig)
    
cpdef cython.bint is_exponentially_weighted_moving_average(gen):
    """
    returns True if gen is an exponentially_weighted_moving_average

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, ExponentiallyWeightedMovingAverage)  
     

# --------------- polyoid ---------------- # 

cpdef clm.mus_any make_polyoid(frequency, partial_amps_and_phases):
    """
    returns a polyoid generator that combines the first and second Chebyshev polynomials 
    to provide a sum of sinusoids each with arbitrary amplitude and initial-phase. 
    """
    length = len(partial_amps_and_phases)
    n = 0
    for i in range(0, length, 3):
        n = max(n, floor(partial_amps_and_phases[i]))   
    topk = n + 1
    sin_amps = np.zeros(topk, dtype=np.double)
    cos_amps = np.zeros(topk, dtype=np.double)
    for j in range(0,length,3):
        n = floor((partial_amps_and_phases[j]))
        amp = partial_amps_and_phases[j+1]
        phase = partial_amps_and_phases[j+2]
        if n > 0:
            sin_amps[n] = amp * cos(phase)
        cos_amps[n] = amp * sin(phase)
    return clm.make_polywave(frequency, xcoeffs=cos_amps, ycoeffs=sin_amps)

cpdef cython.double polyoid(clm.mus_any gen, cython.double fm=0.0):
    """
    returns sum of sinusoids each with arbitrary amplitude and initial-phase.
    :param gen: polyoid gen
    :param fm: fm input
    :rtype: float
    """
    return clm.polywave(gen, fm)
 
# look at this later 
#cpdef cython.double polyoid_env(clm.mus_any gen, cython.double fm=0.0, amps, phases, original_data):
cpdef cython.bint is_polyoid(gen):
    """
    returns True if gen is an polyoid

    :param gen: gen
    :rtype: bool
    """
    return clm.is_polywave(gen) and gen.mus_channel == clm.Polynomial.BOTH_KINDS
    
cpdef polyoid_tn(gen):
    return gen.mus_xcoeffs
    
cpdef polyoid_un(gen):
    return gen.mus_ycoeffs
    
# # # TODO: these require potentially loading a file so
# # # wondering good way to do this. using maybe binary numpy files

# TODO: --------------- noid ---------------- # 
# TODO: --------------- knoid ---------------- # 
# TODO: --------------- roid ---------------- # 

# Removed --------------- waveshape ---------------- # 
    


# --------------- tanhsin ---------------- # 

cdef class Tanhsin(CLMGenerator):
    
    def __init__(self, frequency, r=1.0,initial_phase=0.0):
        self.frequency = frequency
        self.r = r
        self.osc = clm.make_oscil(frequency, initial_phase)
        self.frequency = clm.hz2radians(frequency)

    cpdef cython.double next(self, cython.double fm =0.0):
        return tanh(self.r * clm.oscil(self.osc, fm))
   
    def __call__(self, cython.double fm=0.) -> cython.double:
        return self.next(fm)
        

cpdef Tanhsin make_tanhsin(frequency=0, r=1.):
    """returns a tanhsin generator that produces tanh(r*sin) which approaches a square wave as r increases."""
    return Tanhsin(frequency, r)
    
cpdef cython.double tanhsin(Tanhsin gen, cython.double fm=0.):
    """
    returns tanh(r*sin) which approaches a square wave as r increases.
    
    :param gen: tanhsin gen
    :param fm: fm input
    :rtype: float
    """
    return gen.next(fm)
    
cpdef cython.bint is_tanhsin(gen):
    """
    returns True if gen is an tanhsin

    :param gen: gen
    :rtype: bool
    """
    return isinstance(gen, Tanhsin)    
# 
# # # # # 
# # # # # # --------------- moving-fft ---------------- # 
# # # # # 
# # # # # def moving_fft_wrapper(g):
# # # # #     g.rl = np.zeros(g.n)
# # # # #     g.im = np.zeros(g.n)
# # # # #     g.data = np.zeros(g.n)
# # # # #     g.window = make_fft_window(g.window, g.n)
# # # # #     s = np.sum(g.window)
# # # # #     g.window = g.window * (2./s)
# # # # #     g.outctr = g.n+1
# # # # #     return g
# # # # #     
# # # # # moving_fft_methods = {'mus_data' : [lambda g : g.data, None],
# # # # #                         'mus_xcoeffs' : [lambda g : g.rl, None],
# # # # #                         'mus_ycoeffs' : [lambda g : g.im, None],
# # # # #                         'mus_run' : [lambda g,arg1,arg2 : moving_fft(g), None]}
# # # # # 
# # # # # make_moving_fft, is_moving_fft = make_generator('moving_fft', 
# # # # #                 {'input' : False, 
# # # # #                 'n' : 512, 
# # # # #                 'hop' : 128, 
# # # # #                 'window' : Window.HAMMING},
# # # # #                 wrapper=moving_fft_wrapper, 
# # # # #                 methods=moving_fft_methods,
# # # # #                 docstring="""returns a moving-fft generator.""")
# # # # # 
# # # # # 
# # # # # def moving_fft(gen):
# # # # #     new_data = False
# # # # #     if gen.outctr >= gen.hop:
# # # # #         if gen.outctr > gen.n:
# # # # #             for i in range(gen.n):
# # # # #                 gen.data[i] = readin(gen.input)
# # # # #         else:
# # # # #             mid = gen.n - gen.hop
# # # # #             gen.data = np.roll(gen.data, gen.hop)
# # # # #             for i in range(mid,gen.n):
# # # # #                 gen.data[i] = readin(gen.input)
# # # # #         
# # # # #         gen.outctr = 0
# # # # #         new_data = True
# # # # #         gen.im.fill(0.0)
# # # # #         np.copyto(gen.rl, gen.data)        
# # # # #         gen.rl *= gen.window
# # # # #         mus_fft(gen.rl,gen.im, gen.n,1)
# # # # #         gen.rl = rectangular2polar(gen.rl,gen.im)
# # # # #     gen.outctr += 1
# # # # #     return new_data

cdef class MovingFFT(CLMGenerator):

# NOte float-vector-move!  and np.roll use opposite shift meanings
    def __init__(self, reader, n=512, hop=128, outctr=0):
        self.reader = reader
        self.last_moving_fft_window = False
        self.n = n
        self.hop = hop
        self.outctr = outctr
        self.rl = np.zeros(self.n)
        self.im = np.zeros(self.n)
        self.data = np.zeros(self.n)
        
        if isinstance(self.last_moving_fft_window, np.ndarray) and len(self.last_moving_fft_window) == self.n:
            self.window = self.last_moving_fft_window
        else:
            self.last_moving_fft_window = clm.make_fft_window(clm.Window.HAMMING, self.n)
            self.window = self.last_moving_fft_window
        self.window *= 2.0 / (.54 * self.n)
        self.outctr = self.n + 1
       
    cpdef cython.double next(self, cython.double x=0): 
        new_data = False
        cdef cython.long i = 0
        if self.outctr >= self.hop:
            if self.outctr > self.n:
                for i in range(self.n):
                    self.data[i] = clm.readin(self.reader)
            else:
              mid = self.n - self.hop
              self.data = np.roll(self.data, -self.hop)
              for i in range(mid,self.n):
                self.data[i] = clm.readin(self.reader)
            
            self.outctr = 0
            new_data = True
            self.im.fill(0.0)
            np.copyto(self.rl, self.data)     
            #self.rl = self.data[0:self.n]
            self.rl *= self.window
            clm.mus_fft(self.rl, self.im, self.n, 1)
            clm.mus_rectangular2polar(self.rl, self.im)
        self.outctr += 1
        return new_data
        
    def __call__(self, cython.double insig=0.) -> cython.double:
        return self.next(insig)
    
    @property
    def mus_data(self) -> cython.double:
        return self.data
        
    @property
    def mus_xcoeffs(self) -> cython.double:
        return self.rl

    @property
    def mus_ycoeffs(self) -> cython.double:
        return self.im
    
    cpdef mus_run(self, arg1, arg2):
        self.next()

cpdef MovingFFT make_moving_fft(clm.mus_any reader, n=512, hop=128, outctr=0):
    return MovingFFT(reader, n, hop, outctr)
    
cpdef cython.double moving_fft(MovingFFT gen):
    return gen.next()
    
cpdef cython.bint is_moving_fft(gen):
    return isinstance(gen, MovingFFT)    

# # # TODO --------------- moving-spectrum ---------------- # 
# # # # TODO: I am not convinced this is working properly
# # # 
# # # def phasewrap(x):
# # #     return x - 2.0 * np.pi * np.round(x / (2.0 * np.pi))
# # # 
# # # 
# # # def moving_spectrum_wrapper(g):
# # #     g.amps = np.zeros(g.n)
# # #     g.phases = np.zeros(g.n)
# # #     g.amp_incs = np.zeros(g.n)
# # #     g.freqs = np.zeros(g.n)
# # #     g.freq_incs = np.zeros(g.n)
# # #     g.new_freq_incs = np.zeros(g.n)
# # #     g.data = np.zeros(g.n)
# # #     g.dataloc = 0
# # #     g.window = make_fft_window(g.window, g.n)
# # #     s = np.sum(g.window)
# # #     g.window = g.window * (2./s)
# # #     g.outctr = g.n+1
# # #     return g
# # #     
# # # moving_spectrum_methods = {'mus_xcoeffs' : [lambda g : g.phases, None],
# # #                         'mus_ycoeffs' : [lambda g : g.amps, None],
# # #                         'mus_run' : [lambda g,arg1,arg2 : moving_spectrum(g), None]}
# # # 
# # # make_moving_spectrum, is_moving_spectrum = make_generator('moving_spectrum', 
# # #                 {'input' : False, 
# # #                 'n' : 512, 
# # #                 'hop' : 128, 
# # #                 'window' : Window.HAMMING},
# # #                 wrapper=moving_spectrum_wrapper, 
# # #                 methods=moving_spectrum_methods,
# # #                 docstring="""returns a moving-spectrum generator.""")    
# # # 
# # # 
# # # 
# # # def moving_spectrum(gen):
# # #     if gen.outctr >= gen.hop:
# # #         # first time through fill data array with n samples
# # #         if gen.outctr > gen.n:
# # #             for i in range(gen.n):
# # #                 gen.data[i] = readin(gen.input)
# # #         #
# # #         else:
# # #             mid = gen.n - gen.hop
# # #             gen.data = np.roll(gen.data, gen.hop)
# # #             for i in range(mid,gen.n):
# # #                 gen.data[i] = readin(gen.input)
# # #         
# # #         gen.outctr = 0
# # #         gen.dataloc = gen.dataloc % gen.n
# # # 
# # #         gen.new_freq_incs.fill(0.0)
# # #        
# # #         data_start = 0
# # #         data_end = gen.n - gen.dataloc
# # #         
# # # 
# # #         gen.amp_incs[gen.dataloc:gen.n] = gen.window[data_start:data_end] * gen.data[data_start:data_end]
# # # 
# # #         if gen.dataloc > 0:
# # #             data_start = gen.n - gen.dataloc
# # #             data_end = data_start + gen.dataloc
# # #             gen.amp_incs[0:gen.dataloc] = gen.window[data_start:data_end] * gen.data[data_start:data_end]  
# # #         
# # #         gen.dataloc += gen.hop
# # #         
# # #         mus_fft(gen.amp_incs, gen.new_freq_incs, gen.n, 1)
# # # 
# # #         gen.amp_incs = rectangular2polar(gen.amp_incs, gen.new_freq_incs)
# # #                 
# # #         scl = 1.0 / gen.hop
# # #         kscl = (np.pi*2) / gen.n
# # #         gen.amp_incs -= gen.amps
# # # 
# # #         gen.amp_incs *= scl
# # # 
# # #         
# # #         
# # #         n2 = gen.n // 2
# # #         ks = 0.0
# # #         for i in range(n2):
# # #             diff = (gen.new_freq_incs[i] - gen.freq_incs[i]) #% (np.pi*2)
# # #             gen.freq_incs[i] = gen.new_freq_incs[i]
# # #            # diff = phasewrap(diff)
# # #             if diff > np.pi:
# # #                 diff = diff - (2*np.pi)
# # #             if diff < -np.pi:
# # #                 diff = diff + (2*np.pi)
# # #             gen.new_freq_incs[i] = diff*scl + ks
# # #             ks += kscl
# # #         gen.new_freq_incs -= gen.freqs
# # #         gen.new_freq_incs *= scl
# # # 
# # #         
# # # 
# # #     gen.outctr += 1
# # #     
# # #     gen.amps += gen.amp_incs
# # #     gen.freqs += gen.new_freq_incs
# # #     gen.phases += gen.freqs
# # # 
# # # # #  
# # # # # 
# --------------- moving-scentroid ---------------- # 

# cdef class MovingScentroid(CLMGenerator):
# 
#     def __init__(self, dbfloor=-40.0, rfreq=100., size=4096, hop=1024, outctr=0):
#         self.dbfloor = dbfloor
#         self.rfreq = rfreq
#         self.size = size
#         self.outctr = outctr
#         self.curval = 0.0
#         self.rl = np.zeros(self.n)
#         self.im = np.zeros(self.n)
#         self.dly = clm.make_delay(self.n)
#         self.rms = make_moving_rms(self.n)
#         self.hop = floor(clm.get_srate() / self.rfreq)
#         self.binwidth = (clm.get_srate() / self.n)
#         
#     cpdef cython.double next(self, cython.double x =0.0):
#         cdef cython.double rms = moving_rms(self.rms, x)
#         cdef np.ndarray data
#         cdef cython.int fft2 = 0
#         cdef cython.double numsum = 0.0
#         cdef cython.double densum = 0.0
# 
#         if self.outctr >= self.hop:
#             self.outctr = 0
#             if clm.linear2db(rms) < self.dbfloor:
#                 self.curval = 0.0
#             else:
#                 data = self.dly.mus_data
#                 fft2 = self.size // 2
#                 self.im.fill(0.)
#                 np.copyto(self.rl, data[self.size - 1])
#                 clm.mus_fft(self.rl, self.im, self.size, 1)
#                 clm.mus_rectangular2magnitudes(self.rl, self.im)
#                 numsum = 0.0
#                 densum = 0.0
#                 for k in range(fft2):
#                     self.curval = (self.binwidth*numsum) / densum
#                     numsum += k * self.rl[k]
#                     densum += self.rl[k]
#         clm.delay(self.dly, x)
#         self.outctr += 1
#         return self.curval
#    
#     def __call__(self, cython.double x=0.) -> cython.double:
#         return self.next(x)
#         
# 
# cpdef MovingScentroid make_moving_scentroid(dbfloor=-40.0, rfreq=100., size=4096, hop=1024, outctr=0):
#     return MovingScentroid(dbfloor, rfreq, size, hop, outctr)
#     
# cpdef cython.double moving_scentroid(MovingScentroid gen, cython.double x=0.):
#     return gen.next(x)
#     
# cpdef cython.bint is_moving_scentroid(gen):
#     return isinstance(gen, MovingScentroid)    
    

# # 
# # # TODO: --------------- moving-autocorrelation ---------------- # 
# # 
# # # TODO: --------------- moving-pitch ---------------- # 
# # 
# # # TODO: --------------- flocsig ---------------- # 
# 
