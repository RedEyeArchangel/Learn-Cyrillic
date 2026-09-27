#!/usr/bin/env python3
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Learn Cyrillic: browse the alphabet, hear the pronunciation, learn like in driving school.

Start: python learn_cyrillic.py   ·   Self-test: python learn_cyrillic.py --test
The code lives in the package cyrillic/ (data, questions, scheduler, stats, storage, gui/).
"""
import sys

if __name__ == "__main__":
    if "--test" in sys.argv:
        from cyrillic import i18n
        i18n.LANG = "en"  # the asserts check the English texts
        from cyrillic.selftest import selftest
        selftest()
    else:
        from cyrillic.gui.app import App
        App().mainloop()
