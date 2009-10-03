#!/usr/bin/env python

import time

import fluidsynth

settings = fluidsynth.FluidSettings()
settings.quality = "low"

synth = fluidsynth.FluidSynth(settings)
synth.load_soundfont("double.sf2")

driver = fluidsynth.FluidAudioDriver(settings, synth)

sequencer = fluidsynth.FluidSequencer()
sequencer.ticks_per_second = 720/4

dest = sequencer.add_synth(synth)

c_scale = []

for note in range(60, 72):
    event = fluidsynth.FluidEvent()
    event.dest = dest[0]
    event.note(0, note, 127, 720/8)
    c_scale.append(event) 

ticks = sequencer.ticks + 10

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[4], ticks)
sequencer.send(c_scale[7], ticks)

ticks += 720/8

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[5], ticks)
sequencer.send(c_scale[9], ticks)

ticks += 720/8

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[4], ticks)
sequencer.send(c_scale[7], ticks)

ticks += 720/8

sequencer.send(c_scale[2], ticks)
sequencer.send(c_scale[5], ticks)
sequencer.send(c_scale[7], ticks)
sequencer.send(c_scale[11], ticks)

ticks += 720/8

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[4], ticks)
sequencer.send(c_scale[7], ticks)

time.sleep(16)
