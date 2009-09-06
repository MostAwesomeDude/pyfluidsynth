import ctypes
import ctypes.util

class FSSettings(object):
    def __init__(self, settings):
        self.settings = settings

class FS(object):
    def __init__(self):
        path = ctypes.util.find_library("fluidsynth")
        print "[fs] Using %s for FluidSynth library" % path
        self.libfs = ctypes.cdll.LoadLibrary(path)
        self.settings = FSSettings(self.libfs.new_fluid_settings())
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
