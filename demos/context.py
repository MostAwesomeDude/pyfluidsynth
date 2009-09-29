#!/usr/bin/env python

import fluidsynth

settings = fluidsynth.FluidSettings()

synth = fluidsynth.FluidSynth(settings)

driver = fluidsynth.FluidAudioDriver(settings, synth)

player = fluidsynth.FluidPlayer(synth)

sequencer = fluidsynth.FluidSequencer()
