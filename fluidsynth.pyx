cdef extern from "fluidsynth.h":

    enum fluid_types_enum:
        FLUID_NO_TYPE, FLUID_NUM_TYPE, FLUID_INT_TYPE, FLUID_STR_TYPE, \
            FLUID_SET_TYPE

    ctypedef struct fluid_settings_t:
        pass
    ctypedef struct fluid_synth_t:
        pass
    ctypedef struct fluid_player_t:
        pass

    # From settings.h
    fluid_settings_t* new_fluid_settings()
    void delete_fluid_settings(fluid_settings_t*)

    fluid_types_enum fluid_settings_get_type(fluid_settings_t*, char*)
    int fluid_settings_getnum(fluid_settings_t*, char*, double*)
    int fluid_settings_getint(fluid_settings_t*, char*, int*)
    int fluid_settings_getstr(fluid_settings_t*, char*, char**)

    int fluid_settings_setnum(fluid_settings_t*, char*, double)
    int fluid_settings_setint(fluid_settings_t*, char*, int)
    int fluid_settings_setstr(fluid_settings_t*, char*, char*)

    fluid_synth_t* new_fluid_synth(fluid_settings_t*)
    void delete_fluid_synth(fluid_synth_t*)

    fluid_player_t* new_fluid_player(fluid_synth_t*)
    void delete_fluid_player(fluid_player_t*)

cdef class FluidSettings(object):
    cdef fluid_settings_t* settings

    def __init__(self):
        self.settings = new_fluid_settings()

    def __del__(self):
        delete_fluid_settings(self.settings)

    def __getitem__(self, char* key):
        cdef int key_type
        cdef double d
        cdef int i
        cdef char* c

        key_type = fluid_settings_get_type(self.settings, key)
        if key_type == FLUID_NUM_TYPE:
            if fluid_settings_getnum(self.settings, key, &d):
                return d
            else:
                raise KeyError
        elif key_type == FLUID_INT_TYPE:
            if fluid_settings_getint(self.settings, key, &i):
                return i
            else:
                raise KeyError
        elif key_type == FLUID_STR_TYPE:
            if fluid_settings_getstr(self.settings, key, &c):
                return c
            else:
                raise KeyError
        else:
            raise KeyError

    def __setitem__(self, key, value):
        key_type = fluid_settings_get_type(self.settings, key)
        if key_type == FLUID_NUM_TYPE:
            if not fluid_settings_setnum(self.settings, key, value):
                raise KeyError
        elif key_type == FLUID_INT_TYPE:
            if not fluid_settings_setint(self.settings, key, value):
                raise KeyError
        elif key_type == FLUID_STR_TYPE:
            if not fluid_settings_setstr(self.settings, key, value):
                raise KeyError
        else:
            raise KeyError

cdef class FluidSynth(object):
    cdef fluid_synth_t* synth

    def __init__(self, FluidSettings settings):
        self.synth = new_fluid_synth(settings.settings)

    def __del__(self):
        delete_fluid_synth(self.synth)

cdef class FluidPlayer(object):
    cdef fluid_player_t* player

    def __init__(self, FluidSynth synth):
        self.player = new_fluid_player(synth.synth)

    def __del__(self):
        delete_fluid_player(self.player)
