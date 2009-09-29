#!/usr/bin/env python

import fluidsynth

settings = fluidsynth.FluidSettings()

settings["synth.chorus.active"] = "off"
settings["synth.reverb.active"] = "off"
settings["synth.sample-rate"] = 22050

synth = fluidsynth.FluidSynth(settings)

driver = fluidsynth.FluidAudioDriver(settings, synth)

player = fluidsynth.FluidPlayer(synth)
