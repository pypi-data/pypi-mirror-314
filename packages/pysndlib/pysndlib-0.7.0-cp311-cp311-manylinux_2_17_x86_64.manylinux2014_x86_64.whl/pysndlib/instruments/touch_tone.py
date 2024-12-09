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


# --------------- touch_tone ---------------- #
# ;;; I think the dial tone is 350 + 440
# ;;; http://www.hackfaq.org/telephony/telephone-tone-frequencies.shtml

@cython.ccall
def touch_tone(start, telephone_number):
    touch_tab_1 = [0,697,697,697,770,770,770,852,852,852,941,941,941]
    touch_tab_2 = [0,1209,1336,1477,1209,1336,1477,1209,1336,1477,1209,1336,1477]
    
    
    i: cython.long = 0
    j: cython.long = 0
    
    for i in range(len(telephone_number)):
        k = telephone_number[i]
        beg: cython.long = clm.seconds2samples(start + (i * .4))
        end:  cython.long = beg + clm.seconds2samples(.3)
        if clm.is_number(k):
            i = k if not (0 == k) else 11
        else:
            i = 10 if k == '*' else 12
        
        frq1: clm.mus_any  = clm.make_oscil(touch_tab_1[i])
        frq2: clm.mus_any  = clm.make_oscil(touch_tab_2[i])
        
        for j in range(beg, end):
            clm.outa(j, (.1 * (clm.oscil(frq1) + clm.oscil(frq2))))

if __name__ == '__main__':             
    with clm.Sound( play = True, statistics=True):
        touch_tone(0, [8,6,7,5,3,0,9])
        
