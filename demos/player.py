#!/usr/bin/env python

import sys

from fluidsynth import fluidsynth

if len(sys.argv) < 3:
    print "Usage: %s soundfont.sf2 song.mid" % sys.argv[0]
    sys.exit()

settings = fluidsynth.FluidSettings()
settings.quality = "low"

synth = fluidsynth.FluidSynth(settings)
synth.load_soundfont(sys.argv[1])

driver = fluidsynth.FluidAudioDriver(settings, synth)

player = fluidsynth.FluidPlayer(synth)

player.play(sys.argv[2])
player.join()
