#!/usr/bin/env python

import fluidsynth

settings = fluidsynth.FluidSettings()

settings.quality = "low"

synth = fluidsynth.FluidSynth(settings)

driver = fluidsynth.FluidAudioDriver(settings, synth)

player = fluidsynth.FluidPlayer(synth)
