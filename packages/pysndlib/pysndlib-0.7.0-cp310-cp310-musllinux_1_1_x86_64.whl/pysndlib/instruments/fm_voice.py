#==================================================================================
# The code is from Rick Taube's faithful translation of Bill Schottstedaet's 'jcvoi.scm' 
# file  available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

# from VOIDAT.SAI[220,JDC] and GLSVOI.SAI[220,JDC], then (30 years later) jcvoi.ins

# python -m jcvoi

import math
import cython
import numpy as np
from pysndlib.env import add_envelopes, scale_envelope
import pysndlib.clm as clm
if cython.compiled:
    from cython.cimports.pysndlib import clm



# globals
fnc = [None] * 288  # 288 = (* 3 6 4 4)
vibfreqfun = [None] * 3
i3fun1 = [None] * 3
i3fun2 = [None] * 3


def flipxy(data):
    # SEG functions expected data in (y x) pairs.
    unseg = []
    length = len(data)
    i = 0
    while i < length:
        x = data[i + 1]
        y = data[i]
        unseg.append(x)
        unseg.append(y)
        i += 2
    return clm.make_env(unseg)


def setf_aref(vect, a, b, c, d, val):
    vect[a + (3 * b) + (18 * c) + (72 * d)] = val

    
def aref(vect, a, b, c, d):
    return vect[a + (3 * b) + (18 * c) + (72 * d)]

# init the envelopes (this was in a fucniot)
setf_aref(fnc, 1, 1, 1, 1, flipxy([350, 130.8, 524, 261.6, 392, 392, 523, 523.2, 784, 784, 1046, 1064, 1568, 1568]))
setf_aref(fnc, 1, 1, 1, 2, flipxy([0.3, 130.8, 0.8, 261.6, 0.9, 392, 0.9, 523.2, 0.7, 784, 0.86, 1064, 0.86, 1568]))
setf_aref(fnc, 1, 1, 1, 3, flipxy([1.4, 130.8, 1.4, 261.6, 1.0, 392, 0.8, 523.2, 0.5, 784, 0.3, 1064, 0.2, 1568]))
setf_aref(fnc, 1, 1, 2, 1, flipxy([1100, 130.8, 1100, 261.6, 1100, 392, 1200, 523.2, 1500, 784, 1800, 1064, 2200, 1568]))
setf_aref(fnc, 1, 1, 2, 2, flipxy([0.1, 130.8, 0.2, 261.6, 0.3, 392, 0.3, 523.2, 0.1, 784, 0.05, 1064, 0.05, 1568]))
setf_aref(fnc, 1, 1, 2, 3, flipxy([1.0, 130.8, 1.0, 261.6, 0.4, 392, 0.4, 523.2, 0.2, 784, 0.2, 1064, 0.1, 1568]))
setf_aref(fnc, 1, 1, 3, 1, flipxy([3450, 130.8, 3400, 261.6, 3400, 392, 3600, 523.2, 4500, 784, 5000, 1064, 5800, 1568]))
setf_aref(fnc, 1, 1, 3, 2, flipxy([0.04, 130.8, 0.04, 261.6, 0.04, 392, 0.045, 523.2, 0.03, 784, 0.02, 1064, 0.02, 1568]))
setf_aref(fnc, 1, 1, 3, 3, flipxy([3.5, 130.8, 2.0, 261.6, 1.5, 392, 1.2, 523.2, 0.8, 784, 0.8, 1064, 1.0, 1568]))
setf_aref(fnc, 1, 2, 1, 1, flipxy([175, 130.8, 262, 261.6, 392, 392, 523, 523.2, 784, 784, 1046, 1064, 1568, 1568]))
setf_aref(fnc, 1, 2, 1, 2, flipxy([0.25, 130.8, 0.6, 261.6, 0.6, 392, 0.6, 523.2, 0.7, 784, 0.86, 1064, 0.86, 1568]))
setf_aref(fnc, 1, 2, 1, 3, flipxy([0.5, 130.8, 0.3, 261.6, 0.1, 392, 0.05, 523.2, 0.04, 784, 0.03, 1064, 0.02, 1568]))
setf_aref(fnc, 1, 2, 2, 1, flipxy([2900, 130.8, 2700, 261.6, 2600, 392, 2400, 523.2, 2300, 784, 2200, 1064, 2100, 1568]))
setf_aref(fnc, 1, 2, 2, 2, flipxy([0.01, 130.8, 0.05, 261.6, 0.08, 392, 0.1, 523.2, 0.1, 784, 0.1, 1064, 0.05, 1568]))
setf_aref(fnc, 1, 2, 2, 3, flipxy([1.5, 130.8, 1.0, 261.6, 1.0, 392, 1.0, 523.2, 1.0, 784, 1.0, 1064, 0.5, 1568]))
setf_aref(fnc, 1, 2, 3, 1, flipxy([4200, 130.8, 3900, 261.6, 3900, 392, 3900, 523.2, 3800, 784, 3700, 1064, 3600, 1568]))
setf_aref(fnc, 1, 2, 3, 2, flipxy([0.01, 130.8, 0.04, 261.6, 0.03, 392, 0.03, 523.2, 0.03, 784, 0.03, 1064, 0.02, 1568]))
setf_aref(fnc, 1, 2, 3, 3, flipxy([1.2, 130.8, 0.8, 261.6, 0.8, 392, 0.8, 523.2, 0.8, 784, 0.8, 1064, 0.5, 1568]))
setf_aref(fnc, 1, 3, 1, 1, flipxy([175, 130.8, 262, 261.6, 392, 392, 523, 523.2, 784, 784, 1046, 1064, 1568, 1568]))
setf_aref(fnc, 1, 3, 1, 2, flipxy([0.3, 130.8, 0.7, 261.6, 0.8, 392, 0.6, 523.2, 0.7, 784, 0.86, 1064, 0.86, 1568]))
setf_aref(fnc, 1, 3, 1, 3, flipxy([0.4, 130.8, 0.2, 261.6, 0.4, 392, 0.4, 523.2, 0.7, 784, 0.5, 1064, 0.2, 1568]))
setf_aref(fnc, 1, 3, 2, 1, flipxy([1000, 130.8, 1000, 261.6, 1100, 392, 1200, 523.2, 1400, 784, 1800, 1064, 2200, 1568]))
setf_aref(fnc, 1, 3, 2, 2, flipxy([0.055, 130.8, 0.1, 261.6, 0.15, 392, 0.13, 523.2, 0.1, 784, 0.1, 1064, 0.05, 1568]))
setf_aref(fnc, 1, 3, 2, 3, flipxy([0.3, 130.8, 0.4, 261.6, 0.4, 392, 0.4, 523.2, 0.3, 784, 0.2, 1064, 0.1, 1568]))
setf_aref(fnc, 1, 3, 3, 1, flipxy([2600, 130.8, 2600, 261.6, 3000, 392, 3400, 523.2, 4500, 784, 5000, 1064, 5800, 1568]))
setf_aref(fnc, 1, 3, 3, 2, flipxy([0.005, 130.8, 0.03, 261.6, 0.04, 392, 0.04, 523.2, 0.02, 784, 0.02, 1064, 0.02, 1568]))
setf_aref(fnc, 1, 3, 3, 3, flipxy([1.1, 130.8, 1.0, 261.6, 1.2, 392, 1.2, 523.2, 0.8, 784, 0.8, 1064, 1.0, 1568]))
setf_aref(fnc, 1, 4, 1, 1, flipxy([353, 130.8, 530, 261.6, 530, 392, 523, 523.2, 784, 784, 1046, 1064, 1568, 1568]))
setf_aref(fnc, 1, 4, 1, 2, flipxy([0.5, 130.8, 0.8, 261.6, 0.8, 392, 0.6, 523.2, 0.7, 784, 0.86, 1064, 0.86, 1568]))
setf_aref(fnc, 1, 4, 1, 3, flipxy([0.6, 130.8, 0.7, 261.6, 1.0, 392, 0.8, 523.2, 0.7, 784, 0.5, 1064, 0.2, 1568]))
setf_aref(fnc, 1, 4, 2, 1, flipxy([1040, 130.8, 1040, 261.6, 1040, 392, 1200, 523.2, 1400, 784, 1800, 1064, 2200, 1568]))
setf_aref(fnc, 1, 4, 2, 2, flipxy([0.050, 130.8, 0.05, 261.6, 0.1, 392, 0.2, 523.2, 0.1, 784, 0.1, 1064, 0.05, 1568]))
setf_aref(fnc, 1, 4, 2, 3, flipxy([0.1, 130.8, 0.1, 261.6, 0.1, 392, 0.4, 523.2, 0.3, 784, 0.2, 1064, 0.1, 1568]))
setf_aref(fnc, 1, 4, 3, 1, flipxy([2695, 130.8, 2695, 261.6, 2695, 392, 3400, 523.2, 4500, 784, 5000, 1064, 5800, 1568]))
setf_aref(fnc, 1, 4, 3, 2, flipxy([0.05, 130.8, 0.05, 261.6, 0.04, 392, 0.04, 523.2, 0.02, 784, 0.02, 1064, 0.02, 1568]))
setf_aref(fnc, 1, 4, 3, 3, flipxy([1.2, 130.8, 1.2, 261.6, 1.2, 392, 1.2, 523.2, 0.8, 784, 0.8, 1064, 1.0, 1568]))
setf_aref(fnc, 1, 5, 1, 1, flipxy([175, 130.8, 262, 261.6, 392, 392, 523, 523.2, 784, 784, 1046, 1064, 1568, 1568]))
setf_aref(fnc, 1, 5, 1, 2, flipxy([0.4, 130.8, 0.4, 261.6, 0.8, 392, 0.8, 523.2, 0.8, 784, 0.8, 1064, 0.8, 1568]))
setf_aref(fnc, 1, 5, 1, 3, flipxy([0.1, 130.8, 0.1, 261.6, 0.1, 392, 0.1, 523.2, 0.0, 784, 0.0, 1064, 0.0, 1568]))
setf_aref(fnc, 1, 5, 2, 1, flipxy([350, 130.8, 524, 261.6, 784, 392, 950, 523.2, 1568, 784, 2092, 1064, 3136, 1568]))
setf_aref(fnc, 1, 5, 2, 2, flipxy([0.8, 130.8, 0.8, 261.6, 0.4, 392, 0.2, 523.2, 0.1, 784, 0.1, 1064, 0.0, 1568]))
setf_aref(fnc, 1, 5, 2, 3, flipxy([0.5, 130.8, 0.1, 261.6, 0.1, 392, 0.1, 523.2, 0.0, 784, 0.0, 1064, 0.0, 1568]))
setf_aref(fnc, 1, 5, 3, 1, flipxy([2700, 130.8, 2700, 261.6, 2500, 392, 2450, 523.2, 2400, 784, 2350, 1064, 4500, 1568]))
setf_aref(fnc, 1, 5, 3, 2, flipxy([.1,  130.8, .15, 261.6, .15, 392, .15, 523.2, .15, 784, .1,  1064,  .1,  1568]))
setf_aref(fnc, 1, 5, 3, 3, flipxy([2.0, 130.8, 1.6, 261.6, 1.6, 392, 1.6, 523.2, 1.6, 784, 1.6, 1064, 1.0,  1568]))
setf_aref(fnc, 2, 1, 1, 1, flipxy([33, 16.5, 33, 24.5, 33, 32.7, 49, 49.0, 65, 65.41, 98, 98, 131, 130.8]))
setf_aref(fnc, 2, 1, 1, 2, flipxy([0.3, 16.5, 0.5, 24.5, 0.6, 32.7, 0.5, 49.0, 0.47, 65.41, 0.135, 98, 0.2, 130.8]))
setf_aref(fnc, 2, 1, 1, 3, flipxy([2.4, 16.5, 2.0, 24.5, 1.8, 32.7, 1.6, 49.0, 1.5, 65.41, 1.2, 98, 0.8, 130.8]))
setf_aref(fnc, 2, 1, 2, 1, flipxy([400, 16.5, 400, 24.5, 400, 32.7, 400, 49.0, 400, 65.41, 400, 98, 400, 130.8]))
setf_aref(fnc, 2, 1, 2, 2, flipxy([0.2, 16.5, 0.2, 24.5, 0.35, 32.7, 0.37, 49.0, 0.4, 65.41, 0.6, 98, 0.8, 130.8]))
setf_aref(fnc, 2, 1, 2, 3, flipxy([6.0, 16.5, 5.0, 24.5, 4.0, 32.7, 3.0, 49.0, 2.7, 65.41, 2.2, 98, 1.8, 130.8]))
setf_aref(fnc, 2, 1, 3, 1, flipxy([2142, 16.5, 2142, 24.5, 2142, 32.7, 2142, 49.0, 2142, 65.41, 2142, 98, 2142, 130.8]))
setf_aref(fnc, 2, 1, 3, 2, flipxy([0.02, 16.5, 0.025, 24.5, 0.05, 32.7, 0.09, 49.0, 0.13, 65.41, 0.29, 98, 0.4, 130.8]))
setf_aref(fnc, 2, 1, 3, 3, flipxy([9.0, 16.5, 8.0, 24.5, 7.2, 32.7, 5.5, 49.0, 3.9, 65.41, 3.0, 98, 1.8, 130.8]))
setf_aref(fnc, 2, 2, 1, 1, flipxy([33, 16.5, 33, 24.5, 33, 32.7, 49, 49.0, 65, 65.41, 98, 98, 131, 130.8]))
setf_aref(fnc, 2, 2, 1, 2, flipxy([0.75, 16.5, 0.83, 24.5, 0.91, 32.7, 0.88, 49.0, 0.90, 65.41, 0.87, 98, 0.85, 130.8]))
setf_aref(fnc, 2, 2, 1, 3, flipxy([1.4, 16.5, 1.4, 24.5, 1.4, 32.7, 1.4, 49.0, 1.4, 65.41, 1.4, 98, 1.4, 130.8]))
setf_aref(fnc, 2, 2, 2, 1, flipxy([1500, 16.5, 1500, 24.5, 1500, 32.7, 1500, 49.0, 1500, 65.41, 1500, 98, 1500, 130.8]))
setf_aref(fnc, 2, 2, 2, 2, flipxy([0.01, 16.5, 0.02, 24.5, 0.02, 32.7, 0.02, 49.0, 0.02, 65.41, 0.08, 98, 0.08, 130.8]))
setf_aref(fnc, 2, 2, 2, 3, flipxy([1.5, 16.5, 1.37, 24.5, 1.25, 32.7, 1.07, 49.0, 0.9, 65.41, 0.7, 98, 0.5, 130.8]))
setf_aref(fnc, 2, 2, 3, 1, flipxy([2300, 16.5, 2300, 24.5, 2300, 32.7, 2325, 49.0, 2350, 65.41, 2375, 98, 2400, 130.8]))
setf_aref(fnc, 2, 2, 3, 2, flipxy([0.05, 16.5, 0.05, 24.5, 0.05, 32.7, 0.05, 49.0, 0.05, 65.41, 0.075, 98, 0.1, 130.8]))
setf_aref(fnc, 2, 2, 3, 3, flipxy([11.0, 16.5, 10.0, 24.5, 10.0, 32.7, 7.7, 49.0, 5.4, 65.41, 3.7, 98, 2.0, 130.8]))
setf_aref(fnc, 2, 3, 1, 1, flipxy([33, 16.5, 33, 24.5, 33, 32.7, 49, 49.0, 65, 65.41, 98, 98, 131, 130.8]))
setf_aref(fnc, 2, 3, 1, 2, flipxy([0.75, 16.5, 0.83, 24.5, 0.87, 32.7, 0.88, 49.0, 0.90, 65.41, 0.87, 98, 0.85, 130.8]))
setf_aref(fnc, 2, 3, 1, 3, flipxy([1.4, 16.5, 1.4, 24.5, 1.4, 32.7, 1.4, 49.0, 1.4, 65.41, 1.4, 98, 1.4, 130.8]))
setf_aref(fnc, 2, 3, 2, 1, flipxy([450, 16.5, 450, 24.5, 450, 32.7, 450, 49.0, 450, 65.41, 450, 98, 450, 130.8]))
setf_aref(fnc, 2, 3, 2, 2, flipxy([0.01, 16.5, 0.02, 24.5, 0.08, 32.7, 0.065, 49.0, 0.05, 65.41, 0.05, 98, 0.05, 130.8]))
setf_aref(fnc, 2, 3, 2, 3, flipxy([3.0, 16.5, 2.6, 24.5, 2.1, 32.7, 1.75, 49.0, 1.4, 65.41, 1.05, 98, 0.7, 130.8]))
setf_aref(fnc, 2, 3, 3, 1, flipxy([2100, 16.5, 2100, 24.5, 2100, 32.7, 2125, 49.0, 2150, 65.41, 2175, 98, 2100, 130.8]))
setf_aref(fnc, 2, 3, 3, 2, flipxy([0.05, 16.5, 0.05, 24.5, 0.05, 32.7, 0.05, 49.0, 0.05, 65.41, 0.075, 98, 0.1, 130.8]))
setf_aref(fnc, 2, 3, 3, 3, flipxy([9.0, 16.5, 8.0, 24.5, 7.0, 32.7, 4.5, 49.0, 2.1, 65.41, 1.75, 98, 1.4, 130.8]))
setf_aref(fnc, 2, 4, 1, 1, flipxy([33, 16.5, 33, 24.5, 33, 32.7, 49, 49.0, 65, 65.41, 98, 98, 131, 130.8]))
setf_aref(fnc, 2, 4, 1, 2, flipxy([0.35, 16.5, 0.40, 24.5, 0.43, 32.7, 0.47, 49.0, 0.50, 65.41, 0.57, 98, 0.45, 130.8]))
setf_aref(fnc, 2, 4, 1, 3, flipxy([1.4, 16.5, 1.4, 24.5, 1.0, 32.7, 1.0, 49.0, 1.0, 65.41, 1.1, 98, 1.0, 130.8]))
setf_aref(fnc, 2, 4, 2, 1, flipxy([300, 16.5, 300, 24.5, 300, 32.7, 300, 49.0, 300, 65.41, 300, 98, 300, 130.8]))
setf_aref(fnc, 2, 4, 2, 2, flipxy([0.75, 16.5, 0.80, 24.5, 0.85, 32.7, 0.90, 49.0, 0.95, 65.41, 0.99, 98, 0.99, 130.8]))
setf_aref(fnc, 2, 4, 2, 3, flipxy([3.0, 16.5, 2.5, 24.5, 2.0, 32.7, 1.9, 49.0, 1.8, 65.41, 1.65, 98, 0.25, 130.8]))
setf_aref(fnc, 2, 4, 3, 1, flipxy([2200, 16.5, 2200, 24.5, 2200, 32.7, 2225, 49.0, 2250, 65.41, 2275, 98, 2300, 130.8]))
setf_aref(fnc, 2, 4, 3, 2, flipxy([0.02, 16.5, 0.02, 24.5, 0.02, 32.7, 0.035, 49.0, 0.05, 65.41, 0.07, 98, 0.05, 130.8]))
setf_aref(fnc, 2, 4, 3, 3, flipxy([5.0, 16.5, 4.0, 24.5, 3.0, 32.7, 2.8, 49.0, 2.6, 65.41, 1.9, 98, 1.2, 130.8]))
setf_aref(fnc, 2, 5, 1, 1, flipxy([  33, 16.5,   33,  24.5,   33, 32.7,  49,  49.0,   65, 65.41,   98, 98,  131, 130.8]))
setf_aref(fnc, 2, 5, 1, 2, flipxy([ .40, 16.5,  .40,  24.5,  .80, 32.7, .80,  49.0,  .80, 65.41,  .80, 98,  .80, 130.8]))
setf_aref(fnc, 2, 5, 1, 3, flipxy([ 0.1, 16.5,  0.1,  24.5,  0.1, 32.7, 0.1,  49.0,  0.0, 65.41,  0.0, 98,  0.0, 130.8]))
setf_aref(fnc, 2, 5, 2, 1, flipxy([ 350, 16.5,  524,  24.5,  784, 32.7,  950, 49.0, 1568, 65.41, 2092, 98, 3136, 130.8]))
setf_aref(fnc, 2, 5, 2, 2, flipxy([ .80, 16.5,  .80,  24.5,  .40, 32.7,  .20, 49.0,  .10, 65.41,  .10, 98,  .00, 130.8]))
setf_aref(fnc, 2, 5, 2, 3, flipxy([ 0.5, 16.5,  0.1,  24.5,  0.1, 32.7,  0.1, 49.0,  0.0, 65.41,  0.0, 98,  0.0, 130.8]))
setf_aref(fnc, 2, 5, 3, 1, flipxy([2700, 16.5, 2700,  24.5, 2500, 32.7, 2450, 49.0, 2400, 65.41, 2350, 98, 4500, 130.8]))
setf_aref(fnc, 2, 5, 3, 2, flipxy([ .10, 16.5,  .15,  24.5,  .15, 32.7,  .15, 49.0,  .15, 65.41,  .10, 98,  .10, 130.8]))
setf_aref(fnc, 2, 5, 3, 3, flipxy([ 2.0, 16.5,  1.6,  24.5,  1.6, 32.7,  1.6, 49.0,  1.6, 65.41,  1.5, 98,  1.0, 130.8]))	
# these are vibrato frequencies functions (pitch dependent);
vibfreqfun[1] = flipxy([4.5, 138.8, 5, 1568])
vibfreqfun[2] = flipxy([4.5, 16.5, 5, 130.8])
# these are index functions for cascade modulater (pitch dependent);
i3fun1[1] = flipxy([4, 138.8, 4, 784, 1, 1568])
i3fun1[2] = flipxy([4, 16.5, 4, 65.41, 1, 130.8])
i3fun2[1] = flipxy([0.4, 138.8, 0.1, 1568])
i3fun2[2] = flipxy([0.4, 16.5, 0.1, 130.8])


@cython.ccall
def fncval(ptr, pitch):
    return clm.envelope_interp(pitch, ptr)


@cython.ccall
def fm_voice(beg, dur, pitch, amp, vowel_1, sex_1, ampfun1, ampfun2, ampfun3, indxfun, skewfun, vibfun, ranfun,
             dis, pcrev, deg, vibscl, pcran, skewscl, glissfun, glissamt):
             
    vowel = int(vowel_1)
    sex = int(sex_1)
    ampref = amp ** 0.8
    deg -= 45
    fm2: cython.double = 3
    mscale: cython.double = 1
    vibfreq = fncval(vibfreqfun[sex], pitch)
    vibpc = 0.01 * math.log(pitch, 2) * (0.15 + math.sqrt(amp)) * vibscl
    ranpc = 0.002 * math.log(pitch, 2) * (2 - amp ** 0.25) * pcran
    #print(f"skewscl: {skewscl}, ampref: {ampref}, sex: {sex}")
    skewpc = skewscl * math.sqrt(0.1 + (0.05 * ampref * ((1568 - 130.8) if (sex == 1) else (130.8 - 16.5))))
    form1 = fncval(aref(fnc, sex, vowel, 1, 1), pitch) / pitch
    form2 = fncval(aref(fnc, sex, vowel, 2, 1), pitch) / pitch
    form3 = fncval(aref(fnc, sex, vowel, 3, 1), pitch) / pitch
    mconst = 0
    fmntfreq1: cython.double = round(form1)
    fmntfreq2: cython.double = round(form2)
    fmntfreq3: cython.double = round(form3)
    mfq: cython.double = pitch * mscale + mconst
    c: cython.double = 261.62
    amp1 = math.sqrt(amp)
    amp2 = amp ** 1.5
    amp3 = amp * amp
    indx1 = 1
    formscl1: cython.double = abs(form1 - fmntfreq1)
    formscl2: cython.double = abs(form2 - fmntfreq2)
    formscl3: cython.double = abs(form3 - fmntfreq3)
    if pitch < c/2:
        i3 = fncval(i3fun1[sex], pitch)
    else:
        i3 = fncval(i3fun2[sex], pitch)  
    indx0 = 0 if vowel in [3, 4] else 1.5
    caramp1sc = fncval(aref(fnc, sex, vowel, 1, 2), pitch) * (1 - formscl1) * amp1
    caramp2sc = fncval(aref(fnc, sex, vowel, 2, 2), pitch) * (1 - formscl2) * amp2
    caramp3sc = fncval(aref(fnc, sex, vowel, 3, 2), pitch) * (1 - formscl3) * amp3
    ranfreq = 20
    scdev1 = fncval(aref(fnc, sex, vowel, 1, 3), pitch)
    scdev2 = fncval(aref(fnc, sex, vowel, 2, 3), pitch)
    scdev3 = fncval(aref(fnc, sex, vowel, 3, 3), pitch)
    dev: cython.double = clm.hz2radians(i3 * mfq)
    dev0 = clm.hz2radians(indx0 * mfq) 
    dev1 = clm.hz2radians((indx1 - indx0) * mfq)
    gens1 = clm.make_oscil(0)
    gens2 = clm.make_oscil(0, math.pi / 2.0)
    gens2ampenv = clm.make_env(indxfun, duration=dur, scaler=scdev1 * dev1, offset=scdev1 * dev0)
    gens3= clm.make_oscil(0, math.pi / 2.0)
    gens3ampenv = clm.make_env(indxfun, duration=dur, scaler=scdev2 * dev1, offset=scdev2 * dev0)
    gens4 = clm.make_oscil(0, math.pi / 2.0)
    gens4ampenv = clm.make_env(indxfun, duration=dur, scaler=scdev3 * dev1, offset=scdev3 * dev0)
    gens5 = clm.make_oscil(0)
    gens5ampenv = clm.make_env(ampfun1, duration=dur, scaler=amp * caramp1sc * 0.75)
    gens6 = clm.make_oscil(0)
    gens6ampenv = clm.make_env(ampfun2, duration=dur, scaler=amp * caramp2sc * 0.75)
    gens7 = clm.make_oscil(0)
    gens7ampenv = clm.make_env(ampfun3, duration=dur, scaler=amp * caramp3sc * 0.75)
    #freqenv = make_env(addenv(glissfun, glissamt * pitch, 0, skewfun, skewscl * pitch, pitch), duration=dur,
    #                  scaler=hz2radians(1.0))
    freqenv = clm.make_env(add_envelopes(scale_envelope(glissfun, glissamt * pitch, 0),
                                     scale_envelope(skewfun, skewscl * pitch, pitch)),
                       duration=dur, scaler=clm.hz2radians(1.0))
    pervenv = clm.make_env(vibfun, duration=dur, scaler=vibpc)
    ranvenv = clm.make_env(envelope=ranfun, duration=dur, scaler=ranpc)
    per_vib = clm.make_triangle_wave(frequency=vibfreq, amplitude=clm.hz2radians(pitch))
    ran_vib = clm.make_rand_interp(frequency=ranfreq, amplitude=clm.hz2radians(pitch))
    loc = clm.make_locsig(degree=deg, distance=dis, reverb=pcrev)
    
    start: cython.long = clm.seconds2samples(beg)
    end: cython.long = clm.seconds2samples(beg+dur)
    i: cython.long = 0
    
    for i in range(start, end):
        vib: cython.double = clm.env(freqenv) + (clm.env(pervenv) * clm.triangle_wave(per_vib)) + (clm.env(ranvenv) * clm.rand_interp(ran_vib))
        cascadeout: cython.double = dev * clm.oscil(gens1, vib * fm2)
        a: cython.double = clm.env(gens5ampenv) * clm.oscil(gens5, (vib * fmntfreq1) + ( clm.env(gens2ampenv) * clm.oscil(gens2, cascadeout + (vib * mscale))))
        b: cython.double = clm.env(gens6ampenv) * clm.oscil(gens6, (vib * fmntfreq2) + ( clm.env(gens3ampenv) * clm.oscil(gens3, cascadeout + (vib * mscale))))
        c: cython.double = clm.env(gens7ampenv) * clm.oscil(gens7, (vib * fmntfreq3) + ( clm.env(gens4ampenv) * clm.oscil(gens4, cascadeout + (vib * mscale))))
        clm.locsig(loc, i, a + b + c)


# if __name__ == '__main__':
# 
#     # with Sound (play=True):
#     #     ampf = [0, 0, 1, 1, 2, 1, 3, 0]
#     #     fm_voice(0, 4, 300, .8, 3, 1, ampf, ampf, ampf, ampf, ampf, ampf, ampf,
#     #               1, 0, 0, .25, .01, 0, ampf, .01)
# 
#     # exit()
# 
#     # Old MacDonald -- including the lyrics to the first verse -- without consonants!
#     # --William Andrew Burnson <burnson2 (at) uiuc.edu>
# 
#     import musx
# 
#     gtime = 0
#     ampf = [0, 0, .4, 1, 2.6, 1, 3, 0]
#     w8 = 0.25
#     w4 = 0.5
#     w2 = 1.0
# 
#     def pwait(dur):
#         global gtime
#         gtime += dur
# 
#     def cow():
#         fm_voice(gtime, 1.0, 110, 0.8, 5, 1, 
#                  ampf, ampf, ampf, ampf, ampf, ampf, ampf,
#                  1, 0, 0, 0.0, 1, 0, [0, 1, 1, 0], 0.2)
# 
#     def vox(dur, note, vowel, sex, vib):
#         '''
#         dur is in seconds, note is in note name,
#         vowel is :ah :oh :ee :uh :ow :ay, sex is :male "female"
#         '''
#         v = 1
#         s = 1
#         if vowel in ['ah', 'oh']: v = 1
#         elif vowel == 'ee': v = 2
#         elif vowel == 'uh': v = 3
#         elif vowel == 'ow': v = 4
#         elif vowel == 'ay': v = 5
#         else: raise ValueError(f"Not a supported vowel: {vowel}")
# 
#         if sex == 'male': s = 1
#         elif sex == 'female': s = 2
#         else: raise ValueError(f"Not a supported sex: {sex}")
#         #print(gtime, dur, musx.hertz(note), 0.5, v, s,
#         #         'ampf', 'ampf', 'ampf', 'ampf', 'ampf', 'ampf', 'ampf',
#         #         1, 0, 0, 0.0, 1, 0.00, 'ampf', 0.00)
#         fm_voice(gtime, dur, musx.hertz(note)/2, 0.5, v, s,
#                  ampf, ampf, ampf, ampf, ampf, ampf, ampf,
#                  1, 0, 0, 0.0, 1, 0.00, ampf, 0.00)
#     
#     with Sound(play=True, channels=1, output="jcvoi-py-test.wav"):
# 
#         vox(w4, "c3", 'ah', 'male', 0.0)   
#         pwait(w8)
# 
#         vox(w8, "g3", "ow", "female", 0.0)
#         vox(w8, "e4", "ow", "female", 0.0)
#         pwait(w8)
# 
#         vox(w4, "ef3", "ee", "male", 0.0)
#         pwait(w8)
#   
#         vox(w8, "g3", "ow", "female", 0.0)
#         vox(w8, "e4", "ow", "female", 0.0)
#         pwait(w8)
# 
#         vox(w4, "f3", "ay", "female", 0.0)
#         pwait(w8)
#         
#         vox(w8, "c4", "ow", "female", 0.0)
#         vox(w8, "fs4", "ow", "female", 0.0)
#         pwait(w8)
#         
#         vox(w4, "a3", "uh", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "cs4", "ow", "female", 0.0)
#         vox(w8, "gs4", "ow", "female", 0.0)
#         pwait(w8)
#         
# 
#         
#         vox(w4, "d3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "a3", "ow", "female", 0.0)
#         vox(w8, "fs4", "ow", "female", 0.0)
#         pwait(w8)
#         
#         vox(w4, "g3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "b3", "ow", "female", 0.0)
#         vox(w8, "f4", "ow", "female", 0.0)
#         pwait(w8)
#         
# 
#         cow()
#         
#         vox(w8, "g4", "ee", "female", 0.0)
#         vox(w8, "e5", "ee", "female", 0.0)
#         pwait(w8)
#         vox(w8, "fs4", "ee", "female", 0.0)
#         vox(w8, "ds5", "ee", "female", 0.0)
#         pwait(w8)
#         vox(w8, "f4", "ee", "female", 0.0)
#         vox(w8, "d5", "ee", "female", 0.0)
#         pwait(w8)
#         vox(w8, "ef4", "ee", "female", 0.0)
#         vox(w8, "cs5", "ee", "female", 0.0)
#         pwait(w8)
#         
#         
# 
#         
#         vox(w8, "c6", "ow", "female", 0.5)
#         vox(w4, "c3", "ah", "male", 0.0)
#         pwait(w8)
#         
#         
#         vox(w8, "c6", "ay", "female", 0.5)
#         vox(w8, "g3", "ow", "female", 0.0)
#         vox(w8, "e4", "ow", "female", 0.0)
#         pwait(w8)
# 
#         vox(w8, "c6", "ah", "female", 0.5)
#         vox(w4, "ef3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "g5", "uh", "female", 0.5) 
#         vox(w8, "g3", "ow", "female", 0.0)
#         vox(w8, "e4", "ow", "female", 0.0)
#         pwait(w8)
#         
#         
# 
#         
#         vox(w8, "a5", "ah", "female", 0.5)
#         vox(w4, "f3", "ay", "female", 0.0)
#         pwait(w8)
#         
#         vox(w8, "a5", "ay", "female", 0.5)
#         vox(w8, "c4", "ow", "female", 0.0)
#         vox(w8, "fs4", "oh", "female", 0.0)
#         pwait(w8)
#         
#         vox(w4, "g5", "ah", "female", 0.5)
#         vox(w4, "a3", "uh", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "cs5", "ow", "female", 0.0)
#         vox(w8, "gs5", "ow", "female", 0.0)
#         pwait(w8)
#         
# 
#         vox(w8, "e6", "ee", "female", 0.5)
#         vox(w4, "d3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "e6", "ay", "female", 0.5)
#         vox(w8, "a3", "ow", "female", 0.0)
#         vox(w8, "fs4", "ow", "female", 0.0)
#         pwait(w8)
#         
#         vox(w8, "d6", "ee", "female", 0.5)
#         vox(w4, "g3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "d6", "ay", "female", 0.5)
#         vox(w8, "b3", "ow", "female", 0.0)
#         vox(w8, "f4", "ow", "female", 0.0)
#         pwait(w8)
#         
# 
#         vox(w4, "c6", "oh", "female", 0.5)
#         
#         vox(w8, "g4", "ee", "female", 0.0)
#         vox(w8, "e5", "ee", "female", 0.0)
#         pwait(w8)
#         vox(w8, "fs4", "ee", "female", 0.0)
#         vox(w8, "ds5", "ee", "female", 0.0)
#         pwait(w8)
#         (cow)
#         vox(w4, "g5", "ah", "female", 0.5)
#         vox(w8, "f4", "ee", "female", 0.0)
#         vox(w8, "d5", "ee", "female", 0.0)
#         pwait(w8)
#         vox(w8, "ef4", "ee", "female", 0.0)
#         vox(w8, "cs5", "ee", "female", 0.0)
#         pwait(w8)
#         
# 
#         
#         vox(w8, "c6", "ah", "female", 0.5)
#         vox(w4, "c3", "ah", "male", 0.0)
#         pwait(w8)
#         
#         
#         vox(w8, "c6", "ee", "female", 0.5)
#         vox(w8, "g3", "ow", "female", 0.0)
#         vox(w8, "e4", "ow", "female", 0.0)
#         pwait(w8)
#         
#         vox(w8, "c6", "ah", "female", 0.5)
#         vox(w4, "ef3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "g5", "ee", "female", 0.5)
#         vox(w8, "g3", "ow", "female", 0.0)
#         vox(w8, "e4", "ow", "female", 0.0)
#         pwait(w8)
#         
#         
#         
#         vox(w8, "a5", "ah", "female", 0.5)
#         vox(w4, "f3", "ay", "female", 0.0)
#         pwait(w8)
#         
#         vox(w8, "a5", "ay", "female", 0.5)
#         vox(w8, "c4", "ow", "female", 0.0)
#         vox(w8, "fs4", "oh", "female", 0.0)
#         pwait(w8)
#         
#         vox(w4, "g5", "ow", "female", 0.5)
#         vox(w4, "a3", "uh", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "cs5", "ow", "female", 0.0)
#         vox(w8, "gs5", "ow", "female", 0.0)
#         pwait(w8)
#         
# 
#         vox(w8, "e6", "ee", "female", 0.5)
#         vox(w4, "d3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "e6", "ay", "female", 0.5)
#         vox(w8, "a3", "ow", "female", 0.0)
#         vox(w8, "fs4", "ow", "female", 0.0)
#         pwait(w8)
#         
#         vox(w8, "d6", "ee", "female", 0.5)
#         vox(w4, "g3", "ee", "male", 0.0)
#         pwait(w8)
#         
#         vox(w8, "d6", "ay", "female", 0.5)
#         vox(w8, "b3", "ow", "female", 0.0)
#         vox(w8, "f4", "ow", "female", 0.0)
#         pwait(w8)
#         
# 
#         vox(w2, "c3", "ah", "male", 1.0)
#         vox(w2, "g3", "ah", "male", 1.0)
#         vox(w2, "c4", "ah", "male", 1.0)
#         vox(w2, "e5", "ah", "female", 1.0)
#         vox(w2, "c6", "oh", "female", 0.5) 
