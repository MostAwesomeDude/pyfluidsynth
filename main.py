#!/usr/bin/env python

from ctypes import *
import ctypes.util

def load_fs():
    path = ctypes.util.find_library("fluidsynth")
    print "[fs] Using %s for FluidSynth library" % path
    libfs = cdll.LoadLibrary(path)

    # Argtypes
    libfs.fluid_settings_setint.argtypes = [c_void_p, c_char_p, c_int]
    libfs.fluid_settings_setnum.argtypes = [c_void_p, c_char_p, c_double]
    libfs.fluid_settings_setstr.argtypes = [c_void_p, c_char_p, c_char_p]

    return libfs

class FSSettings(object):
    def __init__(self, libfs):
        self.libfs = libfs
        self.settings = self.libfs.new_fluid_settings()

    def set_float(self, key, value):
        self.libfs.fluid_settings_setnum(self.settings, key, value)

    def set_int(self, key, value):
        self.libfs.fluid_settings_setint(self.settings, key, value)

    def set_string(self, key, value):
        self.libfs.fluid_settings_setstr(self.settings, key, value)

class FS(object):
    def __init__(self):
        self.libfs = load_fs()

        self.settings = FSSettings(self.libfs)
        self.settings.set_string("synth.chorus.active", "no")
        self.settings.set_string("synth.reverb.active", "no")

        self.synth = self.libfs.new_fluid_synth(self.settings.settings)

        self.sfd = {}

    def __del__(self):
        self.destroy()

    def destroy(self):
        for sf in self.sfd:
            self.unloadsf(sf)

        self.libfs.delete_fluid_synth(self.synth)
        self.libfs.delete_fluid_settings(self.settings.settings)

    def loadsf(self, sf):
        if sf in self.sfd:
            id = self.libfs.fluid_synth_sfreload(self.synth, self.sfd[sf])
        else:
            id = self.libfs.fluid_synth_sfload(self.synth, sf, True)
            self.sfd[sf] = id
        if id == -1:
            print "[fs] Error loading soundfont %s" % sf
        else:
            print "[fs] Soundfont %s loaded successfully" % sf

    def unloadsf(self, sf):
        if sf in self.sfd:
            if self.libfs.fluid_synth_sfunload(self.synth, self.sfd[sf],
                    True):
                print "[fs] Error unloading soundfont %s" % sf
            else:
                print "[fs] Soundfont %s unloaded successfully" % sf
        else:
            print "[fs] Soundfont %s was never loaded" % sf

def test():
    fs = FS()
    fs.loadsf("double.sf2")
    del fs

test()
