#!/usr/bin/env python

import fluidsynth

def test():
    settings = fluidsynth.FluidSettings()
    settings["audio.driver"] = "alsa"
    settings["audio.alsa.device"] = "plughw:0"
    settings["synth.chorus.active"] = "off"
    settings["synth.reverb.active"] = "off"
    settings["synth.sample-rate"] = 22050
    fs = fluidsynth.FluidSynth(settings)
    fs.load_soundfont("double.sf2")
    driver = fluidsynth.FluidAudioDriver(settings, fs)
    player = fluidsynth.FluidPlayer(fs)
    player.play("cross.mid")
