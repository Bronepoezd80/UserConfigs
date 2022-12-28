#!/usr/bin/env python
"""
    Jakob Janzen (me)
    jakob.janzen80@gmail.com
    2022-12-28

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

def pactl_volume_state(default_sink_):
    output = run_command(["pactl", "get-sink-volume", default_sink_])
    print(output)
    return

def main():
    default_sink = run_command(["pactl", "get-default-sink"])
    print("default sink: {}".format(default_sink))
    pactl_volume_state(default_sink)
    run_command(["pactl", "set-sink-volume", default_sink, "30%"])
    pactl_volume_state(default_sink)
    return

if __name__ == "__main__":
    main()

