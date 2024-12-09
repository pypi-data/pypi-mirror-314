cimport pysndlib.csndlib as csndlib

#==================================================================================
# The code is part of an attempt at translation of Bill Schottstedaet's clm 
# available at https://ccrma.stanford.edu/software/snd/sndlib/
#==================================================================================

cdef extern from "clm.h":
    """
    typedef mus_float_t (*connect_points_cb)(mus_float_t val);
    typedef mus_float_t (*input_cb)(void *arg, int direction);
    typedef int (*edit_cb)(void *closure);
    typedef bool (*analyze_cb)(void *arg, mus_float_t (*input)(void *arg1, int direction));
	typedef mus_float_t (*synthesize_cb)(void *arg);
	typedef void (*detour_cb)(mus_any *ptr, mus_long_t val);

    typedef mus_any* mus_any_ptr;
    typedef mus_any** mus_any_ptr_ptr;
    """
    
    
    ctypedef signed long int64_t
    ctypedef double mus_float_t
    ctypedef unsigned long uint64_t
    ctypedef int64_t mus_long_t 
    
    ctypedef struct mus_any_class:
        pass
        
    ctypedef struct mus_any:
        pass

    ctypedef enum mus_clm_extended_t:
        pass
        
    ctypedef enum mus_interp_t:
        pass
    
    ctypedef enum mus_fft_window_t:
        pass
    
    ctypedef enum mus_spectrum_t:
        pass
         
    ctypedef enum mus_polynomial_t:
        pass
        
        
    ctypedef enum mus_sample_t:
        pass
        
#     ctypedef enum mus_header_t:
#         pass
        
    ctypedef mus_any* mus_any_ptr
    
    ctypedef mus_any** mus_any_ptr_ptr
    
    ctypedef mus_float_t (*connect_points_cb)(mus_float_t val)
    ctypedef mus_float_t (*input_cb)(void *arg, int direction)
    ctypedef bint (*analyze_cb)(void *arg, mus_float_t (*input)(void *arg1, int direction))
    ctypedef int (*edit_cb)(void *closure)
    ctypedef void (*detour_cb)(mus_any *ptr, mus_long_t val)
    ctypedef mus_float_t (*synthesize_cb)(void *arg)

    void mus_initialize()

    int mus_make_generator_type()
    


    mus_any_class *mus_generator_class(mus_any *ptr)
    mus_any_class *mus_make_generator(int type, char *name, 
                         void (*release)(mus_any *ptr), 
                         char *(*describe)(mus_any *ptr), 
                         bint (*equalp)(mus_any *gen1, mus_any *gen2))

    void mus_generator_set_length(mus_any_class *p, mus_long_t (*length)(mus_any *ptr))
    void mus_generator_set_scaler(mus_any_class *p, mus_float_t (*scaler)(mus_any *ptr))
    void mus_generator_set_channels(mus_any_class *p, int (*channels)(mus_any *ptr))
    void mus_generator_set_location(mus_any_class *p, mus_long_t (*location)(mus_any *ptr))
    void mus_generator_set_set_location(mus_any_class *p, mus_long_t (*set_location)(mus_any *ptr, mus_long_t loc))
    void mus_generator_set_channel(mus_any_class *p, int (*channel)(mus_any *ptr))
    void mus_generator_set_file_name(mus_any_class *p, char *(*file_name)(mus_any *ptr))
    void mus_generator_set_extended_type(mus_any_class *p, mus_clm_extended_t extended_type)
    void mus_generator_set_read_sample(mus_any_class *p, mus_float_t (*read_sample)(mus_any *ptr, mus_long_t samp, int chan))
    void mus_generator_set_feeders(mus_any *g, 
                      mus_float_t (*feed)(void *arg, int direction),
                      mus_float_t (*block_feed)(void *arg, int direction, mus_float_t *block, mus_long_t start, mus_long_t end))
    void mus_generator_copy_feeders(mus_any *dest, mus_any *source)

    mus_float_t mus_radians_to_hz(mus_float_t radians)
    mus_float_t mus_hz_to_radians(mus_float_t hz)
    mus_float_t mus_degrees_to_radians(mus_float_t degrees)
    mus_float_t mus_radians_to_degrees(mus_float_t radians)
    mus_float_t mus_db_to_linear(mus_float_t x)
    mus_float_t mus_linear_to_db(mus_float_t x)
    mus_float_t mus_odd_multiple(mus_float_t x, mus_float_t y)
    mus_float_t mus_even_multiple(mus_float_t x, mus_float_t y)
    mus_float_t mus_odd_weight(mus_float_t x)
    mus_float_t mus_even_weight(mus_float_t x)
    const char *mus_interp_type_to_string(int type)

    mus_float_t mus_srate()
    mus_float_t mus_set_srate(mus_float_t val)
    mus_long_t mus_seconds_to_samples(mus_float_t secs)
    mus_float_t mus_samples_to_seconds(mus_long_t samps)
    int mus_array_print_length()
    int mus_set_array_print_length(int val)
    mus_float_t mus_float_equal_fudge_factor()
    mus_float_t mus_set_float_equal_fudge_factor(mus_float_t val)

    mus_float_t mus_ring_modulate(mus_float_t s1, mus_float_t s2)
    mus_float_t mus_amplitude_modulate(mus_float_t s1, mus_float_t s2, mus_float_t s3)
    mus_float_t mus_contrast_enhancement(mus_float_t sig, mus_float_t index)
    mus_float_t mus_dot_product(mus_float_t *data1, mus_float_t *data2, mus_long_t size)
#     #if HAVE_COMPLEX_TRIG
#     complex double mus_edot_product(complex double freq, complex double *data, mus_long_t size)
#     #endif

    bint mus_arrays_are_equal(mus_float_t *arr1, mus_float_t *arr2, mus_float_t fudge, mus_long_t len)
    mus_float_t mus_polynomial(mus_float_t *coeffs, mus_float_t x, int ncoeffs)
    void mus_rectangular_to_polar(mus_float_t *rl, mus_float_t *im, mus_long_t size)
    void mus_rectangular_to_magnitudes(mus_float_t *rl, mus_float_t *im, mus_long_t size)
    void mus_polar_to_rectangular(mus_float_t *rl, mus_float_t *im, mus_long_t size)
    mus_float_t mus_array_interp(mus_float_t *wave, mus_float_t phase, mus_long_t size)
    mus_float_t mus_bessi0(mus_float_t x)
    mus_float_t mus_interpolate(mus_interp_t type, mus_float_t x, mus_float_t *table, mus_long_t table_size, mus_float_t y)
    bint mus_is_interp_type(int val)
    bint mus_is_fft_window(int val)

    int mus_sample_type_zero(mus_sample_t samp_type)
    mus_float_t (*mus_run_function(mus_any *g))(mus_any *gen, mus_float_t arg1, mus_float_t arg2)
    mus_float_t (*mus_run1_function(mus_any *g))(mus_any *gen, mus_float_t arg)


#     /* -------- generic functions -------- */

    int mus_type(mus_any *ptr)
    void mus_free(mus_any *ptr)
    char *mus_describe(mus_any *gen)
    bint mus_equalp(mus_any *g1, mus_any *g2)
    mus_float_t mus_phase(mus_any *gen)
    mus_float_t mus_set_phase(mus_any *gen, mus_float_t val)
    mus_float_t mus_set_frequency(mus_any *gen, mus_float_t val)
    mus_float_t mus_frequency(mus_any *gen)
    mus_float_t mus_run(mus_any *gen, mus_float_t arg1, mus_float_t arg2)
    mus_long_t mus_length(mus_any *gen)
    mus_long_t mus_set_length(mus_any *gen, mus_long_t len)
    mus_long_t mus_order(mus_any *gen)
    mus_float_t *mus_data(mus_any *gen)
    mus_float_t *mus_set_data(mus_any *gen, mus_float_t *data)
    const char *mus_name(mus_any *ptr)
    mus_float_t mus_scaler(mus_any *gen)
    mus_float_t mus_set_scaler(mus_any *gen, mus_float_t val)
    mus_float_t mus_offset(mus_any *gen)
    mus_float_t mus_set_offset(mus_any *gen, mus_float_t val)
    mus_float_t mus_width(mus_any *gen)
    mus_float_t mus_set_width(mus_any *gen, mus_float_t val)
    char *mus_file_name(mus_any *ptr)
    void mus_reset(mus_any *ptr)
    mus_any *mus_copy(mus_any *gen)
    mus_float_t *mus_xcoeffs(mus_any *ptr)
    mus_float_t *mus_ycoeffs(mus_any *ptr)
    mus_float_t mus_xcoeff(mus_any *ptr, int index)
    mus_float_t mus_set_xcoeff(mus_any *ptr, int index, mus_float_t val)
    mus_float_t mus_ycoeff(mus_any *ptr, int index)
    mus_float_t mus_set_ycoeff(mus_any *ptr, int index, mus_float_t val)
    mus_float_t mus_increment(mus_any *rd)
    mus_float_t mus_set_increment(mus_any *rd, mus_float_t dir)
    mus_long_t mus_location(mus_any *rd)
    mus_long_t mus_set_location(mus_any *rd, mus_long_t loc)
    int mus_channel(mus_any *rd)
    int mus_channels(mus_any *ptr)
    int mus_position(mus_any *ptr) #/* only C, envs (snd-env.c), shares slot with mus_channels */
    int mus_interp_type(mus_any *ptr)
    mus_long_t mus_ramp(mus_any *ptr)
    mus_long_t mus_set_ramp(mus_any *ptr, mus_long_t val)
    mus_long_t mus_hop(mus_any *ptr)
    mus_long_t mus_set_hop(mus_any *ptr, mus_long_t val)
    mus_float_t mus_feedforward(mus_any *gen)
    mus_float_t mus_set_feedforward(mus_any *gen, mus_float_t val)
    mus_float_t mus_feedback(mus_any *rd)
    mus_float_t mus_set_feedback(mus_any *rd, mus_float_t dir)

    bint mus_phase_exists(mus_any *gen)
    bint mus_frequency_exists(mus_any *gen)
    bint mus_length_exists(mus_any *gen)
    bint mus_order_exists(mus_any *gen)
    bint mus_data_exists(mus_any *gen)
    bint mus_name_exists(mus_any *gen)
    bint mus_scaler_exists(mus_any *gen)
    bint mus_offset_exists(mus_any *gen)
    bint mus_width_exists(mus_any *gen)
    bint mus_file_name_exists(mus_any *gen)
    bint mus_xcoeffs_exists(mus_any *gen)
    bint mus_ycoeffs_exists(mus_any *gen)
    bint mus_increment_exists(mus_any *gen)
    bint mus_location_exists(mus_any *gen)
    bint mus_channel_exists(mus_any *gen)
    bint mus_channels_exists(mus_any *gen)
    bint mus_position_exists(mus_any *gen)
    bint mus_interp_type_exists(mus_any *gen)
    bint mus_ramp_exists(mus_any *gen)
    bint mus_hop_exists(mus_any *gen)
    bint mus_feedforward_exists(mus_any *gen)
    bint mus_feedback_exists(mus_any *gen)


#     /* -------- generators -------- */

    mus_float_t mus_oscil(mus_any *o, mus_float_t fm, mus_float_t pm)
    mus_float_t mus_oscil_unmodulated(mus_any *ptr)
    mus_float_t mus_oscil_fm(mus_any *ptr, mus_float_t fm)
    mus_float_t mus_oscil_pm(mus_any *ptr, mus_float_t pm)
    bint mus_is_oscil(mus_any *ptr)
    mus_any *mus_make_oscil(mus_float_t freq, mus_float_t phase)

    bint mus_is_oscil_bank(mus_any *ptr)
    mus_float_t mus_oscil_bank(mus_any *ptr)
    mus_any *mus_make_oscil_bank(int size, mus_float_t *freqs, mus_float_t *phases, mus_float_t *amps, bint stable)

    mus_any *mus_make_ncos(mus_float_t freq, int n)
    mus_float_t mus_ncos(mus_any *ptr, mus_float_t fm)
    bint mus_is_ncos(mus_any *ptr)

    mus_any *mus_make_nsin(mus_float_t freq, int n)
    mus_float_t mus_nsin(mus_any *ptr, mus_float_t fm)
    bint mus_is_nsin(mus_any *ptr)

    mus_any *mus_make_nrxysin(mus_float_t frequency, mus_float_t y_over_x, int n, mus_float_t r)
    mus_float_t mus_nrxysin(mus_any *ptr, mus_float_t fm)
    bint mus_is_nrxysin(mus_any *ptr)

    mus_any *mus_make_nrxycos(mus_float_t frequency, mus_float_t y_over_x, int n, mus_float_t r)
    mus_float_t mus_nrxycos(mus_any *ptr, mus_float_t fm)
    bint mus_is_nrxycos(mus_any *ptr)

    mus_any *mus_make_rxykcos(mus_float_t freq, mus_float_t phase, mus_float_t r, mus_float_t ratio)
    mus_float_t mus_rxykcos(mus_any *ptr, mus_float_t fm)
    bint mus_is_rxykcos(mus_any *ptr)

    mus_any *mus_make_rxyksin(mus_float_t freq, mus_float_t phase, mus_float_t r, mus_float_t ratio)
    mus_float_t mus_rxyksin(mus_any *ptr, mus_float_t fm)
    bint mus_is_rxyksin(mus_any *ptr)

    mus_float_t mus_delay(mus_any *gen, mus_float_t input, mus_float_t pm)
    mus_float_t mus_delay_unmodulated(mus_any *ptr, mus_float_t input)
    mus_float_t mus_tap(mus_any *gen, mus_float_t loc)
    mus_float_t mus_tap_unmodulated(mus_any *gen)
    mus_any *mus_make_delay(int size, mus_float_t *line, int line_size, mus_interp_t type)
    bint mus_is_delay(mus_any *ptr)
    bint mus_is_tap(mus_any *ptr)
    mus_float_t mus_delay_tick(mus_any *ptr, mus_float_t input)
    mus_float_t mus_delay_unmodulated_noz(mus_any *ptr, mus_float_t input)

    mus_float_t mus_comb(mus_any *gen, mus_float_t input, mus_float_t pm)
    mus_float_t mus_comb_unmodulated(mus_any *gen, mus_float_t input)
    mus_any *mus_make_comb(mus_float_t scaler, int size, mus_float_t *line, int line_size, mus_interp_t type)
    bint mus_is_comb(mus_any *ptr)
    mus_float_t mus_comb_unmodulated_noz(mus_any *ptr, mus_float_t input)

    mus_float_t mus_comb_bank(mus_any *bank, mus_float_t inval)
    mus_any *mus_make_comb_bank(int size, mus_any **combs)
    bint mus_is_comb_bank(mus_any *g)

    mus_float_t mus_notch(mus_any *gen, mus_float_t input, mus_float_t pm)
    mus_float_t mus_notch_unmodulated(mus_any *gen, mus_float_t input)
    mus_any *mus_make_notch(mus_float_t scaler, int size, mus_float_t *line, int line_size, mus_interp_t type)
    bint mus_is_notch(mus_any *ptr)

    mus_float_t mus_all_pass(mus_any *gen, mus_float_t input, mus_float_t pm)
    mus_float_t mus_all_pass_unmodulated(mus_any *gen, mus_float_t input)
    mus_any *mus_make_all_pass(mus_float_t backward, mus_float_t forward, int size, mus_float_t *line, int line_size, mus_interp_t type)
    bint mus_is_all_pass(mus_any *ptr)
    mus_float_t mus_all_pass_unmodulated_noz(mus_any *ptr, mus_float_t input)

    mus_float_t mus_all_pass_bank(mus_any *bank, mus_float_t inval)
    mus_any *mus_make_all_pass_bank(int size, mus_any **combs)
    bint mus_is_all_pass_bank(mus_any *g)

    mus_any *mus_make_moving_average(int size, mus_float_t *line)
    mus_any *mus_make_moving_average_with_initial_sum(int size, mus_float_t *line, mus_float_t sum)
    bint mus_is_moving_average(mus_any *ptr)
    mus_float_t mus_moving_average(mus_any *ptr, mus_float_t input)

    mus_any *mus_make_moving_max(int size, mus_float_t *line)
    bint mus_is_moving_max(mus_any *ptr)
    mus_float_t mus_moving_max(mus_any *ptr, mus_float_t input)

    mus_any *mus_make_moving_norm(int size, mus_float_t *line, mus_float_t norm)
    bint mus_is_moving_norm(mus_any *ptr)
    mus_float_t mus_moving_norm(mus_any *ptr, mus_float_t input)

    mus_float_t mus_table_lookup(mus_any *gen, mus_float_t fm)
    mus_float_t mus_table_lookup_unmodulated(mus_any *gen)
    mus_any *mus_make_table_lookup(mus_float_t freq, mus_float_t phase, mus_float_t *wave, mus_long_t wave_size, mus_interp_t type)
    bint mus_is_table_lookup(mus_any *ptr)
    mus_float_t *mus_partials_to_wave(mus_float_t *partial_data, int partials, mus_float_t *table, mus_long_t table_size, bint normalize)
    mus_float_t *mus_phase_partials_to_wave(mus_float_t *partial_data, int partials, mus_float_t *table, mus_long_t table_size, bint normalize)

    mus_float_t mus_sawtooth_wave(mus_any *gen, mus_float_t fm)
    mus_any *mus_make_sawtooth_wave(mus_float_t freq, mus_float_t amp, mus_float_t phase)
    bint mus_is_sawtooth_wave(mus_any *gen)

    mus_float_t mus_square_wave(mus_any *gen, mus_float_t fm)
    mus_any *mus_make_square_wave(mus_float_t freq, mus_float_t amp, mus_float_t phase)
    bint mus_is_square_wave(mus_any *gen)

    mus_float_t mus_triangle_wave(mus_any *gen, mus_float_t fm)
    mus_any *mus_make_triangle_wave(mus_float_t freq, mus_float_t amp, mus_float_t phase)
    bint mus_is_triangle_wave(mus_any *gen)
    mus_float_t mus_triangle_wave_unmodulated(mus_any *ptr)

    mus_float_t mus_pulse_train(mus_any *gen, mus_float_t fm)
    mus_any *mus_make_pulse_train(mus_float_t freq, mus_float_t amp, mus_float_t phase)
    bint mus_is_pulse_train(mus_any *gen)
    mus_float_t mus_pulse_train_unmodulated(mus_any *ptr)

    void mus_set_rand_seed(uint64_t seed)
    uint64_t mus_rand_seed()
    mus_float_t mus_random(mus_float_t amp)
    mus_float_t mus_frandom(mus_float_t amp)
    int mus_irandom(int amp)

    mus_float_t mus_rand(mus_any *gen, mus_float_t fm)
    mus_any *mus_make_rand(mus_float_t freq, mus_float_t base)
    bint mus_is_rand(mus_any *ptr)
    mus_any *mus_make_rand_with_distribution(mus_float_t freq, mus_float_t base, mus_float_t *distribution, int distribution_size)


    mus_float_t mus_rand_interp(mus_any *gen, mus_float_t fm)
    mus_any *mus_make_rand_interp(mus_float_t freq, mus_float_t base)
    bint mus_is_rand_interp(mus_any *ptr)
    mus_any *mus_make_rand_interp_with_distribution(mus_float_t freq, mus_float_t base, mus_float_t *distribution, int distribution_size)
    mus_float_t mus_rand_interp_unmodulated(mus_any *ptr)
    mus_float_t mus_rand_unmodulated(mus_any *ptr)

    mus_float_t mus_asymmetric_fm(mus_any *gen, mus_float_t index, mus_float_t fm)
    mus_float_t mus_asymmetric_fm_unmodulated(mus_any *gen, mus_float_t index)
    mus_any *mus_make_asymmetric_fm(mus_float_t freq, mus_float_t phase, mus_float_t r, mus_float_t ratio)
    bint mus_is_asymmetric_fm(mus_any *ptr)

    mus_float_t mus_one_zero(mus_any *gen, mus_float_t input)
    mus_any *mus_make_one_zero(mus_float_t a0, mus_float_t a1)
    bint mus_is_one_zero(mus_any *gen)

    mus_float_t mus_one_pole(mus_any *gen, mus_float_t input)
    mus_any *mus_make_one_pole(mus_float_t a0, mus_float_t b1)
    bint mus_is_one_pole(mus_any *gen)

    mus_float_t mus_two_zero(mus_any *gen, mus_float_t input)
    mus_any *mus_make_two_zero(mus_float_t a0, mus_float_t a1, mus_float_t a2)
    bint mus_is_two_zero(mus_any *gen)
    mus_any *mus_make_two_zero_from_frequency_and_radius(mus_float_t frequency, mus_float_t radius)

    mus_float_t mus_two_pole(mus_any *gen, mus_float_t input)
    mus_any *mus_make_two_pole(mus_float_t a0, mus_float_t b1, mus_float_t b2)
    bint mus_is_two_pole(mus_any *gen)
    mus_any *mus_make_two_pole_from_frequency_and_radius(mus_float_t frequency, mus_float_t radius)

    mus_float_t mus_one_pole_all_pass(mus_any *f, mus_float_t input)
    mus_any *mus_make_one_pole_all_pass(int size, mus_float_t coeff)
    bint mus_is_one_pole_all_pass(mus_any *ptr)

    mus_float_t mus_formant(mus_any *ptr, mus_float_t input) 
    mus_any *mus_make_formant(mus_float_t frequency, mus_float_t radius)
    bint mus_is_formant(mus_any *ptr)
    mus_float_t mus_set_formant_frequency(mus_any *ptr, mus_float_t freq_in_hz)
    void mus_set_formant_radius_and_frequency(mus_any *ptr, mus_float_t radius, mus_float_t frequency)
    mus_float_t mus_formant_with_frequency(mus_any *ptr, mus_float_t input, mus_float_t freq_in_radians)

    mus_float_t mus_formant_bank(mus_any *bank, mus_float_t inval)
    mus_float_t mus_formant_bank_with_inputs(mus_any *bank, mus_float_t *inval)
    mus_any *mus_make_formant_bank(int size, mus_any **formants, mus_float_t *amps)
    bint mus_is_formant_bank(mus_any *g)

    mus_float_t mus_firmant(mus_any *ptr, mus_float_t input)
    mus_any *mus_make_firmant(mus_float_t frequency, mus_float_t radius)
    bint mus_is_firmant(mus_any *ptr)
    mus_float_t mus_firmant_with_frequency(mus_any *ptr, mus_float_t input, mus_float_t freq_in_radians)

    mus_float_t mus_filter(mus_any *ptr, mus_float_t input)
    mus_any *mus_make_filter(int order, mus_float_t *xcoeffs, mus_float_t *ycoeffs, mus_float_t *state)
    bint mus_is_filter(mus_any *ptr)

    mus_float_t mus_fir_filter(mus_any *ptr, mus_float_t input)
    mus_any *mus_make_fir_filter(int order, mus_float_t *xcoeffs, mus_float_t *state)
    bint mus_is_fir_filter(mus_any *ptr)

    mus_float_t mus_iir_filter(mus_any *ptr, mus_float_t input)
    mus_any *mus_make_iir_filter(int order, mus_float_t *ycoeffs, mus_float_t *state)
    bint mus_is_iir_filter(mus_any *ptr)
    mus_float_t *mus_make_fir_coeffs(int order, mus_float_t *env, mus_float_t *aa)

    mus_float_t *mus_filter_set_xcoeffs(mus_any *ptr, mus_float_t *new_data)
    mus_float_t *mus_filter_set_ycoeffs(mus_any *ptr, mus_float_t *new_data)
    int mus_filter_set_order(mus_any *ptr, int order)

    mus_float_t mus_filtered_comb(mus_any *ptr, mus_float_t input, mus_float_t pm)
    mus_float_t mus_filtered_comb_unmodulated(mus_any *ptr, mus_float_t input)
    bint mus_is_filtered_comb(mus_any *ptr)
    mus_any *mus_make_filtered_comb(mus_float_t scaler, int size, mus_float_t *line, int line_size, mus_interp_t type, mus_any *filt)

    mus_float_t mus_filtered_comb_bank(mus_any *bank, mus_float_t inval)
    mus_any *mus_make_filtered_comb_bank(int size, mus_any **combs)
    bint mus_is_filtered_comb_bank(mus_any *g)

    mus_float_t mus_wave_train(mus_any *gen, mus_float_t fm)
    mus_float_t mus_wave_train_unmodulated(mus_any *gen)
    mus_any *mus_make_wave_train(mus_float_t freq, mus_float_t phase, mus_float_t *wave, mus_long_t wsize, mus_interp_t type)
    bint mus_is_wave_train(mus_any *gen)

    mus_float_t *mus_partials_to_polynomial(int npartials, mus_float_t *partials, mus_polynomial_t kind)
    mus_float_t *mus_normalize_partials(int num_partials, mus_float_t *partials)

    mus_any *mus_make_polyshape(mus_float_t frequency, mus_float_t phase, mus_float_t *coeffs, int size, int cheby_choice)
    mus_float_t mus_polyshape(mus_any *ptr, mus_float_t index, mus_float_t fm)
    mus_float_t mus_polyshape_unmodulated(mus_any *ptr, mus_float_t index)
    #define mus_polyshape_no_input(Obj) mus_polyshape(Obj, 1.0, 0.0)
    bint mus_is_polyshape(mus_any *ptr)

    mus_any *mus_make_polywave(mus_float_t frequency, mus_float_t *coeffs, int n, int cheby_choice)
    mus_any *mus_make_polywave_tu(mus_float_t frequency, mus_float_t *tcoeffs, mus_float_t *ucoeffs, int n)
    bint mus_is_polywave(mus_any *ptr)
    mus_float_t mus_polywave_unmodulated(mus_any *ptr)
    mus_float_t mus_polywave(mus_any *ptr, mus_float_t fm)
    mus_float_t mus_chebyshev_t_sum(mus_float_t x, int n, mus_float_t *tn)
    mus_float_t mus_chebyshev_u_sum(mus_float_t x, int n, mus_float_t *un)
    mus_float_t mus_chebyshev_tu_sum(mus_float_t x, int n, mus_float_t *tn, mus_float_t *un)
    mus_float_t (*mus_polywave_function(mus_any *g))(mus_any *gen, mus_float_t fm)

    mus_float_t mus_env(mus_any *ptr)
    mus_any *mus_make_env(mus_float_t *brkpts, int npts, mus_float_t scaler, mus_float_t offset, mus_float_t base, 
                 mus_float_t duration, mus_long_t end, mus_float_t *odata)
    bint mus_is_env(mus_any *ptr)
    mus_float_t mus_env_interp(mus_float_t x, mus_any *env)
    mus_long_t *mus_env_passes(mus_any *gen)        #/* for Snd */
    mus_float_t *mus_env_rates(mus_any *gen)        #/* for Snd */
    mus_float_t mus_env_offset(mus_any *gen)        #/* for Snd */
    mus_float_t mus_env_scaler(mus_any *gen)        #/* for Snd */
    mus_float_t mus_env_initial_power(mus_any *gen) #/* for Snd */
    int mus_env_breakpoints(mus_any *gen)     # /* for Snd */
    mus_float_t mus_env_any(mus_any *e, mus_float_t (*connect_points)(mus_float_t val))
    mus_float_t (*mus_env_function(mus_any *g))(mus_any *gen)


    mus_any *mus_make_pulsed_env(mus_any *e, mus_any *p)
    bint mus_is_pulsed_env(mus_any *ptr)
    mus_float_t mus_pulsed_env(mus_any *pl, mus_float_t inval)
    mus_float_t mus_pulsed_env_unmodulated(mus_any *pl)

    bint mus_is_file_to_sample(mus_any *ptr)
    mus_any *mus_make_file_to_sample(const char *filename)
    mus_any *mus_make_file_to_sample_with_buffer_size(const char *filename, mus_long_t buffer_size)
    mus_float_t mus_file_to_sample(mus_any *ptr, mus_long_t samp, int chan)

    mus_float_t mus_readin(mus_any *rd)
    mus_any *mus_make_readin_with_buffer_size(const char *filename, int chan, mus_long_t start, int direction, mus_long_t buffer_size)
    #define mus_make_readin(Filename, Chan, Start, Direction) mus_make_readin_with_buffer_size(Filename, Chan, Start, Direction, mus_file_buffer_size())
    bint mus_is_readin(mus_any *ptr)

    bint mus_is_output(mus_any *ptr)
    bint mus_is_input(mus_any *ptr)
    mus_float_t mus_in_any(mus_long_t frample, int chan, mus_any *IO)
    bint mus_in_any_is_safe(mus_any *IO)

    #/* new 6.0 */
    mus_float_t *mus_file_to_frample(mus_any *ptr, mus_long_t samp, mus_float_t *f)
    mus_any *mus_make_file_to_frample(const char *filename)
    bint mus_is_file_to_frample(mus_any *ptr)
    mus_any *mus_make_file_to_frample_with_buffer_size(const char *filename, mus_long_t buffer_size)
    mus_float_t *mus_frample_to_frample(mus_float_t *matrix, int mx_chans, mus_float_t *in_samps, int in_chans, mus_float_t *out_samps, int out_chans)

    bint mus_is_frample_to_file(mus_any *ptr)
    mus_float_t *mus_frample_to_file(mus_any *ptr, mus_long_t samp, mus_float_t *data)
    mus_any *mus_make_frample_to_file_with_comment(const char *filename, int chans, mus_sample_t samp_type, csndlib.mus_header_t head_type, const char *comment)
    #define mus_make_frample_to_file(Filename, Chans, SampType, HeadType) mus_make_frample_to_file_with_comment(Filename, Chans, SampType, HeadType, NULL)
    mus_any *mus_continue_frample_to_file(const char *filename)

    void mus_file_mix_with_reader_and_writer(mus_any *outf, mus_any *inf,
                            mus_long_t out_start, mus_long_t out_framples, mus_long_t in_start, 
                            mus_float_t *mx, int mx_chans, mus_any ***envs)
    void mus_file_mix(const char *outfile, const char *infile, 
                 mus_long_t out_start, mus_long_t out_framples, mus_long_t in_start, 
                 mus_float_t *mx, int mx_chans, mus_any ***envs)

    bint mus_is_sample_to_file(mus_any *ptr)
    mus_any *mus_make_sample_to_file_with_comment(const char *filename, int out_chans, mus_sample_t samp_type, csndlib.mus_header_t head_type, const char *comment)
    #define mus_make_sample_to_file(Filename, Chans, SampType, HeadType) mus_make_sample_to_file_with_comment(Filename, Chans, SampType, HeadType, NULL)
    mus_float_t mus_sample_to_file(mus_any *ptr, mus_long_t samp, int chan, mus_float_t val)
    mus_any *mus_continue_sample_to_file(const char *filename)
    int mus_close_file(mus_any *ptr)
    mus_any *mus_sample_to_file_add(mus_any *out1, mus_any *out2)

    mus_float_t mus_out_any(mus_long_t frample, mus_float_t val, int chan, mus_any *IO)
    mus_float_t mus_safe_out_any_to_file(mus_long_t samp, mus_float_t val, int chan, mus_any *IO)
    bint mus_out_any_is_safe(mus_any *IO)
    mus_float_t mus_out_any_to_file(mus_any *ptr, mus_long_t samp, int chan, mus_float_t val)

    void mus_locsig(mus_any *ptr, mus_long_t loc, mus_float_t val)
    mus_any *mus_make_locsig(mus_float_t degree, mus_float_t distance, mus_float_t reverb, int chans, 
                    mus_any *output, int rev_chans, mus_any *revput, mus_interp_t type)
    bint mus_is_locsig(mus_any *ptr)
    mus_float_t mus_locsig_ref(mus_any *ptr, int chan)
    mus_float_t mus_locsig_set(mus_any *ptr, int chan, mus_float_t val)
    mus_float_t mus_locsig_reverb_ref(mus_any *ptr, int chan)
    mus_float_t mus_locsig_reverb_set(mus_any *ptr, int chan, mus_float_t val)
    void mus_move_locsig(mus_any *ptr, mus_float_t degree, mus_float_t distance)
    mus_float_t *mus_locsig_outf(mus_any *ptr)
    mus_float_t *mus_locsig_revf(mus_any *ptr)
    void *mus_locsig_closure(mus_any *ptr)
    void mus_locsig_set_detour(mus_any *ptr, void (*detour)(mus_any *ptr, mus_long_t val))
    int mus_locsig_channels(mus_any *ptr)
    int mus_locsig_reverb_channels(mus_any *ptr)

    bint mus_is_move_sound(mus_any *ptr)
    mus_float_t mus_move_sound(mus_any *ptr, mus_long_t loc, mus_float_t val)
    mus_any *mus_make_move_sound(mus_long_t start, mus_long_t end, int out_channels, int rev_channels,
                    mus_any *doppler_delay, mus_any *doppler_env, mus_any *rev_env,
                    mus_any **out_delays, mus_any **out_envs, mus_any **rev_envs,
                    int *out_map, mus_any *output, mus_any *revput, bint free_arrays, bint free_gens)
    mus_float_t *mus_move_sound_outf(mus_any *ptr)
    mus_float_t *mus_move_sound_revf(mus_any *ptr)
    void *mus_move_sound_closure(mus_any *ptr)
    void mus_move_sound_set_detour(mus_any *ptr, void (*detour)(mus_any *ptr, mus_long_t val))
    int mus_move_sound_channels(mus_any *ptr)
    int mus_move_sound_reverb_channels(mus_any *ptr)

    mus_any *mus_make_src(mus_float_t (*input)(void *arg, int direction), mus_float_t srate, int width, void *closure)
    mus_any *mus_make_src_with_init(mus_float_t (*input)(void *arg, int direction), mus_float_t srate, int width, void *closure, void (*init)(void *p, mus_any *g))
    mus_float_t mus_src(mus_any *srptr, mus_float_t sr_change, mus_float_t (*input)(void *arg, int direction))
    bint mus_is_src(mus_any *ptr)
    mus_float_t *mus_src_20(mus_any *srptr, mus_float_t *in_data, mus_long_t dur)
    mus_float_t *mus_src_05(mus_any *srptr, mus_float_t *in_data, mus_long_t dur)
    void mus_src_to_buffer(mus_any *srptr, mus_float_t (*input)(void *arg, int direction), mus_float_t *out_data, mus_long_t dur)
    void mus_src_init(mus_any *ptr)

    bint mus_is_convolve(mus_any *ptr)
    mus_float_t mus_convolve(mus_any *ptr, mus_float_t (*input)(void *arg, int direction))
    mus_any *mus_make_convolve(mus_float_t (*input)(void *arg, int direction), mus_float_t *filter, mus_long_t fftsize, mus_long_t filtersize, void *closure)

    mus_float_t *mus_spectrum(mus_float_t *rdat, mus_float_t *idat, mus_float_t *window, mus_long_t n, mus_spectrum_t type)
    void mus_fft(mus_float_t *rl, mus_float_t *im, mus_long_t n, int di)
    mus_float_t *mus_make_fft_window(mus_fft_window_t type, mus_long_t size, mus_float_t beta)
    mus_float_t *mus_make_fft_window_with_window(mus_fft_window_t type, mus_long_t size, mus_float_t beta, mus_float_t mu, mus_float_t *window)
    const char *mus_fft_window_name(mus_fft_window_t win)
    const char **mus_fft_window_names()

    mus_float_t *mus_autocorrelate(mus_float_t *data, mus_long_t n)
    mus_float_t *mus_correlate(mus_float_t *data1, mus_float_t *data2, mus_long_t n)
    mus_float_t *mus_convolution(mus_float_t *rl1, mus_float_t *rl2, mus_long_t n)
    void mus_convolve_files(const char *file1, const char *file2, mus_float_t maxamp, const char *output_file)
    mus_float_t *mus_cepstrum(mus_float_t *data, mus_long_t n)

    bint mus_is_granulate(mus_any *ptr)
    mus_float_t mus_granulate(mus_any *ptr, mus_float_t (*input)(void *arg, int direction))
    mus_float_t mus_granulate_with_editor(mus_any *ptr, mus_float_t (*input)(void *arg, int direction), int (*edit)(void *closure))
    mus_any *mus_make_granulate(mus_float_t (*input)(void *arg, int direction), 
                       mus_float_t expansion, mus_float_t length, mus_float_t scaler, 
                       mus_float_t hop, mus_float_t ramp, mus_float_t jitter, int max_size, 
                       int (*edit)(void *closure),
                       void *closure)
    int mus_granulate_grain_max_length(mus_any *ptr)
    void mus_granulate_set_edit_function(mus_any *ptr, int (*edit)(void *closure))

    mus_long_t mus_set_file_buffer_size(mus_long_t size)
    mus_long_t mus_file_buffer_size()

    mus_float_t mus_apply(mus_any *gen, mus_float_t f1, mus_float_t f2)

    bint mus_is_phase_vocoder(mus_any *ptr)
    mus_any *mus_make_phase_vocoder(mus_float_t (*input)(void *arg, int direction), 
                       int fftsize, int overlap, int interp,
                       mus_float_t pitch,
                       bint (*analyze)(void *arg, mus_float_t (*input)(void *arg1, int direction)),
                       int (*edit)(void *arg), #/* return value is ignored (int return type is intended to be consistent with granulate) */
                       mus_float_t (*synthesize)(void *arg), 
                       void *closure)
    mus_float_t mus_phase_vocoder(mus_any *ptr, mus_float_t (*input)(void *arg, int direction))
    mus_float_t mus_phase_vocoder_with_editors(mus_any *ptr, 
                        mus_float_t (*input)(void *arg, int direction),
                        bint (*analyze)(void *arg, mus_float_t (*input)(void *arg1, int direction)),
                        int (*edit)(void *arg), 
                        mus_float_t (*synthesize)(void *arg))

    mus_float_t *mus_phase_vocoder_amp_increments(mus_any *ptr)
    mus_float_t *mus_phase_vocoder_amps(mus_any *ptr)
    mus_float_t *mus_phase_vocoder_freqs(mus_any *ptr)
    mus_float_t *mus_phase_vocoder_phases(mus_any *ptr)
    mus_float_t *mus_phase_vocoder_phase_increments(mus_any *ptr)


    mus_any *mus_make_ssb_am(mus_float_t freq, int order)
    bint mus_is_ssb_am(mus_any *ptr)
    mus_float_t mus_ssb_am_unmodulated(mus_any *ptr, mus_float_t insig)
    mus_float_t mus_ssb_am(mus_any *ptr, mus_float_t insig, mus_float_t fm)

    void mus_clear_sinc_tables()
    void *mus_environ(mus_any *gen)
    void *mus_set_environ(mus_any *gen, void *e)
    mus_any *mus_bank_generator(mus_any *g, int i)
    

    
    



