from ctypes import (CFUNCTYPE, cdll, c_char_p, c_double, c_int, c_uint,
    c_short, c_void_p)

# The shared object we're gonna use.
handle = cdll.LoadLibrary("libfluidsynth.so.1")

# From settings.h
(FLUID_NO_TYPE, FLUID_NUM_TYPE, FLUID_INT_TYPE, FLUID_STR_TYPE,
    FLUID_SET_TYPE) = range(-1, 4)

handle.new_fluid_settings.argtypes = ()
handle.new_fluid_settings.restype = c_void_p

handle.delete_fluid_settings.argtypes = (c_void_p,)
handle.delete_fluid_settings.restype = None

handle.fluid_settings_get_type.argtypes = (c_void_p, c_char_p)
handle.fluid_settings_get_type.restype = c_int

handle.fluid_settings_getnum.argtypes = (c_void_p, c_char_p, c_void_p)
handle.fluid_settings_getnum.restype = c_int

handle.fluid_settings_getint.argtypes = (c_void_p, c_char_p, c_void_p)
handle.fluid_settings_getint.restype = c_int

handle.fluid_settings_getstr.argtypes = (c_void_p, c_char_p, c_void_p)
handle.fluid_settings_getstr.restype = c_int

handle.fluid_settings_setnum.argtypes = (c_void_p, c_char_p, c_double)
handle.fluid_settings_setnum.restype = c_int

handle.fluid_settings_setint.argtypes = (c_void_p, c_char_p, c_int)
handle.fluid_settings_setint.restype = c_int

handle.fluid_settings_setstr.argtypes = (c_void_p, c_char_p, c_char_p)
handle.fluid_settings_setstr.restype = c_int

# From synth.h
handle.new_fluid_synth.argtypes = (c_void_p,)
handle.new_fluid_synth.restype = c_void_p

handle.delete_fluid_synth.argtypes = (c_void_p,)
handle.delete_fluid_synth.restype = None

handle.fluid_synth_sfload.argtypes = (c_void_p, c_char_p, c_int)
handle.fluid_synth_sfload.restype = c_int

handle.fluid_synth_sfreload.argtypes = (c_void_p, c_uint)
handle.fluid_synth_sfreload.restype = c_int

handle.fluid_synth_sfunload.argtypes = (c_void_p, c_uint, c_int)
handle.fluid_synth_sfunload.restype = c_int

handle.fluid_synth_noteon.argtypes = (c_void_p, c_int, c_int, c_int)
handle.fluid_synth_noteon.restype = c_int

handle.fluid_synth_noteoff.argtypes = (c_void_p, c_int, c_int)
handle.fluid_synth_noteoff.restype = c_int

handle.fluid_synth_cc.argtypes = (c_void_p, c_int, c_int, c_int)
handle.fluid_synth_cc.restype = c_int

handle.fluid_synth_pitch_bend.argtypes = (c_void_p, c_int, c_int)
handle.fluid_synth_pitch_bend.restype = c_int

handle.fluid_synth_pitch_wheel_sens.argtypes = (c_void_p, c_int, c_int)
handle.fluid_synth_pitch_wheel_sens.restype = c_int

handle.fluid_synth_program_change.argtypes = (c_void_p, c_int, c_int)
handle.fluid_synth_program_change.restype = c_int

handle.fluid_synth_bank_select.argtypes = (c_void_p, c_int, c_int)
handle.fluid_synth_bank_select.restype = c_int

# From audio.h
handle.new_fluid_audio_driver.argtypes = (c_void_p, c_void_p)
handle.new_fluid_audio_driver.restype = c_void_p

handle.delete_fluid_audio_driver.argtypes = (c_void_p,)
handle.delete_fluid_audio_driver.restype = None

# From midi.h
handle.new_fluid_player.argtypes = (c_void_p,)
handle.new_fluid_player.restype = c_void_p

handle.delete_fluid_player.argtypes = (c_void_p,)
handle.delete_fluid_player.restype = c_int

handle.fluid_player_add.argtypes = (c_void_p, c_char_p)
handle.fluid_player_add.restype = c_int

handle.fluid_player_play.argtypes = (c_void_p,)
handle.fluid_player_play.restype = c_int

handle.fluid_player_stop.argtypes = (c_void_p,)
handle.fluid_player_stop.restype = c_int

handle.fluid_player_join.argtypes = (c_void_p,)
handle.fluid_player_join.restype = c_int

# From event.h
handle.new_fluid_event.argtypes = ()
handle.new_fluid_event.restype = c_void_p

handle.delete_fluid_event.argtypes = (c_void_p,)
handle.delete_fluid_event.restype = None

handle.fluid_event_timer.argtypes = (c_void_p, c_void_p)
handle.fluid_event_timer.restype = None

handle.fluid_event_note.argtypes = (c_void_p, c_int, c_short, c_short, c_uint)
handle.fluid_event_note.restype = None

handle.fluid_event_noteon.argtypes = (c_void_p, c_int, c_short, c_short)
handle.fluid_event_noteon.restype = None

handle.fluid_event_noteoff.argtypes = (c_void_p, c_int, c_short)
handle.fluid_event_noteoff.restype = None

handle.fluid_event_get_source.argtypes = (c_void_p,)
handle.fluid_event_get_source.restype = c_short

handle.fluid_event_set_source.argtypes = (c_void_p, c_short)
handle.fluid_event_set_source.restype = None

handle.fluid_event_get_dest.argtypes = (c_void_p,)
handle.fluid_event_get_dest.restype = c_short

handle.fluid_event_set_dest.argtypes = (c_void_p, c_short)
handle.fluid_event_set_dest.restype = None

# From seq.h
fluid_event_callback_t = CFUNCTYPE(None, c_uint, c_void_p, c_void_p, c_void_p)

handle.new_fluid_sequencer.argtypes = ()
handle.new_fluid_sequencer.restype = c_void_p

handle.delete_fluid_sequencer.argtypes = (c_void_p,)
handle.delete_fluid_sequencer.restype = None

handle.fluid_sequencer_count_clients.argtypes = (c_void_p,)
handle.fluid_sequencer_count_clients.restype = c_int

handle.fluid_sequencer_get_client_id.argtypes = (c_void_p, c_int)
handle.fluid_sequencer_get_client_id.restype = c_int

handle.fluid_sequencer_get_client_name.argtypes = (c_void_p, c_int)
handle.fluid_sequencer_get_client_name.restype = c_char_p

handle.fluid_sequencer_client_is_dest.argtypes = (c_void_p, c_int)
handle.fluid_sequencer_client_is_dest.restype = c_int

handle.fluid_sequencer_register_client.argtypes = (c_void_p, c_char_p,
    fluid_event_callback_t, c_void_p)
handle.fluid_sequencer_register_client.restype = c_short

handle.fluid_sequencer_unregister_client.argtypes = (c_void_p, c_short)
handle.fluid_sequencer_unregister_client.restype = None

handle.fluid_sequencer_send_now.argtypes = (c_void_p, c_void_p)
handle.fluid_sequencer_send_now.restype = None

handle.fluid_sequencer_send_at.argtypes = (c_void_p, c_void_p, c_uint, c_int)
handle.fluid_sequencer_send_at.restype = c_int

handle.fluid_sequencer_get_time_scale.argtypes = (c_void_p,)
handle.fluid_sequencer_get_time_scale.restype = c_double

handle.fluid_sequencer_set_time_scale.argtypes = (c_void_p, c_double)
handle.fluid_sequencer_set_time_scale.restype = None

handle.fluid_sequencer_get_tick.argtypes = (c_void_p,)
handle.fluid_sequencer_get_tick.restype = c_uint

# From seqbind.h
handle.fluid_sequencer_register_fluidsynth.argtypes = (c_void_p, c_void_p)
handle.fluid_sequencer_register_fluidsynth.restype = c_short
