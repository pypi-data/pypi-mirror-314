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

# --------------- scratch ---------------- #

# Made changes based on callback functions and such in python


def scratch(start, file, src_ratio, turnaroundlist):
    f = clm.make_file2frample(file)
    beg = clm.seconds2samples(start)
    turntable = turnaroundlist
    turn_i = 1
    turns = len(turnaroundlist)
    cur_sample = clm.seconds2samples(turntable[0])
    
    turn_sample = clm.seconds2samples(turntable[1])
    
    def func(direction):
        nonlocal cur_sample
        inval = clm.file2sample(f, cur_sample)
        cur_sample = cur_sample + direction
        return inval
   
    turning = 0
    last_val = 0.0
    last_val2 = 0.0
    rd = clm.make_src(func, srate=src_ratio)
    forwards = src_ratio > 0.0
    
    if forwards and turn_sample < cur_sample:
        rd.mus_increment = -src_ratio
    
    i: cython.long = beg
    
    while turn_i < turns:

        val = clm.src(rd, 0.0)

        if turning == 0:
            if forwards and (cur_sample >= turn_sample):
                turning = 1
            else:
                if (not forwards) and (cur_sample <= turn_sample):
                    turning = -1
        else:                
            if ((last_val2 <= last_val) and (last_val >= val)) or ((last_val2 >= last_val) and (last_val <= val)):
                turn_i += 1
                if turn_i < turns:
                    turn_sample = clm.seconds2samples(turntable[turn_i])
                    forwards = not forwards
                    rd.mus_increment = -rd.mus_increment
                turning = 0
        last_val2 = last_val
        last_val = val
        clm.outa(i, val)
        i += 1

if __name__ == '__main__': 
    with clm.Sound( play = True, statistics=True):
        scratch(0.0, '../examples/yeah.aiff', 1., [0.0, .5, .25, 1.0, .5, 5.0])    


                   
                    
