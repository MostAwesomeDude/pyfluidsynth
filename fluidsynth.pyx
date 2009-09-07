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

    # From synth.h
    fluid_synth_t* new_fluid_synth(fluid_settings_t*)
    void delete_fluid_synth(fluid_synth_t*)

    int fluid_synth_sfload(fluid_synth_t*, char*, int)
    int fluid_synth_sfreload(fluid_synth_t*, unsigned int)
    int fluid_synth_sfunload(fluid_synth_t*, unsigned int, int)

    # From midi.h
    fluid_player_t* new_fluid_player(fluid_synth_t*)
    void delete_fluid_player(fluid_player_t*)

class FluidError(Exception):
    pass

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
    cdef object _sf_dict

    def __init__(self, FluidSettings settings):
        self.synth = new_fluid_synth(settings.settings)

        self._sf_dict = {}

    def __del__(self):
        for sf in self._sf_dict:
            if fluid_synth_sfunload(self.synth, self._sf_dict[sf], True):
                raise FluidError, "Couldn't unload soundfont %s" % sf
        delete_fluid_synth(self.synth)

    def load_soundfont(self, sf, reload_presets=True):
        cdef int id

        if sf in self._sf_dict:
            if fluid_synth_sfreload(self.synth, self._sf_dict[sf]) == -1:
                raise FluidError, "Couldn't reload soundfont %s" % sf
        else:
            id = fluid_synth_sfload(self.synth, sf, reload_presets)
            if id == -1:
                raise FluidError, "Couldn't load soundfont %s" % sf
            else:
                self._sf_dict[sf] = id

    def unload_soundfont(self, sf, reload_presets=True):
        if sf not in self._sf_dict:
            raise FluidError, "Soundfont %s never loaded" % sf
        if fluid_synth_sfunload(self.synth, self._sf_dict[sf],
                reload_presets):
            raise FluidError, "Couldn't unload soundfont %s" % sf
        else:
            del self._sf_dict[sf]

cdef class FluidPlayer(object):
    cdef fluid_player_t* player

    def __init__(self, FluidSynth synth):
        self.player = new_fluid_player(synth.synth)

    def __del__(self):
        delete_fluid_player(self.player)
