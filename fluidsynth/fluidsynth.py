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

class FluidSynth(object):

    def __init__(self, settings):
        self._sf_dict = {}
        self.synth = handle.new_fluid_synth(settings.settings)

    def __del__(self):
        failed = []
        for sf in self._sf_dict:
            if handle.fluid_synth_sfunload(self.synth, self._sf_dict[sf],
                True):
                failed.append(sf)
        handle.delete_fluid_synth(self.synth)

        if failed:
            raise FluidError("Couldn't unload soundfonts: %s" % failed)

    def load_soundfont(self, sf, reload_presets=True):
        if sf in self._sf_dict:
            if (handle.fluid_synth_sfreload(self.synth, self._sf_dict[sf])
                == -1):
                raise FluidError("Couldn't reload soundfont %s" % sf)
        else:
            i = handle.fluid_synth_sfload(self.synth, sf, reload_presets)
            if i == -1:
                raise FluidError, "Couldn't load soundfont %s" % sf
            else:
                self._sf_dict[sf] = i

    def unload_soundfont(self, sf, reload_presets=True):
        if sf not in self._sf_dict:
            raise FluidError("Soundfont %s never loaded" % sf)
        if handle.fluid_synth_sfunload(self.synth, self._sf_dict[sf],
            reload_presets):
            raise FluidError("Couldn't unload soundfont %s" % sf)
        else:
            del self._sf_dict[sf]

    def noteon(self, channel, pitch, velocity):
        if isinstance(velocity, float):
            velocity = int(velocity * 127)
        handle.fluid_synth_noteon(self.synth, channel, pitch, velocity)

    def noteoff(self, channel, pitch):
        handle.fluid_synth_noteoff(self.synth, channel, pitch)

    def cc(self, channel, control, value):
        handle.fluid_synth_cc(self.synth, channel, control, value)

    control_change = cc

    def pitch_bend(self, channel, value):
        handle.fluid_synth_pitch_bend(self.synth, channel, value)

    def pitch_wheel_sens(self, channel, value):
        handle.fluid_synth_pitch_wheel_sens(self.synth, channel, value)

    pitch_wheel_sensitivity = pitch_wheel_sens

    def program_change(self, channel, program):
        handle.fluid_synth_program_change(self.synth, channel, program)

    def bank_select(self, channel, bank):
        handle.fluid_synth_bank_select(self.synth, channel, bank)

class FluidAudioDriver(object):
    def __init__(self, settings, synth):
        self.audio_driver = handle.new_fluid_audio_driver(settings.settings,
            synth.synth)

    def __del__(self):
        handle.delete_fluid_audio_driver(self.audio_driver)

class FluidPlayer(object):

    paused = True

    def __init__(self, synth):
        self.player = handle.new_fluid_player(synth.synth)

    def __del__(self):
        self.stop()
        self.join()

        if handle.delete_fluid_player(self.player):
            raise FluidError("Couldn't delete fluid player!")

    def add(self, midi):
        handle.fluid_player_add(self.player, midi)

    def play(self, midi=None):
        if midi:
            self.add(midi)
        handle.fluid_player_play(self.player)
        self.paused = False

    def stop(self):
        handle.fluid_player_stop(self.player)
        self.paused = True

    def join(self):
        handle.fluid_player_join(self.player)

    def pause(self):
        self.play() if self.paused else self.stop()
        self.paused = not self.paused

class FluidEvent(object):

    source = -1
    dest = -1

    def __init__(self):
        self.event = handle.new_fluid_event()

    def __del__(self):
        handle.delete_fluid_event(self.event)

    @property
    def source(self):
        return handle.fluid_event_get_source(self.event)

    @source.setter
    def source(self, value):
        handle.fluid_event_set_source(self.event, value)

    @property
    def dest(self):
        return handle.fluid_event_get_dest(self.event)

    @dest.setter
    def dest(self, value):
        handle.fluid_event_set_dest(self.event, value)

    def timer(self):
        # XXX should support callbacks
        handle.fluid_event_timer(self.event, None)

    def note(self, channel, key, velocity, duration):
        handle.fluid_event_note(self.event, channel, key, velocity, duration)

    def noteon(self, channel, key, velocity):
        handle.fluid_event_noteon(self.event, channel, key, velocity)

    def noteoff(self, channel, key):
        handle.fluid_event_noteoff(self.event, channel, key)

class FluidSequencer(dict):

    _bpm = 120
    _tpb = 120

    def __init__(self, *synths):
        super(FluidSequencer, self).__init__()

        self.seq = handle.new_fluid_sequencer()

        if synths:
            for synth in synths:
                self.add_synth(synth)

        self._update_tps()

    def __del__(self):
        handle.delete_fluid_sequencer(self.seq)

    def __delitem__(self, key):
        id, name = self[key]
        handle.fluid_sequencer_unregister_client(self.seq, id)

        super(FluidSequencer, self).__delitem__(key)

    @property
    def beats_per_minute(self):
        return self._bpm

    @beats_per_minute.setter
    def beats_per_minute(self, value):
        self._bpm = value
        self._update_tps()

    @property
    def ticks_per_beat(self):
        return self._tpb

    @ticks_per_beat.setter
    def ticks_per_beat(self, value):
        self._tpb = value
        self._update_tps()

    @property
    def ticks_per_second(self):
        return handle.fluid_sequencer_get_time_scale(self.seq)

    @ticks_per_second.setter
    def ticks_per_second(self, value):
        handle.fluid_sequencer_set_time_scale(self.seq, value)

    @property
    def ticks(self):
        return handle.fluid_sequencer_get_tick(self.seq)

    def _update_tps(self):
        self.ticks_per_second = (self._tpb * self._bpm) / 60.0

    def is_dest(self, id):
        return bool(handle.fluid_sequencer_client_is_dest(self.seq, id))

    def add_synth(self, synth):
        id = handle.fluid_sequencer_register_fluidsynth(self.seq, synth.synth)
        name = handle.fluid_sequencer_get_client_name(self.seq, id)

        self[synth] = (id, name)

        return (id, name)

    def send(self, event, timestamp, absolute=True):
        handle.fluid_sequencer_send_at(self.seq, event.event, timestamp,
            absolute)

    def send_right_now(self, event):
        handle.fluid_sequencer_send_now(self.seq, event.event)
