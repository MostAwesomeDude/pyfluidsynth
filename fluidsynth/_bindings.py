from ctypes import cdll, c_char_p, c_double, c_int, c_void_p

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
