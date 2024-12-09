# cython: c_string_type=unicode
# cython: c_string_encoding=utf8

cimport cython
import numpy as np
cimport numpy as np
cimport pysndlib.cclm as cclm
cimport pysndlib.csndlib as csndlib
from pysndlib.sndlib cimport Sample, Header

np.import_array()




# --------------- clm enums ---------------- #
cpdef enum Interp:
    """
    various interpolation types
    """
    NONE, LINEAR,SINUSOIDAL, ALL_PASS, LAGRANGE, BEZIER, HERMITE

cpdef enum Window:
    """
    many useful windows
    """
    RECTANGULAR, HANN, WELCH, PARZEN, BARTLETT, HAMMING, BLACKMAN2, BLACKMAN3, BLACKMAN4, EXPONENTIAL, RIEMANN, KAISER, CAUCHY, POISSON, GAUSSIAN, TUKEY, DOLPH_CHEBYSHEV, HANN_POISSON, CONNES, SAMARAKI, ULTRASPHERICAL, BARTLETT_HANN, BOHMAN, FLAT_TOP, BLACKMAN5, BLACKMAN6, BLACKMAN7, BLACKMAN8, BLACKMAN9, BLACKMAN10, RV2, RV3, RV4, MLT_SINE, PAPOULIS, DPSS, SINC,

cpdef enum Spectrum:
    """
    types of normalizations when using the spectrum function. the results are in db if in_db, or linear and normalized to 1.0 normalized, or linear unnormalized raw
    """
    IN_DB, NORMALIZED, RAW
    
cpdef enum Polynomial:
    """
    used for polynomial based gens 
    """
    EITHER_KIND, FIRST_KIND, SECOND_KIND, BOTH_KINDS



cdef class mus_any:
    """
    a wrapper class for mus_any pointers in c
    
    instances of this class have the following properties, which may be 
    used if supported by the type of generator used to make the instance:
    
    
    """
    
    cdef cclm.mus_any *_ptr
    cdef bint ptr_owner
    cdef cclm.input_cb _inputcallback
    cdef cclm.edit_cb _editcallback
    cdef cclm.analyze_cb _analyzecallback
    cdef cclm.synthesize_cb _synthesizecallback
    cdef list _cache
    cdef cython.double* _data_ptr
    cdef np.ndarray _data
    cdef cython.double* _xcoeffs_ptr
    cdef np.ndarray _xcoeffs
    cdef cython.double* _ycoeffs_ptr
    cdef np.ndarray _ycoeffs
    cdef cython.double* _pv_amp_increments_ptr
    cdef np.ndarray _pv_amp_increments
    cdef cython.double* _pv_amps_ptr
    cdef np.ndarray _pv_amps
    cdef cython.double* _pv_freqs_ptr
    cdef np.ndarray _pv_freqs
    cdef cython.double* _pv_phases_ptr
    cdef np.ndarray _pv_phases
    cdef cython.double* _pv_phase_increments_ptr
    cdef np.ndarray _pv_phase_increments


    # these should all be considered private
    @staticmethod
    cdef mus_any from_ptr(cclm.mus_any *_ptr, bint owner=*, cython.int length=*)

    cpdef cache_append(self, obj)
    cpdef cache_extend(self, obj)
    cpdef set_up_data(self , cython.int length=*)
    cpdef set_up_xcoeffs(self)
    cpdef set_up_ycoeffs(self)
    cpdef set_up_pv_data(self)
    
    # these should all be considered public
    cpdef mus_reset(self)
    cpdef next(self, cython.double arg1=*, cython.double arg2=*)



cpdef int mus_close(mus_any obj)
cpdef bint mus_is_output(mus_any obj)
cpdef bint mus_is_input(mus_any obj)
cpdef mus_reset(mus_any obj)
cpdef cython.long get_length(obj)
cpdef cython.double get_srate(obj=*)
cpdef cython.long get_framples(obj)
cpdef cython.long get_channels(obj)
cpdef cython.double random(cython.double x=*)
cpdef bint is_zero( cython.double x)
cpdef bint is_even(n)
cpdef bint is_odd(n)
cpdef cython.double radians2hz(cython.double radians )
cpdef cython.double hz2radians(cython.double hz)
cpdef cython.double degrees2radians(cython.double degrees)
cpdef cython.double radians2degrees(cython.double radians)
cpdef cython.double db2linear(cython.double x)
cpdef cython.double linear2db(cython.double x)
cpdef cython.double odd_multiple(cython.double x, cython.double y)
cpdef cython.double even_multiple(cython.double x, cython.double y)
cpdef cython.double odd_weight(cython.double x)
cpdef cython.double even_weight(cython.double x)
cpdef cython.double set_srate(cython.double r)
cpdef cython.long seconds2samples(cython.double secs)
cpdef cython.double samples2seconds(cython.long samples)
cpdef cython.double ring_modulate(cython.double s1, cython.double s2)
cpdef cython.double amplitude_modulate(cython.double s1, cython.double s2, cython.double s3)
cpdef cython.double contrast_enhancement(cython.double insig, cython.double fm_index=* )
cpdef cython.double dot_product(np.ndarray data1, np.ndarray  data2)
cpdef cython.double polynomial(np.ndarray coeffs, cython.double x )
cpdef cython.double array_interp(np.ndarray  fn, cython.double  x)
cpdef cython.double bessi0(cython.double x)
cpdef cython.double mus_interpolate(Interp interp_type, cython.double x, np.ndarray table, cython.double y1 =*)
cpdef np.ndarray make_fft_window(Window window_type, cython.int size, cython.double beta=* , cython.double alpha=*)

cpdef file2ndarray(str filename, channel=*, beg=*, size=*)
cpdef ndarray2file(str filename, np.ndarray arr, size=*, sr=*, sample_type=*, header_type=*, comment=* )


cpdef np.ndarray mus_fft(np.ndarray rdat, np.ndarray  idat, cython.int fft_size , cython.int sign)
cpdef tuple fft(np.ndarray rdat, np.ndarray idat,  cython.int fft_size, cython.int sign )
cpdef np.ndarray mus_rectangular2polar(np.ndarray  rdat, np.ndarray  idat)
cpdef tuple rectangular2polar(np.ndarray rdat, np.ndarray  idat)
cpdef np.ndarray mus_rectangular2magnitudes(np.ndarray rdat, np.ndarray idat)
cpdef tuple rectangular2magnitudes(np.ndarray rdat, np.ndarray idat)
cpdef np.ndarray mus_polar2rectangular(np.ndarray rdat,  np.ndarray idat)
cpdef tuple polar2rectangular(np.ndarray rdat, np.ndarray idat)
cpdef np.ndarray mus_spectrum(np.ndarray rdat, np.ndarray  idat, np.ndarray  window, Spectrum norm_type=*)
cpdef tuple spectrum(np.ndarray rdat,np.ndarray idat,np.ndarray window, Spectrum norm_type=*)
cpdef np.ndarray mus_spectrum(np.ndarray rdat, np.ndarray  idat, np.ndarray  window, Spectrum norm_type=*)
cpdef np.ndarray convolution(np.ndarray rl1, np.ndarray  rl2, fft_size = *)
cpdef np.ndarray mus_convolution(np.ndarray  rl1, np.ndarray  rl2, fft_size=*)
cpdef np.ndarray autocorrelate(np.ndarray data)
cpdef np.ndarray mus_autocorrelate(np.ndarray data)
cpdef np.ndarray mus_correlate( np.ndarray data1, np.ndarray  data2)
cpdef np.ndarray correlate(np.ndarray data1, np.ndarray  data2)
cpdef np.ndarray mus_cepstrum( np.ndarray data)
cpdef np.ndarray cepstrum(np.ndarray data)
cpdef np.ndarray partials2wave(partials, np.ndarray wave=*, table_size=*, bint norm=* )
cpdef np.ndarray phase_partials2wave(partials, np.ndarray wave=*, table_size=*, bint norm=* )
cpdef np.ndarray partials2polynomial(partials, Polynomial kind=*)
cpdef np.ndarray normalize_partials(partials)
cpdef cython.double chebyshev_tu_sum(cython.double x, tcoeffs, ucoeffs)
cpdef cython.double chebyshev_t_sum(cython.double x, tcoeffs)
cpdef cython.double chebyshev_u_sum(cython.double x, ucoeffs)

# ---------------- clm gen ---------------- #

cpdef cython.double oscil(mus_any gen, cython.double fm=*, cython.double pm=*)
cpdef cython.double oscil_unmodulated(mus_any gen)
cpdef bint is_oscil(mus_any gen)


cpdef cython.double oscil_bank(mus_any gen)
cpdef bint is_oscil_bank(mus_any gen)

#
cpdef cython.double env(mus_any gen )
cpdef bint is_env(mus_any gen)
cpdef cython.double env_interp(cython.double x , mus_any env)
cpdef cython.double envelope_interp(cython.double x, mus_any env)
cpdef np.ndarray env_rates( mus_any gen)
cpdef cython.double env_any(mus_any gen , connection_function)

cpdef cython.double pulsed_env(mus_any gen, cython.double fm=*)
cpdef cython.double pulsed_env_unmodulated(mus_any gen)
cpdef bint is_pulsed_env(mus_any gen)

cpdef cython.double table_lookup(mus_any gen, cython.double fm=*)
cpdef cython.double table_lookup_unmodulated(mus_any gen)
cpdef bint is_table_lookup(mus_any gen)
cpdef mus_any make_table_lookup_with_env(cython.double frequency, envelope, size= *)

cpdef cython.double polywave(mus_any gen, cython.double fm=*)
cpdef cython.double polywave_unmodulated(mus_any gen)        
cpdef bint is_polywave(mus_any gen)

cpdef cython.double polyshape(mus_any gen, cython.double index=*, cython.double fm=*)
cpdef cython.double polyshape_unmodulated(mus_any gen, cython.double index=*)
cpdef bint is_polyshape(mus_any gen)

cpdef cython.double triangle_wave(mus_any gen, cython.double fm=*)
cpdef cython.double triangle_wave_unmodulated(mus_any gen)
cpdef bint is_triangle_wave(mus_any gen)

cpdef cython.double square_wave(mus_any gen, cython.double fm=*)
cpdef bint is_square_wave(mus_any gen)

cpdef mus_any make_sawtooth_wave(cython.double frequency, cython.double amplitude=*, cython.double phase=*)
cpdef cython.double sawtooth_wave(mus_any gen, cython.double fm =*)
cpdef bint is_sawtooth_wave(mus_any gen)

cpdef cython.double pulse_train(mus_any gen, cython.double fm=*)
cpdef cython.double pulse_train_unmodulated(mus_any gen)
cpdef bint is_pulse_train(mus_any gen)

cpdef cython.double ncos(mus_any gen, cython.double fm=*)
cpdef bint is_ncos(mus_any gen)

cpdef cython.double nsin(mus_any gen, cython.double fm=*)
cpdef bint is_nsin(mus_any gen )

cpdef cython.double nrxysin(mus_any gen, cython.double fm=*)
cpdef bint is_nrxysin(mus_any gen)

cpdef cython.double nrxycos(mus_any gen, cython.double fm=*)
cpdef bint is_nrxycos(mus_any gen)

cpdef cython.double rxykcos(mus_any gen, cython.double fm=*)
cpdef bint is_rxykcos(mus_any gen)

cpdef cython.double rxyksin(mus_any gen, cython.double fm=*)
cpdef bint is_rxyksin(mus_any gen)

cpdef cython.double ssb_am(mus_any gen, cython.double insig, cython.double fm=*)
cpdef cython.double ssb_am_unmodulated(mus_any gen, cython.double insig)
cpdef bint is_ssb_am(mus_any gen)

cpdef cython.double wave_train(mus_any gen, cython.double fm=*)
cpdef cython.double wave_train_unmodulated(mus_any gen)
cpdef bint is_wave_train(mus_any gen)

cpdef cython.double rand(mus_any gen, cython.double sweep=*)
cpdef cython.double rand_unmodulated(mus_any gen)
cpdef bint is_rand(mus_any gen)

cpdef rand_interp(mus_any gen, cython.double sweep=*)
cpdef rand_interp_unmodulated(mus_any gen)
cpdef bint is_rand_interp(mus_any gen)

cpdef cython.double one_pole(mus_any gen, cython.double insig)
cpdef bint is_one_pole(mus_any gen)

cpdef cython.double one_zero(mus_any gen, cython.double insig)
cpdef bint is_one_zero(mus_any gen)

cpdef cython.double two_pole(mus_any gen, cython.double insig)
cpdef bint is_two_pole(mus_any gen)

cpdef cython.double two_zero(mus_any gen, cython.double insig)
cpdef bint is_two_zero(mus_any gen)

cpdef cython.double formant(mus_any gen, cython.double insig, cython.double radians=*)
cpdef bint is_formant(mus_any gen)

cpdef cython.double formant_bank(mus_any gen, inputs)
cpdef bint is_formant_bank(mus_any gen)

cpdef firmant(mus_any gen, cython.double insig, cython.double radians=*)
cpdef is_firmant(mus_any gen)

cpdef cython.double filter(mus_any gen, cython.double insig)
cpdef bint is_filter(mus_any gen)

cpdef cython.double fir_filter(mus_any gen, cython.double insig)
cpdef bint is_fir_filter(mus_any gen)

cpdef cython.double iir_filter(mus_any gen, cython.double insig)
cpdef bint is_iir_filter(mus_any gen)

cpdef cython.double delay(mus_any gen, cython.double insig, cython.double pm=*)
cpdef cython.double delay_unmodulated(mus_any gen, cython.double insig)
cpdef bint is_delay(mus_any gen)
cpdef cython.double tap(mus_any gen, offset=*)
cpdef cython.double tap_unmodulated(mus_any gen)
cpdef bint is_tap(mus_any gen)
cpdef cython.double delay_tick(mus_any gen, cython.double insig )

cpdef cython.double comb(mus_any gen, cython.double insig, pm=*)
cpdef bint is_comb(mus_any gen)

cpdef cython.double comb_bank(mus_any gen, cython.double insig)
cpdef bint is_comb_bank(mus_any gen)

cpdef cython.double filtered_comb(mus_any gen, cython.double insig, cython.double pm=*)
cpdef cython.double filtered_comb_unmodulated(mus_any gen, cython.double insig)
cpdef bint is_filtered_comb(mus_any gen)

cpdef cython.double filtered_comb_bank(mus_any gen, cython.double insig)
cpdef bint is_filtered_comb_bank(mus_any gen)

cpdef cython.double notch(mus_any gen, cython.double insig, cython.double pm=*)
cpdef cython.double notch_unmodulated(mus_any gen, cython.double insig)
cpdef bint is_notch(mus_any gen)

cpdef cython.double all_pass(mus_any gen, cython.double insig, pm=*)
cpdef is_all_pass(mus_any gen)

cpdef cython.double all_pass_bank(mus_any gen, cython.double insig)
cpdef bint is_all_pass_bank(mus_any gen)

cpdef cython.double one_pole_all_pass(mus_any gen, cython.double insig)
cpdef bint is_one_pole_all_pass(mus_any gen)

cpdef cython.double moving_average(mus_any gen, cython.double  insig)
cpdef bint is_moving_average(mus_any gen)

cpdef cython.double moving_max(mus_any gen, cython.double insig)
cpdef bint is_moving_max(mus_any gen)

cpdef cython.double moving_norm(mus_any gen, cython.double insig)
cpdef is_moving_norm(mus_any gen)

cpdef cython.double asymmetric_fm(mus_any gen, cython.double index, cython.double fm=*)
cpdef cython.double asymmetric_fm_unmodulated(mus_any gen, cython.double index)
cpdef bint is_asymmetric_fm(mus_any gen)

cpdef cython.double file2sample(mus_any gen, cython.long loc, cython.int chan=*)
cpdef bint is_file2sample(mus_any gen)

cpdef cython.double sample2file(mus_any gen, cython.long samp, cython.int chan, cython.double val)
cpdef bint is_sample2file(mus_any gen)

cpdef file2frample(mus_any gen, cython.long loc)
cpdef is_file2frample(mus_any gen)

cpdef cython.double frample2file(mus_any gen, cython.long samp, vals)
cpdef bint is_frample2file(mus_any gen)
cpdef mus_any continue_frample2file(str name)

cpdef cython.double readin(mus_any gen)
cpdef is_readin(mus_any gen)

cpdef cython.double src(mus_any gen, cython.double sr_change=*)
cpdef bint is_src(mus_any gen)

cpdef cython.double convolve(mus_any gen)
cpdef bint is_convolve(mus_any gen)

cpdef cython.double granulate(mus_any gen)
cpdef bint is_granulate(mus_any e)

cpdef cython.double phase_vocoder(mus_any gen)
cpdef bint is_phase_vocoder(mus_any gen)
cpdef np.ndarray phase_vocoder_amp_increments(mus_any gen)
cpdef np.ndarray phase_vocoder_amps(mus_any gen)
cpdef np.ndarray phase_vocoder_freqs(mus_any gen)
cpdef np.ndarray phase_vocoder_phases(mus_any gen)
cpdef np.ndarray phase_vocoder_phase_increments(mus_any gen)

cpdef out_any(cython.long loc, cython.double data, cython.int channel, output=*)
cpdef outa(cython.long loc, cython.double data, output=*)
cpdef outb(cython.long loc, cython.double data, output=*)
cpdef outc(cython.long loc, cython.double data, output=*)
cpdef outd(cython.long loc, cython.double data, output=*)
cpdef in_any(cython.long loc, cython.int channel, inp)

cpdef ina(cython.long loc, inp)
cpdef inb(cython.long loc, inp)

cpdef out_bank(gens, cython.long loc, cython.double val)

cpdef cython.double locsig(mus_any gen, cython.long loc, cython.double val)
cpdef bint is_locsig(mus_any gen)
cpdef cython.double locsig_ref(mus_any gen, cython.int chan)
cpdef cython.double locsig_set(mus_any gen, cython.int chan, cython.double val)
cpdef cython.double locsig_reverb_ref(mus_any gen, cython.int chan)
cpdef cython.double locsig_reverb_set(mus_any gen, cython.int chan, cython.double val)
cpdef move_locsig(mus_any gen,cython.double degree, cython.double distance)

cpdef convolve_files(str file1, str file2, cython.double maxamp=*, str outputfile=*, sample_type=*, header_type=*)


#cpdef mus_any make_dcblock()
cpdef cython.double dcblock(mus_any gen, cython.double insig)

cpdef cython.double biquad(mus_any gen, cython.double insig)
cpdef bint is_biquad(mus_any gen)
cpdef biquad_set_resonance(mus_any gen, cython.double fc, cython.double radius, bint normalize=*)
cpdef biquad_set_equal_gain_zeroes(mus_any gen)
cpdef cython.double bes_j0(cython.double x)
cpdef cython.double bes_j1(cython.double x)
cpdef cython.double bes_jn(cython.int n, cython.double x)
cpdef cython.double bes_y0(cython.double x)  
cpdef cython.double bes_y1(cython.double x)
cpdef cython.double bes_yn(cython.int n, cython.double x)


cpdef cython.doublecomplex edot_product(cython.doublecomplex freq, np.ndarray data, size=*)

#cpdef mus_any make_oscil(cython.double frequency=*,cython.double  initial_phase = *)
#cpdef mus_any make_oscil_bank(freqs, phases, amps=*, bint stable=*)
#cpdef mus_any make_env(envelope, cython.double duration=*, cython.double scaler=*, cython.double offset=*, cython.double base=*, cython.int length=*)
#cpdef mus_any make_pulsed_env(envelope, cython.double duration , cython.double frequency )
#cpdef mus_any make_table_lookup(cython.double frequency=*, cython.double initial_phase=*, wave=*, cython.int size=*, interp interp_type=*)
#cpdef mus_any make_polywave(cython.double frequency, partials = *, polynomial kind=*, xcoeffs=*, ycoeffs=*)
#cpdef mus_any make_polyshape(cython.double frequency, cython.double initial_phase=*, coeffs = *, partials = *, polynomial kind=*)
#cpdef mus_any make_triangle_wave(cython.double frequency, cython.double amplitude=*, cython.double phase=*)
#cpdef mus_any make_square_wave(cython.double frequency , cython.double amplitude=*, cython.double phase=*)
#cpdef mus_any make_pulse_train(cython.double frequency=*, cython.double amplitude=*, cython.double phase=*)
#cpdef mus_any make_ncos(cython.double frequency, cython.int n=*)
#cpdef mus_any make_nsin(cython.double frequency, cython.int n =*)
#cpdef mus_any make_nrxysin( cython.double frequency,  cython.double ratio=*, cython.int n=*, cython.double r=*)
#cpdef mus_any make_nrxycos(cython.double frequency , cython.double ratio=*, cython.int n=*, cython.double r=*)
#cpdef mus_any make_rxykcos(cython.double frequency, cython.double phase=*, cython.double r=*, cython.double ratio=*)
#cpdef mus_any make_rxyksin(cython.double frequency, cython.double phase, cython.double r=*, cython.double ratio=*)
#cpdef mus_any make_ssb_am(cython.double frequency, cython.int order=*)
#cpdef mus_any make_wave_train(cython.double frequency, wave=*, cython.double initial_phase=*, interp interp_type=*)
#cpdef mus_any make_wave_train_with_env(cython.double frequency, envelope, size=*)
#cpdef mus_any make_rand(cython.double frequency, cython.double amplitude=*, distribution=*)
#cpdef mus_any make_rand_interp(cython.double frequency, cython.double amplitude=*, distribution=*)
#cpdef mus_any make_one_pole(cython.double a0, cython.double b1)
#cpdef mus_any make_one_zero(cython.double a0 , cython.double a1)
#cpdef make_two_pole(frequency=*, radius=*, a0=*,b1=*,b2=*)
#cpdef make_two_zero(frequency=*, radius=*, a0=*,a1=*,a2=*)
#cpdef mus_any make_formant(cython.double frequency, cython.double radius)
#cpdef mus_any make_formant_bank(list filters, amps=*)
#cpdef mus_any make_firmant(cython.double frequency, cython.double radius)
#cpdef mus_any make_filter(cython.int order, xcoeffs, ycoeffs)
#cpdef mus_any make_fir_filter(cython.int order, xcoeffs)
#cpdef mus_any make_iir_filter(cython.int order, ycoeffs)
#cpdef np.ndarray make_fir_coeffs(cython.int order, envelope)
#cpdef mus_any make_delay(cython.long size, initial_contents=*, initial_element=*, max_size=*, interp interp_type=*)
#cpdef mus_any make_comb(cython.double feedback=*,size=*, initial_contents=*, initial_element=*, max_size=*, interp interp_type=*)
#cpdef mus_any make_comb_bank(list combs)
#cpdef mus_any make_filtered_comb(cython.double feedback,cython.long size, mus_any filter, initial_contents=*,  cython.double initial_element=*, max_size=*, interp interp_type=*)
#cpdef mus_any make_filtered_comb_bank(list fcombs)
#cpdef mus_any make_notch(cython.double feedforward=*,size=*, initial_contents=*, cython.double initial_element=*, max_size=*,interp interp_type=*)
#cpdef mus_any make_all_pass(cython.double feedback, cython.double  feedforward, cython.long  size, initial_contents= *, cython.double  initial_element = *,  max_size= *, interp interp_type = *)
#cpdef mus_any make_all_pass_bank(list all_passes)
#cpdef mus_any make_one_pole_all_pass(cython.long size, cython.double coeff)
#cpdef mus_any make_moving_average(cython.long size, initial_contents=*, cython.double initial_element=*)
#cpdef mus_any make_moving_max(cython.long size, initial_contents=*, cython.double initial_element=*)
#cpdef mus_any make_moving_norm(cython.long size, initial_contents=*, cython.double scaler=*)
#cpdef mus_any make_asymmetric_fm(cython.double frequency, cython.double initial_phase=*, cython.double r=*, cython.double ratio=*)
#cpdef mus_any make_file2sample(str filename, buffer_size=*)
#cpdef mus_any make_sample2file(str filename, cython.int chans=*, sample sample_type=*, header header_type=*, comment=*)
#cpdef mus_any make_file2frample(str filename, buffer_size=*)
#cpdef mus_any make_frample2file(str filename, cython.int chans=*, sample sample_type=*, header header_type=*, comment=*)
#cpdef mus_any make_readin(str filename, cython.int chan=*, cython.long start=*, cython.int direction=*, buffer_size=*)
#cpdef mus_any make_src(inp , cython.double srate=*, cython.int width=*)
#cpdef mus_any make_convolve(inp, filt, cython.long fft_size=*, filter_size=*)
#cpdef mus_any make_granulate(inp, cython.double expansion=*, cython.double length=*, cython.double scaler=*, cython.double hop=*, cython.double ramp=*, cython.double jitter=*, cython.int max_size=*, edit=*)
#cpdef make_phase_vocoder(inp, cython.int fft_size=*, cython.int overlap=*, cython.int  interp=*, cython.double pitch=*, analyze=*, edit=*, synthesize=*)
#cpdef mus_any make_locsig(cython.double degree=*, cython.double distance=*,  cython.double reverb=*, output=*, revout=*, channels=*, reverb_channels=*,interp interp_type=*)



