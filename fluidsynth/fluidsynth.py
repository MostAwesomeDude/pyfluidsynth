from ctypes import byref, c_char_p, c_double, c_int
import sys

from ._bindings import FLUID_INT_TYPE, FLUID_NUM_TYPE, FLUID_STR_TYPE, handle

def coerce_to_int(s):
    """
    Turn a string into an integer.
    """

    try:
        return int(s)
    except ValueError:
        return int(s.lower() not in ("false", "no", "off"))

class FluidError(Exception):
    """
    Something bad happened.
    """

class FluidSettings(object):

    def __init__(self):
        self.settings = handle.new_fluid_settings()
        self.quality = "med"

        if "linux" in sys.platform:
            self["audio.driver"] = "alsa"

    def __del__(self):
        handle.delete_fluid_settings(self.settings)

    def __getitem__(self, key):
        key_type = handle.fluid_settings_get_type(self.settings, key)
        if key_type == FLUID_NUM_TYPE:
            v = c_double()
            f = handle.fluid_settings_getnum
        elif key_type == FLUID_INT_TYPE:
            v = c_int()
            f = handle.fluid_settings_getint
        elif key_type == FLUID_STR_TYPE:
            v = c_char_p()
            f = handle.fluid_settings_getstr
        else:
            raise KeyError(key)

        if f(self.settings, key, byref(v)):
            return v.value
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        key_type = handle.fluid_settings_get_type(self.settings, key)
        if key_type == FLUID_STR_TYPE:
            if not handle.fluid_settings_setstr(self.settings, key, value):
                raise KeyError(key)
        else:
            # Coerce to integer before going further
            value = coerce_to_int(value)
            if key_type == FLUID_NUM_TYPE:
                if not handle.fluid_settings_setnum(self.settings, key, value):
                    raise KeyError
            elif key_type == FLUID_INT_TYPE:
                if not handle.fluid_settings_setint(self.settings, key, value):
                    raise KeyError
            else:
                raise KeyError

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value):
        self._quality = value
        if value == "low":
            self["synth.chorus.active"] = "off"
            self["synth.reverb.active"] = "off"
            self["synth.sample-rate"] = 22050
        elif value == "med":
            self["synth.chorus.active"] = "off"
            self["synth.reverb.active"] = "on"
            self["synth.sample-rate"] = 44100
        elif value == "high":
            self["synth.chorus.active"] = "on"
            self["synth.reverb.active"] = "on"
            self["synth.sample-rate"] = 44100
