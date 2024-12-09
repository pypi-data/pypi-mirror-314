
#==================================================================================
# The code is part of an attempt at translation of Bill Schottstedaet's sndlib 
# available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

cdef extern from "sndlib.h":
    ctypedef signed long  int64_t
    ctypedef double mus_float_t
    ctypedef unsigned char uint8_t
    
    ctypedef int64_t mus_long_t 
    
    
    ctypedef enum mus_header_t:
        pass

    ctypedef enum mus_sample_t:
        pass
        

    int mus_sound_initialize()
    ctypedef void mus_error_handler_t(int type, char *msg)
    mus_error_handler_t *mus_error_set_handler(mus_error_handler_t *new_error_handler)
    const char *mus_error_type_to_string(int err)

    ctypedef void mus_print_handler_t(char *msg)
    mus_print_handler_t *mus_print_set_handler(mus_print_handler_t *new_print_handler)

    ctypedef mus_float_t mus_clip_handler_t(mus_float_t val)
    #mus_clip_handler_t *mus_clip_set_handler(mus_clip_handler_t *new_clip_handler)
    #mus_clip_handler_t *mus_clip_set_handler_and_checker(mus_clip_handler_t *new_clip_handler, bool (*checker)(void))

    mus_long_t mus_sound_samples(const char *arg)
    mus_long_t mus_sound_framples(const char *arg)
    int mus_sound_datum_size(const char *arg)
    mus_long_t mus_sound_data_location(const char *arg)
    int mus_sound_chans(const char *arg)
    int mus_sound_srate(const char *arg)
    mus_header_t mus_sound_header_type(const char *arg)
    mus_sample_t mus_sound_sample_type(const char *arg)
    int mus_sound_original_sample_type(const char *arg)
   
    mus_long_t mus_sound_comment_start(const char *arg)
    mus_long_t mus_sound_comment_end(const char *arg)
    mus_long_t mus_sound_length(const char *arg)
    int mus_sound_fact_samples(const char *arg)
    #time_t mus_sound_write_date(const char *arg)
    int mus_sound_type_specifier(const char *arg)
    int mus_sound_block_align(const char *arg)
    int mus_sound_bits_per_sample(const char *arg)

    int mus_sound_set_chans(const char *arg, int val)
    int mus_sound_set_srate(const char *arg, int val)
    mus_header_t mus_sound_set_header_type(const char *arg, mus_header_t val)
    mus_sample_t mus_sound_set_sample_type(const char *arg, mus_sample_t val)
    int mus_sound_set_data_location(const char *arg, mus_long_t val)
    int mus_sound_set_samples(const char *arg, mus_long_t val)

    const char *mus_header_type_name(mus_header_t type)
    const char *mus_header_type_to_string(mus_header_t type)
    const char *mus_sample_type_name(mus_sample_t samp_type)
    const char *mus_sample_type_to_string(mus_sample_t samp_type)
    const char *mus_sample_type_short_name(mus_sample_t samp_type)

    char *mus_sound_comment(const char *name)
    int mus_bytes_per_sample(mus_sample_t samp_type)
    float mus_sound_duration(const char *arg)
    int mus_sound_initialize()
    int mus_sound_override_header(const char *arg, int srate, int chans, mus_sample_t samp_type, mus_header_t type, mus_long_t location, mus_long_t size)
    int mus_sound_forget(const char *name)
    int mus_sound_prune()
   # void mus_sound_report_cache(FILE *fp)
    int *mus_sound_loop_info(const char *arg)
    void mus_sound_set_loop_info(const char *arg, int *loop)
    int mus_sound_mark_info(const char *arg, int **mark_ids, int **mark_positions)

    int mus_sound_open_input(const char *arg)
    int mus_sound_open_output(const char *arg, int srate, int chans, mus_sample_t sample_type, mus_header_t header_type, const char *comment)
    int mus_sound_reopen_output(const char *arg, int chans, mus_sample_t samp_type, mus_header_t type, mus_long_t data_loc)
    int mus_sound_close_input(int fd)
    int mus_sound_close_output(int fd, mus_long_t bytes_of_data)
    #define mus_sound_read(Fd, Beg, End, Chans, Bufs) mus_file_read(Fd, Beg, End, Chans, Bufs)
    #define mus_sound_write(Fd, Beg, End, Chans, Bufs) mus_file_write(Fd, Beg, End, Chans, Bufs)

    mus_long_t mus_sound_maxamps(const char *ifile, int chans, mus_float_t *vals, mus_long_t *times)
    int mus_sound_set_maxamps(const char *ifile, int chans, mus_float_t *vals, mus_long_t *times)
    bint mus_sound_maxamp_exists(const char *ifile)
    bint mus_sound_channel_maxamp_exists(const char *file, int chan)
    mus_float_t mus_sound_channel_maxamp(const char *file, int chan, mus_long_t *pos)
    void mus_sound_channel_set_maxamp(const char *file, int chan, mus_float_t mx, mus_long_t pos)
    mus_long_t mus_file_to_array(const char *filename, int chan, mus_long_t start, mus_long_t samples, mus_float_t *array)
    int mus_array_to_file(const char *filename, mus_float_t *ddata, mus_long_t len, int srate, int channels)
    const char *mus_array_to_file_with_error(const char *filename, mus_float_t *ddata, mus_long_t len, int srate, int channels)
    mus_long_t mus_file_to_float_array(const char *filename, int chan, mus_long_t start, mus_long_t samples, mus_float_t *array)
    int mus_float_array_to_file(const char *filename, mus_float_t *ddata, mus_long_t len, int srate, int channels)

    mus_float_t **mus_sound_saved_data(const char *arg)
    void mus_sound_set_saved_data(const char *arg, mus_float_t **data)
    void mus_file_save_data(int tfd, mus_long_t framples, mus_float_t **data)

    int mus_audio_open_output(int dev, int srate, int chans, mus_sample_t samp_type, int size)
    int mus_audio_open_input(int dev, int srate, int chans, mus_sample_t samp_type, int size)
    int mus_audio_write(int line, char *buf, int bytes)
    int mus_audio_close(int line)
    int mus_audio_read(int line, char *buf, int bytes)

    int mus_audio_initialize()
    char *mus_audio_moniker()
    int mus_audio_api()
    mus_sample_t mus_audio_compatible_sample_type(int dev)

    #if HAVE_OSS || HAVE_ALSA
    void mus_oss_set_buffers(int num, int size)
    char *mus_alsa_playback_device()
    char *mus_alsa_set_playback_device(const char *name)
    char *mus_alsa_capture_device()
    char *mus_alsa_set_capture_device(const char *name)
    char *mus_alsa_device()
    char *mus_alsa_set_device(const char *name)
    int mus_alsa_buffer_size()
    int mus_alsa_set_buffer_size(int size)
    int mus_alsa_buffers()
    int mus_alsa_set_buffers(int num)
    bint mus_alsa_squelch_warning()
    bint mus_alsa_set_squelch_warning(bint val)
    #endif

    #if __APPLE__
    bint mus_audio_output_properties_mutable(bint mut)
    #endif

    int mus_audio_device_channels(int dev)
    mus_sample_t mus_audio_device_sample_type(int dev)


    int mus_file_open_descriptors(int tfd, const char *arg, mus_sample_t df, int ds, mus_long_t dl, int dc, mus_header_t dt)
    int mus_file_open_read(const char *arg)
    bint mus_file_probe(const char *arg)
    int mus_file_open_write(const char *arg)
    int mus_file_create(const char *arg)
    int mus_file_reopen_write(const char *arg)
    int mus_file_close(int fd)
    mus_long_t mus_file_seek_frample(int tfd, mus_long_t frample)
    mus_long_t mus_file_read(int fd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs)
    mus_long_t mus_file_read_chans(int fd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs, mus_float_t **cm)
    int mus_file_write(int tfd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs)
    mus_long_t mus_file_read_any(int tfd, mus_long_t beg, int chans, mus_long_t nints, mus_float_t **bufs, mus_float_t **cm)
    mus_long_t mus_file_read_file(int tfd, mus_long_t beg, int chans, mus_long_t nints, mus_float_t **bufs)
    mus_long_t mus_file_read_buffer(int charbuf_sample_type, mus_long_t beg, int chans, mus_long_t nints, mus_float_t **bufs, char *charbuf)
    int mus_file_write_file(int tfd, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs)
    int mus_file_write_buffer(int charbuf_sample_type, mus_long_t beg, mus_long_t end, int chans, mus_float_t **bufs, char *charbuf, bint clipped)
    char *mus_expand_filename(const char *name)
    char *mus_getcwd()

    bint mus_clipping()
    bint mus_set_clipping(bint new_value)
    bint mus_file_clipping(int tfd)
    int mus_file_set_clipping(int tfd, bint clipped)

    int mus_file_set_header_type(int tfd, mus_header_t type)
    mus_header_t mus_file_header_type(int tfd)
    char *mus_file_fd_name(int tfd)
    int mus_file_set_chans(int tfd, int chans)

    int mus_iclamp(int lo, int val, int hi)
    mus_long_t mus_oclamp(mus_long_t lo, mus_long_t val, mus_long_t hi)
    mus_float_t mus_fclamp(mus_float_t lo, mus_float_t val, mus_float_t hi)

    void mus_reset_io_c()
    void mus_reset_headers_c()
    void mus_reset_audio_c()

    int mus_samples_bounds(uint8_t *data, int bytes, int chan, int chans, mus_sample_t samp_type, mus_float_t *min_samp, mus_float_t *max_samp)

    mus_long_t mus_max_malloc()
    mus_long_t mus_set_max_malloc(mus_long_t new_max)
    mus_long_t mus_max_table_size()
    mus_long_t mus_set_max_table_size(mus_long_t new_max)

    char *mus_strdup(const char *str)
    int mus_strlen(const char *str)
    bint mus_strcmp(const char *str1, const char *str2)
    char *mus_strcat(char *errmsg, const char *str, int *err_size)


    bint mus_is_sample_type(int n)
    bint mus_is_header_type(int n)


    mus_long_t mus_header_samples()
    mus_long_t mus_header_data_location()
    int mus_header_chans()
    int mus_header_srate()
    mus_header_t mus_header_type()
    mus_sample_t mus_header_sample_type()
    mus_long_t mus_header_comment_start()
    mus_long_t mus_header_comment_end()
    int mus_header_type_specifier()
    int mus_header_bits_per_sample()
    int mus_header_fact_samples()
    int mus_header_block_align()
    int mus_header_loop_mode(int which)
    int mus_header_loop_start(int which)
    int mus_header_loop_end(int which)
    int mus_header_mark_position(int id)
    int mus_header_mark_info(int **marker_ids, int **marker_positions)
    int mus_header_base_note()
    int mus_header_base_detune()
    void mus_header_set_raw_defaults(int sr, int chn, mus_sample_t frm)
    void mus_header_raw_defaults(int *sr, int *chn, mus_sample_t *frm)
    mus_long_t mus_header_true_length()
    int mus_header_original_sample_type()
    mus_long_t mus_samples_to_bytes(mus_sample_t samp_type, mus_long_t size)
    mus_long_t mus_bytes_to_samples(mus_sample_t samp_type, mus_long_t size)
    int mus_header_read(const char *name)
    int mus_header_write(const char *name, mus_header_t type, int srate, int chans, mus_long_t loc, mus_long_t size_in_samples, 
        mus_sample_t samp_type, const char *comment, int len)
    int mus_write_header(const char *name, mus_header_t type, int in_srate, int in_chans, mus_long_t size_in_samples, 
        mus_sample_t samp_type, const char *comment)
    mus_long_t mus_header_aux_comment_start(int n)
    mus_long_t mus_header_aux_comment_end(int n)
    int mus_header_initialize()
    bint mus_header_writable(mus_header_t type, mus_sample_t samp_type)
    void mus_header_set_aiff_loop_info(int *data)
    int mus_header_sf2_entries()
    char *mus_header_sf2_name(int n)
    int mus_header_sf2_start(int n)
    int mus_header_sf2_end(int n)
    int mus_header_sf2_loop_start(int n)
    int mus_header_sf2_loop_end(int n)
    const char *mus_header_original_sample_type_name(int samp_type, mus_header_t type)
    bint mus_header_no_header(const char *name)

    char *mus_header_riff_aux_comment(const char *name, mus_long_t *starts, mus_long_t *ends)
    char *mus_header_aiff_aux_comment(const char *name, mus_long_t *starts, mus_long_t *ends)

    int mus_header_change_chans(const char *filename, mus_header_t type, int new_chans)
    int mus_header_change_srate(const char *filename, mus_header_t type, int new_srate)
    int mus_header_change_type(const char *filename, mus_header_t new_type, mus_sample_t new_sample_type)
    int mus_header_change_sample_type(const char *filename, mus_header_t type, mus_sample_t new_sample_type)
    int mus_header_change_location(const char *filename, mus_header_t type, mus_long_t new_location)
    int mus_header_change_comment(const char *filename, mus_header_t type, const char *new_comment)
    int mus_header_change_data_size(const char *filename, mus_header_t type, mus_long_t bytes)
    
    #complex double mus_edot_product(complex double freq, complex double *data, mus_long_t size)

    #typedef void mus_header_write_hook_t(const char *filename)
    #mus_header_write_hook_t *mus_header_write_set_hook(mus_header_write_hook_t *new_hook)
    
    
	
