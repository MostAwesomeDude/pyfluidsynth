#!/usr/bin/env python

import time

import fluidsynth

settings = fluidsynth.FluidSettings()
settings.quality = "low"

synth = fluidsynth.FluidSynth(settings)
synth.load_soundfont("double.sf2")

driver = fluidsynth.FluidAudioDriver(settings, synth)

scale = (60, 62, 64, 65, 67, 69, 71, 72)

for i in scale:
    synth.noteon(0, i, 127)
    time.sleep(0.5)
    synth.noteoff(0, i)

for i in reversed(scale):
    synth.noteon(0, i, 127)
    time.sleep(0.5)
    synth.noteoff(0, i)
