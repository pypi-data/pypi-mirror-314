# cython: c_string_type=unicode
# cython: c_string_encoding=utf8

#==================================================================================
# The code is part of an attempt at translation of Bill Schottstedaet's clm 
# available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================


import ctypes
import functools
import math
import os
import random
import subprocess
import sys
import tempfile
import time
import types
import cython
from cython.cimports.cpython.mem import PyMem_Malloc, PyMem_Realloc, PyMem_Free
from cython cimport view
import numpy as np
cimport numpy as np
cimport pysndlib.cclm as cclm
cimport pysndlib.csndlib as csndlib


cimport pysndlib.clm 
cimport pysndlib.sndlib



# --------------- function types for ctypes ---------------- #
_inputcallback = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_void_p, ctypes.c_int)
_editcallback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
_analyzecallback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_void_p, ctypes.c_int))
_synthesizecallback = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_void_p)
_locsigdetourcallback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_longlong) 
_envfunction = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double) # for env_any    

#these may need to be set based on system type etc
DEFAULT_OUTPUT_SRATE = 44100
DEFAULT_OUTPUT_CHANS = 1



DEFAULT_FILE_PLAYER = None

if sys.platform.startswith("darwin"):
    DEFAULT_FILE_PLAYER = 'afplay'
    DEFAULT_FILE_NAME = 'test.wav'
    DEFAULT_OUTPUT_HEADER_TYPE = Header.RIFF
    DEFAULT_OUTPUT_SAMPLE_TYPE = Sample.LFLOAT 

if sys.platform.startswith("linux"):
    DEFAULT_FILE_PLAYER = 'aplay'
    DEFAULT_FILE_NAME = 'test.wav'
    DEFAULT_OUTPUT_HEADER_TYPE = Header.RIFF
    DEFAULT_OUTPUT_SAMPLE_TYPE = Sample.LFLOAT

# --------------- main clm prefs ---------------- #

default  = types.SimpleNamespace(
    file_name = DEFAULT_FILE_NAME,
    srate = DEFAULT_OUTPUT_SRATE,
    channels = DEFAULT_OUTPUT_CHANS,
    sample_type = DEFAULT_OUTPUT_SAMPLE_TYPE,
    header_type = DEFAULT_OUTPUT_HEADER_TYPE,
    player = DEFAULT_FILE_PLAYER,
    verbose = False,
    play = False,
    statistics = False,
    reverb = None,
    reverb_channels = 1,
    reverb_data = None,
    reverb_file_name = 'test.rev',
    table_size = 512,
    buffer_size = 65536,
    locsig_type = Interp.LINEAR,
    clipped = False,
    output = False,
    delete_reverb = False
)


if os.path.exists(os.path.expanduser('~/.pysndlib')):
    exec(open(os.path.expanduser('~/.pysndlib')).read())

# --------------- initializations ---------------- #

cclm.mus_initialize()
cclm.mus_set_rand_seed(int(time.time()))
csndlib.mus_sound_initialize()

cdef void clm_error_handler(int error_type, char* msg):
    message =  msg + ". "  +  csndlib.mus_error_type_to_string(error_type)
    raise SNDLibError(message) 
    
class SNDLibError(Exception):
    """
    this is general class to raise an print errors as defined in sndlib. it is to be used internally by the defined error handler registered with sndlib
    
    :meta private:
    """
    
    def ___init___(self, message):
        super().__init__(self.message)
        
        
        
cpdef check_ndim(arr: npt.NDArray[np.float64], dim=1):
    if arr.ndim != dim:
        raise TypeError(f'expecting {dim} dimemsions but received {arr.ndim}.')
        
cpdef check_range(arg: str, x, low=None, high=None):
    if x is None:
        return
    if low is not None:
        if x < low:
            raise ValueError(f'{arg} is out of range. {x} < {low}')
    if high is not None:
        if x > high:
            raise ValueError(f'{arg} is out of range. {x} > {high}')
    
        
cpdef compare_shapes(arr1: npt.NDArray[np.float64], arr2: npt.NDArray[np.float64]):
    if arr1.shape != arr2.shape:
        raise RuntimeError(f'ndarrays of unequal shape {arr1.shape } vs. {arr2.shape }.')

csndlib.mus_error_set_handler(<csndlib.mus_error_handler_t *>clm_error_handler)


cdef bint is_simple_filter(gen: mus_any):
    return cclm.mus_is_one_zero(gen._ptr) or cclm.mus_is_one_pole(gen._ptr) or cclm.mus_is_two_zero(gen._ptr) or cclm.mus_is_two_pole(gen._ptr)
    

# cdef bint is_poly(gen: mus_any):
#     return cclm.mus_is_polywave(gen._ptr) or cclm.mus_is_polyshape(gen._ptr) 
    
# todo add mus_set_xcoeff and mus_set_ycoeff

    


# --------------- extension types ---------------- #

cdef class mus_any:
    """
    a wrapper class for mus_any pointers in c
    
    instances of this class have the following properties, which may be 
    used if supported by the type of generator used to make the instance:
    
    
    """
    # member variables in pxd definition    

  
    def __cinit__(self):
        self.ptr_owner = False
        self._cache = []
        self._inputcallback = NULL
        self._editcallback = NULL
        self._analyzecallback = NULL
        self._synthesizecallback = NULL
        self._cache = []

        
    def __dealloc__(self):
        if self._ptr is not NULL and self.ptr_owner is True:
            cclm.mus_free(self._ptr)
            self._ptr = NULL
    

    def __init__(self):
        # prevent accidental instantiation from normal python code
        # since we cannot pass a struct pointer into a python constructor.
        raise TypeError("this class cannot be instantiated directly.")


    @staticmethod
    cdef mus_any from_ptr(cclm.mus_any *_ptr, bint owner=True, int length=0): #adding brkpoints as want to know number of brkpoints in envelope. kind of hacky 
        """
        factory function to create mus_any objects from
        given mus_any pointer.

        setting ``owner`` flag to ``True`` causes
        the extension type to ``free`` the structure pointed to by ``_ptr``
        when the wrapper object is deallocated.

        :meta private:
        """
        # fast call to __new__() that bypasses the __init__() constructor.
        cdef mus_any wrapper = mus_any.__new__(mus_any)
        wrapper._ptr = _ptr
        wrapper.ptr_owner = owner
        if cclm.mus_data_exists(wrapper._ptr):
            wrapper.set_up_data(length=length)
        if cclm.mus_xcoeffs_exists(wrapper._ptr):  
            # do not setup this for polywave or polyshape
            if not (cclm.mus_is_polywave(wrapper._ptr) or cclm.mus_is_polyshape(wrapper._ptr)):
                wrapper.set_up_xcoeffs()
        if cclm.mus_ycoeffs_exists(wrapper._ptr):  
            # do not setup this for polywave or polyshape
           if not (cclm.mus_is_polywave(wrapper._ptr) or cclm.mus_is_polyshape(wrapper._ptr)):
                wrapper.set_up_ycoeffs()
        if is_phase_vocoder(wrapper):
            wrapper.set_up_pv_data()
            
        return wrapper
       
    cpdef cache_append(self, obj):
        """
        :meta private:
        """
        self._cache.append(obj) 

    cpdef cache_extend(self, obj):
        """
        :meta private:
        """
        self._cache.extend(obj) 
        
    # this stuff with view.array is to work around an apparent bug when automatic string handling is turned on
    # https://github.com/cython/cython/issues/4521        
    cpdef set_up_data(self , cython.int length=0):
        """
        :meta private:
        """
        cdef view.array arr = None
        cdef cclm.mus_long_t size = cclm.mus_length(self._ptr)
        
        if cclm.mus_is_env(self._ptr):
            size = length
        
        
        if size > 0:
            self._data_ptr = cclm.mus_data(self._ptr)
            arr = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
            arr.data = <char*>self._data_ptr
            self._data = np.asarray(arr)       
        else:
            self._data = None
                 
    cpdef set_up_xcoeffs(self):
        """
        :meta private:
        """
        cdef cclm.mus_long_t size = 0
        cdef view.array arr = None
        #if simple filter the size will always be 3 and we do not want to
        #allocate a buffer
        # in other cases mus_order will be size and we do want to allocate
       
        if is_simple_filter(self):
            size = 3      
            self._xcoeffs_ptr = cclm.mus_xcoeffs(self._ptr)
            arr = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
            arr.data = <char*>self._xcoeffs_ptr
            self._xcoeffs = np.asarray(arr)
            #print('setup xcoeffs', size,is_simple_filter(self), self._xcoeffs, arr)
        else: 
            size = cclm.mus_order(self._ptr)   
            #print(size)
            self._xcoeffs_ptr = cclm.mus_xcoeffs(self._ptr)
            # setting allocate_buffer to false because array should be already allocated (?_)
            # this means tis could be simplified to just us esize if simple filter all the rest would besame
            arr = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
            arr.data = <char*>self._xcoeffs_ptr
            self._xcoeffs = np.asarray(arr)
        
    cpdef set_up_ycoeffs(self):
        """
        :meta private:
        """
        cdef cclm.mus_long_t size = 0
        cdef view.array arr = None
        #if simple filter the size will always be 3 and we do not want to
        #allocate a buffer
        # in other cases mus_order will be size and we do want to allocate
        
        if is_simple_filter(self):
            size = 3      
            self._ycoeffs_ptr = cclm.mus_ycoeffs(self._ptr)
            arr = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
            arr.data = <char*>self._ycoeffs_ptr
            self._ycoeffs = np.asarray(arr)
           # print('setup ycoeffs',  size,is_simple_filter(self), self._xcoeffs, arr)
        else: 
            size = cclm.mus_order(self._ptr)   
            #print(size)
            self._ycoeffs_ptr = cclm.mus_ycoeffs(self._ptr)
            arr = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
            arr.data = <char*>self._ycoeffs_ptr
            self._ycoeffs = np.asarray(arr)    
        
    
    
        
    cpdef set_up_pv_data(self):
        """
        :meta private:
        """
        cdef cclm.mus_long_t size = cclm.mus_length(self._ptr)
        
        self._pv_amp_increments_ptr = cclm.mus_phase_vocoder_amp_increments(self._ptr)
        cdef view.array pvai = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
        pvai.data = <char*>self._pv_amp_increments_ptr
        self._pv_amp_increments = np.asarray(pvai)
        self._pv_amp_increments.fill(0.0)
        
        self._pv_amps_ptr = cclm.mus_phase_vocoder_amps(self._ptr)
        cdef view.array pva = view.array(shape=(size // 2,),itemsize=sizeof(double), format='d', allocate_buffer=False)
        pva.data = <char*>self._pv_amps_ptr
        self._pv_amps = np.asarray(pva)    
        self._pv_amps.fill(0.0)
        
        self._pv_freqs_ptr = cclm.mus_phase_vocoder_freqs(self._ptr)
        cdef view.array pvf = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
        pvf.data = <char*>self._pv_freqs_ptr
        self._pv_freqs = np.asarray(pvf)    
        self._pv_freqs.fill(0.0)
        
        self._pv_phases_ptr = cclm.mus_phase_vocoder_phases(self._ptr)
        cdef view.array pvp = view.array(shape=(size // 2,),itemsize=sizeof(double), format='d', allocate_buffer=False)
        pvp.data = <char*>self._pv_phases_ptr
        self._pv_phases = np.asarray(pvp)
        self._pv_phases.fill(0.0)
        
        self._pv_phase_increments_ptr = cclm.mus_phase_vocoder_phase_increments(self._ptr)
        cdef view.array pvpi = view.array(shape=(size // 2,),itemsize=sizeof(double), format='d', allocate_buffer=False)
        pvpi.data = <char*>self._pv_phase_increments_ptr
        self._pv_phase_increments = np.asarray(pvpi)  
        self._pv_phase_increments.fill(0.0)
        
    def __call__(self, arg1=0.0, arg2=0.0):
        return cclm.mus_run(self._ptr, arg1,arg2)
        
    def __str__(self):
        return f'{mus_any} {cclm.mus_describe(self._ptr)}'
     
    cpdef mus_reset(self):
        cclm.mus_reset(self._ptr)
        
    cpdef next(self, cython.double arg1=0.0, cython.double arg2=0.0):
        return cclm.mus_run(self._ptr, arg1,arg2)
        
        
    @property
    def mus_frequency(self):
        """
        frequency (hz), float
        """
        return cclm.mus_frequency(self._ptr)
    
    @mus_frequency.setter
    def mus_frequency(self, v):
        cclm.mus_set_frequency(self._ptr, v)
    
    @property
    def mus_phase(self):
        """
        phase (radians), float
        """
        return cclm.mus_phase(self._ptr)
    
    @mus_phase.setter
    def mus_phase(self, v):
        cclm.mus_set_phase(self._ptr, v)
        
    @property
    def mus_length(self):
        """
        data length, int
        """
        return cclm.mus_length(self._ptr)
    
    @mus_length.setter
    def mus_length(self, v):
        cclm.mus_set_length(self._ptr, v)  
        
    @property
    def mus_increment(self):
        """
        various increments, int
        """
        return cclm.mus_increment(self._ptr)
    
    @mus_increment.setter
    def mus_increment(self, v):
        cclm.mus_set_increment(self._ptr, v)  
        
    @property
    def mus_location(self):
        """
        sample location for reads/write, int
        """
        return cclm.mus_location(self._ptr)
    
    @mus_location.setter
    def mus_location(self, v):
        cclm.mus_set_location(self._ptr, v)  
    
    @property
    def mus_offset(self):
        return cclm.mus_offset(self._ptr)
    
    @mus_offset.setter
    def mus_offset(self, v):
        """
        envelope offset, int
        """
        cclm.mus_set_offset(self._ptr, v)  
        
    @property
    def mus_channels(self):
        """
        channels open, int
        """
        return cclm.mus_channels(self._ptr)
    
        
    @property
    def mus_interp_type(self):
        """
        interpolation type (inter.linear, etc), interp
        not setable
        """
        return cclm.mus_interp_type(self._ptr)
    
    @property
    def mus_width(self):
        """
        width of interpolation tables, etc, int
        """
        return cclm.mus_width(self._ptr)
    
    @mus_width.setter
    def mus_width(self, v):
        cclm.mus_set_width(self._ptr, v)  
        
    @property
    def mus_order(self):
        """
        filter order, int
        """
        return cclm.mus_order(self._ptr)

    @property
    def mus_scaler(self):
        """
        scaler, normally on an amplitude, float
        """
        return cclm.mus_scaler(self._ptr)
    
    @mus_scaler.setter
    def mus_scaler(self, v):
        cclm.mus_set_scaler(self._ptr, v)  
        
    @property
    def mus_feedback(self):
        """
        feedback coefficient, float
        """
        return cclm.mus_feedback(self._ptr)
    
    @mus_feedback.setter
    def mus_feedback(self, v):
        cclm.mus_set_feedback(self._ptr, v)  
        
    @property
    def mus_feedforward(self):
        """
        feedforward coefficient, float
        """
        return cclm.mus_feedforward(self._ptr)
    
    @mus_feedforward.setter
    def mus_feedforward(self, v):
        cclm.mus_set_feedforward(self._ptr, v) 

    @property
    def mus_hop(self):
        """
        hop size for block processing, int
        """
        return cclm.mus_hop(self._ptr)
    
    @mus_hop.setter
    def mus_hop(self, v):
        cclm.mus_set_hop(self._ptr, v) 
        
    @property
    def mus_ramp(self):
        """
        granulate grain envelope ramp setting, int
        """
        return cclm.mus_ramp(self._ptr)
    
    @mus_ramp.setter
    def mus_ramp(self, v):
        cclm.mus_set_ramp(self._ptr, v) 
    
    @property
    def mus_channel(self):
        """
        channel being read/written, int
        """
        return cclm.mus_channel(self._ptr)

    @property
    def mus_data(self):
        """
        array of data, np.ndarray
        """
        if not cclm.mus_data_exists(self._ptr):   #could do this on all properties but seems best with array 
            raise TypeError(f'mus_data can not be called on {cclm.mus_name(self._ptr)}')
        return self._data 

    @mus_data.setter
    def mus_data(self, data: npt.NDArray[np.float64]):
        if not cclm.mus_data_exists(self._ptr):   #could do this on all properties but seems best with array 
            raise TypeError(f'mus_data can not be called on {cclm.mus_name(self._ptr)}')
                
        np.copyto(self._data , data)

    @property
    def mus_xcoeffs(self):
        """
        x (input) coefficient, np.ndarray
        not setable
        """
        if not cclm.mus_xcoeffs_exists(self._ptr):   #could do this on all properties but seems best with array 
            raise TypeError(f'mus_xcoeffs can not be called on {cclm.mus_name(self._ptr)}')
        return self._xcoeffs
    
    @property
    def mus_ycoeffs(self):
        """
        y (output, feedback) coefficient, np.ndarray
        not setable
        """
        if not cclm.mus_ycoeffs_exists(self._ptr):   #could do this on all properties but seems best with array 
            raise TypeError(f'mus_ycoeffs can not be called on {cclm.mus_name(self._ptr)}')
        return self._ycoeffs
    
    @property
    def mus_file_name(self):
        """
        file being read/written
        """
        return cclm.mus_file_name(self._ptr)
   
cdef class mus_any_array:
    """
    a wrapper class arrays of mus_any objects
    :meta private:
    """
    cdef  cclm.mus_any_ptr_ptr data
    item_count: cython.size_t
    def __cinit__(self, number: cython.size_t):
        # allocate some memory (uninitialised, may contain arbitrary data)
        if number > 0:
            self.data = cython.cast(cclm.mus_any_ptr_ptr, PyMem_Malloc(
                number * cython.sizeof(cclm.mus_any_ptr)))
            if not self.data:
                raise MemoryError()
        self.item_count = number


    def __dealloc__(self):
        PyMem_Free(self.data)  # no-op if self.data is null
    
    def __len__(self):
        return self.item_count
        
    def __str__(self):
        return f"count {self.item_count}"

    @staticmethod
    cdef mus_any_array from_pylist(lst: list):
        """
        factory function to create a wrapper around mus_float_t (double) and fill it with values from the list
        """
        cdef int i
        
        cdef mus_any_array wrapper = mus_any_array(len(lst))
        for i in range(len(lst)):
            wrapper.data[i] = (<mus_any>lst[i])._ptr
        return wrapper
        



# --------------- callbacks ---------------- #
        
cdef double input_callback_func(void* arg, int direction):
    cdef cclm.mus_any_ptr gen = <cclm.mus_any_ptr>arg
    return cclm.mus_apply(gen, direction, 0.)        
    

cdef void locsig_detour_callback_func(cclm.mus_any *ptr, cclm.mus_long_t val):
    cdef int channels = cclm.mus_locsig_channels(ptr)
    cdef int reverb_channels = cclm.mus_locsig_reverb_channels(ptr)
    cdef cclm.mus_float_t* outf = cclm.mus_locsig_outf(ptr)
    cdef cclm.mus_float_t* revf = cclm.mus_locsig_revf(ptr)
    for i in range(channels):
         default.output[i][val] += outf[i]
    for i in range(reverb_channels):
         default.reverb[i][val] += revf[i]
         
         
# --------------- file2ndarray, ndarray2file ---------------- #                 
cpdef file2ndarray(str filename, channel=None, beg=None, size=None):
    """
    return an ndarray with samples from file and the sample rate of the data
    
    :param filename: filename
    :param channel: if None, will read all channels, otherwise just channel specified 
    :param beg: beginning positions to read in samples
    :param size: size in samples to read
    :return: tuple of np.ndarray and sample rate
    :rtype: tuple
    
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f'file2ndarray: {filename} does not exist.')
    
    size = size or get_length(filename)
    chans = get_channels(filename)
    sr = get_srate(filename)
    bg = beg or 0
    out = np.zeros((1 if (channel != None) else chans, size), dtype=np.double)

    cdef double [: , :] arr_view = out

    if channel is None:
        for i in range(chans):  
            csndlib.mus_file_to_array(filename, i, bg, size, &arr_view[i][0])
    else:
        csndlib.mus_file_to_array(filename,channel, bg, size, &arr_view[0][0])
    return out, sr
    
cpdef ndarray2file(str filename, np.ndarray arr, size=None, sr=None, sample_type=None, header_type=None, comment=None ):
    """
    write an ndarray of samples to file
    
    :param filename: name of file
    :param arr: np.ndarray of samples
    :param size: number of samples to write. if None write all
    :param sr: sample rate of file to write
    :param sample_type: type of sample type to use. defaults to clm.sample_type
    :param header_type: header of sample type to use. defaults to clm.header_type
    :return: length in samples of file
    :rtype: int
    
    """
    #sample_type: Optional[sndlib.sample]=CLM.sample_type, header_type: Optional[sndlib.header]=CLM.header_type
    sr = sr or default.srate
        
    sample_type = sample_type or default.sample_type
    header_type = header_type or default.header_type

    if arr.ndim == 1:
        print('ndim', arr.ndim)
        arr = np.copy(arr)
        size = size or np.shape(arr)[0]
        arr.resize(size)
        arr = np.reshape(arr,(1,size))
        
    else:
        
        size = size or np.shape(arr)[1]
        
    chans = np.shape(arr)[0]

    fd = csndlib.mus_sound_open_output(filename, int(sr), chans, sample_type, header_type, NULL)
    cdef cclm.mus_float_t **obuf = <cclm.mus_float_t**>PyMem_Malloc(chans * sizeof(cclm.mus_float_t*))

    if not obuf:
        raise MemoryError()
    
    cdef double [:] arr_view = arr[0]
    
    try:
        for i in range(chans):
            arr_view = arr[i]
            obuf[i] = &arr_view[0]
    
    finally:
        err = csndlib.mus_file_write(fd, 0, size, chans, obuf)
        csndlib.mus_sound_close_output(fd, size * csndlib.mus_bytes_per_sample(sample_type)*chans)
        PyMem_Free(obuf)
        
    return size

# --------------- with sound context manager ---------------- #      
class Sound(object):
    """
    context manager which handles creating output and other options
    
    :param output: Can be a filename string or np.ndarray
    :param channels: number of channels \in main output
    :param srate:  output sampling rate 
    :param sample_type: output sample data type
    :param header_type: output header type 
    :param comment: any comment to store \in the header
    :param verbose: if True, print out some info (doesn't do anything now)
    :param reverb: reverb instrument
    :param reverb_data: arguments passed to the reverb (dictionary)
    :param reverb_channels: chans \in the reverb intermediate file
    :param revfile: reverb intermediate output file name
    :param continue_old_file: if True, continue a previous computation
    :param statistics: if True, print info at end of with-sound (compile time, maxamps)
    :param scaled_to: if a number, scale the output to peak at that amp
    :param scaled_by: is a number, scale output by that amp
    :param play: if True, play the sound automatically
    :param finalize: a function to call on exit from the context. should be a function that takes one argument, the name of the sound file or the ndarray 
        used as output
    """           
    
    def __init__(self, output=None, 
                        channels=None, 
                        srate=None, 
                        sample_type = None,
                        header_type = None,
                        comment = False,
                        verbose = False,
                        reverb = None,
                        revfile = None,
                        reverb_data = None,
                        reverb_channels = None,
                        continue_old_file = False,
                        statistics = None,
                        scaled_to = False,
                        scaled_by = False,
                        play = None,
                        clipped = None,
                        finalize = None):                  
        self.output = output if output is not None else default.file_name
        self.channels = channels if channels is not None else default.channels
        self.srate = srate if srate is not None else default.srate
        self.sample_type = sample_type if sample_type is not None else default.sample_type
        self.header_type = header_type if header_type is not None else  default.header_type
        self.comment = comment
        self.verbose = verbose if verbose is not None else default.verbose
        self.reverb = reverb
        self.revfile = revfile if revfile is not None else default.reverb_file_name
        self.reverb_data = reverb_data if reverb_data is not None else default.reverb_data
        self.reverb_channels = reverb_channels if reverb_channels is not None else default.reverb_channels
        self.continue_old_file = continue_old_file
        self.statistics = statistics if statistics is not None else default.statistics
        self.scaled_to = scaled_to
        self.scaled_by = scaled_by
        self.play = play if play is not None else default.play
        self.clipped = clipped if clipped is not None else default.clipped
        self.output_to_file = isinstance(self.output, str)
        self.reverb_to_file = self.reverb is not None and isinstance(self.output, str)
        self.old_srate = get_srate()
        self.finalize = finalize
        
    def __enter__(self):
        if not self.clipped:
            if (self.scaled_by or self.scaled_to) and (self.sample_type in [Sample.BFLOAT, Sample.LFLOAT, Sample.BDOUBLE, Sample.LDOUBLE]):
                csndlib.mus_set_clipping(False)
            else:
                csndlib.mus_set_clipping(default.clipped)
        else:
            csndlib.mus_set_clipping(self.clipped)
        
        set_srate(self.srate)
        default.srate = self.srate

        # in original why use reverb-1?
        if  self.statistics :
            self.tic = time.perf_counter()
        

        
        if self.output_to_file :
            if self.continue_old_file:
                default.output = continue_sample2file(self.filename)
                set_srate(csndlib.mus_sound_srate(self.filename)) # maybe print warning or at least note 
            else:
                default.output = make_sample2file(self.output,self.channels, sample_type=self.sample_type , header_type=self.header_type)
        elif is_list_or_ndarray(self.output):
            default.output = self.output
        else:
            raise TypeError(f"writing to  {type(self.output)} not supported")
            
        if self.reverb_to_file:
            if self.continue_old_file:
                default.reverb = continue_sample2file(self.revfile)
            else:
                default.reverb = make_sample2file(self.revfile,self.reverb_channels, sample_type=self.sample_type , header_type=self.header_type)
        
        if self.reverb and not self.reverb_to_file and is_list_or_ndarray(self.output):
            default.reverb = np.zeros((self.reverb_channels, np.shape(default.output)[1]), dtype=default.output.dtype)
    
        return self
        
    def __exit__(self, *args):
        cdef cclm.mus_float_t [:] vals_view = None
        cdef cclm.mus_long_t [:] times_view = None
        maxamp_result = [0.0] * self.channels
        if self.reverb: 
            
            if self.reverb_to_file:
                mus_close(default.reverb)
  
                default.reverb = make_file2sample(self.revfile)
                
                if isinstance(self.reverb, functools.partial):
                    self.reverb() ## reverb_data will be ignored in this case
                else:
                    if self.reverb_data:
                        self.reverb(**self.reverb_data)
                    else:
                        self.reverb()()
                    
                mus_close(default.reverb)

            if is_list_or_ndarray(default.reverb):
                if isinstance(self.reverb, functools.partial):
                    self.reverb() ## reverb_data will be ignored in this case
                else:
                    if self.reverb_data:
                        self.reverb()(**self.reverb_data)
                    else:
                        self.reverb()()          

        if self.output_to_file:
            mus_close(default.output)
            
    
        if  self.statistics :
            toc = time.perf_counter()
            
            statstr = ''
            if isinstance(self.output, str):
                statstr = f"{self.output}: "
            if self.output_to_file:
                    chans = get_channels(self.output)
                    vals = np.zeros(chans, dtype=np.double)
                    times = np.zeros(chans, dtype=np.int64)
                    vals_view = vals
                    times_view = times
                    maxamp = csndlib.mus_sound_maxamps(self.output, chans, &vals_view[0], &times_view[0])
                    maxamp_result = maxamp
                    statstr += f" channels: {get_channels(self.output)},"
                    statstr += f" length: {get_length(self.output)} samples,"
                    statstr += f" duration: {get_length(self.output) / get_srate()} seconds,"
                    statstr += f" maxamp: {vals} {times}, "

            else:
                chans = get_channels(self.output)
                vals = np.zeros(chans, dtype=np.double)
                times = np.zeros(chans, dtype=np.int64)
                for i in range(chans):
                    mabs = np.abs(self.output[i])
                    vals[i] = np.amax(mabs)
                    times[i] = np.argmax(mabs)
                statstr += f" channels: {get_channels(self.output)},"
                statstr += f" length: {get_length(self.output)} samples,"
                statstr += f" duration: {get_length(self.output) / get_srate()} seconds,"
                statstr += f" maxamp: {vals} {times}, "
                maxamp_result = vals
                
              
            if self.scaled_by or self.scaled_to:
                statstr += "(before scaling) "
            
            statstr += f"compute time: {toc - self.tic:0.8f} seconds, "
            statstr += f"compute ratio: {(toc - self.tic) / (get_length(self.output) / get_srate())}, " 
            
            
            if self.reverb_to_file:
                    chans = get_channels(self.revfile)
                    vals = np.zeros(chans, dtype=np.double)
                    times = np.zeros(chans, dtype=np.int_)
                    vals_view = vals
                    times_view = times
                    maxamp = csndlib.mus_sound_maxamps(self.revfile, chans, &vals_view[0], &times_view[0])
                    statstr += f"revmax: {vals} {times}"
            elif self.reverb and not self.reverb_to_file and is_list_or_ndarray(self.output):
                chans = get_channels(default.reverb)
                
                vals = np.zeros(chans, dtype=np.double)
                times = np.zeros(chans, dtype=np.int_)
                for i in range(chans):
                    mabs = np.abs(default.reverb[i])
                    vals[i] = np.amax(mabs)
                    times[i] = np.argmax(mabs)
                statstr += f"revmax: {vals} {times}"
            
            print(statstr)
         
        if self.scaled_to:
            if self.output_to_file:
                arr, _ = file2ndarray(self.output)
                arr *= (self.scaled_to / np.max(np.abs(arr)))
                # handle error
                ndarray2file(self.output, arr)
            else:
                self.output *= (self.scaled_to / np.max(np.abs(self.output)))
        elif self.scaled_by:
            if self.output_to_file:
                arr, _ = file2ndarray(self.output)
                arr *= self.scaled_by
                ndarray2file(self.output, arr)
            else:
                self.output *= self.scaled_by
       
        if self.play and self.output_to_file:
            if self.play:
                subprocess.run([default.player,self.output])
            else:
                raise RuntimeError("no player specified")
        # need some safety if errors
        
        set_srate(self.old_srate)
        default.srate = self.old_srate
        
        if self.finalize:
            self.finalize(self.output)
         

cpdef is_list_or_ndarray(x):
    return isinstance(x, list) or isinstance(x, np.ndarray)
    
cpdef is_power_of_2(x):
    return (((x) - 1) & (x)) == 0

cpdef next_power_of_2(x):
    return 2**int(1 + (float(math.log(x + 1)) / math.log(2.0)))
    
    
# TODO: could be simplified now
cpdef np.ndarray to_partials(harms):
    if isinstance(harms, list):
        p = harms[::2]
        maxpartial = max(p)
        partials = np.zeros(int(maxpartial)+1, dtype=np.double)
        check_ndim(partials)
        for i in range(0, len(harms),2):
            partials[int(harms[i])] = harms[i+1]
        #print('to_partials', partials)
        return partials
    elif isinstance(harms[0], np.double): 
        p = harms[::2]
        maxpartial = np.max(p)
        partials = np.zeros(int(maxpartial)+1, dtype=np.double)
        check_ndim(partials)
        for i in range(0, len(harms),2):
            partials[int(harms[i])] = harms[i+1]
        #print('to_partials', partials)
        return partials
    else: 
        raise TypeError(f'{type(harms)} cannot be converted to a mus_float_array')
        
    
# --------------- generic functions ---------------- #


cpdef int mus_close(mus_any obj):
    return cclm.mus_close_file(obj._ptr)
    
cpdef bint mus_is_output(mus_any obj):
    """
    returns True if gen is a type of output
    """
    return cclm.mus_is_output(obj._ptr)
    
cpdef bint mus_is_input(mus_any obj):
    """
    returns True if gen is a type of output
    """
    return cclm.mus_is_input(obj._ptr)

cpdef mus_reset(mus_any obj):
    """
    set gen to default starting state
    """
    cclm.mus_reset(obj._ptr)
    

# prepending clm to functions to avoid name clashes
    
# --------------- length ---------------- #

cpdef cython.long get_length(obj):
    """Returns length in samples of a sound file, list, ndarray, or generator"""
    #assume file
    if isinstance(obj, str):
        return csndlib.mus_sound_framples(obj)
    #sndlib gen    
    elif  isinstance(obj, mus_any):
        return obj.mus_length
    elif isinstance(obj, list):
        if isinstance(obj[0], list):
            return len(obj[0])
        else:
            return len(obj)
    elif isinstance(obj, np.ndarray):
        if obj.ndim == 1:
            return np.shape(obj)[0]
        elif obj.ndim == 2:
            return np.shape(obj)[1]
        else:
            raise RuntimeError(f'ndarray must have 1 or 2 dimensions not {obj.ndim}.')
    else:
        raise RuntimeError(f'object {obj} has no meaningful length. ')




# --------------- channels ---------------- #

cpdef cython.long get_channels(obj):
    """Returns number of channels of a sound file, list, ndarray"""
    if isinstance(obj, str):
        return csndlib.mus_sound_chans(obj)
    elif isinstance(obj, mus_any):
        return obj.mus_channels
    elif isinstance(obj, list):
        return len(obj)
    elif isinstance(obj, np.ndarray):
        if obj.ndim == 1:
            return 1
        elif obj.ndim == 2:
            return np.shape(obj)[0]
        else:
            raise RuntimeError(f'ndarray must have 1 or 2 dimensions not {obj.ndim}. ')      
    else:
        raise RuntimeError(f'object {obj} has no meaningful channels. ')


        
# --------------- srate ---------------- #

    
cpdef cython.double get_srate(obj=None):
    """Return current sample rate"""
    if obj is None:
            return cclm.mus_srate()
    else:
        return csndlib.mus_sound_srate(obj)
  
# --------------- framples ---------------- #

cpdef cython.long get_framples(obj):
    """Returns length in frames of a sound file, list, ndarray, or generator"""
    if isinstance(obj, str):
        return csndlib.mus_sound_framples(obj)
    elif isinstance(obj, mus_any):
        return obj.mus_length
    elif isinstance(obj, list):
        if isinstance(obj[0], list):
            return len(obj[0])
        else:
            return len(obj)
    elif isinstance(obj, np.ndarray):
        if obj.ndim == 1:
            return np.shape(obj)[0]
        elif obj.ndim == 2:
            return np.shape(obj)[1]
        else:
            raise RuntimeError(f'ndarray must have 1 or 2 dimensions not {obj.ndim}. ')
    else:
        raise RuntimeError(f'object {obj} has no meaningful framples. ')
        
# --------------- clm random ---------------- # 
 
cpdef cython.double random(cython.double x=1.0):
    """Returns random number +- x"""
    return cclm.mus_random(x)
# --------------- just some extra utils ---------------- #    

def validate_envelope(e):
    # is env even number length
    if len(e) < 2:
        raise RuntimeError("a valid envelope needs at least 2 elements") 
    if len(e) % 2 != 0:
        raise RuntimeError("a valid envelope needs even number of elements. This has {len(e)}")
    if isinstance(e, list):
        if all([isinstance(i, int | float) for i in e]):
            raise RuntimeError("a valid envelope can only contain numbers.")
    if not all(i < j for i, j in zip(e[: : 2], e[2: : 2])):
        raise RuntimeError("x values of envelope must be increasing")
        
        
cpdef bint is_zero(cython.double x):
    return x == 0
    
cpdef bint is_number(n):
    return type(n) == int or type(n) == float
    
cpdef bint is_odd(n):
    return n % 2 == 0

cpdef bint is_even(n):
    return n % 2 != 0

# # --------------- clm utility functions ---------------- #
# 
cpdef cython.double radians2hz(cython.double radians ):
    """
    convert radians per sample to frequency:  `hz = rads * srate / (2 * pi)`.
    
    :param radians: frequency \in radians
    :return: frequency \in hertz
    :rtype: float
    """
    return cclm.mus_radians_to_hz(radians)

cpdef cython.double hz2radians(cython.double hz):
    """
    convert frequency in hz to radians per sample:  `hz * 2 * pi / srate`.
    
    :param hz: frequency \in hertz
    :return: frequency \in radians
    :rtype: float
    """
    return cclm.mus_hz_to_radians(hz)

cpdef cython.double degrees2radians(cython.double degrees):
    """
    convert degrees to radians:  `degrees * 2 * pi / 360`.
    
    :param degrees: angle in degrees
    :return: angle in radians
    :rtype: float
    
    """
    return cclm.mus_degrees_to_radians(degrees)
    
cpdef cython.double radians2degrees(cython.double radians):
    """
    convert radians to degrees: `rads * 360 / (2 * pi)`.
    
    :param radians: angle in radians
    :return: degree
    :rtype: float
    
    """
    
    return cclm.mus_radians_to_degrees(radians)
    
cpdef cython.double db2linear(cython.double x):
    """
    convert decibel value db to linear value: `pow(10, db / 20)`.

    :param x: decibel
    :return: linear amplitude
    :rtype: float
    
    """
    
    return cclm.mus_db_to_linear(x)
    
cpdef cython.double linear2db(cython.double x):
    """
    convert linear value to decibels 20 * log10(lin).

    :param x: linear amplitude
    :return: decibel
    :rtype: float
    
    """
    
    return cclm.mus_linear_to_db(x)
    
cpdef cython.double odd_multiple(cython.double x, cython.double y):
    """
    return y times the nearest odd integer to x.
    
    :param x:
    :param y:
    :return: nearest odd integer as a float
    :rtype: float
    
    """
    
    return cclm.mus_odd_multiple(x,y)
    
cpdef cython.double even_multiple(cython.double x, cython.double y):
    """
    return y times the nearest even integer to x.
    
    :param x:
    :param y:
    :return: nearest even integer as a float
    :rtype: float
    """
    
    return cclm.mus_even_multiple(x,y)
    
cpdef cython.double odd_weight(cython.double x):
    """
    return a number between 0.0 (x is even) and 1.0 (x is odd).
    
    :param x:
    :return weight:
    :rtype: float
    
    """
    
    return cclm.mus_odd_weight(x)
    
cpdef cython.double even_weight(cython.double x):
    """
    return a number between 0.0 (x is odd) and 1.0 (x is even).
    
    :param x:
    :return weight:
    :rtype: float
    """
    
    return cclm.mus_even_weight(x)
    
# cpdef cython.double get_srate():
#     """
#     return current sample rate.
#     
#     :return samplerate:
#     :rtype: float
#     
#     """
#     return cclm.mus_srate()
    
cpdef cython.double set_srate(cython.double r):
    """
    set current sample rate.
    """
    return cclm.mus_set_srate(r)
    
cpdef cython.long seconds2samples(cython.double secs):
    """
    use mus_srate to convert seconds to samples.
    
    :param secs: time in seconds
    :return: time in samples
    :rtype: int
    """
    return cclm.mus_seconds_to_samples(secs)

cpdef cython.double samples2seconds(cython.long samples):
    """
    use mus_srate to convert samples to seconds.
    
    :param samples: number of samples
    :return: time in seconds
    :rtype: float
    
    """
    return cclm.mus_samples_to_seconds(samples)
    
cpdef cython.double ring_modulate(cython.double s1, cython.double s2):
    """
    return s1 * s2 (sample by sample multiply).
    
    :param s1: input 1
    :param s2: input 2
    :return: result
    :rtype: float
    
    """
    
    return cclm.mus_ring_modulate(s1, s2)
    
cpdef cython.double amplitude_modulate(cython.double s1, cython.double s2, cython.double s3):
    """
    carrier in1 in2): in1 * (carrier + in2).
        
    :param s1: input 1
    :param s2: input 2
    :param s3: input 3
    :return: result
    :rtype: float
    
    """
    return cclm.mus_amplitude_modulate(s1, s2, s3)
    
cpdef cython.double contrast_enhancement(cython.double insig, cython.double fm_index= 1.0 ):
    """
    returns insig (index 1.0)): sin(sig * pi / 2 + fm_index * sin(sig * 2 * pi))
    contrast_enhancement passes its input to sin as a kind of phase modulation.
    
    :param insig: input
    :param fm_index: 
    :return: result
    :rtype: float
    
    """
    return cclm.mus_contrast_enhancement(insig, fm_index)
    

cpdef cython.double dot_product(np.ndarray data1, np.ndarray  data2):
    """
    returns v1 v2 (size)): sum of v1[i] * v2[i] (also named scalar product).
    
    :param data1: input 1
    :param data2: input 2
    :return: result
    :rtype: float
    
    """
    check_ndim(data1)
    check_ndim(data2)
    compare_shapes(data1, data2)
    
    cdef double [:] data1_view = data1
    cdef double [:] data2_view = data2
    return cclm.mus_dot_product(&data1_view[0], &data2_view[0], len(data1))

# changed 11-26-23 to not modify inplace
cpdef cython.double polynomial(np.ndarray coeffs, cython.double x ):
    """
    evaluate a polynomial at x.  coeffs are in order of degree, so coeff[0] is the constant term.
    
    :param coeffs: coefficients where coeffs[0] is the constant term, and so on.
    :param x: input
    :return: result
    :rtype: float
    
    """
    check_ndim(coeffs)
    cdef double [:] coeffs_view = coeffs
    return cclm.mus_polynomial(&coeffs_view[0], x, len(coeffs))
    
cpdef cython.double array_interp(np.ndarray  fn, cython.double  x):
    """
    taking into account wrap-around (size is size of data), with linear interpolation if phase is not an integer.
    
    :param fn: input array
    :param x: interp point
    :return: result
    :rtype: float
    
    """
    check_ndim(fn)
    cdef double [:] fn_view = fn
    return cclm.mus_array_interp(&fn_view[0], x, len(fn))

cpdef cython.double bessi0(cython.double x):
    """
    bessel function of zeroth order
    """
    return cclm.mus_bessi0(x)
    
cpdef cython.double mus_interpolate(Interp interp_type, cython.double x, np.ndarray table, cython.double y1 =0.):
    """
    interpolate in data ('table' is a ndarray) using interpolation 'type', such as Interp.linear.
    
    :param interp_type: type of interpolation
    :param x: interpolation value
    :param table: table to interpolate in
    :return: result
    :rtype: float
    
    """
    check_ndim(table)
    cdef double [:] table_view = table
    return cclm.mus_interpolate(<cclm.mus_interp_t>interp_type, x, &table_view[0], len(table), y1)
   
cpdef np.ndarray make_fft_window(Window window_type, cython.int size, cython.double beta=0.0 , cython.double alpha=0.0):
    """
    fft data window (a ndarray). type is one of the sndlib fft window identifiers such as
    window.kaiser, beta is the window family parameter, if any.
    
    :param window_type: type of window
    :param size: window size
    :param beta: beta parameter if needed
    :param alpha: alpha parameter if needed
    :return: window
    :rtype: np.ndarray
    
    """
    win = np.zeros(size, dtype=np.double)
    check_ndim(win)
    
    cdef double [:] win_view = win
    cclm.mus_make_fft_window_with_window(<cclm.mus_fft_window_t>window_type, size, beta, alpha, &win_view[0])
    return win
    
cpdef np.ndarray mus_fft(np.ndarray rdat, np.ndarray  idat, cython.int fft_size , cython.int sign):
    """
    in-place operation. return the fft of rl and im which contain the real and imaginary parts of the data; len should be a
    power of 2, dir = 1 for fft, -1 for inverse-fft.
    
    :param rdat: real data
    :param imaginary: imaginary data
    :param fft_size: must be power of two
    :param sign: 1 for fft, -1 for inverse-fft
    :return: result written into rdat
    :rtype: np.ndarray
    
    """
    check_ndim(rdat)
    check_ndim(idat)
    compare_shapes(rdat, idat)
    
    cdef double [:] rdat_view = rdat
    cdef double [:] idat_view = idat
    res = cclm.mus_fft(&rdat_view[0], &idat_view[0], fft_size, sign)
    return rdat
    
    
cpdef tuple fft(np.ndarray rdat, np.ndarray idat,  cython.int fft_size, cython.int sign ):
    """
    return the fft of rl and im which contain the real and imaginary parts of the data; len should be a
    power of 2, dir = 1 for fft, -1 for inverse-fft.
    
    :param rdat: real data
    :param imaginary: imaginary data
    :param fft_size: must be power of two
    :param sign: 1 for fft, -1 for inverse-fft
    :return: tuple of copy of rdat and idat
    :rtype: tuple
    
    """
    check_ndim(rdat)
    check_ndim(idat)
    compare_shapes(rdat, idat)
    
    rdat_cpy = np.copy(rdat)
    idat_cpy = np.copy(idat)
    
    cdef double [:] rdat_view = rdat_cpy
    cdef double [:] idat_view = idat_cpy
    res = cclm.mus_fft(&rdat_view[0], &idat_view[0], fft_size, sign)
    return rdat_cpy, idat_cpy



cpdef np.ndarray mus_rectangular2polar(np.ndarray  rdat, np.ndarray  idat):
    """
    in-place operation. convert real/imaginary data in s rl and im from rectangular form (fft output) to polar form (a
    spectrum).
    
    :param rdat: real data
    :param imaginary:  imaginary data
    :return: magnitude written into rdat, idat contains phases
    :rtype: np.ndarray
    
    """
    size = len(rdat)
    
    check_ndim(rdat)
    check_ndim(idat)
    compare_shapes(rdat, idat)
    
    cdef double [:] rdat_view = rdat
    cdef double [:] idat_view = idat
    res = cclm.mus_rectangular_to_polar(&rdat_view[0], &idat_view[0], size)
    return rdat
    
cpdef tuple rectangular2polar(np.ndarray  rdat, np.ndarray  idat):
    """
    convert real/imaginary data in rdat and idat from rectangular form (fft output) to polar form (a
    spectrum).
    
    :param rdat: real data
    :param imaginary:  imaginary data
    :return::return: tuple of magnitude and phases
    :rtype: tuple
    
    """
    size = len(rdat)
    
    check_ndim(rdat)
    check_ndim(idat)
    compare_shapes(rdat, idat)
    
    rdat_cpy = np.copy(rdat)
    idat_cpy = np.copy(idat)
    
    cdef double [:] rdat_view = rdat_cpy
    cdef double [:] idat_view = idat_cpy
    res = cclm.mus_rectangular_to_polar(&rdat_view[0], &idat_view[0], size)
    return rdat_cpy, idat_cpy

cpdef np.ndarray mus_rectangular2magnitudes(np.ndarray rdat, np.ndarray idat):
    """
    in-place operation. convert real/imaginary data in rl and im from rectangular form (fft output) to polar form, but
    ignore the phases.
    
    :param rdat: real data
    :param imaginary:  imaginary data
    :return: magnitude written into rdat
    :rtype: np.ndarray
    
    """
    size = len(rdat)
    compare_shapes(rdat, idat)
    cdef double [:] rdat_view = rdat
    cdef double [:] idat_view = idat

    
    cclm.mus_rectangular_to_magnitudes(&rdat_view[0], &idat_view[0], size)
    return rdat
    
cpdef tuple rectangular2magnitudes(np.ndarray rdat, np.ndarray idat):
    """
    convert real/imaginary data in rl and im from rectangular form (fft output) to polar form, but
    ignore the phases.
    
    :param rdat: real data
    :param imaginary:  imaginary data
    :return: magnitude
    :rtype: np.ndarray
    
    """
    size = len(rdat)
    compare_shapes(rdat, idat)
    rdat_cpy = np.copy(rdat)
    idat_cpy = np.copy(idat) #probably don't need to do this because idat should not be changed
    
    cdef double [:] rdat_view = rdat_cpy
    cdef double [:] idat_view = idat_cpy

    
    cclm.mus_rectangular_to_magnitudes(&rdat_view[0], &idat_view[0], size)
    return rdat_cpy, idat_cpy

cpdef np.ndarray mus_polar2rectangular( np.ndarray rdat,  np.ndarray idat):
    """
    in-place operation. convert real/imaginary data in rl and im from polar (spectrum) to rectangular (fft).
    
    :param rdat: magnitude data
    :param imaginary: phases data
    :return: real data written into rdat, idat contains imaginary
    :rtype: np.ndarray
    
    """
    size = len(rdat)
    cdef double [:] rdat_view = rdat
    cdef double [:] idat_view = idat
    compare_shapes(rdat, idat)
    
    cclm.mus_polar_to_rectangular(&rdat_view[0], &idat_view[0], size)
    return rdat


cpdef tuple polar2rectangular(np.ndarray rdat, np.ndarray idat):
    """
    in-place operation. convert real/imaginary data in rl and im from polar (spectrum) to rectangular (fft).
    
    :param rdat: magnitude data
    :param imaginary: phases data
    :return: real and imaginary
    :rtype: tuple
    
    """
    size = len(rdat)
    compare_shapes(rdat, idat)

   
    rdat_cpy = np.copy(rdat)
    idat_cpy = np.copy(idat) #probably don't need to do this because idat should not be changed
    cdef double [:] rdat_view = rdat_cpy
    cdef double [:] idat_view = idat_cpy
    
    cclm.mus_polar_to_rectangular(&rdat_view[0], &idat_view[0], size)
    return rdat_cpy, idat_cpy

    
cpdef np.ndarray mus_spectrum(np.ndarray  rdat, np.ndarray   idat, np.ndarray  window, Spectrum norm_type= Spectrum.IN_DB):
    """
    in-place operation. real and imaginary data in ndarrays rl and im, returns (in rl) the spectrum thereof; window is the
    fft data window (a ndarray as returned by make_fft_window  and type determines how the spectral data is
    scaled:
    spectrum.in_db= data in db,
    spectrum.normalized (default) = linear and normalized
    spectrum.raw = linear and un-normalized.
    
    :param rdat: real data
    :param imaginary: imaginary data
    :param window: fft window
    :param norm_type: normalization type
    :return: spectrum
    :rtype: np.ndarray
              
    """
    if isinstance(window, list):
        window = np.array(window, dtype=np.double)
    size = len(rdat)
    check_ndim(rdat)
    check_ndim(idat)
    check_ndim(window)
    compare_shapes(rdat, idat)
    
    cdef double [:] rdat_view = rdat
    cdef double [:] idat_view = idat
    cdef double [:] window_view = window
    

    cclm.mus_spectrum(&rdat_view[0], &idat_view[0], &window_view[0], size, <cclm.mus_spectrum_t>norm_type)
    return rdat
    

cpdef tuple spectrum(np.ndarray rdat,np.ndarray  idat,np.ndarray window, Spectrum norm_type=Spectrum.IN_DB):
    """
    real and imaginary data in ndarrays rl and im, returns (in rl) the spectrum thereof; window is the
    fft data window (a ndarray as returned by make_fft_window  and type determines how the spectral data is
    scaled:
    spectrum.in_db= data in db,
    spectrum.normalized (default) = linear and normalized
    spectrum.raw = linear and un-normalized.
    
    :param rdat: real data
    :param imaginary: imaginary data
    :param window: fft window
    :param norm_type: normalization type
    :return: spectrum
    :rtype: np.ndarray
              
    """
    if isinstance(window, list):
        window = np.array(window, dtype=np.double)
    size = len(rdat)
    check_ndim(rdat)
    check_ndim(idat)
    check_ndim(window)
    compare_shapes(rdat, idat)
    rdat_cpy = np.copy(rdat)
    idat_cpy = np.copy(idat) #probably don't need to do this because idat should not be changed

    cdef double [:] rdat_view = rdat_cpy
    cdef double [:] idat_view = idat_cpy
    cdef double [:] window_view = window
    
    cclm.mus_spectrum(&rdat_view[0], &idat_view[0], &window_view[0], size, <cclm.mus_spectrum_t>norm_type)
    return rdat_cpy, idat_cpy
    

cpdef np.ndarray mus_convolution(np.ndarray  rl1, np.ndarray  rl2, fft_size = 512):
    """
    in-place operation. convolution of ndarrays v1 with v2, using fft of size len (a power of 2), result in v1.

    :param rl1: input data 1
    :param rl2: input  data 2
    :param fft_size: fft size
    :return: convolved output. also written into rl1
    :rtype: np.ndarray
    
    """
    # size = len(rl1)
    cdef double [:] rl1_view = rl1
    cdef double [:] rl2_view = rl2
    check_ndim(rl1)
    check_ndim(rl2)
   # compare_shapes(rl1, rl2)
    
    cclm.mus_convolution(&rl1_view[0], &rl2_view[0], fft_size)
    return rl1
    
    

cpdef np.ndarray convolution(np.ndarray  rl1, np.ndarray  rl2, fft_size = 512):
    """
    convolution of ndarrays v1 with v2, using fft of size len (a power of 2), result in v1.

    :param rl1: input data 1
    :param rl2: input  data 2
    :param fft_size: fft size
    :return: convolved output.
    :rtype: np.ndarray
    
    """
    # size = len(rl1)
    check_ndim(rl1)
    check_ndim(rl2)
   # compare_shapes(rl1, rl2)
    rl1_cpy = np.copy(rl1)
    rl2_cpy = np.copy(rl2) #probably do
    
    
    cdef double [:] rl1_view = rl1_cpy
    cdef double [:] rl2_view = rl2_cpy

    
    cclm.mus_convolution(&rl1_view[0], &rl2_view[0], fft_size)
    return rl1_cpy

cpdef np.ndarray mus_autocorrelate(np.ndarray data):
    """
    in place autocorrelation of data (a ndarray).

    :param data: data
    :return: autocorrelation result
    :rtype: np.ndarray

    """
    size = len(data)
    check_ndim(data)
    
    cdef double [:] data_view = data
    cclm.mus_autocorrelate(&data_view[0], size)
    return data
    
    
cpdef np.ndarray autocorrelate(np.ndarray data):
    """
    autocorrelation of data (a ndarray).

    :param data: data
    :return: autocorrelation result
    :rtype: np.ndarray

    """
    size = len(data)
    check_ndim(data)
    data_cpy = np.copy(data) #probably do
    
    cdef double [:] data_view = data_cpy
    cclm.mus_autocorrelate(&data_view[0], size)
    return data_cpy
    
cpdef np.ndarray mus_correlate( np.ndarray  data1,  np.ndarray  data2):
    """
    in place cross-correlation of data1 and data2 (both ndarrays).
    
    :param data1: data 1
    :param data2: data 2
    :return: correlation result written into data1
    :rtype: np.ndarray
    
    
    """
    
    size = len(data1)
    check_ndim(data1)
    check_ndim(data2)
    compare_shapes(data1, data2)
    cdef double [:] data1_view = data1
    cdef double [:] data2_view = data2

    cclm.mus_correlate(&data1_view[0], &data2_view[0], size)
    return data1
    
    
cpdef np.ndarray correlate(np.ndarray  data1, np.ndarray  data2):
    """
    cross-correlation of data1 and data2 (both ndarrays).
    
    :param data1: data 1
    :param data2: data 2
    :return: correlation result
    :rtype: np.ndarray
    
    
    """
    
    size = len(data1)
    check_ndim(data1)
    check_ndim(data2)
    data1_cpy = np.copy(data1)
    data2_cpy = np.copy(data2) 
    compare_shapes(data1, data2)
    cdef double [:] data1_view = data1_cpy
    cdef double [:] data2_view = data2_cpy

    cclm.mus_correlate(&data1_view[0], &data2_view[0], size)
    return data1_cpy

cpdef np.ndarray mus_cepstrum( np.ndarray  data):
    """
    return cepstrum of signal
    
    :param data: samples to analyze
    :return: cepstrum. also written into data
    :rtype: np.ndarray
    """
    size = len(data)
    check_ndim(data)
    cdef double [:] data_view = data
    cclm.mus_cepstrum(&data_view[0], size)
    return data
    
cpdef np.ndarray cepstrum(np.ndarray data):
    """
    return cepstrum of signal
    
    :param data: samples to analyze
    :return: cepstrum.
    :rtype: np.ndarray
    """
    size = len(data)
    check_ndim(data)
    data_cpy = np.copy(data)
    cdef double [:] data_view = data_cpy
    cclm.mus_cepstrum(&data_view[0], size)
    return data_cpy
    
cpdef np.ndarray partials2wave(partials,  np.ndarray wave=None, table_size=None, bint norm=True ):
    """
    take a list or np.ndarray of partials (harmonic number and associated amplitude) and produce a
    waveform for use in table_lookup.
    
    :param partials: list or np.ndarray of partials (harm and amp)
    :param wave: array to write wave into. if not provided, one will be allocated
    :param table_size: size of table
    :param norm: whether to normalize partials
    :return: array provided in wave or new array.
    :rtype: np.ndarray
    
    """
    
    if isinstance(partials, list):
        partials = np.array(partials, dtype=np.double)
    
    if isinstance(wave, list):
        wave = np.array(wave, dtype=np.double)
                        
    if not wave:
        if table_size is not None:
            wave = np.zeros(table_size)
        else:
            table_size = default.table_size
            wave = np.zeros(default.table_size)
    else:
        table_size = len(wave)

    check_ndim(partials)
    check_ndim(wave)

    cdef double [:] wave_view = wave
    cdef double [:] partials_view = partials
    
    cclm.mus_partials_to_wave(&partials_view[0], len(partials) // 2, &wave_view[0], table_size, norm)
    return wave
    
cpdef np.ndarray phase_partials2wave(partials, np.ndarray wave=None, table_size=None, bint norm=True ):
    """
    take a list of partials (harmonic number, amplitude, initial phase) and produce a waveform for use
    in table_lookup.
    
    :param partials: list or np.ndarray of partials (harm, amp, phase)
    :param wave: array to write wave into. if not provided, one will be allocated
    :param table_size: size of table
    :param norm: whether to normalize partials
    :return: array provided in wave or new array.
    :rtype: np.ndarray
    
    """

    if isinstance(partials, list):
        partials = np.array(partials, dtype=np.double)        
            
    if wave is None:
        if table_size:
            wave = np.zeros(table_size)
        else:
            wave = np.zeros(default.table_size)
    else:
        table_size = len(wave)
    
    check_ndim(wave)
    check_ndim(partials)
    
    cdef double [:] wave_view = wave
    cdef double [:] partials_view = partials
    
    cclm.mus_partials_to_wave(&partials_view[0], len(partials) // 3, &wave_view[0], table_size, norm)
    return wave
    
cpdef np.ndarray partials2polynomial(partials, Polynomial kind=Polynomial.FIRST_KIND):
    """
    returns a chebyshev polynomial suitable for use with the polynomial generator to create (via
    waveshaping) the harmonic spectrum described by the partials argument.
    
    :param partials: list or np.ndarray of partials (harm and amp)
    :param kind: Polynomial.EITHER_KIND, Polynomial.FIRST_KIND, Polynomial.SECOND_KIND, Polynomial.BOTH_KINDS
    :return: chebyshev polynomial
    :rtype: np.ndarray
    
    """
    if isinstance(partials, list):
        partials = np.array(partials, dtype=np.double)
   
    check_ndim(partials)     
    
    p = to_partials(partials)
    
    cdef double [:] p_view = p
    
    cclm.mus_partials_to_polynomial(len(p), &p_view[0], <cclm.mus_polynomial_t>kind)
    return p
    
    
cpdef np.ndarray normalize_partials(partials):
    """
    scales the partial amplitudes in the list/array or list 'partials' by the inverse of their sum (so
    that they add to 1.0). creates new array

    :param partials: list or np.ndarray of partials (harm and amp)
    :return: normalized partials
    :rtype: np.ndarray      
    
    """
    # forgoing use of clm function as having some memory issues 
    # also c function is meant for in place operation
    #allocate new array. 
    partials_arr = np.array(partials, dtype=np.double)
    
    check_ndim(partials_arr)

    p = partials_arr[::2]

    v = partials_arr[1::2]

    v_normalized = v / v.sum()
    result = np.empty((p.size + v.size), dtype=np.double)
    result[0::2] = p
    result[1::2] = v_normalized

    
    return result

cpdef cython.double chebyshev_tu_sum( cython.double x, tcoeffs, ucoeffs):
    """
    returns the sum of the weighted chebyshev polynomials tn and un, with phase x
    
    :param x: input
    :param tcoeffs: tn
    :param ucoeffs: un
    :rtype: float
    
    """
    tcoeffs_cpy = np.array(tcoeffs)
    ucoeffs_cpy = np.array(ucoeffs)
    check_ndim(tcoeffs_cpy)
    check_ndim(ucoeffs_cpy)
    compare_shapes(tcoeffs_cpy, ucoeffs_cpy)

    
    cdef double [:] tcoeffs_view = tcoeffs_cpy
    cdef double [:] ucoeffs_view = ucoeffs_cpy
    return cclm.mus_chebyshev_tu_sum(x, len(tcoeffs_cpy), &tcoeffs_view[0], &ucoeffs_view[0])
    

cpdef cython.double chebyshev_t_sum(cython.double x, tcoeffs):
    """
    returns the sum of the weighted chebyshev polynomials tn
    
    :param x: nput
    :param tcoeffs: tn
    :rtype: float
    
    """
    tcoeffs_cpy = np.array(tcoeffs)    
    check_ndim(tcoeffs_cpy)

    cdef double [:] tcoeffs_view = tcoeffs_cpy
    return cclm.mus_chebyshev_t_sum(x,len(tcoeffs_cpy), &tcoeffs_view[0])

cpdef cython.double chebyshev_u_sum(cython.double x, ucoeffs):
    """
    returns the sum of the weighted chebyshev polynomials un
    
    :param x: input
    :param ucoeffs: un
    :rtype: float
    
    """
    ucoeffs_cpy = np.array(ucoeffs)
    
    check_ndim(ucoeffs)
    
    cdef double [:] ucoeffs_view = ucoeffs_cpy
    return cclm.mus_chebyshev_u_sum(x,len(ucoeffs_cpy), &ucoeffs_view[0])
    



# ---------------- oscil ---------------- #
cpdef mus_any make_oscil(cython.double frequency=0.,cython.double  initial_phase = 0.0):
    """
    return a new oscil (sinewave) generator
    
    :param frequency: frequency in hz
    :param initial_phase: initial phase in radians
    :return: oscil gen
    """
    check_range('frequency', frequency, 0., get_srate() / 2)
    
    
    return mus_any.from_ptr(cclm.mus_make_oscil(frequency, initial_phase))
    
## Changing to avoid None overhead. Think it slows thing s down even if mus_oscil_unmodulated can be used.
cpdef cython.double oscil(mus_any gen, cython.double fm=0.0, cython.double pm=0.0):
    """
    return next sample from oscil gen: val = sin(phase + pm); phase += (freq + fm)
    
    :param gen: oscil gen
    :param fm: fm input
    :param pm: pm input
    :rtype: float
    
    """    
    return cclm.mus_oscil(gen._ptr, fm, pm)
    
cpdef cython.double oscil_unmodulated(mus_any gen):
    """
    return next sample from oscil gen. no modulation
    
    :param gen: oscil gen
    :rtype: float
    
    """    
    return cclm.mus_oscil_unmodulated(gen._ptr)
               
cpdef bint is_oscil(mus_any gen):
    """
    returns True if gen is an oscil
    
    :param gen: oscil gen
    :rtype: bool
    
    """
    return cclm.mus_is_oscil(gen._ptr)
    
# ---------------- oscil-bank ---------------- #

cpdef mus_any make_oscil_bank(freqs, phases, amps=None, bint stable=False):
    """
    return a new oscil_bank generator. (freqs in radians)
    
    :param freqs: list or np.ndarray of frequencies in radians
    :param phases: list or np.ndarray of initial phases in radians
    :param stable:  if it is true, oscil_bank can assume that the frequency. this is not operative
    :return: oscil_bank gen
    :rtype: mus_any
    
    """
    cdef cclm.mus_float_t [:] freqs_view = None
    cdef cclm.mus_float_t [:] phases_view = None
    cdef cclm.mus_float_t [:] amps_view = None
    
    if isinstance(freqs, list):
        freqs = np.array(freqs, dtype=np.double)
    if isinstance(phases, list):
        phases = np.array(phases, dtype=np.double)        

    check_ndim(freqs)
    check_ndim(phases)
    compare_shapes(freqs, phases)

    freqs_view = freqs
    phases_view = phases
    
    if amps is not None:
        if isinstance(amps, list):
            amps = np.array(amps, dtype=np.double)    
        check_ndim(amps)
        amps_view = amps
        gen = mus_any.from_ptr(cclm.mus_make_oscil_bank(len(freqs), &freqs_view[0], &phases_view[0], &amps_view[0], stable))
    else:
        gen = mus_any.from_ptr(cclm.mus_make_oscil_bank(len(freqs), &freqs_view[0], &phases_view[0], NULL, stable))
    
    gen.cache_extend([freqs, phases, amps])
    return gen

cpdef cython.double oscil_bank(mus_any gen):
    """
    sum an array of oscils
    
    :param gen: oscil_bank gen
    :rtype: float
    """
    return cclm.mus_oscil_bank(gen._ptr)
    
cpdef bint is_oscil_bank(mus_any gen):
    """
    returns True if gen is an oscil_bank
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_oscil_bank(gen._ptr)




# ---------------- env ---------------- #
cpdef mus_any make_env(envelope, cython.double duration=1.0, cython.double scaler=1.0, cython.double offset=0.0, cython.double base=1.0, cython.int length=0):
    """
    return a new envelope generator.  'envelope' is a list/array of break-point pairs. to create the
    envelope, these points are offset by 'offset', scaled by 'scaler', and mapped over the time interval
    defined by either 'duration' (seconds) or 'length' (samples).  if 'base' is 1.0, the connecting segments
    are linear, if 0.0 you get a step function, and anything else produces an exponential connecting segment.
    
    :param envelope: list or np.ndarry of breakpoint pairs
    :param scaler: scaler on every y value (before offset is added)
    :param duration: duration \in seconds
    :param offset: value added to every y value
    :param base: type of connecting line between break-points
    :param length:  duration \in samples
    :result: env gen
    :rtype: mus_any

    """
#     print(envelope)
    validate_envelope(envelope)
    check_range('duration', duration, 0.0, None)
    
    if length > 0:
        duration = samples2seconds(length)
    
    if isinstance(envelope, list):
        envelope = np.array(envelope, dtype=np.double)        

    check_ndim(envelope)

    cdef double [:] envelope_view = envelope
    gen =  mus_any.from_ptr(cclm.mus_make_env(&envelope_view[0], len(envelope) // 2, scaler, offset, base, duration, 0, NULL),owner=True, length=len(envelope))
    #sprint(gen)
    gen.cache_append(envelope)
    return gen

cpdef cython.double env(mus_any gen ):
    """
    next sample from envelope generator.
    
    :param gen: env gen
    :rtype: float
    """
    return cclm.mus_env(gen._ptr)

cpdef bint is_env(mus_any gen):
    """
    returns True if gen is an env.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_env(gen._ptr)

cpdef cython.double env_interp(cython.double x , mus_any env):
    """
    value of envelope env at x.
    
    :param x: location \in envelope
    :param env: env gen
    :rtype: float
    """
    return cclm.mus_env_interp(x, env._ptr)

cpdef cython.double envelope_interp(cython.double x ,  mus_any env):
    """
    value of envelope env at x.
    
    :param x: location \in envelope
    :param env: env gen
    :rtype: float
    """
    return cclm.mus_env_interp(x, env._ptr)
    
      
# #mus_env_rates
cpdef np.ndarray env_rates(gen: mus_any):
    cdef view.array arr = None
    cdef cclm.mus_long_t size = cclm.mus_length(gen._ptr)
    cdef cclm.mus_float_t* rates_ptr = cclm.mus_env_rates(gen._ptr)
    arr = view.array(shape=(size,),itemsize=sizeof(double), format='d', allocate_buffer=False)
    arr.data = <char*>rates_ptr
    return np.asarray(arr)
#             
    

# this is slow because of needing ctypes to define function at runtime
# but no other way to do it with cython without changing sndlib code
cpdef cython.double env_any(mus_any gen, connection_function):
    """
    generate env output using conncection_func to 'connect the dots'.
    
    the env-any connecting function takes one argument, the current envelope value treated as going between 0.0 and 1.0 between each two points. 
    :param env: env gen
    :param connection_function: function used to connect points
    :rtype: float
    """
    
    f = _envfunction(connection_function)
    cdef cclm.connect_points_cb cy_f_ptr = (<cclm.connect_points_cb*><size_t>ctypes.addressof(f))[0]
    return cclm.mus_env_any(gen._ptr, cy_f_ptr)


# ---------------- pulsed-env ---------------- #    
cpdef mus_any make_pulsed_env(envelope, cython.double duration , cython.double frequency ):
    """
    produces a repeating envelope. env sticks at its last value, but pulsed-env repeats it over and over. 
    
    :param env: env gen
    :param duration: duration of envelope
    :param frequency: repetition rate \in hz
    :return: env output
    :rtype: float
    """
    
    if isinstance(envelope, list):
        envelope = np.array(envelope, dtype=np.double)        

    pl = mus_any.from_ptr(cclm.mus_make_pulse_train(frequency, 1.0, 0.0))
    
    check_ndim(envelope)
    
    cdef double [:] envelope_view = envelope
    
    ge =  mus_any.from_ptr(cclm.mus_make_env(&envelope_view[0], len(envelope) // 2, 1.0, 0, 1.0, duration, 0, NULL))
    gen = mus_any.from_ptr(cclm.mus_make_pulsed_env(ge._ptr, pl._ptr))
    gen.cache_extend([pl, ge, envelope])
    return gen
    
cpdef cython.double pulsed_env(mus_any gen, cython.double fm=0.0):
    """
    next sample from envelope generator.
    
    :param gen: env gen
    :param fm: change frequency of repetition
    :rtype: float
    """
    return cclm.mus_pulsed_env(gen._ptr, fm)
    
cpdef cython.double pulsed_env_unmodulated(mus_any gen):
    """
    next sample from envelope generator. no modulations
    
    :param gen: env gen
    :rtype: float
    """
    return cclm.mus_pulsed_env_unmodulated(gen._ptr)
        
cpdef bint is_pulsed_env(mus_any gen):
    """
    returns True if gen is a pulsed_env.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_pulsed_env(gen._ptr)
        
# todo envelope-interp different than env-interp

# ---------------- table-lookup ---------------- #
cpdef mus_any make_table_lookup(cython.double frequency=0.0, cython.double initial_phase=0.0, wave= None, size=None, Interp interp_type=Interp.LINEAR):        
    """
    return a new table_lookup generator. the default table size is 512; use size to set some other
    size, or pass your own list/array as the 'wave'.
    
    :param frequency: frequency of gen \in hz
    :param initial_phase: initial phase of gen \in radians
    :param wave: np.ndarray if provided is waveform
    :param size: if no wave provided, this will allocate a table of size 
    :param interp_type: type of interpolation used
    :return: table_lookup gen
    :rtype: mus_any
    """                                               
    size = size or default.table_size

    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    if wave is None:
        wave = np.zeros(size)
    
    if isinstance(wave, list):
        wave = np.array(wave, dtype=np.double)        
    
    check_ndim(wave)
    
    cdef double [:] wave_view = wave


    #print(frequency, initial_phase, wave, size, interp_type)
    gen =  mus_any.from_ptr(cclm.mus_make_table_lookup(frequency, initial_phase, &wave_view[0], size, <cclm.mus_interp_t>interp_type))
    gen.cache_append(wave)
    return gen
    
cpdef cython.double table_lookup(mus_any gen, cython.double fm =0.0):
    """
    return next sample from table_lookup generator.
    
    :param gen: table_lookup gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_table_lookup(gen._ptr, fm)
        
cpdef cython.double table_lookup_unmodulated(mus_any gen):
    """
    return next sample from table_lookup generator. unmodulated
    
    :param gen: table_lookup gen
    :rtype: float
    """
    return cclm.mus_table_lookup_unmodulated(gen._ptr)
        
cpdef bint is_table_lookup(mus_any gen):
    """
    returns True if gen is a table_lookup.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_table_lookup(gen._ptr)


cpdef mus_any make_table_lookup_with_env(cython.double frequency, envelope, size= None):
    """
    return a new table_lookup generator with the envelope loaded \in with size.
    
    :param frequency: frequency of gen \in hz
    :param env: envelope shape to load into generator
    :param size: size of table derived from envelope
    :return: table_lookup gen
    :rtype: mus_any
    
    """
    
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    size = size or default.table_size
    table = np.zeros(size)  
    e = make_env(envelope, length=size)
    for i in range(size):
        table[i] = env(e)
    cdef double [:] table_view = table
    
    gen =  mus_any.from_ptr(cclm.mus_make_table_lookup(frequency, 0, &table_view[0], size, <cclm.mus_interp_t>Interp.LINEAR))
    gen.cache_append(table)
    return gen
         
# ---------------- polywave ---------------- #
cpdef mus_any make_polywave(cython.double frequency,  partials = [0.,1.], Polynomial kind=Polynomial.FIRST_KIND, xcoeffs=None, ycoeffs=None):
    """
    return a new polynomial-based waveshaping generator. make_polywave(440.0, partials=[1.0,1.0]) is
    the same \in effect as make_oscil.
    
    :param frequency: polywave frequency
    :param partials: a list of harmonic numbers and their associated amplitudes
    :param kind: Chebyshev polynomial choice
    :param xcoeffs: tn for tu-sum case
    :param ycoeffs: un for tu-sum case
    :return: polywave gen
    :rtype: mus_any
    """
   # print(f'make_polywave: f: {frequency} p: {partials} x: {xcoeffs} y: {ycoeffs}')
    
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    cdef double [:] xcoeffs_view = None
    cdef double [:] ycoeffs_view = None
    
    # TODO : catch when only one exists
    if  isinstance(xcoeffs, (np.ndarray, list)) and isinstance(ycoeffs, (np.ndarray, list)):
        xcoeffs_arr = np.array(xcoeffs, dtype=np.double)        
        xcoeffs_view = xcoeffs_arr
        ycoeffs_arr = np.array(ycoeffs, dtype=np.double)        
        ycoeffs_view = ycoeffs_arr
        check_ndim(xcoeffs_arr)
        check_ndim(ycoeffs_arr)
        compare_shapes(xcoeffs_arr, ycoeffs_arr)
        
        gen = mus_any.from_ptr(cclm.mus_make_polywave_tu(frequency,&xcoeffs_view[0],&ycoeffs_view[0], len(xcoeffs_arr)))
        gen.cache_extend([xcoeffs_arr, ycoeffs_arr])
        return gen
    else:
        partials_arr = None
        
        if isinstance(partials, np.ndarray):
            partials_arr = partials
        if isinstance(partials, list):
            partials_arr = np.array(partials, dtype=np.double)     
        
        p = partials_arr[::2]
        maxpartial = max(p)
        
        prtls = np.zeros(int(maxpartial)+1, dtype=np.double)
        
        check_ndim(prtls)
        
        for i in range(0, len(partials_arr),2):
            curpartial = partials_arr[i]
            prtls[int(curpartial)] = partials_arr[i+1]
        
        xcoeffs_view = prtls
        
        gen = mus_any.from_ptr(cclm.mus_make_polywave(frequency, &xcoeffs_view[0], len(prtls), kind))

        gen.cache_extend([prtls])
        return gen
    
    
cpdef cython.double polywave(mus_any gen, cython.double fm=0.0):
    """
    next sample of polywave waveshaper.
    
    :param gen: polywave gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_polywave(gen._ptr, fm)

    
cpdef cython.double polywave_unmodulated(mus_any gen):
    """
    next sample of polywave waveshaper. unmodulated
    
    :param gen: polywave gen
    :rtype: float
    """
    return cclm.mus_polywave_unmodulated(gen._ptr)
        
cpdef bint is_polywave(mus_any gen):
    """
    returns True if gen is a polywave.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_polywave(gen._ptr)



# ---------------- polyshape ---------------- #

cpdef mus_any make_polyshape(cython.double frequency, cython.double initial_phase=0.0, coeffs = None, partials = [1.,1.], Polynomial kind=Polynomial.FIRST_KIND):
                    
    """
    return a new polynomial-based waveshaping generator.
    
    :param frequency: frequency of gen \in hz
    :param initial_phase: initial phase of gen \in radians
    :param coeff: coefficients can be passed to polyshape
    :param partials: a list of harmonic numbers and their associated amplitudes
    :param kind: Chebyshev polynomial choice
    :return: polyshape gen
    :rtype: mus_any
    """
    
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    if coeffs:
        if isinstance(coeffs, list):
            data = np.array(coeffs, dtype=np.double)     
        else:
            data = coeffs   

    else:
        data = partials2polynomial(partials, kind)

    check_ndim(data) 

    cdef double [:] data_view = data
    
    gen = mus_any.from_ptr(cclm.mus_make_polyshape(frequency, initial_phase, &data_view[0], len(data), kind))
    gen.cache_append(data)
    return gen
    
cpdef cython.double polyshape(mus_any gen, cython.double index=1.0, cython.double fm=0.0):
    """
    next sample of polynomial-based waveshaper.
    
    :param gen: polyshape gen
    :param index: fm index
    :param fm: fm input
    :rtype: float
    """
    if fm:
        return cclm.mus_polyshape(gen._ptr, index, fm)
    else:
        return cclm.mus_polyshape_unmodulated(gen._ptr, index)
        
cpdef cython.double polyshape_unmodulated(mus_any gen, cython.double index=1.0):
    """
    next sample of polynomial-based waveshaper. unmodulated
    
    :param gen: polyshape gen
    :param index: fm index
    :rtype: float
    """
    return cclm.mus_polyshape_unmodulated(gen._ptr, index)
        
        
cpdef bint is_polyshape(mus_any gen):
    """
    returns True if gen is a polyshape.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_polyshape(gen._ptr)


# ---------------- triangle-wave ---------------- #    
cpdef mus_any make_triangle_wave(cython.double frequency, cython.double amplitude=1.0, cython.double phase=np.pi):
    """
    return a new triangle_wave generator.
    
    :param frequency: frequency of generator
    :param amplitude: amplitude of generator
    :param phase: initial phase
    :return: triangle_wave gen
    :rtype: mus_any
    
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    return mus_any.from_ptr(cclm.mus_make_triangle_wave(frequency, amplitude, phase))
    
cpdef cython.double triangle_wave(mus_any gen, cython.double fm=0.0):
    """
    next triangle wave sample from generator. 
    
    :param gen: polyshape gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_triangle_wave(gen._ptr, fm)

    
cpdef cython.double triangle_wave_unmodulated(mus_any gen):
    """
    next triangle wave sample from generator. unmodulated
    
    :param gen: polyshape gen
    :rtype: float
    """
    return cclm.mus_triangle_wave_unmodulated(gen._ptr)
    
cpdef bint is_triangle_wave(mus_any gen):
    """
    returns True if gen is a triangle_wave.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_triangle_wave(gen._ptr)

# ---------------- square-wave ---------------- #    
cpdef mus_any make_square_wave(cython.double frequency , cython.double amplitude=1.0, cython.double phase=0.0):
    """
    return a new square_wave generator.
    
    :param frequency: frequency of generator
    :param amplitude: amplitude of generator
    :param phase: initial phase
    :return: square_wave gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    return mus_any.from_ptr(cclm.mus_make_square_wave(frequency, amplitude, phase))
    
cpdef cython.double square_wave(mus_any gen, cython.double fm=0.0):
    """
    next square wave sample from generator.
    
    :param gen: polyshape gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_square_wave(gen._ptr, fm)
    
cpdef bint is_square_wave(mus_any gen):
    """
    returns True if gen is a square_wave.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_square_wave(gen._ptr)
    
# ---------------- sawtooth-wave ---------------- #    
cpdef mus_any make_sawtooth_wave(cython.double frequency, cython.double amplitude=1.0, cython.double phase=np.pi):
    """
    return a new sawtooth_wave generator.
    
    :param frequency: frequency of generator
    :param amplitude: amplitude of generator
    :param phase: initial phase
    :return: sawtooth_wave gen
    :rtype: mus_any
    """
    
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    return mus_any.from_ptr(cclm.mus_make_sawtooth_wave(frequency, amplitude, phase))
    
cpdef cython.double sawtooth_wave(mus_any gen, cython.double fm =0.0):
    """
    next sawtooth wave sample from generator.
    
    :param gen: polyshape gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_sawtooth_wave(gen._ptr, fm)

    
cpdef bint is_sawtooth_wave(mus_any gen):
    """
    returns True if gen is a sawtooth_wave.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_sawtooth_wave(gen._ptr)

# ---------------- pulse-train ---------------- #        
cpdef mus_any make_pulse_train(cython.double frequency=1.0, cython.double amplitude=1.0, cython.double phase=(np.pi*2)):
    """
    return a new pulse_train generator. this produces a sequence of impulses.
    
    :param frequency: frequency of generator
    :param amplitude: amplitude of generator
    :param phase: initial phase
    :return: pulse_train gen
    :rtype: mus_any
    """
    
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    return mus_any.from_ptr(cclm.mus_make_pulse_train(frequency, amplitude, phase))
    
cpdef cython.double pulse_train(mus_any gen, cython.double fm=0.0):
    """
    next pulse train sample from generator.
    
    :param gen: pulse_train gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_pulse_train(gen._ptr, fm)

        
cpdef cython.double pulse_train_unmodulated(mus_any gen):
    """
    next pulse train sample from generator. unmodulated
    :param gen: pulse_train gen
    :rtype: float
    """
    return cclm.mus_pulse_train_unmodulated(gen._ptr)
     
cpdef bint is_pulse_train(mus_any gen):
    """
    returns True if gen is a pulse_train.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_pulse_train(gen._ptr)
    
# ---------------- ncos ---------------- #

cpdef mus_any make_ncos(cython.double frequency, cython.int n=1):
    """
    return a new ncos generator, producing a sum of 'n' equal amplitude cosines.
    
    :param frequency: frequency of generator
    :param n: number of cosines
    :return: ncos gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    check_range('n', n, 0, None)
    return mus_any.from_ptr(cclm.mus_make_ncos(frequency, n))
    
cpdef cython.double ncos(mus_any gen, cython.double fm=0.0):
    """
    get the next sample from 'gen', an ncos generator.
    
    :param gen: ncos gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_ncos(gen._ptr, fm)

cpdef bint is_ncos(mus_any gen):
    """
    returns True if gen is a ncos.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_ncos(gen._ptr)
    
    
# ---------------- nsin ---------------- #
cpdef mus_any make_nsin(cython.double frequency, cython.int n =1):
    """
    return a new nsin generator, producing a sum of 'n' equal amplitude sines.
    
    :param frequency: frequency of generator
    :param n: number of sines
    :return: nsin gen
    :rtype: mus_any
    """
    
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    check_range('n', n, 0, None)
    
    return mus_any.from_ptr(cclm.mus_make_nsin(frequency, n))
    
cpdef cython.double nsin(mus_any gen, cython.double fm=0.0):
    """
    get the next sample from 'gen', an nsin generator.
    
    :param gen: ncos gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_nsin(gen._ptr, fm)
    
cpdef bint is_nsin(mus_any gen ):
    """
    returns True if gen is a nsin.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_nsin(gen._ptr)
    
# ---------------- nrxysin and nrxycos ---------------- #

cpdef mus_any make_nrxysin( cython.double frequency,  cython.double ratio=1., cython.int n=1, cython.double r=.5):
    """
    return a new nrxysin generator.
    
    :param frequency: frequency of generator
    :param ratio: ratio between frequency and the spacing between successive sidebands
    :param n: number of sidebands
    :param r: amplitude ratio between successive sidebands (-1.0 < r < 1.0)
    :return: nrxysin gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    check_range('r', r, -1.0, 1.0)
    check_range('n', n, 0, None) 
    
    return mus_any.from_ptr(cclm.mus_make_nrxysin(frequency, ratio, n, r))
    
cpdef cython.double nrxysin(mus_any gen, cython.double fm=0.):
    """
    next sample of nrxysin generator.
    
    :param gen: ncos gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_nrxysin(gen._ptr, fm)
    
cpdef bint is_nrxysin(mus_any gen):
    """
    returns True if gen is a nrxysin.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_nrxysin(gen._ptr)
    
    
cpdef mus_any make_nrxycos(cython.double frequency , cython.double ratio=1., cython.int n=1, cython.double r=.5):
    """
    return a new nrxycos generator.
    
    :param frequency: frequency of generator
    :param ratio: ratio between frequency and the spacing between successive sidebands
    :param n: number of sidebands
    :param r: amplitude ratio between successive sidebands (-1.0 < r < 1.0)
    :return: nrxycos gen
    :rtype: mus_any
    """
    
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    check_range('r', r, -1.0, 1.0)
    check_range('n', n, 0, None)   
    
    return mus_any.from_ptr(cclm.mus_make_nrxycos(frequency, ratio, n, r))
    
cpdef cython.double nrxycos(mus_any gen, cython.double fm=0.):
    """
    next sample of nrxycos generator.
    
    :param gen: ncos gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_nrxycos(gen._ptr, fm)
    
cpdef bint is_nrxycos(mus_any gen):
    """
    returns True if gen is a nrxycos.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_nrxycos(gen._ptr)
    
    
# ---------------- rxykcos and rxyksin ---------------- #    
cpdef mus_any make_rxykcos(cython.double frequency, cython.double phase=0.0, cython.double r=.5, cython.double ratio=1.):
    """
    return a new rxykcos generator.
    
    :param frequency: frequency of generator
    :param ratio: ratio between frequency and the spacing between successive sidebands
    :param r: amplitude ratio between successive sidebands (-1.0 < r < 1.0)
    :return: rxykcos gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    check_range('r', r, -1.0, 1.0)
    
    return mus_any.from_ptr(cclm.mus_make_rxykcos(frequency, phase, r, ratio))
    
cpdef cython.double rxykcos(mus_any gen, cython.double fm=0.):
    """
    next sample of rxykcos generator.
    
    :param gen: rxykcos gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_rxykcos(gen._ptr, fm)
    
cpdef bint is_rxykcos(gen: mus_any):
    """
    returns True if gen is a rxykcos.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_rxykcos(gen._ptr)

cpdef mus_any make_rxyksin(cython.double frequency, cython.double phase, cython.double r=.5, cython.double ratio=1.):
    """
    return a new rxyksin generator.
    
    :param frequency: frequency of generator
    :param ratio: ratio between frequency and the spacing between successive sidebands
    :param r: amplitude ratio between successive sidebands (-1.0 < r < 1.0)
    :return: rxyksin gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    check_range('r', r, -1.0, 1.0)
    
    return mus_any.from_ptr(cclm.mus_make_rxyksin(frequency, phase, r, ratio))

cpdef cython.double rxyksin(mus_any gen, cython.double fm=0.):
    """
    next sample of rxyksin generator.
    
    :param gen: rxyksin gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_rxyksin(gen._ptr, fm)
    
cpdef bint  is_rxyksin(mus_any gen):
    """
    returns True if gen is a rxyksin.
    
    :param gen: gen
    :rtype: bool
    """    
    return cclm.mus_is_rxyksin(gen._ptr)
        
# ---------------- ssb-am ---------------- #    
cpdef mus_any make_ssb_am(cython.double frequency, cython.int order=40):
    """
    return a new ssb_am generator.
    
    :param frequency: frequency of generator
    :param order: embedded delay line size
    :return: ssb_am gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    return mus_any.from_ptr(cclm.mus_make_ssb_am(frequency, order))
    
cpdef cython.double ssb_am(mus_any gen, cython.double insig , cython.double  fm=0.0):
    """
    get the next sample from ssb_am generator.
    
    :param gen: ssb_am gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_ssb_am(gen._ptr, insig, fm)


cpdef cython.double ssb_am_unmodulated(mus_any gen, cython.double insig):
    """
    get the next sample from ssb_am generator. unmodulated.
    
    :param gen: ssb_am gen
    :rtype: float
    """
    return cclm.mus_ssb_am_unmodulated(gen._ptr, insig)
        
cpdef bint is_ssb_am(mus_any gen):
    """
    returns True if gen is a ssb_am.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_ssb_am(gen._ptr)



# ---------------- wave-train ----------------#
cpdef mus_any make_wave_train(cython.double frequency, wave=None, cython.double initial_phase=0., Interp interp_type=Interp.LINEAR):
    """
    return a new wave-train generator (an extension of pulse-train). frequency is the repetition rate
    of the wave found \in wave. successive waves can overlap.
    
    :param frequency: frequency of gen \in hz
    :param wave: np.ndarray if provided is waveform
    :param initial_phase: initial phase of gen \in radians
    :param interp_type: type of interpolation used
    :return: wave_train gen
    :rtype: mus_any
    """
    if isinstance(wave, list):
        wave = np.array(wave)
    
    check_ndim(wave)
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    cdef double [:] wave_view = wave
    gen = mus_any.from_ptr(cclm.mus_make_wave_train(frequency, initial_phase, &wave_view[0], len(wave), <cclm.mus_interp_t>interp_type))
    gen.cache_append(wave)
    return gen
    
cpdef cython.double wave_train(mus_any gen, cython.double fm=0.0):
    """
    next sample of wave_train.
    
    :param gen: wave_train gen
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_wave_train(gen._ptr, fm)

        
cpdef cython.double wave_train_unmodulated(mus_any gen):
    """
    next sample of wave_train. unmodulated
    
    :param gen: wave_train gen
    :rtype: float
    """
    return cclm.mus_wave_train_unmodulated(gen._ptr)
    
cpdef bint is_wave_train(mus_any gen):
    """
    returns True if gen is a wave_train.
    
    :param gen: gen
    :rtype: bool
    """    
    return cclm.mus_is_wave_train(gen._ptr)


cpdef mus_any make_wave_train_with_env(cython.double frequency, envelope, size=None):
    """
    return a new wave-train generator with the envelope loaded \in with size.
    
    :param frequency: frequency of gen \in hz
    :param env: envelope shape to load into generator
    :param size: size of wave derived from envelope
    :return: wave_train gen
    :rtype: mus_any
    
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    size = size or default.table_size
    wave = np.zeros(size)  
    e = make_env(envelope, length=size)
    for i in range(size):
        wave[i] = env(e)
    cdef double [:] wave_view = wave
    gen = mus_any.from_ptr(cclm.mus_make_wave_train(frequency, 0.0, &wave_view[0], size, <cclm.mus_interp_t>Interp.LINEAR))
    gen.cache_append(wave)
    return gen

# ---------------- rand, rand_interp ---------------- #
cpdef mus_any make_rand(cython.double frequency, cython.double amplitude=1.0, distribution=None):
    """
    return a new rand generator, producing a sequence of random numbers (a step  function). frequency
    is the rate at which new numbers are chosen.
    
    :param frequency: frequency at which new random numbers occur
    :param amplitude: numbers are between -amplitude and amplitude
    :param distribution: distribution envelope
    :return: rand gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate())
    cdef double [:] distribution_view = None
    
    if distribution:
        check_ndim(distribution)
        distribution_view = distribution
        gen =  mus_any.from_ptr(cclm.mus_make_rand_with_distribution(frequency, amplitude, &distribution_view[0], len(distribution)))
        gen.cache_append(distribution)
        return gen
    else:
        return mus_any.from_ptr(cclm.mus_make_rand(frequency, amplitude))

cpdef cython.double rand(mus_any gen, cython.double sweep=0.0):
    """
    gen's current random number. sweep modulates the rate at which the current number is changed.
    
    :param gen: rand gen
    :param sweep: fm
    :rtype: float
    
    """
    return cclm.mus_rand(gen._ptr, sweep)
        
cpdef cython.double rand_unmodulated(mus_any gen):
    """
    gen's current random number. sweep modulates the rate at which the current number is changed. unmodulated
    
    :param gen: rand gen
    :rtype: float
    
    """
    return cclm.mus_rand_unmodulated(gen._ptr)
    
cpdef bint is_rand(mus_any gen):
    """
    returns True if gen is a rand.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_rand(gen._ptr)

cpdef mus_any make_rand_interp(cython.double frequency, cython.double amplitude=1.0, distribution=None):
    """
    return a new rand_interp generator, producing linearly interpolated random numbers. frequency is
    the rate at which new end-points are chosen.
    
    :param frequency: frequency at which new random numbers occur
    :param amplitude: numbers are between -amplitude and amplitude
    :param distribution: distribution envelope
    :return: rand_interp gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate())
    cdef double [:] distribution_view = None
    
    if distribution:
        check_ndim(distribution)
        distribution_view = distribution
        gen = mus_any.from_ptr(cclm.mus_make_rand_interp_with_distribution(frequency, amplitude, &distribution_view[0], len(distribution)))
        gen.cache_append(distribution)
        return gen
    else:
        return mus_any.from_ptr(cclm.mus_make_rand_interp(frequency, amplitude))
    
cpdef rand_interp(mus_any gen, cython.double sweep=0.):
    """
    gen's current (interpolating) random number. fm modulates the rate at which new segment end-points
    are chosen.
    
    :param gen: rand_interp gen
    :param sweep: fm 
    :rtype: float
    """
    return cclm.mus_rand_interp(gen._ptr, sweep)
    
cpdef rand_interp_unmodulated(mus_any gen):
    """
    gen's current (interpolating) random number. fm modulates the rate at which new segment end-points
    are chosen. unmodulated
    
    :param gen: rand_interp gen
    :rtype: float
    """
    return cclm.mus_rand_interp_unmodulated(gen._ptr)
    
    
cpdef bint is_rand_interp(mus_any gen):
    """
    returns True if gen is a rand_interp.
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_rand_interp(gen._ptr)    
    
    
# ---------------- simple filters ---------------- #
cpdef mus_any make_one_pole(cython.double a0, cython.double b1):
    """
    return a new one_pole filter: y(n) = a0 x(n) - b1 y(n-1)
    b1 < 0.0 gives lowpass, b1 > 0.0 gives highpass.
    
    :param a0: coefficient
    :param b1: coefficient
    :return: one_pole gen
    :rtype: mus_any
    """
    
    return mus_any.from_ptr(cclm.mus_make_one_pole(a0, b1))

    
    
cpdef cython.double one_pole(mus_any gen, cython.double insig):
    """
    one pole filter of input.
    
    :param gen: one_pole gen
    :param insig: input 
    :rtype: float
    """
    
    return cclm.mus_one_pole(gen._ptr, insig)
    
cpdef bint is_one_pole(mus_any gen):
    """
    returns True if gen is a one_pole.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_one_pole(gen._ptr)


cpdef mus_any make_one_zero(cython.double a0 , cython.double a1):
    """
    return a new one_zero filter: y(n) = a0 x(n) + a1 x(n-1)
    a1 > 0.0 gives weak lowpass, a1 < 0.0 highpass.
    
    :param a0: coefficient
    :param a1: coefficient
    :return: one_pole gen
    :rtype: mus_any
    """
    return mus_any.from_ptr(cclm.mus_make_one_zero(a0, a1))
    
cpdef cython.double one_zero(mus_any gen, cython.double insig):
    """
    one zero filter of input.
    
    :param gen: one_zero gen
    :param insig: input 
    :rtype: float
    """
    return cclm.mus_one_zero(gen._ptr, insig)
    
cpdef bint is_one_zero(mus_any gen):
    """
    returns True if gen is a one_zero.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_one_zero(gen._ptr)    


cpdef make_two_pole(frequency=None, radius=None, a0=None,b1=None,b2=None):
    """
    return a new two_pole filter: y(n) = a0 x(n) - b1 y(n-1) - b2 y(n-2).
    
    :param frequency: Center frequency \in Hz
    :param radius: Radius of filter. Refers to the unit circle, so it should be between 0.0 and (less than) 1.0. 
    :param kwargs: If frequency and radius not provided, these should be keyword arguments 'a0', 'b1', 'b2'
    :return: two_pole gen
    :rtype: mus_any
    """
    if all((frequency, radius)):
        return mus_any.from_ptr(cclm.mus_make_two_pole_from_frequency_and_radius(frequency, radius))
    elif any((frequency, radius)):
        raise RuntimeError("If not specifying coeffs, must provide frequency and radius. got frequency: {frequency}, radius: {radius}")
    else:  
        if all((a0,b1,b2)):
            return mus_any.from_ptr(cclm.mus_make_two_pole(a0,b2,b2))
        else:
            raise KeyError(f'Filter needs values for a0, b1, b2 got a0: {a0}, b1: {b1}, b2: {b2}')

                  
cpdef cython.double two_pole(mus_any gen, cython.double insig):
    """
    two pole filter of input.
    
    :param gen: two_pole gen
    :param insig: input 
    :rtype: float  
    
    """
    return cclm.mus_two_pole(gen._ptr, insig)
    
cpdef bint is_two_pole(mus_any gen):
    """
    returns True if gen is a two_pole.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_two_pole(gen._ptr)


cpdef make_two_zero(frequency=None, radius=None, a0=None,a1=None,a2=None):
    """
    return a new two_zero filter: y(n) = a0 x(n) + a1 x(n-1) + a2 x(n-2).
    
    :param frequency: Center frequency \in Hz
    :param radius: Radius of filter. Refers to the unit circle, so it should be between 0.0 and (less than) 1.0. 
    :param kwargs: If frequency and radius not provided, these should be keyword arguments 'a0', 'a1', 'a2'
    :return: two_zero gen
    :rtype: mus_any
    """
    if all((frequency, radius)):
        return mus_any.from_ptr(cclm.mus_make_two_zero_from_frequency_and_radius(frequency, radius))
    elif any((frequency, radius)):
        raise RuntimeError("If not specifying coeffs, must provide frequency and radius. got frequency: {frequency}, radius: {radius}")
    else:  
        if all((a0,a1,a2)):
            return mus_any.from_ptr(cclm.mus_make_two_zero(a0,a1,a2))
        else:
            raise KeyError(f'Filter needs values for a0, a1, a2 got a0: {a0}, a1: {a1}, a2: {a2}')


cpdef cython.double two_zero(mus_any gen, cython.double insig):
    """
    two zero filter of input. 
    
    :param gen: two_zero gen
    :param insig: input 
    :rtype: float  
    """
    return cclm.mus_two_zero(gen._ptr, insig)
    
cpdef bint is_two_zero(mus_any gen):
    """
    returns True if gen is a two_zero.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_two_zero(gen._ptr)
    



# ---------------- formant ---------------- #
cpdef mus_any make_formant(cython.double frequency, cython.double radius):
    """
    return a new formant generator (a resonator). radius sets the pole radius (in terms of the 'unit circle').
    frequency sets the resonance center frequency (hz).
    
    :param frequency: resonance center frequency \in Hz
    :param radius: resonance width, refers to the unit circle, so it should be between 0.0 and (less than) 1.0. 
    :return: formant gen
    :rtype: mus_any
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
        
    return mus_any.from_ptr(cclm.mus_make_formant(frequency, radius))

cpdef cython.double formant(mus_any gen, cython.double insig, cython.double radians=0.0):
    """
    next sample from formant generator.
    
    :param gen: formant gen
    :param insig: input value
    :param radians: frequency \in radians
    :rtype: float
    
    """
    if radians == 0.0:
        return cclm.mus_formant(gen._ptr, insig)
    else:
        return cclm.mus_formant_with_frequency(gen._ptr, insig, radians)

    
cpdef bint is_formant(mus_any gen):
    """
    returns True if gen is a formant.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_formant(gen._ptr)

# ---------------- formant-bank ---------------- #   
cpdef mus_any make_formant_bank(list filters, amps=None):
    """
    return a new formant-bank generator.
    
    :param filters: list of filter gens
    :param amps: list of amps to apply to filters
    :return: formant_bank gen
    :rtype: mus_any
    """
    
    p = list(map(is_formant, filters))
    
    if not all(p):
        raise TypeError(f'filter list contains at least one element that is not a formant.')
        
    cdef double [:] amps_view = None
    
    filt_array = mus_any_array.from_pylist(filters)
    
    if amps is not None:
        if isinstance(amps, list):
            amps = np.array(amps)
        amps_view = amps
        gen = mus_any.from_ptr(cclm.mus_make_formant_bank(len(filters),filt_array.data, &amps_view[0]))
    else: 
        gen = mus_any.from_ptr(cclm.mus_make_formant_bank(len(filters),filt_array.data, NULL))    
    gen.cache_extend([filt_array, amps, filters])
    return gen


cpdef cython.double formant_bank(mus_any gen, inputs):
    """
    sum a bank of formant generators.
    
    :param gen: formant_bank gen
    :param inputs: can be a list/array of inputs or a single input
    :rtype: float
    
    """
    
    cdef double [:] inputs_view = None
    
    if isinstance(inputs, np.ndarray): 
        inputs_view = inputs
        res = cclm.mus_formant_bank_with_inputs(gen._ptr, &inputs_view[0])
        return res
    else:
        res = cclm.mus_formant_bank(gen._ptr, inputs)
    return res
     
cpdef bint is_formant_bank(mus_any gen):
    """
    returns True if gen is a formant_bank.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_formant_bank(gen._ptr)

# ---------------- firmant ---------------- #
cpdef mus_any make_firmant(cython.double frequency, cython.double radius):
    """
    return a new firmant generator (a resonator).  radius sets the pole radius (in terms of the 'unit
    circle'). frequency sets the resonance center frequency (hz).
    
    :param frequency: resonance center frequency \in Hz
    :param radius: resonance width, refers to the unit circle, so it should be between 0.0 and (less than) 1.0. 
    :return: formant gen
    :rtype: mus_any       
    """
    check_range('frequency', frequency, 0.0, get_srate() / 2)
    
    return mus_any.from_ptr(cclm.mus_make_firmant(frequency, radius))

cpdef firmant(mus_any gen, cython.double insig, cython.double radians=0.0 ):
    """
    next sample from resonator generator.
    
    next sample from firmant generator.
    :param gen: firmant gen
    :param insig: input value
    :param radians: frequency \in radians
    :rtype: float
    """
    if radians == 0.0:
        return cclm.mus_firmant(gen._ptr, insig)
    else:
        return cclm.mus_firmant_with_frequency(gen._ptr, insig, radians)
   
            
cpdef is_firmant(mus_any gen):
    """
    returns True if gen is a firmant.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_firmant(gen._ptr)

# ---------------- filter ---------------- #
cpdef mus_any make_filter(cython.int order, xcoeffs, ycoeffs):   
    """
    return a new direct form fir/iir filter, coeff args are list/ndarray.
    
    :param order: filter order
    :param xcoeffs: x coeffs
    :param ycoeffs: y coeffs
    :return: filter gen
    :rtype: mus_any
    """

    xcoeffs_cpy = np.array(xcoeffs, dtype=np.double)        
    ycoeffs_cpy = np.array(ycoeffs, dtype=np.double)        
       
    cdef double [:] xcoeffs_view = xcoeffs_cpy
    cdef double [:] ycoeffs_view = ycoeffs_cpy

    gen =  mus_any.from_ptr(cclm.mus_make_filter(order, &xcoeffs_view[0], &ycoeffs_view[0], NULL))
    
    gen.cache_extend([xcoeffs_cpy, ycoeffs_cpy])
    return gen
    
cpdef cython.double filter(mus_any gen, cython.double insig): # todo : conflicts with buitl in function
    """
    next sample from filter.
    
    :param gen: filter gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_filter(gen._ptr, insig)
    
cpdef bint is_filter(mus_any gen ):
    """
    returns True if gen is a filter.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_filter(gen._ptr)

# ---------------- fir-filter ---------------- #
cpdef mus_any make_fir_filter(cython.int order, xcoeffs):
    """
    return a new fir filter, xcoeffs a list/ndarray.
    
    :param order: filter order
    :param xcoeffs: x coeffs
    :return: fir_filter gen
    :rtype: mus_any
    """
    cdef double [:] xcoeffs_view = None

    if isinstance(xcoeffs, list):
        xcoeffs = np.array(xcoeffs, dtype=np.double)        
    
    xcoeffs_view = xcoeffs   

    gen =  mus_any.from_ptr(cclm.mus_make_fir_filter(order, &xcoeffs_view[0], NULL))
    gen.cache_append(xcoeffs)
    
    return gen
    
cpdef cython.double fir_filter(mus_any gen, cython.double insig):
    """
    next sample from fir filter.
    
    :param gen: fir_filter gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_fir_filter(gen._ptr, insig)
    
cpdef bint is_fir_filter(mus_any gen):
    """
    returns True if gen is a fir_filter.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_fir_filter(gen._ptr)


# ---------------- iir-filter ---------------- #
cpdef mus_any make_iir_filter(cython.int order, ycoeffs):
    """
    return a new iir filter, ycoeffs a list/ndarray.
    
    :param order: filter order
    :param ycoeffs: y coeffs
    :return: iir_filter gen
    :rtype: mus_any
    """
    cdef double [:] ycoeffs_view = None

    if isinstance(ycoeffs, list):
        ycoeffs = np.array(ycoeffs, dtype=np.double)        
    
    ycoeffs_view = ycoeffs   
    
        
    gen = mus_any.from_ptr(cclm.mus_make_iir_filter(order, &ycoeffs_view[0], NULL))
    gen.cache_append(ycoeffs)
    return gen
    
cpdef cython.double iir_filter(mus_any gen, cython.double insig ):
    """
    next sample from iir filter.
    
    :param gen: iir_filter gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_iir_filter(gen._ptr, insig)
    
cpdef bint is_iir_filter(mus_any gen):
    """
    returns True if gen is a iir_filter
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_iir_filter(gen._ptr)

cpdef np.ndarray make_fir_coeffs(cython.int order, envelope):
    """
    translates a frequency response envelope (actually, evenly spaced points \in a float-vector) into
    the corresponding FIR filter coefficients. The order of the filter determines how close you get to the
    envelope.
    
    :param order: order of the filter
    :param envelope: response envelope
    """
    cdef double [:] envelope_view = None
        
    if isinstance(envelope, list):
        envelope = np.ndarray(envelope)

    check_ndim(envelope)
    
    envelope_view = envelope
    
    coeffs = np.zeros(order+1, dtype=np.double)
    
    cdef double [:] coeffs_view = coeffs
    
    cclm.mus_make_fir_coeffs(order, &envelope_view[0], &coeffs_view[0])
    return coeffs


# ---------------- delay ---------------- #
cpdef mus_any make_delay(cython.long size, initial_contents=None, initial_element=None, max_size=None, Interp interp_type=Interp.NONE):
    """
    return a new delay line of size elements. if the delay length will be changing at run-time,
    max-size sets its maximum length.
    
    :param size: delay length \in samples
    :param initial_contents: delay line's initial values
    :param initial_element: delay line's initial element
    :param max_size: maximum delay size \in case the delay changes
    :param type: interpolation type
    :return: delay gen
    :rtype: mus_any
    """
    
    check_range('size', size, 0, None)

    cdef double [:] initial_contents_view = None
    
    if not max_size:
        max_size = size
        
    if max_size != size and interp_type == Interp.NONE:
        interp_type = Interp.LAGRANGE #think this is correct from clm2xen.c
        
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        check_ndim(initial_contents)
        initial_contents_view = initial_contents

    elif initial_element:
        initial_contents = np.zeros(max_size, dtype=np.double)
        check_ndim(initial_contents)
        initial_contents.fill(initial_element)
        initial_contents_view = initial_contents

    if initial_contents_view is not None:
        gen = mus_any.from_ptr(cclm.mus_make_delay(size, &initial_contents_view[0], max_size, <cclm.mus_interp_t>interp_type))
    else:   
        gen = mus_any.from_ptr(cclm.mus_make_delay(size, NULL, max_size, <cclm.mus_interp_t>interp_type))
    
    gen.cache_append(initial_contents)
    return gen
    
cpdef cython.double delay(mus_any gen, cython.double insig, cython.double pm=0.0):
    """
    delay val according to the delay line's length and pm ('phase-modulation').
    if pm is greater than 0.0, the max-size argument used to create gen should have accommodated 
    its maximum value. 
    
    :param gen: delay gen
    :param insig: input value
    :param pm: change \in delay length size. can be + or -
    :rtype: float

    """ 
    return cclm.mus_delay(gen._ptr, insig, pm)

        
cpdef cython.double delay_unmodulated(mus_any gen, cython.double insig):
    """
    delay val according to the delay line's length and pm ('phase-modulation').
    if pm is greater than 0.0, the max-size argument used to create gen should have accommodated 
    its maximum value. 
    
    :param gen: delay gen
    :param insig: input value
    :rtype: float

    """
    return cclm.mus_delay_unmodulated(gen._ptr, insig)
        
cpdef bint is_delay(mus_any gen):
    """
    returns True if gen is a delay.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_delay(gen._ptr)

cpdef cython.double tap(mus_any gen, offset=0.):
    """
    tap the delay mus_any offset by pm
    
    :param gen: delay gen
    :param offset: offset in samples from output point
    :rtype: float
    
    """

    return cclm.mus_tap(gen._ptr, offset)

cpdef cython.double tap_unmodulated(mus_any gen):
    """
    tap the delay mus_any offset by pm
    
    :param gen: delay gen
    :param offset: offset in samples from output point
    :rtype: float
    
    """
    return cclm.mus_tap_unmodulated(gen._ptr)
    
cpdef bint is_tap(mus_any gen):
    """
    returns True if gen is a tap.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_tap(gen._ptr)
    
cpdef cython.double delay_tick(mus_any gen, cython.double insig ):
    """
    delay val according to the delay line's length. this merely 'ticks' the delay line forward.
    the argument 'insi' is returned.
    
    :param gen: delay gen
    :rtype: float
    """
    return cclm.mus_delay_tick(gen._ptr, insig)


# ---------------- comb ---------------- #
cpdef mus_any make_comb(cython.double feedback=1.0,size=None, initial_contents=None, initial_element=None, max_size=None, Interp interp_type=Interp.NONE):
    """
    return a new comb filter (a delay line with a scaler on the feedback) of size elements. if the comb
    length will be changing at run-time, max-size sets its maximum length.       
    
    :param feedback: scaler on feedback
    :param size: delay length \in samples
    :param initial_contents: delay line's initial values
    :param initial_element: delay line's initial element
    :param max_size: maximum delay size \in case the delay changes
    :param type: interpolation type
    :return: comb gen
    :rtype: mus_any
        
    """                
    
    check_range('size', size, 0.0, None)
    
    cdef double [:] initial_contents_view = None
    
    if not max_size:
        max_size = size
        
    if max_size != size and interp_type == Interp.NONE:
        interp_type = Interp.BEZIER #think this is correct from clm2xen.c
    
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        check_ndim(initial_contents)
        initial_contents_view = initial_contents

    elif initial_element:
        initial_contents = np.zeros(max_size)
        check_ndim(initial_contents)
        initial_contents.fill(initial_element)
        initial_contents_view = initial_contents
        
    if initial_contents_view is not None:
        gen = mus_any.from_ptr(cclm.mus_make_comb(feedback, size, &initial_contents_view[0], max_size, <cclm.mus_interp_t>interp_type))
    else:
        gen = mus_any.from_ptr(cclm.mus_make_comb(feedback, size, NULL, max_size,  <cclm.mus_interp_t>interp_type))
    gen.cache_append(initial_contents)
    return gen    
           
cpdef cython.double comb(mus_any gen, cython.double insig, pm=None):
    """
    comb filter val, pm changes the delay length.
    
    :param gen: comb gen
    :param insig: input value
    :param pm: change \in delay length size. can be + or -
    :rtype: float
    """
    if pm:
        return cclm.mus_comb(gen._ptr, insig, pm)
    else:
        return cclm.mus_comb_unmodulated(gen._ptr, insig)
    
cpdef bint is_comb(mus_any gen):
    """
    returns True if gen is a comb.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_comb(gen._ptr)    

# ---------------- comb-bank ---------------- #
cpdef mus_any make_comb_bank(list combs):
    """
    return a new comb-bank generator.
    
    :param combs: list of comb gens
    :return: comb_bank gen
    :rtype: mus_any
    
    """
    
    p = list(map(is_comb, combs))
    if not all(p):
        raise TypeError(f'filter list contains at least one element that is not a formant.')

    comb_array = mus_any_array.from_pylist(combs)
    
    gen = mus_any.from_ptr(cclm.mus_make_comb_bank(len(combs), comb_array.data))
    gen.cache_extend([comb_array, combs])
    return gen

cpdef cython.double comb_bank(mus_any gen, cython.double insig):
    """
    sum an array of comb filters.
    
    :param gen: comb_bank gen
    :param inputs: can be a list/array of inputs or a single input
    :rtype: float
    """
    return cclm.mus_comb_bank(gen._ptr, insig)
    
cpdef bint is_comb_bank(mus_any gen):
    """
    returns True if gen is a comb_bank
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_comb_bank(gen._ptr)


# ---------------- filtered-comb ---------------- #
cpdef mus_any make_filtered_comb(cython.double feedback,cython.long size, mus_any filter, initial_contents=None,  cython.double initial_element=0.0, max_size=None, Interp interp_type=Interp.NONE):
                
    """
    return a new filtered comb filter (a delay line with a scaler and a filter on the feedback) of size
    elements. if the comb length will be changing at run-time, max-size sets its maximum length.     
    
    :param feedback: scaler on feedback
    :param size: delay length \in samples
    :param filter: filter to apply 
    :param initial_contents: delay line's initial values
    :param initial_element: delay line's initial element
    :param max_size: maximum delay size \in case the delay changes
    :param type: interpolation type
    :return: filtered_comb gen
    :rtype: mus_any
    """
    check_range('size', size, 0.0, None)
    
    cdef double [:] initial_contents_view = None
    
    if not max_size:
        max_size = size
        
    if max_size != size and interp_type == Interp.NONE:
        interp_type = Interp.BEZIER #think this is correct from clm2xen.c
    
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        initial_contents_view = initial_contents

    elif initial_element:
        initial_contents = np.zeros(max_size)
        check_ndim(initial_contents)
        initial_contents.fill(initial_element)
        initial_contents_view = initial_contents
    
    if initial_contents_view is not None:
        gen = mus_any.from_ptr(cclm.mus_make_filtered_comb(feedback, int(size), &initial_contents_view[0], int(max_size), <cclm.mus_interp_t>interp_type, filter._ptr))
    else:
        gen = mus_any.from_ptr(cclm.mus_make_filtered_comb(feedback, int(size), NULL, int(max_size), <cclm.mus_interp_t>interp_type, filter._ptr))
    gen.cache_extend([initial_contents, filter])
    return gen    
        
cpdef cython.double filtered_comb(mus_any gen, cython.double insig, cython.double pm=0.0):
    """
    filtered comb filter val, pm changes the delay length.
    
    :param gen: filtered_comb gen
    :param insig: input value
    :param pm: change \in delay length size. can be + or -
    :rtype: float
    """
    return cclm.mus_filtered_comb(gen._ptr, insig, pm)

        
cpdef cython.double filtered_comb_unmodulated(mus_any gen, cython.double insig):
    """
    filtered comb filter val, pm changes the delay length. unmodulated
    
    :param gen: filtered_comb gen
    :param insig: input value
    :param pm: change \in delay length size. can be + or -
    :rtype: float
    """
    return cclm.mus_filtered_comb_unmodulated(gen._ptr, insig)
        
cpdef bint is_filtered_comb(mus_any gen):
    """
    returns True if gen is a filtered_comb.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_filtered_comb(gen._ptr)
    
# ---------------- filtered-comb-bank ---------------- #      
cpdef mus_any make_filtered_comb_bank(list fcombs):
    """
    return a new filtered_comb-bank generator.
    
    :param fcombs: list of filtered_comb gens
    :return: filtered_comb_bank gen
    :rtype: mus_any
    """
    p = list(map(is_filtered_comb, fcombs))
    if not all(p):
        raise TypeError(f'filter list contains at least one element that is not a filtered_comb.')

    fcomb_array = mus_any_array.from_pylist(fcombs)
    
    gen =  mus_any.from_ptr(cclm.mus_make_filtered_comb_bank(len(fcombs), fcomb_array.data))
    gen.cache_extend([fcomb_array, fcombs])
    return gen

cpdef cython.double filtered_comb_bank(mus_any gen, cython.double insig):
    """
    sum an array of filtered_comb filters.
    
    :param gen: filtered_comb gen
    :param inputs: can be a list/array of inputs or a single input
    :rtype: float
    """
    return cclm.mus_filtered_comb_bank(gen._ptr, insig)
    
cpdef bint is_filtered_comb_bank(mus_any gen):
    """
    returns True if gen is a filtered_comb_bank.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_filtered_comb_bank(gen._ptr)

# ---------------- notch ---------------- #
cpdef mus_any make_notch(cython.double feedforward=1.0,size=None, 
                initial_contents=None, 
                cython.double initial_element=0.0, 
                max_size=None,
                Interp interp_type=Interp.NONE):

    """
    return a new notch filter (a delay line with a scaler on the feedforward) of size elements.
    if the notch length will be changing at run-time, max-size sets its maximum length.
    
    :param feedforward: scaler on input
    :param size: delay length \in samples
    :param initial_contents: delay line's initial values
    :param initial_element: delay line's initial element
    :param max_size: maximum delay size \in case the delay changes
    :param type: interpolation type
    :return: comb gen
    :rtype: mus_any
    """
    
    check_range('size', size, 0.0, None)
    
    cdef double [:] initial_contents_view = None
    
    if not max_size:
        max_size = size
        
    if max_size != size and interp_type == Interp.NONE:
        interp_type = Interp.BEZIER #think this is correct from clm2xen.c
     
    
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        check_ndim(initial_contents)
        initial_contents_view = initial_contents
        
    elif initial_element:
        initial_contents = np.zeros(max_size, dtype=np.double)
        check_ndim(initial_contents)
        initial_contents.fill(initial_element)
        initial_contents_view = initial_contents
    
    if initial_contents_view is not None:
        gen = mus_any.from_ptr(cclm.mus_make_notch(feedforward, size, &initial_contents_view[0], max_size, <cclm.mus_interp_t>interp_type))
    else:
        gen = mus_any.from_ptr(cclm.mus_make_notch(feedforward, size, NULL, max_size, <cclm.mus_interp_t>interp_type))
    gen.cache_append(initial_contents)
    return gen    

cpdef cython.double notch(mus_any gen, cython.double insig, cython.double pm=0.0):
    """
    notch filter val, pm changes the delay length.
        
    :param gen: notch gen
    :param insig: input value
    :param pm: change \in delay length size. can be + or -
    :rtype: float
    """
    return cclm.mus_notch(gen._ptr, insig, pm)

   
cpdef cython.double notch_unmodulated(mus_any gen, cython.double insig):
    """
    notch filter val, pm changes the delay length. unmodulated
        
    :param gen: notch gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_notch_unmodulated(gen._ptr, insig)
        
         
cpdef bint is_notch(mus_any gen):
    """
    returns True if gen is a notch.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_notch(gen._ptr)
 
# ---------------- all-pass ---------------- #
cpdef mus_any make_all_pass(cython.double feedback, cython.double  feedforward, cython.long  size, initial_contents= None, cython.double  initial_element = 0.0,  max_size= None, Interp interp_type = Interp.NONE):

    """
    return a new allpass filter (a delay line with a scalers on both the feedback and the feedforward).
    if length will be changing at run-time, max-size sets its maximum length.
    
    :param feedback: scaler on feedback
    :param feedforward: scaler on input
    :param size: length \in samples of the delay line
    :param initial_contents: delay line's initial values
    :param initial_element: delay line's initial element
    :param max_size: maximum delay size \in case the delay changes
    :param interp_type: interpolation type
    :return: a new allpass filter
    :rtype: mus_any
     
    """

    check_range('size', size, 0.0, None)
    
    cdef double [:] initial_contents_view = None
    
    if not max_size:
        max_size = size
        
    if max_size != size and interp_type == Interp.NONE:
        interp_type = Interp.HERMITE #think this is correct from clm2xen.c
     
    
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        check_ndim(initial_contents)
        initial_contents_view = initial_contents

    elif initial_element:
        initial_contents = np.zeros(max_size, dtype=np.double)
        check_ndim(initial_contents)
        initial_contents.fill(initial_element)
        initial_contents_view = initial_contents
            
    if initial_contents_view is not None:
        gen = mus_any.from_ptr(cclm.mus_make_all_pass(feedback,feedforward, size, &initial_contents_view[0], max_size, <cclm.mus_interp_t>interp_type))
    else:
        gen = mus_any.from_ptr(cclm.mus_make_all_pass(feedback,feedforward, size,NULL, max_size,  <cclm.mus_interp_t>interp_type))
    gen.cache_append(initial_contents)
    return gen
    
cpdef cython.double all_pass(mus_any gen, cython.double insig, pm=None):
    """
    all-pass filter insig value, pm changes the delay length.
    
    :param gen: all_pass gen
    :param insig: input value
    :param pm: change \in delay length size. can be + or -
    :rtype: float
    """
    if pm:
        return cclm.mus_all_pass(gen._ptr, insig, pm)
    else:
        return cclm.mus_all_pass_unmodulated(gen._ptr, insig)
    
cpdef is_all_pass(mus_any gen):
    """
    returns True if gen is a all_pass.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_all_pass(gen._ptr)
    

# ---------------- all-pass-bank ---------------- #
cpdef mus_any make_all_pass_bank(all_passes: list):
    """
    return a new all_pass-bank generator.
    
    :param all_passes: list of all_pass gens
    :return: all_pass_bank gen
    :rtype: mus_any
    """
    p = list(map(is_all_pass, all_passes))
    if not all(p):
        raise TypeError(f'allpass list contains at least one element that is not a all_pass.')
        
    all_passes_array = mus_any_array.from_pylist(all_passes)
    gen =  mus_any.from_ptr(cclm.mus_make_all_pass_bank(len(all_passes), all_passes_array.data))
    gen.cache_extend([all_passes_array, all_passes])
    return gen

cpdef cython.double all_pass_bank(mus_any gen, cython.double insig):
    """
    sum an array of all_pass filters.
    
    :param gen: all_pass_bank gen
    :param inputs: can be a list/array of inputs or a single input
    :rtype: float
    """
    return cclm.mus_all_pass_bank(gen._ptr, insig)
    
cpdef bint is_all_pass_bank(mus_any gen):
    """
    returns True if gen is a all_pass_bank.
    
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_all_pass_bank(gen._ptr)
    
    
# ---------------- one_pole_all_pass ---------------- #
cpdef mus_any make_one_pole_all_pass(cython.long size, cython.double coeff):
    """
    return a new one_pole all_pass filter size, coeff.
    
    
    :param size: length \in samples of the delay line
    :param coeff: coeff of one pole filter
    :return: one_pole_all_pass gen
    :rtype: mus_any
    """
    return mus_any.from_ptr(cclm.mus_make_one_pole_all_pass(size, coeff))
    
cpdef cython.double one_pole_all_pass(mus_any gen, cython.double insig):
    """
    one pole all pass filter of input.
    
    :param gen: one_pole_all_pass gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_one_pole_all_pass(gen._ptr, insig)
    
cpdef bint is_one_pole_all_pass(mus_any gen):
    """
    returns True if gen is a one_pole_all_pass.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_one_pole_all_pass(gen._ptr)
        
# ---------------- moving-average ---------------- #
cpdef mus_any make_moving_average(cython.long size, initial_contents=None, cython.double initial_element=0.0):
    """
    return a new moving_average generator. 
    
    :param size: averaging length \in samples
    :param initial_contents: initial values
    :param initial_element: initial element
    :return: moving_average gen
    :rtype: mus_any
    """
    
    check_range('size', size, 0.0, None)
    
    cdef double [:] initial_contents_view = None
    
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        check_ndim(initial_contents)
        initial_contents_view = initial_contents
    else:
        initial_contents = np.zeros(size, dtype=np.double)
        check_ndim(initial_contents)
        initial_contents.fill(initial_element)
        initial_contents_view = initial_contents
    
    if initial_contents_view is not None:    
        gen = mus_any.from_ptr(cclm.mus_make_moving_average(size, &initial_contents_view[0]))

    gen.cache_append(initial_contents)
    return gen
        
        
cpdef cython.double moving_average(mus_any gen, cython.double  insig):
    """
    moving window average.
    
    :param gen: moving_average gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_moving_average(gen._ptr, insig)
    
cpdef bint is_moving_average(mus_any gen):
    """
    returns True if gen is a moving_average.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_moving_average(gen._ptr)

# ---------------- moving-max ---------------- #
cpdef mus_any make_moving_max(cython.long size, 
                initial_contents=None, 
                cython.double initial_element=0.0):
                
    """
    return a new moving-max generator.
    
    :param size: max window length \in samples
    :param initial_contents: initial values
    :param initial_element: initial element
    :return: moving_max gen
    :rtype: mus_any
    """                
    
    check_range('size', size, 0.0, None)
    
    cdef double [:] initial_contents_view = None
    
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        check_ndim(initial_contents)
        initial_contents_view = initial_contents

    elif initial_element:
        initial_contents = np.zeros(size, dtype=np.double)
        check_ndim(initial_contents)
        initial_contents.fill(initial_element)
        initial_contents_view = initial_contents
    if initial_contents_view is not None:
        gen = mus_any.from_ptr(cclm.mus_make_moving_max(size, &initial_contents_view[0]))
        gen.cache_append(initial_contents)
    else:
        gen = mus_any.from_ptr(cclm.mus_make_moving_max(size, NULL))
    return gen
    
cpdef cython.double moving_max(mus_any gen, cython.double insig):
    """
    moving window max.
    
    :param gen: moving_max gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_moving_max(gen._ptr, insig)
    
cpdef bint is_moving_max(mus_any gen):
    """
    returns True if gen is a moving_max.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_moving_max(gen._ptr)
    
# ---------------- moving-norm ---------------- #
cpdef mus_any make_moving_norm(cython.long size, initial_contents=None, cython.double scaler=1.):
    """
    return a new moving-norm generator.
    
    :param size: averaging length \in samples
    :param initial_contents: initial values
    :param scaler: normalzing value
    :return: moving_norm gen
    :rtype: mus_any
    """
    
    check_range('size', size, 0.0, None)
    
    cdef double [:] initial_contents_view = None
    
        
    if initial_contents is not None:
        if isinstance(initial_contents, list):
            initial_contents = np.array(initial_contents)
        check_ndim(initial_contents)
        initial_contents_view = initial_contents
        
    if initial_contents_view is not None:
        gen = mus_any.from_ptr(cclm.mus_make_moving_norm(size, &initial_contents_view[0], scaler))
        gen.cache_append(initial_contents)
    else:
        gen = mus_any.from_ptr(cclm.mus_make_moving_norm(size, NULL, scaler))
    
    return gen
    
cpdef cython.double moving_norm(mus_any gen, cython.double insig):
    """
    moving window norm.
    
    :param gen: moving_norm gen
    :param insig: input value
    :rtype: float
    """
    return cclm.mus_moving_norm(gen._ptr, insig)
    
cpdef is_moving_norm(mus_any gen ):
    """
    returns True if gen is a moving_norm.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_moving_norm(gen._ptr)
    
    
# ---------------- asymmetric-fm ---------------- #
cpdef mus_any make_asymmetric_fm(cython.double frequency, cython.double initial_phase=0.0, cython.double r=1.0, cython.double ratio=1.):
    """
    return a new asymmetric_fm generator.
    
    :param frequency: frequency of gen
    :param initial_phase: starting phase of gen, \in radians
    :param r: amplitude ratio between successive sidebands
    :param ratio: ratio between carrier and sideband spacing
    :return: asymmetric_fm gen
    :rtype: mus_any
    """
    
    check_range('frequency', frequency, 0.0, None)
    
    return mus_any.from_ptr(cclm.mus_make_asymmetric_fm(frequency, initial_phase, r, ratio))
    
cpdef cython.double asymmetric_fm(mus_any gen, cython.double index, cython.double fm=0.0):
    """
    next sample from asymmetric fm generator.  
       
    :param gen: asymmetric_fm gen
    :param index: fm index
    :param fm: fm input
    :rtype: float
    """
    return cclm.mus_asymmetric_fm(gen._ptr, index, fm)

        
cpdef cython.double asymmetric_fm_unmodulated(mus_any gen, cython.double index):
    """
    next sample from asymmetric fm generator.  
       
    :param gen: asymmetric_fm gen
    :param index: fm index
    :rtype: float
    """ 
    return cclm.mus_asymmetric_fm_unmodulated(gen._ptr, index)
    
cpdef bint is_asymmetric_fm(mus_any gen):
    """
    returns True if gen is a asymmetric_fm.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_asymmetric_fm(gen._ptr)
    
# ---------------- file-to-sample ---------------- #
cpdef mus_any make_file2sample(str filename, buffer_size=None):
    """
    return an input generator reading 'filename' (a sound file).
    
    :param filename: name of file to read
    :param buffer_size: io buffer size
    :return: file2sample gen
    :rtype: mus_any
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f'file2sample: {filename} does not exist.')
        
    buffer_size = buffer_size or default.buffer_size
    return mus_any.from_ptr(cclm.mus_make_file_to_sample_with_buffer_size(filename, buffer_size))
    
cpdef cython.double file2sample(mus_any gen, cython.long loc, cython.int chan=0):
    """
    sample value \in sound file read by 'obj' \in channel chan at sample.
    
    :param gen: file2sample gen
    :param loc: location \in file to read
    :param chan: channel to read
    :rtype: float
    """
    return cclm.mus_file_to_sample(gen._ptr, loc, chan)
    
cpdef bint is_file2sample(mus_any gen):
    """
    returns True if gen is a file2sample.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_file_to_sample(gen._ptr)
    
# ---------------- sample-to-file ---------------- #
cpdef mus_any make_sample2file(str filename, cython.int chans=1, sample_type=None, header_type=None, comment=None):
    """
    return an output generator writing the sound file 'filename' which is set up to have chans'
    channels of 'sample_type' samples with a header of 'header_type'.  the latter should be sndlib
    identifiers.
    
    :param filename: name of file to write
    :param chans: number of channels
    :param sample_type: sample type of file
    :param header_type: header type of file
    :return: sample2file gen
    :rtype: mus_any
    """
    sample_type = sample_type or default.sample_type
    header_type = header_type or default.header_type
    if comment is None:
        return mus_any.from_ptr(cclm.mus_make_sample_to_file_with_comment(filename, chans, <csndlib.mus_sample_t>sample_type, <csndlib.mus_header_t>header_type, NULL))
    else:
        return mus_any.from_ptr(cclm.mus_make_sample_to_file_with_comment(filename, chans, <csndlib.mus_sample_t>sample_type, <csndlib.mus_header_t>header_type, comment))

cpdef cython.double sample2file(mus_any gen, cython.long samp, cython.int chan ,  cython.double val):
    """
    add val to the output stream handled by the output generator 'obj', \in channel 'chan' at frample 'samp'.
    
    :param gen: sample2file gem
    :param samp: location \in file to write
    :param chan: channel to write
    :param val: sample value to write
    :rtype: float
    """
    return cclm.mus_sample_to_file(gen._ptr, samp, chan, val)
    
cpdef bint is_sample2file(mus_any gen): 
    """
    returns True if gen is a sample2file.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_sample_to_file(gen._ptr)
    
cpdef mus_any continue_sample2file(name: str):
    """
    reopen an existing file to continue adding sound data to it.
    
    :param filename: name of file to write
    :return: file2sample gen
    :rtype: mus_any
    """
    return mus_any.from_ptr(cclm.mus_continue_sample_to_file(name))
    
    
# ---------------- file-to-frample ---------------- #
cpdef mus_any make_file2frample(str filename, buffer_size=None):
    """
    return an input generator reading all channels of 'filename' (a sound file).
    
    :param filename: name of file to read
    :param buffer_size: io buffer size
    :return: file2frample gen
    :rtype: mus_any
    """
    buffer_size = buffer_size or default.buffer_size
    if not os.path.isfile(filename):
        raise FileNotFoundError(f'file2frample: {filename} does not exist.')
    return  mus_any.from_ptr(cclm.mus_make_file_to_frample_with_buffer_size(filename, buffer_size))
    
cpdef file2frample(mus_any gen, cython.long loc):
    """
    frample of samples at frample 'samp' \in sound file read by 'obj'.
    
    :param gen: file2frample gen
    :param loc: location \in file to read
    :rtype: np.ndarray
    """
    outf = np.zeros(cclm.mus_channels(gen._ptr), dtype=np.double)
    cdef double [:] outf_view = outf
    cclm.mus_file_to_frample(gen._ptr, loc, &outf_view[0])
    return outf
    
cpdef is_file2frample(mus_any gen):
    """
    returns True if gen is a file2frample.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_file_to_frample(gen._ptr)
    
    
# ---------------- frample-to-file ---------------- #
cpdef mus_any make_frample2file(str filename, cython.int chans=1, sample_type=None, header_type=None, comment=None):
    """
    return an output generator writing the sound file 'filename' which is set up to have 'chans'
    channels of 'sample_type' samples with a header of 'header_type'.  the latter should be sndlib
    identifiers.    
    
    :param filename: name of file to write
    :param chans: number of channels
    :param frample2file: sample type of file
    :param header_type: header type of file
    :return: sample2file gen
    :rtype: mus_any    
    """
    sample_type = sample_type or default.sample_type
    header_type = header_type or default.header_type
    if comment:
        return mus_any.from_ptr(cclm.mus_make_frample_to_file_with_comment(filename, chans, <csndlib.mus_sample_t>sample_type, <csndlib.mus_header_t>header_type, comment))
    else:
        return mus_any.from_ptr(cclm.mus_make_frample_to_file_with_comment(filename, chans, <csndlib.mus_sample_t>sample_type, <csndlib.mus_header_t>header_type, NULL))

cpdef cython.double frample2file(mus_any gen, cython.long samp, vals):
    """
    add frample 'val' to the output stream handled by the output generator 'obj' at frample 'samp'.
    
    :param gen: frample2file gem
    :param samp: location \in file to write
    :param vals: sample value to write. list or np.ndarray
    :rtype: float
    """
    cdef double [:] val_view = None
    
    if isinstance(vals, list):
        vals = np.array(vals)
        
    val_view = vals
    
    frample = val_view
    cclm.mus_frample_to_file(gen._ptr, samp, &frample[0])
    return vals
    
cpdef bint is_frample2file(mus_any gen):
    """
    returns True if gen is a frample2file.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_frample_to_file(gen._ptr)
    

cpdef mus_any continue_frample2file(str name):
    """
    reopen an existing file to continue adding sound data to it.
    
    :param filename: name of file to write
    :return: frample2file gen
    :rtype: mus_any
    """
    return mus_any.from_ptr(cclm.mus_continue_frample_to_file(name))


# ---------------- readin ---------------- #
cpdef mus_any make_readin(str filename, cython.int chan=0, cython.long start=0, cython.int direction=1, buffer_size=None):
    """
    return a new readin (file input) generator reading the sound file 'file' starting at frample
    'start' \in channel 'channel' and reading forward if 'direction' is not -1.
    
    :param filename: name of file to read
    :param chan: channel to read (0 based)
    :param start: location \in samples to start at
    :param direction: forward (1) or backward (-1)
    :param buffer_size: io buffer size
    
    """
    check_range('chan', chan, 0, None)
    check_range('start', start, 0, None)
    check_range('buffer_size', buffer_size, 0, None)

    if not os.path.isfile(filename):
        raise FileNotFoundError(f'readin: {filename} does not exist.')
    
    buffer_size = buffer_size or default.buffer_size
    return mus_any.from_ptr(cclm.mus_make_readin_with_buffer_size(filename, chan, start, direction, buffer_size))
    
cpdef cython.double readin(mus_any gen):
    """
    next sample from readin generator (a sound file reader).
    
    :param gen: readin gen
    :rtype: float
    """
    return cclm.mus_readin(gen._ptr)
    
cpdef is_readin(mus_any gen):
    """
    returns True if gen is a readin.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_readin(gen._ptr)
      
          
# ---------------- src ---------------- #
def make_src(inp , cython.double srate=1.0, cython.int width=10):
    """
    return a new sampling-rate conversion generator (using 'warped sinc interpolation'). 'srate' is the
    ratio between the new rate and the old. 'width' is the sine width (effectively the steepness of the
    low-pass filter), normally between 10 and 100. 'input' if given is an open file stream.
    
    :param inp: gen or function to read from. if a callback, the function takes 1 input, the direction and should return read value
    :param srate: ratio between the old sampling rate and the new
    :param width: how many samples to convolve with sinc function
    :return: src gen
    :rtype: mus_any
    """
        
    check_range('srate', srate, 0, None)
    check_range('width', width, 0, None)       
        
    cdef cclm.input_cb cy_inp_f_ptr 
    
    if(isinstance(inp, mus_any)):
        res = mus_any.from_ptr(cclm.mus_make_src(<cclm.input_cb>input_callback_func, srate, width, <void*>((<mus_any>inp)._ptr)))
        res._inputcallback = <cclm.input_cb>input_callback_func
        res.cache_append(inp)
        return res
        
            
    if not callable(inp):
        raise TypeError(f"input needs to be a clm gen or function not a {type(inp)}")
    
    @_inputcallback
    def inp_f(gen, d):
        return inp(d)
        
    cy_inp_f_ptr = (<cclm.input_cb*><size_t>ctypes.addressof(inp_f))[0]
    res = mus_any.from_ptr(cclm.mus_make_src(<cclm.input_cb>cy_inp_f_ptr, srate, width, NULL))
    res._inputcallback = cy_inp_f_ptr
    res.cache_append(inp_f)
    
    return res
  
cpdef cython.double src(mus_any gen, cython.double sr_change=0.0):
    """
    next sampling rate conversion sample. 'pm' can be used to change the sampling rate on a
    sample-by-sample basis. 'input-function' is a function of one argument (the current input direction,
    normally ignored) that is called internally whenever a new sample of input data is needed.  if the
    associated make_src included an 'input' argument, input-function is ignored.
    
    :param gen: src gen
    :param sr_change: change \in ratio
    :rtype: float  
    """
    if gen._inputcallback:
        return cclm.mus_src(gen._ptr, sr_change, <cclm.input_cb>gen._inputcallback)
    else:
        return 0.0
    
cpdef bint is_src(mus_any gen):
    """
    returns True if gen is a src.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_src(gen._ptr)
 

# ---------------- convolve ---------------- #

def make_convolve(inp, filt, cython.long fft_size=512, filter_size=None):
    """
    return a new convolution generator which convolves its input with the impulse response 'filter'.
    
    :param inp: gen or function to read from
    :param filt: np.array of filter 
    :param fft_size: fft size used \in the convolution
    :param filter_size: how much of filter to use. if None use whole filter
    :return: convolve gen
    :rtype: mus_any
    """
    
    cdef cclm.input_cb cy_input_f_ptr 
    
    cdef double [:] filt_view
    

    if filter_size is None:
        filter_size = get_length(filt)
     
    fft_len = 0
    
    if fft_size < 0 or fft_size == 0:
        raise ValueError(f'fft_size must be a positive number greater than 0 not {fft_size}')
        
    if fft_size > csndlib.mus_max_malloc():
         raise ValueError(f'fft_size too large. cannot allocate {fft_size} size fft')
        
    if is_power_of_2(filter_size):
        fft_len = filter_size * 2
    else :
        fft_len = next_power_of_2(filter_size)
        
    if fft_size < fft_len:
        fft_size = fft_len
    
    if isinstance(filt, list):       
        filt = np.array(filt)
        
    check_ndim(filt)
    
    filt_view = filt
    
    if(isinstance(inp, mus_any)):
        res = mus_any.from_ptr(cclm.mus_make_convolve(<cclm.input_cb>input_callback_func, &filt_view[0], fft_size, filter_size, <void*>(<mus_any>inp)._ptr))
        res._inputcallback = <cclm.input_cb>input_callback_func
        res.cache_append(filt)     
        res.cache_append(inp)
        return res
    
    if not callable(inp):
        raise TypeError(f"input needs to be a clm gen or function not a {type(inp)}")

    #if isinstance(inp,types.FunctionType):
    @_inputcallback
    def inp_f(gen, d):
        return inp(d)
        
    cy_inp_f_ptr = (<cclm.input_cb*><size_t>ctypes.addressof(inp_f))[0]
    res = mus_any.from_ptr(cclm.mus_make_convolve(cy_inp_f_ptr, &filt_view[0], fft_size, filter_size, NULL))
    res._inputcallback = cy_inp_f_ptr
    res.cache_append(inp_f)

    return res

    
cpdef cython.double convolve(mus_any gen):
    """
    next sample from convolution generator.
    
    :param gen: convolve gen
    :rtype: float
    """
    return cclm.mus_convolve(gen._ptr, gen._inputcallback)  
    
cpdef bint is_convolve(mus_any gen):
    """
    returns True if gen is a convolve.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_convolve(gen._ptr)
    

# --------------- granulate ---------------- 
def make_granulate(inp, 
                    expansion: Optional[float]=1.0, 
                    length: Optional[float]=.15,
                    scaler: Optional[float]=.6,
                    hop: Optional[float]=.05,
                    ramp: Optional[float]=.4,
                    jitter: Optional[float]=0.0,
                    max_size: Optional[int]=0,
                    edit=None):
                    
    """
    return a new granular synthesis generator.  'length' is the grain length (seconds), 'expansion' is the
    ratio \in timing between the new and old (expansion > 1.0 slows things down), 'scaler' scales the grains
    to avoid overflows, 'hop' is the spacing (seconds) between successive grains upon output. 'jitter'
    controls the randomness \in that spacing, 'input' can be a file pointer. 'edit' can be a function of one
    arg, the current granulate generator.  it is called just before a grain is added into the output
    buffer. the current grain is accessible via mus_data. the edit function, if any, should return the
    length \in samples of the grain, or 0.
    
    :param inp: gen or function to read from. if a callback, the function takes 1 input, the direction and should return read value
    :param expansion: how much to lengthen or compress the file
    :param length: length of file slices that are overlapped
    :param scaler: amplitude scaler on slices (to avoid overflows)
    :param hop: speed at which slices are repeated \in output
    :param ramp: amount of slice-time spent ramping up/down
    :param jitter: affects spacing of successive grains
    :param max_size: internal buffer size
    :param edit: grain editing function. the function should take one argument, the granulate mus_any and return length of grain or 0

    """

    cdef cclm.input_cb cy_input_f_ptr
    cdef cclm.edit_cb cy_edit_f_ptr 

    if(isinstance(inp, mus_any) and edit is None):
        res = mus_any.from_ptr(cclm.mus_make_granulate(<cclm.input_cb>input_callback_func, expansion, length, scaler, hop, ramp, jitter, max_size, NULL, <void*>(<mus_any>inp)._ptr))
        res._inputcallback = <cclm.input_cb>input_callback_func
        res.cache_append(inp)  
        return res
    
    if not callable(inp):
        raise TypeError(f"input needs to be a clm gen or function not a {type(inp)}")
        
    @_inputcallback
    def inp_f(gen, d):
        return inp(d)
     
    cy_inp_f_ptr = (<cclm.input_cb*><size_t>ctypes.addressof(inp_f))[0]
    res = mus_any.from_ptr(cclm.mus_make_granulate(<cclm.input_cb>cy_inp_f_ptr, expansion, length, scaler, hop, ramp, jitter, max_size, NULL, <void*>(<mus_any>inp)._ptr))
    res._inputcallback = cy_inp_f_ptr
    res.cache_append(inp_f)     
    
    if(edit is None):
        return res

    @_editcallback
    def edit_f(gen):
        return edit(res)
    
    cy_edit_f_ptr = (<cclm.edit_cb*><size_t>ctypes.addressof(edit_f))[0]
    cclm.mus_granulate_set_edit_function(res._ptr, cy_edit_f_ptr)
    res._editcallback  = cy_edit_f_ptr
    cclm.mus_set_environ(res._ptr, <void*>res)
    res.cache_append(edit_f)

    return res
    

    
#todo: mus_granulate_grain_max_length
cpdef cython.double granulate(mus_any gen):
    """
    next sample from granular synthesis generator.
    
    :param gen: granulate gen
    :rtype: float
    
    """
    if gen._editcallback:
        return cclm.mus_granulate_with_editor(gen._ptr, <cclm.input_cb>gen._inputcallback, <cclm.edit_cb>gen._editcallback)
    else:      
        return cclm.mus_granulate(gen._ptr, <cclm.input_cb>gen._inputcallback)
    

cpdef bint is_granulate(mus_any e):
    """
    returns True if gen is a granulate.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_granulate(e._ptr)

#--------------- phase-vocoder ----------------#
def make_phase_vocoder(inp, 
                        fft_size: Optional[int]=512, 
                        overlap: Optional[int]=4, 
                        interp: Optional[int]=128, 
                        pitch: Optional[float]=1.0, 
                        analyze=None, 
                        edit=None, 
                        synthesize=None):
                        
    """
    return a new phase-vocoder generator; input is the input function (it can be set at run-time),
    analyze, edit, and synthesize are either None or functions that replace the default innards of the
    generator, fft_size, overlap and interp set the fft_size, the amount of overlap between ffts, and the
    time between new analysis calls. 'analyze', if given, takes 2 args, the generator and the input
    function; if it returns True, the default analysis code is also called.  'edit', if given, takes 1 arg,
    the generator; if it returns True, the default edit code is run.  'synthesize' is a function of 1 arg,
    the generator; it is called to get the current vocoder output.
    
    :param inp: gen or function to read from. if a callback, the function takes 1 input, the direction and should return read value
    :param fft_size: fft size used
    :param overlap: how many analysis stages overlap
    :param interp: samples between fft
    :param pitch: pitch scaling ratio
    :param analyze: if used, overrides default. should be a function of two arguments, the generator and the input function. 
    :param edit: if used, overrides default. functions of one argument, the phase_vocoder mus_any. change amplitudes and phases
    :param synthesize: if used, overrides default. unctions of one argument, the phase_vocoder mus_any.
    :return: phase_vocoder gen
    
    """

    cdef cclm.input_cb cy_inp_f_ptr
    cdef cclm.edit_cb cy_edit_f_ptr 
    cdef cclm.analyze_cb cy_analyze_f_ptr
    cdef cclm.synthesize_cb cy_synthesize_f_ptr 
   
    if fft_size <= 1:
        raise ValueError(f'fft_size must be a positive number greater than 1 not {fft_size}')
        
    if fft_size > csndlib.mus_max_malloc():
         raise ValueError(f'fft_size too large. cannot allocate {fft_size} size fft')
        
    if not is_power_of_2(fft_size):
        raise ValueError(f'fft_size must be power of 2 not {fft_size}')
        
    if(isinstance(inp, mus_any)):
        res = mus_any.from_ptr(cclm.mus_make_phase_vocoder(<cclm.input_cb>input_callback_func, fft_size, overlap, interp, pitch, NULL, NULL, NULL, <void*>(<mus_any>inp)._ptr))
        res._inputcallback = <cclm.input_cb>input_callback_func
        res.cache_append(inp)
        
        
    elif callable(inp):
        @_inputcallback
        def inp_f(gen, d):
            return inp(d)
        cy_inp_f_ptr = (<cclm.input_cb*><size_t>ctypes.addressof(inp_f))[0]
        res = mus_any.from_ptr(cclm.mus_make_phase_vocoder(cy_inp_f_ptr, fft_size, overlap, interp, pitch, NULL, NULL, NULL, NULL))
        res._inputcallback = cy_inp_f_ptr
        res.cache_append(inp_f)    
        
    else:
        raise TypeError(f"input needs to be a clm gen or a callable not a {type(inp)}")  
    
    if(edit is not None):
        @_editcallback
        def edit_f(gen):
            return edit(res)
        cy_edit_f_ptr = (<cclm.edit_cb*><size_t>ctypes.addressof(edit_f))[0]
        res._editcallback  = cy_edit_f_ptr
        res.cache_append(edit_f)    

    if (analyze is not None):
        @_analyzecallback
        def analyze_f(gen, func):
            return analyze(res, inp)
        cy_analyze_f_ptr = (<cclm.analyze_cb*><size_t>ctypes.addressof(analyze_f))[0]
        res._analyzecallback  = cy_analyze_f_ptr
        res.cache_append(analyze_f)

    if (synthesize is not None):
        @_synthesizecallback
        def synthesize_f(gen):
            return synthesize(res)
        cy_synthesize_f_ptr = (<cclm.synthesize_cb*><size_t>ctypes.addressof(synthesize_f))[0]
        res._synthesizecallback = cy_synthesize_f_ptr
        res.cache_append(synthesize_f)
        
    return res


cpdef cython.double phase_vocoder(mus_any gen):
    """
    next phase vocoder value.
    
    :param gen: phase_vocoder gen
    :rtype: float
    """
    if gen._analyzecallback or gen._synthesizecallback or gen._editcallback :
        return cclm.mus_phase_vocoder_with_editors(gen._ptr, gen._inputcallback, gen._analyzecallback, gen._editcallback, gen._synthesizecallback)
    else:
        return cclm.mus_phase_vocoder(gen._ptr, gen._inputcallback)
    
cpdef bint is_phase_vocoder(mus_any gen):
    """
    returns True if gen is a phase_vocoder.
    
    :param gen: gen
    :rtype: bool
    """
    return cclm.mus_is_phase_vocoder(gen._ptr)


cpdef np.ndarray phase_vocoder_amp_increments(mus_any gen):
    """
    returns a ndarray containing the current output sinusoid amplitude increments per sample.
    """    
    return gen._pv_amp_increments
    
cpdef np.ndarray phase_vocoder_amps(mus_any gen):
    """
    returns a ndarray containing the current output sinusoid amplitudes.
    """
    return gen._pv_amps
    
cpdef np.ndarray phase_vocoder_freqs(mus_any gen):
    """
    returns a ndarray containing the current output sinusoid frequencies.
    """
    return gen._pv_freqs
    
cpdef np.ndarray phase_vocoder_phases(mus_any gen):
    """
    returns a ndarray containing the current output sinusoid phases.
    """
    return gen._pv_phases
    
cpdef np.ndarray phase_vocoder_phase_increments(mus_any gen):
    """
    returns a ndarray containing the current output sinusoid phase increments.
    """
    return gen._pv_phase_increments
    
# --------------- out-any ---------------- #
cpdef out_any(cython.long loc, cython.double data, cython.int channel, output=None):
    """
    add data to output.
    
    :param loc: location to write to \in samples
    :param data: sample value
    :param channel: channel to write to 
    :param output: output to write to. can be an appropriately shaped np.ndarray or sample2file

    """
    
    
    if isinstance(output, np.ndarray): 
        output[channel][loc] += data
    else:
        if not output:
            output = default.output           
        out = <mus_any>output
        cclm.mus_out_any(loc, data, channel, out._ptr)

# --------------- outa ---------------- #
cpdef outa(cython.long loc, cython.double data, output=None):
    """
    add data to output \in channel 0.
    
    :param loc: location to write to \in samples
    :param data: sample value
    :param channel: channel to write to 
    :param output: output to write to. can be an appropriately shaped np.ndarray or sample2file

    """
    if output is not None:
        out_any(loc, data, 0, output)        
    else:
        out_any(loc, data, 0, default.output)

# --------------- outb ---------------- #    
cpdef outb(cython.long loc, cython.double data, output=None):
    """
    add data to output \in channel 1.
    
    :param loc: location to write to \in samples
    :param data: sample value
    :param channel: channel to write to 
    :param output: output to write to. can be an appropriately shaped np.ndarray or sample2fil

    """
    if output is not None:
        out_any(loc, data, 1, output)        
    else:
        out_any(loc, data, 1, default.output)

# --------------- outc ---------------- #    
cpdef outc(cython.long loc, cython.double data, output=None):
    """
    add data to output \in channel 2.
    
    :param loc: location to write to \in samples
    :param data: sample value
    :param channel: channel to write to 
    :param output: output to write to. can be an appropriately shaped np.ndarray or sample2file

    """
    if output is not None:
        out_any(loc, data, 2, output)        
    else:
        out_any(loc, data, 2, default.output) 

# --------------- outd ---------------- #    
cpdef outd(cython.long loc, cython.double data, output=None):
    """
    add data to output \in channel 3.
    
    :param loc: location to write to \in samples
    :param data: sample value
    :param channel: channel to write to 
    :param output: output to write to. can be an appropriately shaped np.ndarray or sample2file

    """
    if output is not None:
        out_any(loc, data, 3, output)        
    else:
        out_any(loc, data, 3, default.output)   

   #      
# --------------- out-bank ---------------- #    
cpdef out_bank(gens, cython.long loc, cython.double val):
    """
    calls each generator \in the gens list, passing it the argument val, then sends that output to the output channels \in the list order (the first generator writes to outa, the second to outb, etc)."

    :param gens: gens to call
    :param loca: location in samples to write to
    :return: data
    :rtype: float
    """
    for i in range(len(gens)):
        gen = gens[i]
        out_any(loc, gen(val, 0.), i, default.output)   



#--------------- in-any ----------------#
cpdef in_any(cython.long loc, cython.int channel, inp):
    """
    input stream sample at loc \in channel chan.
    
    :param loc: location to read from
    :param channel: channel to read from 
    :param inp: input to read from. can be an appropriately shaped np.ndarray or file2sample
    :return: data
    :rtype: float
    """
    if is_list_or_ndarray(input):
        return inp[channel][loc]
    elif isinstance(inp, types.GeneratorType):
        return next(inp)
    elif callable(inp):
        return inp(loc, channel)
    else:
        ipt = <mus_any>inp
        return cclm.mus_in_any(loc, channel, ipt._ptr)

#--------------- ina ----------------#
cpdef ina(cython.long loc, inp):
    """
    input stream sample at loc \in channel 0.
    
    :param loc: location to read from
    :param inp: input to read from. can be an appropriately shaped np.ndarray or file2sample
    :return: data
    :rtype: float
    """
    return in_any(loc, 0, inp)

#--------------- inb ----------------#    
cpdef inb(cython.long loc, inp):
    """
    input stream sample at loc \in channel 1.
    
    :param loc: location to read from
    :param channel: channel to read from 
    :param inp: input to read from. can be an appropriately shaped np.ndarray or file2sample
    :return: data
    :rtype: float
    """
    return in_any(loc, 1, inp)



# --------------- locsig ---------------- #
cpdef mus_any make_locsig(cython.double degree=0.0, cython.double distance=1., cython.double reverb=0.0, output=None, revout=None, channels=None, reverb_channels=None, Interp interp_type=Interp.LINEAR):
    
    """
    return a new generator for signal placement \in n channels.  channel 0 corresponds to 0 degrees.
    
    :param degree: degree to place sound
    :param distance: distance, 1.0 or greater
    :param reverb: reverb amount
    :param output: output to write 'dry' signal to. can be an appropriately shaped np.ndarray or sample2file
    :param revout: output to write 'wet' signal to. can be an appropriately shaped np.ndarray or sample2file
    :param channels: number of main channels
    :param reverb_channels: number of channels for reverb
    :param interp_type: interpolation of position. can be Interp.LINEAR, Interp.SINUSOIDAL
    """
    
    cdef cclm.detour_cb cy_detour_f_ptr
    
    if output is None:
        output = default.output  #todo : check if this exists
    
    if revout is None:
        if default.reverb is not None:
            revout = default.reverb
        else: 
            revout = None #this generates and error but still works

    if channels is None:
        channels = get_channels(output)
    
    if reverb_channels is None:
        if revout is None:
            reverb_channels = 0
        else:
            reverb_channels = get_channels(revout)

    if isinstance(output, mus_any):
     
        out = <mus_any>output
        rout = <mus_any>revout
        if revout is not None:
            res = mus_any.from_ptr(cclm.mus_make_locsig(degree, distance, reverb, channels, out._ptr, reverb_channels, rout._ptr,  <cclm.mus_interp_t>interp_type))
        else:
            res = mus_any.from_ptr(cclm.mus_make_locsig(degree, distance, reverb, channels, out._ptr, reverb_channels, NULL ,  <cclm.mus_interp_t>interp_type))
        return res
        
    # todo: what if revout is not an iterable? while possible not going to deal with it right now :)   
    elif is_list_or_ndarray(output):
        if reverb_channels is None:
            reverb_channels = 0
            
        res = mus_any.from_ptr(cclm.mus_make_locsig(degree, distance, reverb, channels, NULL, reverb_channels, NULL, <cclm.mus_interp_t>interp_type))
        cclm.mus_locsig_set_detour(res._ptr, <cclm.detour_cb>locsig_detour_callback_func)

        return res
            
    else:
        raise TypeError(f"output needs to be a clm gen or np.array not a {type(output)}")  
        
cpdef cython.double locsig(mus_any gen, cython.long loc, cython.double val):
    """
    locsig 'gen' channel 'chan' scaler.
    
    :param gen: locsig gen
    :param loc: location to write to \in samples
    :param val: sample value
    :return: data
    :rtype: float
    """
    cclm.mus_locsig(gen._ptr, loc, val)
    
cpdef bint is_locsig(mus_any gen):
    """
    returns True if gen is a locsig.
    
    :param gen: gen
    :return: result
    :rtype: bool
    """
    return cclm.mus_is_locsig(gen._ptr)
    
cpdef cython.double locsig_ref(mus_any gen, cython.int chan):
    """
    get locsig 'gen' channel 'chan' scaler for main output.
    
    :param gen: locsig gen
    :param chan: channel to get
    :return: scaler of chan
    :rtype: float
    """
    return cclm.mus_locsig_ref(gen._ptr, chan)
    
cpdef cython.double locsig_set(mus_any gen, cython.int chan, cython.double val):
    """
    set the locsig generator's channel 'chan' scaler to 'val'  for main output.
    
    :param gen: locsig gen
    :param chan: channel to set
    :param val: value to set to
    :return: scaler of chan
    :rtype: float
    """
    return cclm.mus_locsig_set(gen._ptr, chan, val)
    
cpdef cython.double locsig_reverb_ref(mus_any gen, cython.int chan):
    """
    get locsig reverb channel 'chan' scaler.
    
    :param gen: locsig gen
    :param chan: channel to get
    :return: scaler of chan
    :rtype: float
    
    """
    return cclm.mus_locsig_reverb_ref(gen._ptr, chan)

cpdef cython.double locsig_reverb_set(mus_any gen, cython.int chan, cython.double val):
    """
    set the locsig reverb channel 'chan' scaler to 'val'.
    
    :param gen: locsig gen
    :param chan: channel to set
    :param val: value to set to
    :return: scaler of chan
    :rtype: float
    """
    return cclm.mus_locsig_reverb_set(gen._ptr, chan, val)
    
cpdef move_locsig(mus_any gen,  cython.double degree, cython.double distance):
    """
    move locsig gen to reflect degree and distance.
    
    :param gen: locsig gen
    :param degree: new degree
    :param distance: new distance
    """
    cclm.mus_move_locsig(gen._ptr, degree, distance)
    
     
# added some options . todo: what about sample rate conversion    
cpdef convolve_files(str file1, str file2, cython.double maxamp=1., str outputfile='test.aif', sample_type=None, header_type=None):
    """
    convolve-files handles a very common special case: convolve two files, then normalize the result to some maxamp.
    
    :param file1: first file
    :param file2: second file
    :param maxamp: amp to scale to
    :param outputfile: output file
    :param sample_type: type of sample type to use. defaults to clm.sample_type
    :param header_type: header of sample type to use. defaults to clm.header_type
    :return: output file 
    :rtype: str
    """
    sample_type = sample_type or default.sample_type
    header_type = header_type or default.header_type
    
    if header_type == Header.NEXT:
        cclm.mus_convolve_files(file1, file2, maxamp,outputfile)
    else:
        temp_file = tempfile.gettempdir() + '/' + 'temp-' + outputfile
        cclm.mus_convolve_files(file1, file2, maxamp, temp_file)
        with Sound(outputfile, header_type=header_type, sample_type=sample_type):
            length = seconds2samples(csndlib.mus_sound_duration(temp_file))
            reader = make_readin(temp_file)
            for i in range(0, length):
                outa(i, readin(reader))
    return outputfile


# --------------- additions ---------------- #




# --------------- dcblock ---------------- #

cpdef mus_any make_dcblock():
    return make_filter(2, [1,-1], [1, -.99])
    
cpdef cython.double dcblock(mus_any gen, cython.double insig):
    return filter(gen, insig)
    

# --------------- biquad ---------------- #

cpdef mus_any make_biquad(cython.double a0, cython.double a1, cython.double a2, cython.double b1, cython.double b2):
    """returns a biquad filter (use with the CLM filter gen)"""
    return make_filter(3, np.array([a0,a1,a2]), np.array([0.0,b1,b2]))
    
cpdef cython.double biquad(mus_any gen, cython.double insig):
    return filter(gen, insig)

cpdef bint is_biquad(mus_any gen):
    return is_filter(gen) and (gen.mus_order == 3)


cpdef mus_any make_biquad_notch(cython.double fc, cython.double radius):
    cdef cython.double sr = get_srate()
    cdef cython.double a0 = 1.0
    cdef cython.double a1 = 2.0 * radius * math.cos((np.pi*2) * fc /  sr)
    cdef cython.double a2 = radius * radius
    cdef cython.double b1 = 0.0
    cdef cython.double b2 = 0.0
    return make_biquad(a0, a1, a2, b1, b2)
    
cpdef mus_any make_biquad_low_pass(cython.double fc, cython.double q):
    cdef cython.double sr = get_srate()
    cdef cython.double k = math.tan(np.pi * fc / sr)
    cdef cython.double ksqr = k * k
    cdef cython.double denom = 1.0 / (ksqr * q + k + q)
    cdef cython.double b1 = 2 * q * (ksqr - 1) * denom
    cdef cython.double b2 = (ksqr * q - k + q) * denom
    
    cdef cython.double a0 = ksqr * q * denom
    cdef cython.double a1 = 2 * a0
    cdef cython.double a2 = a0
    
    return make_biquad(a0, a1, a2, b1, b2)
    
cpdef mus_any make_biquad_high_pass(cython.double fc, cython.double q):
    cdef cython.double sr = get_srate()
    cdef cython.double k = math.tan(np.pi * fc / sr)
    cdef cython.double ksqr = k * k
    cdef cython.double denom = 1.0 / (ksqr * q + k + q)
    cdef cython.double b1 = 2 * q * (ksqr - 1) * denom
    cdef cython.double b2 = (ksqr * q - k + q) * denom
    
    cdef cython.double a0 = q * denom
    cdef cython.double a1 = -2 * a0
    cdef cython.double a2 = a0
    
    return make_biquad(a0, a1, a2, b1, b2)
    
cpdef mus_any make_biquad_band_pass(cython.double fc, cython.double q):
    cdef cython.double sr = get_srate()
    cdef cython.double k = math.tan(np.pi * fc / sr)
    cdef cython.double ksqr = k * k
    cdef cython.double denom = 1.0 / (ksqr * q + k + q)
    cdef cython.double b1 = 2 * q * (ksqr - 1) * denom
    cdef cython.double b2 = (ksqr * q - k + q) * denom
    
    cdef cython.double a0 = k * denom
    cdef cython.double a1 = 0.0
    cdef cython.double a2 = -a0
    
    return make_biquad(a0, a1, a2, b1, b2)
    
cpdef mus_any make_biquad_band_reject(cython.double fc, cython.double q):
    cdef cython.double sr = get_srate()
    cdef cython.double k = math.tan(np.pi * fc / sr)
    cdef cython.double ksqr = k * k
    cdef cython.double denom = 1.0 / (ksqr * q + k + q)
    cdef cython.double b1 = 2 * q * (ksqr - 1) * denom
    cdef cython.double b2 = (ksqr * q - k + q) * denom
    
    cdef cython.double a0 = q * (ksqr + 1.) * denom
    cdef cython.double a1 = 2.0 * q * (ksqr - 1.) * denom
    cdef cython.double a2 = a0
    
    return make_biquad(a0, a1, a2, b1, b2)
    
cpdef mus_any make_biquad_all_pass(cython.double fc, cython.double q):
    cdef cython.double sr = get_srate()
    cdef cython.double k = math.tan(np.pi * fc / sr)
    cdef cython.double ksqr = k * k
    cdef cython.double denom = 1.0 / (ksqr * q + k + q)
    cdef cython.double b1 = 2 * q * (ksqr - 1) * denom
    cdef cython.double b2 = (ksqr * q - k + q) * denom
    
    cdef cython.double a0 = b2
    cdef cython.double a1 = b1
    cdef cython.double a2 = 1.
    
    return make_biquad(a0, a1, a2, b1, b2)
    
cpdef biquad_set_resonance(mus_any gen, cython.double fc, cython.double radius, bint normalize=False):
    cdef cython.double sr = get_srate()
    gen.mus_ycoeffs[2] = radius * radius
    gen.mus_ycoeffs[1] = -2.0 * radius * math.cos((np.pi*2) * fc / sr)

    if normalize:
        gen.mus_xcoeffs[0] = .5 - .5 * gen.mus_ycoeffs[2]
        gen.mus_xcoeffs[1] = 0.0
        gen.mus_xcoeffs[2] = -gen.mus_xcoeffs[0]
    else:
        gen.mus_xcoeffs[0] = 1.0
        gen.mus_xcoeffs[1] = 0.0
        gen.mus_xcoeffs[2] = 0.0
    
cpdef biquad_set_equal_gain_zeroes(mus_any gen):
    gen.mus_xcoeffs[0] = 1.0
    gen.mus_xcoeffs[1] = 0.0
    gen.mus_xcoeffs[2] = -1.0    

    
def convert_frequency(gen):
    gen.frequency = hz2radians(gen.frequency)
    return gen
# 

cdef class array_readin_gen:
    cdef np.ndarray _arr
    cdef int _chan
    cdef cython.longlong _start
    cdef int _direction
    cdef cython.longlong _location
    cdef cython.longlong _length
    cdef float _val

    def __init__(self, arr: npt.NDArray[np.float64], chan: Optional[int]=0, start: Optional[int]=0, direction: Optional[int]=1):
        check_ndim(arr, 2)
        self._arr = arr
        self._chan = chan
        self._start = start
        self._direction = direction
        self._location = self._start
        self._length = np.shape(arr)[1]
    
    @property
    def mus_channel(self):
        return self._chan
        
    @property
    def mus_location(self):
        return self._location
        
    @mus_location.setter
    def mus_location(self, v: int):
       self._location = v
       
    @property
    def mus_increment(self):
        return self._direction
    
    @mus_increment.setter
    def mus_increment(self, v: int):
        self._direction = v
        
    @property
    def mus_length(self):
        return self._length
        
    def __call__(self):
        self._location = max(0, min(self._location, self._length-1))
        self._val = self._arr[self._chan][self._location]
        self._location += self._direction
        return self._val
        
cpdef array_readin_gen make_array_readin(arr: npt.NDArray[np.float64], chan: Optional[int]=0, start: Optional[int]=0, direction: Optional[int]=1):
    return array_readin_gen(arr, chan, start, direction)

cpdef array_readin(gen: array_readin_gen):
    return gen()
    
cpdef is_array_readin(gen):
    return isinstance(gen, array_readin_gen)






# 
# 
# # # todo: maybe add an exception that have to use keyword args
# 
# def make_generator(name, slots, wrapper=None, methods=None, docstring=None):
#     class mus_gen():
#         pass
#     def make_generator(**kwargs):
#         gen = mus_gen()
#         setattr(gen, 'name', name)
#         for k, v  in kwargs.items():
#             setattr(gen, k, v)
#         if methods:
#             for k, v  in methods.items():
#                 setattr(mus_gen, k, property(v[0], v[1], None) )
#         
#         return gen if not wrapper else wrapper(gen)
#     def is_a(gen):
#         return isinstance(gen, mus_gen) and gen.name == name
#     g =  functools.partial(make_generator, **slots)
#     if docstring is not None:
#         g.__doc__ = docstring
#     
#     return g, is_a
# 

  
def clamp(x, lo, hi):
    return max(min(x, hi),lo)  




def _clip(x, lo, hi):
    return max(min(x, hi),lo)
    
    
def _wrap(x, lo, hi):
    r = hi-lo
    if x >= lo and x <= hi:
        return x
    if x < lo:
        return hi + (math.fmod((x-lo), r))
    if x > hi:
        return lo + (math.fmod((x-hi), r))

def array_reader(arr, chan, loop=False):
    ind = 0
    if chan > (get_channels(arr)):
        raise ValueError(f'array has {get_channels(arr)} channels but {chan} asked for')
    length = get_length(arr)
    if loop:
        def reader(direction):
            nonlocal ind
            v = arr[chan][ind]
            ind += direction
            ind = _wrap(ind, 0, length-1)
            return v
            
    else: 
        def reader(direction):
            nonlocal ind
            v = arr[chan][ind]
            ind += direction
            ind = _clip(ind, 0, length-1)
            return v
    return reader    
    
def sndplay(file):
    subprocess.run([default.player,file])

#decorator for reverbs.
def clm_reverb(func):
    @functools.wraps(func)
    def call(*args, **kwargs):
        return functools.partial(func,*args, **kwargs)
    return call 

def array_resample(arr, new_length, interp_type=Interp.LINEAR):
    res = np.zeros(new_length)
    inp = np.array(arr)
    orig_length = len(arr)
    indices = np.linspace(0, orig_length-1,new_length)
    for i in range(new_length):
        res[i] = mus_interpolate(interp_type, indices[i], inp)
    return res


def phase_delay(gen, freq):
    omega_t = 2 * np.pi * freq / get_srate()
    real = 0.
    imag = 0.
    for i in range(len(gen.mus_xcoeffs)):
        real += gen.mus_xcoeffs[i] * math.cos(i * omega_t)
        imag -= gen.mus_xcoeffs[i] * math.sin(i * omega_t)
   # print(gen.mus_xcoeffs[0])
    real *= gen.mus_xcoeffs[0]
    imag *= gen.mus_xcoeffs[0]
    phase = math.atan2(imag, real)
    real = 0.
    imag = 0.
    if not is_fir_filter(gen):
        for i in range(len(gen.mus_ycoeffs)):
            real += gen.mus_ycoeffs[i] * math.cos(i * omega_t)
            imag -= gen.mus_ycoeffs[i] * math.sin(i * omega_t)
        phase -= math.atan2(imag, real)
        phase = math.fmod(-phase, 2 * np.pi)
    return phase / omega_t

                                      
                                      
def impulse_generator(arr):
    n = 0
    num = len(arr)
    while n < num:
        yield arr[n]
        n += 1

# 
# # --------------- bessel functions ---------------- #

from math import fabs, sqrt, exp

cpdef cython.double bes_i0(cython.double x):
    cdef cython.double ax
    cdef cython.double ans
    cdef cython.double y
    ax = fabs(x)
    if  ax < 3.75:
        y = x/3.75
        y *= y
        ans = 1.0+y*(3.5156229+y*(3.0899424+y*(1.2067492+y*(0.2659732+y*(0.360768e-1+y*0.45813e-2)))))
    else:
        y=3.75/ax;
        ans=(exp(ax)/sqrt(ax))*(0.39894228+y*(0.1328592e-1+y*(0.225319e-2+y*(-0.157565e-2+y*(0.916281e-2+
        y*(-0.2057706e-1+y*(0.2635537e-1+y*(-0.1647633e-1+
        y*0.392377e-2))))))))
    return ans

from pysndlib.cmath_sf cimport j0, j1, jn, y0, y1, yn

cpdef cython.double bes_j0(cython.double x):
    return j0(x)
    
cpdef cython.double bes_j1(cython.double x):
    return j1(x)

cpdef cython.double bes_jn(cython.int n, cython.double x):
    return jn(n, x)

cpdef cython.double bes_y0(cython.double x):
    return y0(x)        
    
cpdef cython.double bes_y1(cython.double x):
    return y1(x)         
    
cpdef cython.double bes_yn(cython.int n, cython.double x):
    return yn(n, x)
    

cpdef cython.doublecomplex edot_product(cython.doublecomplex freq, np.ndarray data, size=None):
    if size is None:
        size = len(data)
    c = np.exp(np.arange(size) * freq) * data
    return np.sum(c)
#     
# print(edot_product(complex(.2,.4), np.array([1,3,6])))
#     
#     
# cpdef cython.doublecomplex edot_product(cython.doublecomplex freq, np.ndarray data):
# #     cdef cython.int = 0
#     cdef cython.long size = len(data)
# #     cdef cython.doublecomplex sm = 0.0
#     c = np.exp(np.arange(size) * freq) * data
#     return np.sum(c)
#     
# #     for i in range(size):
# #         sm += np.exp
    
    
    
    
# complex double mus_edot_product(complex double freq, complex double *data,
#                                 mus_long_t size) {
#   int i;
#   complex double sum = 0.0;
#   for (i = 0; i < size; i++)
#     sum += (cexp(i * freq) * data[i]);
#   return (sum);
# }
    
    
#     
# cpdef  np.ndarray fill_array(arr:  npt.NDArray[np.float64], gen: mus_any, arg1: cython.double=0.0, arg2: cython.double=0.0):
#     check_ndim(arr)
#     arr_length = len(arr)
#     cdef i = 0
#     for i in range(arr_length):
#         arr[i] = cclm.mus_apply(gen._ptr, arg1,arg2)
        
        
#########################################
# basic file reading/writing to/from nympy arrays
# note all of this assumes numpy dtype is np.double
# also assumes shape is (chan, length)
# a mono file that is 8000 samples long should
# be a numpy array created with something like
# arr = np.zeroes((1,8000), dtype=np.double)
# librosa follows this convention
#  todo : look at allowing something like np.zeroes((8000), dtype=np.double)
# to just be treated as mono sound buffer 
# the python soundfile library does this differently 
# and would use 
# arr = np.zeros((8000,1), dtype=np.double))
# this seems less intuitive to me 
# very issue to translate with simple np.transpose()


# cpdef sndinfo(filename):
#     """returns a dictionary of info about a sound file including write date (data), sample rate (srate),
#     channels (chans), length in samples (samples), length in second (length), comment (comment), and loop information (loopinfo)"""
#     date = csndlib.mus_sound_write_date(filename)
#     srate = csndlib.mus_sound_srate(filename)
#     chans = csndlib.mus_sound_chans(filename)
#     samples = csndlib.mus_sound_samples(filename)
#     comment = csndlib.mus_sound_comment(filename) 
#     length = samples / (chans * srate)
# 
#     header_type = header(mus_sound_header_type(filename))
#     sample_type = sample(mus_sound_sample_type(filename))
#     
#     loop_info = mus_sound_loop_info(filename)
#     if loop_info:
#         loop_modes = [loop_info[6], loop_info[7]]
#         loop_starts = [loop_info[0], loop_info[2]]
#         loop_ends = [loop_info[1], loop_info[3]]
#         base_note = loop_info[4]
#         base_detune = loop_info[5]
#     
#         loop_info = {'sustain_start' : loop_starts[0], 'sustain_end' : loop_ends[0], 
#                     'release_start' : loop_starts[2], 'release_end' : loop_ends[1],
#                     'base_note' : base_note, 'base_detune' : base_detune, 
#                     'sustain_mode' : loop_modes[0], 'release_mode' : loop_modes[1]}
#     
#     info = {'date' : time.localtime(date), 'srate' : srate, 'chans' : chans, 'samples' : samples,
#             'comment' : comment, 'length' : length, 'header_type' : header_type, 'sample_type' : sample_type,
#             'loop_info' : loop_info}
#     return info

# def sound_loop_info(filename):
#     """returns a dictionary of info about a sound file including write date (data), sample rate (srate),
#     channels (chans), length in samples (samples), length in second (length), comment (comment), and loop information (loopinfo)"""
#     
#     loop_info = sndlib.mus_sound_loop_info(filename)
#     if loop_info:
#         loop_modes = [loop_info[6], loop_info[7]]
#         loop_starts = [loop_info[0], loop_info[2]]
#         loop_ends = [loop_info[1], loop_info[3]]
#         base_note = loop_info[4]
#         base_detune = loop_info[5]
#     
#         loop_info = {'sustain_start' : loop_starts[0], 'sustain_end' : loop_ends[0], 
#                     'release_start' : loop_starts[2], 'release_end' : loop_ends[1],
#                     'base_note' : base_note, 'base_detune' : base_detune, 
#                     'sustain_mode' : loop_modes[0], 'release_mode' : loop_modes[1]}
#     return info
#     
# cpdef np.ndarray file2array(filename: str, channel: Optional[int]=0, beg: Optional[int]=None, dur: Optional[int]=None):
#     """
#     return an ndarray with samples from file
#     """
#     length = dur or csndlib.mus_sound_framples(filename)
#     chans = csndlib.mus_sound_chans(filename)
#     srate = csndlib.mus_sound_srate(filename)
#     bg = beg or 0
#     out = np.zeros(length, dtype=np.double)
#     
#     cdef double [:] out_view = None
#     out_view = out
# 
#     csndlib.mus_file_to_array(filename,channel, bg, length, &out_view[0])
#     return out
#     
# def channel2array(filename: str, channel: Optional[int]=0, beg: Optional[int]=None, dur: Optional[int]=None): 
#     length = dur or mus_sound_framples(filename)
#     srate = mus_sound_srate(filename)
#     bg = beg or 0
#     out = np.zeros((1, length), dtype=np.double)
#     mus_file_to_array(filename,channel, bg, length, out[0].ctypes.data_as(ctypes.pointer(ctypes.c_double)))
#     return out
# 
# def calc_length(start, dur):
#     st = seconds2samples(start)
#     nd = seconds2samples(start+dur)
#     return st, nd
# 
