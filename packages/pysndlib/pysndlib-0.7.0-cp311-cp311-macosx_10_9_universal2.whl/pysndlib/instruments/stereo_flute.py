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

# --------------- stereo_flute ---------------- #
# TODO: Am getting strange artifact at beginning 
@cython.ccall
def stereo_flute(start,dur,freq,flow,
                flow_envelope = [0,1,100,1], 
                decay=.01, 
                noise=0.0356, 
                embouchure_size=0.5,
                fbk_scl1=.5, 
                fbk_scl2=.55, 
                offset_pos=0.764264,
                out_scl=1.0, 
                a0=.7, 
                b1=-.3, 
                vib_rate=5, 
                vib_amount=.03, 
                ran_rate=5, 
                ran_amount=0.03):
                    
    period_samples: cython.double = math.floor(clm.default.srate / freq)
    embouchure_samples: cython.double = math.floor(embouchure_size * period_samples)
    current_excitation: cython.double = 0.0
    current_difference: cython.double = 0.0
    current_flow: cython.double = 0.0
    out_sig: cython.double = 0.0
    tap_sig: cython.double = 0.0
    previous_out_sig: cython.double = 0.0
    previous_tap_sig: cython.double = 0.0
    dc_blocked_a: cython.double = 0.0
    dc_blocked_b: cython.double = 0.0
    previous_dc_blocked_a: cython.double = 0.0
    previous_dc_blocked_b: cython.double = 0.0
    delay_sig: cython.double = 0.0
    emb_sig: cython.double = 0.0
    beg: cython.long = clm.seconds2samples(start)
    end: cython.long = clm.seconds2samples(start + dur)
    flowf = clm.make_env(flow_envelope, scaler=flow, duration=dur - decay)
    periodic_vibrato = clm.make_oscil(vib_rate)
    random_vibrato: clm.mus_any  = clm.make_rand_interp(ran_rate, ran_amount)
    breath  = clm.make_rand(clm.default.srate/2, amplitude=noise)
    embouchure  = clm.make_delay(embouchure_samples, initial_element=0.0)
    bore = clm.make_delay(period_samples)
    offset = math.floor(period_samples * offset_pos)
    reflection_lowpass_filter = clm.make_one_pole(a0, b1)

    i: cython.long = 0

    for i in range(beg, end):
        
        delay_sig = clm.delay(bore, out_sig)
        emb_sig = clm.delay(embouchure, current_difference)
        current_flow = (vib_amount * clm.oscil(periodic_vibrato)) + clm.rand_interp(random_vibrato) + clm.env(flowf)
        current_difference = current_flow + (current_flow * clm.rand(breath) + (fbk_scl1 * delay_sig))
        current_excitation = emb_sig - (emb_sig*emb_sig*emb_sig)
        out_sig = clm.one_pole(reflection_lowpass_filter, (current_excitation + (fbk_scl2 * delay_sig)))
        tap_sig = clm.tap(bore, offset)
        dc_blocked_a = (out_sig + (.995 * previous_dc_blocked_a)) - previous_out_sig
        dc_blocked_b = (tap_sig + (.995 * previous_dc_blocked_b)) - previous_tap_sig
        clm.outa(i, (out_scl * dc_blocked_a))          
        clm.outb(i, (out_scl * dc_blocked_b)) 
        previous_out_sig = out_sig
        previous_dc_blocked_a = dc_blocked_a
        previous_tap_sig = tap_sig
        previous_dc_blocked_b = dc_blocked_b       
                    
                    
if __name__ == '__main__':  
    with clm.Sound( play = True, statistics=True, channels=2 ):
        stereo_flute(0,3,220,.55, flow_envelope=[0,0,25,1,75,1,100,0], ran_amount=.03)
        stereo_flute(3.5,3,220,.55, flow_envelope=[0,0,25,1,75,1,100,0], offset_pos=.5)     
