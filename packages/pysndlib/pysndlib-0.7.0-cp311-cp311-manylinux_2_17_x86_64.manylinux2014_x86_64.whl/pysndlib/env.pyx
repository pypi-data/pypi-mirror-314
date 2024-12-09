#==================================================================================
# The code is an attempt at translation of Bill Schottstedaet's 'env.scm' 
# file available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================


from functools import singledispatch
import operator
import types
import math
import numpy as np
import numpy.typing as npt
cimport numpy as np
import cython
cimport cython
import pysndlib.clm as clm


@cython.ccall
def mapper(e1,e2,op):
    if isinstance(e1, list):
        return list(map(op, e1, e2))
    elif isinstance(e1, np.ndarray):
        return list(map(op, e1, e2))
    else:
        raise TypeError("expects list of ndarray")
    
@cython.ccall
def interleave(a,b):
    if isinstance(a, list):
        return [x for y in zip(a, b) for x in y]
    elif isinstance(a, np.ndarray):
        return np.vstack((a,b)).reshape((-1,),order='F')
    else:
        raise TypeError("expects list of ndarray")
    
    
@cython.ccall
def scale_and_offset(e, scl, offset: cython.double=0.0):
    if isinstance(e, list):
        return [x * scl + offset for x in e]
    elif isinstance(e, np.ndarray):
        return e * scl + offset

# TODO: --------------- window_envelopes ---------------- #    

# --------------- map_envelopes ---------------- #

@cython.ccall
def map_envelopes(func, e1, e2):
    """
    maps func over the breakpoints in env1 and env2 returning a new envelope
    map_envelopes(func, env1, env2) 
    """
    return mapper(e1,e2,func)

# --------------- multiply_envelopes ---------------- #
@cython.ccall
def multiply_envelopes(e1,e2):
    """
    multiplies break-points of env1 and env2 returning a new 
    envelope: multiply_envelopes([0,0,2,.5], [0,0,1,2,2,1]) -> [0,0,0.5,0.5,1.0,0.5]
    """
    return map_envelopes(operator.mul, e1, e2)
    
# --------------- add_envelopes ---------------- #
@cython.ccall
def add_envelopes(e1,e2):
    """
    adds break-points of env1 and env2 returning a new envelope"
    """

    return map_envelopes(operator.add, e1, e2)

# --------------- max-envelope ---------------- #
@cython.ccall
def max_envelope(e):
    """
    max_envelope(e) -> max y value in env
    """
    return max(e[1::2])
  
# --------------- min-envelope ---------------- #  
@cython.ccall
def min_envelope(e):
    """
    min_envelope(e) -> min y value in env
    """
    return min(e[1::2])
    
 
# --------------- integrate-envelope  ---------------- #    
# 
@cython.ccall
def integrate_envelope(e):
    """
    integrate_envelope(e) -> area under env
    """
    sum = 0.0
    for i in range(0,len(e)-2,2):
        sum += (e[i+1] + e[i+3]) * .5 * (e[i+2] - e[i])
    return sum

# --------------- envelope_last_x  ---------------- #  
@cython.ccall
def envelope_last_x(e):
    """
    envelope_last_x(env) -> max x axis break point position
    """
    return e[-2]


# ---------------  stretch_envelope   ---------------- #  
@cython.ccall
def stretch_envelope(fn, old_att, new_att, old_dec=None, new_dec=None):
    """
    takes 'env' and returns a new envelope based on it but with the attack and optionally decay portions stretched 
    or squeezed; 'old_att' is the original x axis attack end point, 'new_att' is where that 
    section should end in the new envelope.  Similarly for 'old_dec' and 'new_dec'.  This mimics 
    divseg in early versions of CLM and its antecedents in Sambox and Mus10 (linen).
    stretch_envelope([0,0,1,1], .1, .2) -> [0,0,0.2,0.1,1.0,1] 
    stretch_envelope([0,0,1,1,2,0], .1, .2, 1.5, 1.6) -> [0,0,0.2,0.1,1.1,1,1.6,0.5,2.0,0]
    """

    if not new_att and old_att:
        raise RuntimeError("new_att and old_att must be specified")
        
    else:
        if not new_att:
            return fn
        else:
            if old_dec and not new_dec:
                raise RuntimeError("old_dec and new_dec must be specified")
            
            else:
                x0 = fn[0]
                y0 = fn[1]
                new_x = x0
                last_x = fn[-2]
                new_fn = [x0,y0]
                scl = (new_att-x0) / max(.0001, old_att-x0)
                
                if old_dec and (old_dec == old_att):
                    old_dec =  .000001 * last_x
                
                for i in range(2,len(fn)-1, 2):
                    x1 = fn[i]
                    y1 = fn[i+1]
 
                    if x0 < old_att and x1 >= old_att:
                        y0 = y1 if x1==old_att else (y0 + ((y1 - y0) * ((old_att - x0) / (x1 - x0))))
                        
                        x0 = old_att

                        new_x = new_att
                        new_fn.extend((new_x,y0))   
                        scl = ((new_dec - new_att) / (old_dec - old_att)) if old_dec else ((last_x - new_att) / (last_x - old_att))
                        
                    if old_dec and x0 < old_dec and x1 >= old_dec:
                        y0 = y1 if x1 == old_dec else y0 + (y1 - y0) * ((old_dec - x0) / (x1 - x0))
                        x0 = old_dec
                        new_x = new_dec
                   
                        new_fn.extend((new_x,y0))
                        scl = (last_x - new_dec) / (last_x - old_dec)

                    if x0 != x1:
                        new_x = new_x + scl * (x1 - x0)
                        new_fn.extend((new_x,y1))
                        x0 = x1
                        y0 = y1
                        
                return new_fn
# --------------- scale_envelope  ---------------- # 
@cython.ccall
def scale_envelope(e, scaler: cython.double, offset: cython.double=0.0):
    """
    scales y axis values by 'scaler' and optionally adds 'offset'
    """
    ys = scale_and_offset(e[1::2], scaler, offset)
    xs = e[0::2]
    return interleave(xs,ys)
    
# --------------- reverse_envelope  ---------------- # 
@cython.ccall
def reverse_envelope(e):
    """
    reverses the breakpoints in env
    """
    xs = e[0::2]
    ys = e[:0:-2]
    return interleave(xs, ys)

# --------------- concatenate_envelopes  ---------------- # 


def concatenate_envelopes(*args, epsilon: cython.double =.01):
    """
    concatenates its arguments into a new envelope
    """
    # get list of last_x of each env
    # also verify each envelope
    res = None
    
    for e in args:
        clm.validate_envelope(e)
        
        if res is None:
            res = np.array(e)
        else:    
            tmp = np.array(e)
            tmp[0::2] += res[-2]
            if tmp[0] == res[-2]:
                tmp[0] += epsilon
            res = np.append(res, tmp)
            
    return list(res)  
    
# --------------- normalize_envelope  ---------------- # 
@cython.ccall
def normalize_envelope(e, new_max: cython.double=1.0):
    maxy = max_envelope(e)
    scl = new_max / maxy
    return scale_envelope(e, scl)
    
    
