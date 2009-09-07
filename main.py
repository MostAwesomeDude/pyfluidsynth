#!/usr/bin/env python

class FSPlayer(object):
    def __init__(self, libfs, player):
        self.libfs = libfs
        self.player = player

    def play(self, midi):
        self.libfs.fluid_player_add(self.player, midi)
        self.libfs.fluid_player_play(self.player)
        self.libfs.fluid_player_join(self.player)

    def __del__(self):
        self.destroy()

    def destroy(self):
        self.libfs.delete_fluid_player(self.player)

class FS(object):
    def __init__(self):
        self.libfs = load_fs()

        self.settings = FSSettings(self.libfs)
        self.settings.set_string("synth.chorus.active", "no")
        self.settings.set_string("synth.reverb.active", "no")

        self.settings.set_string("audio.driver", "alsa")
        self.settings.set_string("audio.alsa.device", "plughw:0")

        self.synth = self.libfs.new_fluid_synth(self.settings.settings)
        self.driver = self.libfs.new_fluid_audio_driver(
            self.settings.settings, self.synth)

def test():
    fs = FS()
    fs.loadsf("double.sf2")
    player = fs.player()
    player.play("finale.mid")
    del fs
