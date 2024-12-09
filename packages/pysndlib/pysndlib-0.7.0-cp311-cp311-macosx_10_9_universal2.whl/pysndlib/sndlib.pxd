# cython: c_string_type=unicode
# cython: c_string_encoding=utf8

import numpy as np
cimport cython
cimport numpy as np
cimport pysndlib.csndlib as csndlib

csndlib.mus_sound_initialize()

cpdef enum Header:
    """
    file types for audio files
    """
    UNKNOWN_HEADER, NEXT, AIFC, RIFF, RF64, BICSF, NIST, INRS, ESPS, SVX, VOC, SNDT, RAW, SMP, AVR, IRCAM, SD1, SPPACK, MUS10, HCOM, PSION, MAUD, IEEE, MATLAB, ADC, MIDI, SOUNDFONT, GRAVIS, COMDISCO, GOLDWAVE, SRFS, MIDI_SAMPLE_DUMP, DIAMONDWARE, ADF, SBSTUDIOII, DELUSION, FARANDOLE, SAMPLE_DUMP, ULTRATRACKER, YAMAHA_SY85, YAMAHA_TX16W, DIGIPLAYER, COVOX, AVI, OMF, QUICKTIME, ASF, YAMAHA_SY99, KURZWEIL_2000, AIFF, PAF, CSL, FILE_SAMP, PVF, SOUNDFORGE, TWINVQ, AKAI4, IMPULSETRACKER, KORG, NVF, CAFF, MAUI, SDIF, OGG, FLAC, SPEEX, MPEG, SHORTEN, TTA, WAVPACK, SOX, NUM_HEADERS,

cpdef enum Sample:
    """
    numerical sample types
    """
    UNKNOWN_SAMPLE, BSHORT, MULAW, BYTE, BFLOAT, BINT, ALAW, UBYTE, B24INT, BDOUBLE, LSHORT, LINT, LFLOAT, LDOUBLE, UBSHORT, ULSHORT, L24INT, BINTN, LINTN, BFLOAT_UNSCALED, LFLOAT_UNSCALED, BDOUBLE_UNSCALED, LDOUBLE_UNSCALED, NUM_SAMPLES,

cpdef enum Error:
    """
    sndlib and clm errors
    """
    NO_ERROR, NO_FREQUENCY, NO_PHASE, NO_GEN, NO_LENGTH, NO_DESCRIBE, NO_DATA, NO_SCALER, MEMORY_ALLOCATION_FAILED, CANT_OPEN_FILE, NO_SAMPLE_INPUT, NO_SAMPLE_OUTPUT, NO_SUCH_CHANNEL, NO_FILE_NAME_PROVIDED, NO_LOCATION, NO_CHANNEL, NO_SUCH_FFT_WINDOW, UNSUPPORTED_SAMPLE_TYPE, HEADER_READ_FAILED, UNSUPPORTED_HEADER_TYPE, FILE_DESCRIPTORS_NOT_INITIALIZED, NOT_A_SOUND_FILE, FILE_CLOSED, WRITE_ERROR, HEADER_WRITE_FAILED, CANT_OPEN_TEMP_FILE, INTERRUPTED, BAD_ENVELOPE, AUDIO_CHANNELS_NOT_AVAILABLE, AUDIO_SRATE_NOT_AVAILABLE, AUDIO_SAMPLE_TYPE_NOT_AVAILABLE, AUDIO_NO_INPUT_AVAILABLE, AUDIO_CONFIGURATION_NOT_AVAILABLE, AUDIO_WRITE_ERROR, AUDIO_SIZE_NOT_AVAILABLE, AUDIO_DEVICE_NOT_AVAILABLE, AUDIO_CANT_CLOSE, AUDIO_CANT_OPEN, AUDIO_READ_ERROR, AUDIO_CANT_WRITE, AUDIO_CANT_READ, AUDIO_NO_READ_PERMISSION, CANT_CLOSE_FILE, ARG_OUT_OF_RANGE, NO_CHANNELS, NO_HOP, NO_WIDTH, NO_FILE_NAME, NO_RAMP, NO_RUN, NO_INCREMENT, NO_OFFSET, NO_XCOEFF, NO_YCOEFF, NO_XCOEFFS, NO_YCOEFFS, NO_RESET, BAD_SIZE, CANT_CONVERT, READ_ERROR, NO_FEEDFORWARD, NO_FEEDBACK, NO_INTERP_TYPE, NO_POSITION, NO_ORDER, NO_COPY, CANT_TRANSLATE, NUM_ERRORS,



cpdef cython.long mus_sound_samples(str file)
cpdef cython.long mus_sound_framples(str file)
cpdef cython.int mus_sound_datum_size(str file)
cpdef cython.long mus_sound_data_location(str file)
cpdef cython.int mus_sound_chans(str file)
cpdef cython.double mus_sound_srate(str file)
cpdef Header mus_sound_header_type(str file)
cpdef Sample mus_sound_sample_type(str file)
cpdef Sample mus_sound_original_sample_type(str file)
cpdef cython.long mus_sound_comment_start(str file)

cpdef cython.long mus_sound_comment_end(str file)
cpdef cython.long mus_sound_length(str file)
cpdef cython.long mus_sound_fact_samples(str file)
cpdef cython.int mus_sound_type_specifier(str file)
cpdef cython.int mus_sound_block_align(str file)
cpdef cython.int mus_sound_bits_per_sample(str file)
cpdef cython.int mus_sound_set_chans(str file,  cython.int val)
cpdef cython.int mus_sound_set_srate(str file, cython.int val)
cpdef Header mus_sound_set_header_type(str file,  csndlib.mus_header_t mus_header)
cpdef Sample mus_sound_set_sample_type(str file, csndlib.mus_sample_t mus_sample)
cpdef cython.int mus_sound_set_data_location(str file, csndlib.mus_long_t val)
cpdef cython.int mus_sound_set_samples(str file, csndlib.mus_long_t val)
cpdef str mus_header_type_name(csndlib.mus_header_t header_type)
cpdef str mus_header_type_to_string(Header header_type)
cpdef str  mus_sample_type_name( csndlib.mus_sample_t samp_type)
cpdef str mus_sample_type_to_string(Sample samp_type)
cpdef str mus_sample_type_short_name(Sample samp_type)
cpdef str mus_sound_comment(str file)
cpdef cython.int mus_bytes_per_sample(Sample samp_type)
cpdef cython.double mus_sound_duration(str file)
cpdef cython.int mus_sound_initialize()
cpdef cython.int mus_sound_override_header(str file, cython.int srate, cython.int chans, Sample sample_type, Header header_type, cython.int location, cython.int size: int )
cpdef np.ndarray mus_sound_loop_info(str filename)
cpdef mus_sound_set_loop_info(str filename, np.ndarray info)
cpdef cython.int  mus_sound_open_input(str filename)
cpdef cython.int  mus_sound_open_output(str file, cython.int srate, cython.int chans, Sample sample_type, Header header_type, str comments)
cpdef cython.int  mus_sound_reopen_output(str file, cython.int srate, cython.int chans, Sample sample_type, Header header_type,  cython.int  location)
cpdef cython.int mus_sound_close_input(cython.int fd)
cpdef cython.int mus_sound_close_output(cython.int fd, csndlib.mus_long_t bytes_of_data)




