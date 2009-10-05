#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    ext_modules = [
        Extension("fluidsynth", ["fluidsynth.c"],
            libraries=["fluidsynth"]
        )
    ]
)
