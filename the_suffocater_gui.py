#!/usr/bin/python3

#
# This thing is called the "Carcass" - the heart of theSuffocater.
# Carcass destiny is to load modules located in the /fear-the-suffocater/modules
# for further using.
# 
# Usually carcass dont receive much updates because its already serving
# its functionality very good.
# 
# This is a graphical frontend, normal cli version is 'the_suffocater_gui.py'.

try:
    import os
    import sys
    modules_dir = os.path.join(os.path.dirname(__file__), "modules")
    sys.path.append(modules_dir)
    import usr
    import glob
    import subprocess
    import tkinter as tk
    import importlib.util
    from usr import RED, GREEN, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: module not found:\n{error}{RESET}")
    sys.exit(1)
