#!/usr/bin/env python3
"""
Check for a Python setup that will work with MCS 275.  Report common
problems if found (e.g. bad Python version, running script using
VS code run button, etc.)
"""
# MCS 275 Spring 2023

# The next line is only needed so that this script works under Python 2.7
# long enough for us to warn the user that we don't support that version
from __future__ import print_function

# Import modules needed to determine aspects of the system we're running on
import sys
import os

warn = False

if sys.version_info.major <= 2:
    # Python 2.x not supported at all
    print(
        "ERROR: You are using Python",
        sys.version_info.major,
        "which is too old for MCS 275.",
    )
    exit(1)
elif sys.version_info.major == 3 and sys.version_info.minor < 8:
    # Python 3.x will work some of the time, but we assume 3.8+
    # in many cases.
    print(
        "WARNING: You are using Python 3."
        + str(sys.version_info.minor)
        + " while version 3.8 or later is required for MCS 275."
    )
    warn = True
else:
    # Python 3.8+ was found
    print("OK: Python version", sys.version.split()[0], "is fine for MCS 275")

script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
working_dir = os.getcwd()
if os.path.samefile(script_dir, working_dir):
    print(
        "OK: You ran this script with the working directory equal to the script directory."
    )
else:
    print(
        "WARNING: This script resides in a different directory than the current working directory."
    )
    print("  Script dir: ", script_dir)
    print("  Working dir:", working_dir)
    print('Did you run this using the "run" button in VS Code or another IDE?')
    print("In MCS 275 you *will* need to know how to run scripts in the terminal.")
    print()
    warn = True

print("Printing emoji / shading / color:", end="")
try:
    print("\U0001F602  \u2591\u2592\u2593\u2588  \u001b[31mRED\u001b[0m")
    print("OK: Printing successful.  Is there red text on previous line?\n")
except:
    print(
        "\nWARNING: It looks like this terminal doesn't support the full unicode character set."
    )
    print(
        "That's fine for most things, but might be a minor inconvenience at some points.\n"
    )
    print()
    warn = True

if warn:
    print(
        "Check the warnings above (you might need to scroll up) and contact course staff"
    )
    print("if you need help resolving them.\n")
else:
    print("Everything looks good so far.\n")


print("INFO: Your Python interpreter path is", sys.executable)
print(
    "INFO: You probably run this interpreter with command:",
    os.path.splitext(os.path.basename(sys.executable))[0],
)

print()
print("As a final check, press ENTER to exit the script. THIS WINDOW SHOULD STAY OPEN.")
print(
    "If the window closes when you press ENTER, try running this script from a terminal"
)
print("instead of a GUI file browser, or ask course staff for help.")

print()
print("If this script appears frozen and nothing happens when you press ENTER, quit by")
print("pressing Control-C (Windows/Linux) or Command-. (MacOS).")

input()
