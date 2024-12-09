# cython: c_string_type=unicode
# cython: c_string_encoding=utf8

#==================================================================================
# The code is part of an attempt at translation of Bill Schottstedaet's sndlib 
# available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

# cimport pysndlib.csndlib as csndlib
import numpy as np
cimport numpy as np
from cython cimport view
cimport pysndlib.sndlib

csndlib.mus_sound_initialize()

# -------- sound.c -------- 

cpdef cython.long mus_sound_samples(str file):
    """
    samples of sound according to header 
    """
    return csndlib.mus_sound_samples(file)
    
cpdef cython.long mus_sound_framples(str file):
    """
    samples per channel
    """
    return csndlib.mus_sound_framples(file)
      
cpdef cython.int mus_sound_datum_size(str file):
    """
    bytes per sample
    """
    return csndlib.mus_sound_datum_size(file) 

cpdef cython.long mus_sound_data_location(str file):
    """
    location of first sample (bytes)
    """
    return csndlib.mus_sound_data_location(file) 

cpdef cython.int mus_sound_chans(str file):
    """
    number of channels (samples are interleaved)
    """
    return csndlib.mus_sound_chans(file)     

cpdef cython.double mus_sound_srate(str file):
    """
    sampling rate
    """
    return csndlib.mus_sound_srate(file)     

cpdef Header mus_sound_header_type(str file):
    """
    header type (aiff etc) 
    """
    return <Header>csndlib.mus_sound_header_type(file)     

cpdef Sample mus_sound_sample_type(str file):
    """
    sample type (alaw etc)
    """
    return <Sample>csndlib.mus_sound_sample_type(file)  

cpdef Sample mus_sound_original_sample_type(str file):
    return <Sample>csndlib.mus_sound_original_sample_type(file)  

cpdef cython.long mus_sound_comment_start(str file):
    """
    comment start (bytes) if any
    """
    return csndlib.mus_sound_comment_start(file)  

cpdef cython.long mus_sound_comment_end(str file):
    """
    comment end (bytes)
    """
    return csndlib.mus_sound_comment_end(file)  

cpdef cython.long mus_sound_length(str file):
    """
    true file length in bytes 
    """
    return csndlib.mus_sound_length(file)  

cpdef cython.long mus_sound_fact_samples(str file):
    return csndlib.mus_sound_fact_samples(file)  

# def mus_sound_write_date(str: file):
#     return csndlib.mus_sound_write_date(file)  

cpdef cython.int mus_sound_type_specifier(str file):
    """
    original header type identifier 
    """
    return csndlib.mus_sound_type_specifier(file)  
    
cpdef cython.int mus_sound_block_align(str file):
    return csndlib.mus_sound_block_align(file)   
    
cpdef cython.int mus_sound_bits_per_sample(str file):
    """
    bits per sample
    """
    return csndlib.mus_sound_bits_per_sample(file)   
 
 
cpdef cython.int mus_sound_set_chans(str file,  cython.int val):
    """
    set number of channels for file
    """
    return csndlib.mus_sound_set_chans(file, val)   

cpdef cython.int mus_sound_set_srate(str file, cython.int val):
    """
    set the sample rate of the file
    """
    return csndlib.mus_sound_set_srate(file, val) 

cpdef Header mus_sound_set_header_type(str file,  csndlib.mus_header_t mus_header):
    """
    set header type of file
    """
    return <Header>csndlib.mus_sound_set_header_type(file, mus_header) 


cpdef Sample mus_sound_set_sample_type(str file, csndlib.mus_sample_t mus_sample):
    """
    set sample type of file
    """
    return <Sample>csndlib.mus_sound_set_sample_type(file, mus_sample) 

cpdef cython.int mus_sound_set_data_location(str file, csndlib.mus_long_t val):
    """
    set the data location of the file
    """
    return csndlib.mus_sound_set_data_location(file, val) 

cpdef cython.int mus_sound_set_samples(str file, csndlib.mus_long_t val):
    """
    set number of samples in the file
    """
    return csndlib.mus_sound_set_samples(file, val) 


cpdef str mus_header_type_name(csndlib.mus_header_t header_type):
    """
    get file header type as a string
    """
    return csndlib.mus_header_type_name(header_type) 

cpdef str mus_header_type_to_string(Header header_type):
    """
    convert a header enum to a string 
    """
    return csndlib.mus_header_type_to_string(<csndlib.mus_header_t>header_type) 

cpdef str  mus_sample_type_name( csndlib.mus_sample_t samp_type):
    """
    get file sample type as a string
    """
    return csndlib.mus_sample_type_name(samp_type) 

cpdef str mus_sample_type_to_string(Sample samp_type):
    """
    convert a sample enum to a string 
    """
    return csndlib.mus_sample_type_to_string(<csndlib.mus_sample_t>samp_type) 

cpdef str mus_sample_type_short_name(Sample samp_type):
    """
    convert a sample enum to a short name string 
    """
    return csndlib.mus_sample_type_short_name(<csndlib.mus_sample_t>samp_type) 



cpdef str mus_sound_comment(str file):
    """
    retrieve file comment if one exists
    """
    return csndlib.mus_sound_comment(file) 

cpdef cython.int mus_bytes_per_sample(Sample samp_type):
    """
    bytes per sample
    """
    return csndlib.mus_bytes_per_sample(<csndlib.mus_sample_t>samp_type) 

cpdef cython.double mus_sound_duration(str file):
    """
     sound duration in seconds
    """
    return csndlib.mus_sound_duration(file)       


cpdef cython.int mus_sound_initialize():
    csndlib.mus_sound_initialize()

cpdef cython.int mus_sound_override_header(str file, cython.int srate, cython.int chans, Sample sample_type, Header header_type, cython.int location, cython.int size ):
    """
    override the header information
    """
    return csndlib.mus_sound_override_header(str, srate, chans, <csndlib.mus_sample_t>sample_type, <csndlib.mus_header_t>header_type, location, size)

cpdef np.ndarray mus_sound_loop_info(str filename):
    """
    8 loop vals (mode,start,end) then base-detune and base-note  (empty list if no loop info found)
    """
    cdef int* info_ptr = csndlib.mus_sound_loop_info(filename)
    cdef view.array arr = None
    
    if info_ptr is NULL:
        return None
    else:
        arr = view.array(shape=(8,),itemsize=sizeof(int), format='i', allocate_buffer=False)
        arr.data = <char*>info_ptr
        return np.asarray(arr)    
 
cpdef mus_sound_set_loop_info(str filename, np.ndarray info):
    """
    set file loop information
    """
    cdef int [:] info_view = info
    csndlib.mus_sound_set_loop_info(filename, &info_view[0])
 
#MUS_EXPORT int mus_sound_mark_info(const char *arg, int **mark_ids, int **mark_positions);
# allocate numpy arrays instead of passsing 

cpdef cython.int mus_sound_open_input(str filename):
    """
    open file to read as input
    """
    return csndlib.mus_sound_open_input(filename)

cpdef cython.int mus_sound_open_output(str file, cython.int srate, cython.int chans, Sample sample_type, Header header_type, str comments):
    """
    open file for output
    """
    return csndlib.mus_sound_open_output(file, srate, chans, <csndlib.mus_sample_t>sample_type, <csndlib.mus_header_t>header_type, comments)

cpdef cython.int mus_sound_reopen_output(str file, cython.int srate, cython.int chans, Sample sample_type, Header header_type,  cython.int  location):
    """
    reopen a file for further input
    """
    return csndlib.mus_sound_reopen_output(file, chans, <csndlib.mus_sample_t>sample_type, <csndlib.mus_header_t>header_type, location)

cpdef cython.int mus_sound_close_input(cython.int fd):
    """
    close file for input
    """
    return csndlib.mus_sound_close_input(fd)

cpdef cython.int mus_sound_close_output(cython.int fd, csndlib.mus_long_t bytes_of_data):
    """
    close file for output
    """
    return csndlib.mus_sound_close_output(fd, bytes_of_data)
    
#mus_sound_read
#mus_sound_write







    
    
    
    
    
    
    
    
    
    

cpdef mus_set_clipping(new_value):
    return csndlib.mus_set_clipping(new_value)



   




# MUS_EXPORT int mus_sound_override_header(const char *arg, int srate, int chans, mus_sample_t samp_type, mus_header_t type, mus_long_t location, mus_long_t size);
# MUS_EXPORT int mus_sound_forget(const char *name);
# MUS_EXPORT int mus_sound_prune(void);
# MUS_EXPORT void mus_sound_report_cache(FILE *fp);

# need to decode return int*
# def mus_sound_loop_info(file: str):
#     return csndlib.mus_sound_loop_info(file)   

# def mus_sound_set_loop_info(file: str, loop: *int):
#     return mus_sound_set_loop_info(file, loop)
# 
# def mus_sound_mark_info(file: str, mark_ids: **int, mark_positions: **int):
#     return mus_sound_mark_info(file, mark_ids, mark_positions)
# 
# 
# def mus_sound_open_input(file: str):
#     return csndlib.mus_sound_open_input(file)  
# 
# def mus_sound_open_output(file: str, srate: int, chans: int, sample_type: mus_sample_t, header_type: mus_header_t, comment: str):
#     return csndlib.mus_sound_open_output(file, srate, chans, sample_type, header_type, comment)
# 
# def mus_sound_reopen_output(file: str, chans: int, sample_type: mus_sample_t, header_type: mus_header_t, data_loc: mus_long_t):
#     return csndlib.mus_sound_reopen_output(file, chans, sample_type, header_type, data_loc)
# 
# def mus_sound_close_input(fd: int):
#     return mus_sound_close_input(fd)
# 
# def mus_sound_close_output(fd: int, bytes_of_data: mus_long_t):
#     return mus_sound_close_output(fd, bytes_of_data)


# MUS_EXPORT int mus_file_write(int tfd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs);
#

# def mus_sound_read(fd: int, beg: mus_long_t, end: mus_long_t, chans: int, bufs: **mus_float_t):
#     return mus_file_read(fd, beg, end, chans, bufs)
#     
# def mus_sound_write(fd: int, beg: mus_long_t, end: mus_long_t, chans: int, bufs: **mus_float_t):
#     return mus_file_write(fd, beg, end, chans, bufs)





# 
# MUS_EXPORT mus_long_t mus_sound_maxamps(const char *ifile, int chans, mus_float_t *vals, mus_long_t *times);
# MUS_EXPORT int mus_sound_set_maxamps(const char *ifile, int chans, mus_float_t *vals, mus_long_t *times);
# MUS_EXPORT bool mus_sound_maxamp_exists(const char *ifile);
# MUS_EXPORT bool mus_sound_channel_maxamp_exists(const char *file, int chan);
# MUS_EXPORT mus_float_t mus_sound_channel_maxamp(const char *file, int chan, mus_long_t *pos);
# MUS_EXPORT void mus_sound_channel_set_maxamp(const char *file, int chan, mus_float_t mx, mus_long_t pos);
# MUS_EXPORT mus_long_t mus_file_to_array(const char *filename, int chan, mus_long_t start, mus_long_t samples, mus_float_t *array);
# MUS_EXPORT int mus_array_to_file(const char *filename, mus_float_t *ddata, mus_long_t len, int srate, int channels);
# MUS_EXPORT const char *mus_array_to_file_with_error(const char *filename, mus_float_t *ddata, mus_long_t len, int srate, int channels);
# MUS_EXPORT mus_long_t mus_file_to_float_array(const char *filename, int chan, mus_long_t start, mus_long_t samples, mus_float_t *array);
# MUS_EXPORT int mus_float_array_to_file(const char *filename, mus_float_t *ddata, mus_long_t len, int srate, int channels);
# 
# MUS_EXPORT mus_float_t **mus_sound_saved_data(const char *arg);
# MUS_EXPORT void mus_sound_set_saved_data(const char *arg, mus_float_t **data);
# MUS_EXPORT void mus_file_save_data(int tfd, mus_long_t framples, mus_float_t **data);
# 
# 
# 
# /* -------- audio.c -------- */
# 
# MUS_EXPORT int mus_audio_open_output(int dev, int srate, int chans, mus_sample_t samp_type, int size);
# MUS_EXPORT int mus_audio_open_input(int dev, int srate, int chans, mus_sample_t samp_type, int size);
# MUS_EXPORT int mus_audio_write(int line, char *buf, int bytes);
# MUS_EXPORT int mus_audio_close(int line);
# MUS_EXPORT int mus_audio_read(int line, char *buf, int bytes);
# 
# MUS_EXPORT int mus_audio_initialize(void);
# MUS_EXPORT char *mus_audio_moniker(void);
# MUS_EXPORT int mus_audio_api(void);
# MUS_EXPORT mus_sample_t mus_audio_compatible_sample_type(int dev);
# 
# #if HAVE_OSS || HAVE_ALSA
# MUS_EXPORT void mus_oss_set_buffers(int num, int size);
# MUS_EXPORT char *mus_alsa_playback_device(void);
# MUS_EXPORT char *mus_alsa_set_playback_device(const char *name);
# MUS_EXPORT char *mus_alsa_capture_device(void);
# MUS_EXPORT char *mus_alsa_set_capture_device(const char *name);
# MUS_EXPORT char *mus_alsa_device(void);
# MUS_EXPORT char *mus_alsa_set_device(const char *name);
# MUS_EXPORT int mus_alsa_buffer_size(void);
# MUS_EXPORT int mus_alsa_set_buffer_size(int size);
# MUS_EXPORT int mus_alsa_buffers(void);
# MUS_EXPORT int mus_alsa_set_buffers(int num);
# MUS_EXPORT bool mus_alsa_squelch_warning(void);
# MUS_EXPORT bool mus_alsa_set_squelch_warning(bool val);
# #endif
# 
# #if __APPLE__
#   MUS_EXPORT bool mus_audio_output_properties_mutable(bool mut);
# #endif
# 
# MUS_EXPORT int mus_audio_device_channels(int dev);
# MUS_EXPORT mus_sample_t mus_audio_device_sample_type(int dev);
# 
# 
# 
# /* -------- io.c -------- */
# 
# MUS_EXPORT int mus_file_open_descriptors(int tfd, const char *arg, mus_sample_t df, int ds, mus_long_t dl, int dc, mus_header_t dt);
# MUS_EXPORT int mus_file_open_read(const char *arg);
# MUS_EXPORT bool mus_file_probe(const char *arg);
# MUS_EXPORT int mus_file_open_write(const char *arg);
# MUS_EXPORT int mus_file_create(const char *arg);
# MUS_EXPORT int mus_file_reopen_write(const char *arg);
# MUS_EXPORT int mus_file_close(int fd);
# MUS_EXPORT mus_long_t mus_file_seek_frample(int tfd, mus_long_t frample);
# MUS_EXPORT mus_long_t mus_file_read(int fd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs);
# MUS_EXPORT mus_long_t mus_file_read_chans(int fd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs, mus_float_t **cm);
# MUS_EXPORT int mus_file_write(int tfd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs);
# MUS_EXPORT mus_long_t mus_file_read_any(int tfd, mus_long_t beg, int chans, mus_long_t nints, mus_float_t **bufs, mus_float_t **cm);
# MUS_EXPORT mus_long_t mus_file_read_file(int tfd, mus_long_t beg, int chans, mus_long_t nints, mus_float_t **bufs);
# MUS_EXPORT mus_long_t mus_file_read_buffer(int charbuf_sample_type, mus_long_t beg, int chans, mus_long_t nints, mus_float_t **bufs, char *charbuf);
# MUS_EXPORT int mus_file_write_file(int tfd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs);
# MUS_EXPORT int mus_file_write_buffer(int charbuf_sample_type, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs, char *charbuf, bool clipped);
# MUS_EXPORT char *mus_expand_filename(const char *name);
# MUS_EXPORT char *mus_getcwd(void);
# 
# MUS_EXPORT bool mus_clipping(void);
# MUS_EXPORT bool mus_set_clipping(bool new_value);
# MUS_EXPORT bool mus_file_clipping(int tfd);
# MUS_EXPORT int mus_file_set_clipping(int tfd, bool clipped);
# 
# MUS_EXPORT int mus_file_set_header_type(int tfd, mus_header_t type);
# MUS_EXPORT mus_header_t mus_file_header_type(int tfd);
# MUS_EXPORT char *mus_file_fd_name(int tfd);
# MUS_EXPORT int mus_file_set_chans(int tfd, int chans);
# 
# MUS_EXPORT int mus_iclamp(int lo, int val, int hi);
# MUS_EXPORT mus_long_t mus_oclamp(mus_long_t lo, mus_long_t val, mus_long_t hi);
# MUS_EXPORT mus_float_t mus_fclamp(mus_float_t lo, mus_float_t val, mus_float_t hi);
# 
# /* for CLM */
# /* these are needed to clear a saved lisp image to the just-initialized state */
# MUS_EXPORT void mus_reset_io_c(void);
# MUS_EXPORT void mus_reset_headers_c(void);
# MUS_EXPORT void mus_reset_audio_c(void);
# 
# MUS_EXPORT int mus_samples_bounds(uint8_t *data, int bytes, int chan, int chans, mus_sample_t samp_type, mus_float_t *min_samp, mus_float_t *max_samp);
# 
# MUS_EXPORT mus_long_t mus_max_malloc(void);
# MUS_EXPORT mus_long_t mus_set_max_malloc(mus_long_t new_max);
# MUS_EXPORT mus_long_t mus_max_table_size(void);
# MUS_EXPORT mus_long_t mus_set_max_table_size(mus_long_t new_max);
# 
# MUS_EXPORT char *mus_strdup(const char *str);
# MUS_EXPORT int mus_strlen(const char *str);
# MUS_EXPORT bool mus_strcmp(const char *str1, const char *str2);
# MUS_EXPORT char *mus_strcat(char *errmsg, const char *str, int *err_size);
# 
# 
# 
# /* -------- headers.c -------- */
# 
# MUS_EXPORT bool mus_is_sample_type(int n);
# MUS_EXPORT bool mus_is_header_type(int n);
# 
# MUS_EXPORT mus_long_t mus_header_samples(void);
# MUS_EXPORT mus_long_t mus_header_data_location(void);
# MUS_EXPORT int mus_header_chans(void);
# MUS_EXPORT int mus_header_srate(void);
# MUS_EXPORT mus_header_t mus_header_type(void);
# MUS_EXPORT mus_sample_t mus_header_sample_type(void);
# MUS_EXPORT mus_long_t mus_header_comment_start(void);
# MUS_EXPORT mus_long_t mus_header_comment_end(void);
# MUS_EXPORT int mus_header_type_specifier(void);
# MUS_EXPORT int mus_header_bits_per_sample(void);
# MUS_EXPORT int mus_header_fact_samples(void);
# MUS_EXPORT int mus_header_block_align(void);
# MUS_EXPORT int mus_header_loop_mode(int which);
# MUS_EXPORT int mus_header_loop_start(int which);
# MUS_EXPORT int mus_header_loop_end(int which);
# MUS_EXPORT int mus_header_mark_position(int id);
# MUS_EXPORT int mus_header_mark_info(int **marker_ids, int **marker_positions);
# MUS_EXPORT int mus_header_base_note(void);
# MUS_EXPORT int mus_header_base_detune(void);
# MUS_EXPORT void mus_header_set_raw_defaults(int sr, int chn, mus_sample_t frm);
# MUS_EXPORT void mus_header_raw_defaults(int *sr, int *chn, mus_sample_t *frm);
# MUS_EXPORT mus_long_t mus_header_true_length(void);
# MUS_EXPORT int mus_header_original_sample_type(void);
# MUS_EXPORT mus_long_t mus_samples_to_bytes(mus_sample_t samp_type, mus_long_t size);
# MUS_EXPORT mus_long_t mus_bytes_to_samples(mus_sample_t samp_type, mus_long_t size);
# MUS_EXPORT int mus_header_read(const char *name);
# MUS_EXPORT int mus_header_write(const char *name, mus_header_t type, int srate, int chans, mus_long_t loc, mus_long_t size_in_samples, 
# 				mus_sample_t samp_type, const char *comment, int len);
# MUS_EXPORT int mus_write_header(const char *name, mus_header_t type, int in_srate, int in_chans, mus_long_t size_in_samples, 
# 				mus_sample_t samp_type, const char *comment);
# MUS_EXPORT mus_long_t mus_header_aux_comment_start(int n);
# MUS_EXPORT mus_long_t mus_header_aux_comment_end(int n);
# MUS_EXPORT int mus_header_initialize(void);
# MUS_EXPORT bool mus_header_writable(mus_header_t type, mus_sample_t samp_type);
# MUS_EXPORT void mus_header_set_aiff_loop_info(int *data);
# MUS_EXPORT int mus_header_sf2_entries(void);
# MUS_EXPORT char *mus_header_sf2_name(int n);
# MUS_EXPORT int mus_header_sf2_start(int n);
# MUS_EXPORT int mus_header_sf2_end(int n);
# MUS_EXPORT int mus_header_sf2_loop_start(int n);
# MUS_EXPORT int mus_header_sf2_loop_end(int n);
# MUS_EXPORT const char *mus_header_original_sample_type_name(int samp_type, mus_header_t type);
# MUS_EXPORT bool mus_header_no_header(const char *name);
# 
# MUS_EXPORT char *mus_header_riff_aux_comment(const char *name, mus_long_t *starts, mus_long_t *ends);
# MUS_EXPORT char *mus_header_aiff_aux_comment(const char *name, mus_long_t *starts, mus_long_t *ends);
# 
# MUS_EXPORT int mus_header_change_chans(const char *filename, mus_header_t type, int new_chans);
# MUS_EXPORT int mus_header_change_srate(const char *filename, mus_header_t type, int new_srate);
# MUS_EXPORT int mus_header_change_type(const char *filename, mus_header_t new_type, mus_sample_t new_sample_type);
# MUS_EXPORT int mus_header_change_sample_type(const char *filename, mus_header_t type, mus_sample_t new_sample_type);
# MUS_EXPORT int mus_header_change_location(const char *filename, mus_header_t type, mus_long_t new_location);
# MUS_EXPORT int mus_header_change_comment(const char *filename, mus_header_t type, const char *new_comment);
# MUS_EXPORT int mus_header_change_data_size(const char *filename, mus_header_t type, mus_long_t bytes);
# 
# typedef void mus_header_write_hook_t(const char *filename);
# MUS_EXPORT mus_header_write_hook_t *mus_header_write_set_hook(mus_header_write_hook_t *new_hook);



