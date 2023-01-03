#!/usr/bin/env python
"""
    Jakob Janzen (me)
    jakob.janzen80@gmail.com
    2023-01-01

"""
import os as _os
import sys as _sys
import subprocess as _subprocess

def run_command(command_, nextline_=False):
    output = _subprocess.run(command_, capture_output=True)
    decoded = output.stdout.decode('utf-8')
    if nextline_:
        return decoded
    return decoded.removesuffix('\n')

def pactl_get_volume():
    output = run_command(["pactl", "get-sink-volume", "0"])
    print(output)
    return

def pactl_set_volume(volume_=0):
    output = run_command(["pactl", "set-sink-volume", "0", str(volume_)+"%"])
    return

def main():
    # Reset volume before set it.
    pactl_get_volume()
    pactl_set_volume()
    pactl_get_volume()
    pactl_set_volume(30)
    pactl_get_volume()
    return

if __name__ == "__main__":
    main()

