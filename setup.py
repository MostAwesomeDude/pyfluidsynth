#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name="pyfluidsynth",
    version="0.1",
    description="Fluidsynth bindings",
    author="Corbin Simpson",
    author_email="MostAwesomeDude@gmail.com",
    url="http://corbinsimpson.com/",
    ext_modules = [
        Extension("fluidsynth", ["fluidsynth.c"],
            libraries=["fluidsynth_lib", "dsound", "winmm", "user32"],
            library_dirs=["C:/Program Files/Microsoft DirectX SDK (August 2006)/Lib/x86"],
        )
    ]
)
