import ctypes

class FSSettings(object):
    def __init__(self, settings):
        self.settings = settings

class FS(object):
    def __init__(self):
        self.libfs = ctypes.cdll.LoadLibrary("libfluidsynth.so.1")
        self.settings = FSSettings(self.libfs.new_fluid_settings())
        self.synth = self.libfs.new_fluid_synth(self.settings.settings)

    def __del__(self):
        self.destroy()

    def destroy(self):
        self.libfs.delete_fluid_synth(self.synth)
        self.libfs.delete_fluid_settings(self.settings.settings)
