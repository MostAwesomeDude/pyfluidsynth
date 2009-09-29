cdef extern from "fluidsynth.h":

    enum fluid_types_enum:
        FLUID_NO_TYPE, FLUID_NUM_TYPE, FLUID_INT_TYPE, FLUID_STR_TYPE, \
            FLUID_SET_TYPE

    ctypedef struct fluid_settings_t:
        pass
    ctypedef struct fluid_synth_t:
        pass
    ctypedef struct fluid_audio_driver_t:
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

    int fluid_synth_noteon(fluid_synth_t*, int, int, int)
    int fluid_synth_noteoff(fluid_synth_t*, int, int)
    int fluid_synth_cc(fluid_synth_t*, int, int, int)
    int fluid_synth_pitch_bend(fluid_synth_t*, int, int)
    int fluid_synth_pitch_wheel_sens(fluid_synth_t*, int, int)
    int fluid_synth_program_change(fluid_synth_t*, int, int)

    int fluid_synth_bank_select(fluid_synth_t*, int, int)

    # From audio.h
    fluid_audio_driver_t* new_fluid_audio_driver(fluid_settings_t*,
        fluid_synth_t*)
    void delete_fluid_audio_driver(fluid_audio_driver_t*)

    # From midi.h
    fluid_player_t* new_fluid_player(fluid_synth_t*)
    void delete_fluid_player(fluid_player_t*)

    int fluid_player_add(fluid_player_t*, char*)
    int fluid_player_play(fluid_player_t*)
    int fluid_player_stop(fluid_player_t*)
    int fluid_player_join(fluid_player_t*)

import sys

class FluidError(Exception):
    pass

cdef class FluidSettings(object):
    cdef fluid_settings_t* settings

    def __init__(self):
        self.settings = new_fluid_settings()

        if "linux" in sys.platform:
            self["audio.driver"] = "alsa"
            self["audio.alsa.device"] = "plughw:0"

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

    property quality:

        def __set__(self, quality):
            if quality == "low":
                self["synth.chorus.active"] = "off"
                self["synth.reverb.active"] = "off"
                self["synth.sample-rate"] = 22050
            elif quality == "med":
                self["synth.chorus.active"] = "off"
                self["synth.reverb.active"] = "on"
                self["synth.sample-rate"] = 44100
            elif quality == "high":
                self["synth.chorus.active"] = "on"
                self["synth.reverb.active"] = "on"
                self["synth.sample-rate"] = 44100

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

    def noteon(self, channel, pitch, velocity):
        if isinstance(velocity, float):
            velocity = int(velocity * 127)
        fluid_synth_noteon(self.synth, channel, pitch, velocity)

    def noteoff(self, channel, pitch):
        fluid_synth_noteoff(self.synth, channel, pitch)

    def cc(self, channel, control, value):
        fluid_synth_cc(self.synth, channel, control, value)

    control_change = cc

    def pitch_bend(self, channel, value):
        fluid_synth_pitch_bend(self.synth, channel, value)

    def pitch_wheel_sens(self, channel, value):
        fluid_synth_pitch_wheel_sens(self.synth, channel, value)

    pitch_wheel_sensitivity = pitch_wheel_sens

    def program_change(self, channel, program):
        fluid_synth_program_change(self.synth, channel, program)

    def bank_select(self, channel, bank):
        fluid_synth_bank_select(self.synth, channel, bank)

cdef class FluidAudioDriver(object):
    cdef fluid_audio_driver_t* audio_driver

    def __init__(self, FluidSettings settings, FluidSynth synth):
        self.audio_driver = new_fluid_audio_driver(settings.settings,
            synth.synth)

    def __del__(self):
        delete_fluid_audio_driver(self.audio_driver)

cdef class FluidPlayer(object):
    cdef fluid_player_t* player
    cdef int paused

    def __init__(self, FluidSynth synth):
        self.player = new_fluid_player(synth.synth)
        self.paused = True

    def __del__(self):
        self.stop()
        self.join()

        delete_fluid_player(self.player)

    cpdef add(self, midi):
        fluid_player_add(self.player, midi)

    cpdef play(self, midi=None):
        if midi:
            self.add(midi)
        fluid_player_play(self.player)
        self.paused = False

    cpdef stop(self):
        fluid_player_stop(self.player)
        self.paused = True

    cpdef join(self):
        fluid_player_join(self.player)

    def pause(self):
        self.play() if self.paused else self.stop()
        self.paused = not self.paused
