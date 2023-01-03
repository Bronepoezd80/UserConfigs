#!/usr/bin/env python
"""
    Jakob Janzen (me)
    jakob.janzen80@gmail.com
    2023-01-03

"""
import os as _os
import sys as _sys
import subprocess as _subprocess


class PACtl(object):
    def __init__(self):
        self.__command = ["pactl"]
        self.output = None

    def __run(self, options_, nextline_=False):
        """ Run command and capture output. """
        self.__command.extend(options_)
        self.output = _subprocess.run(self.__command, capture_output=True)
        self.output = self.output.stdout.decode('utf-8')
        if nextline_:
            return self.output
        return self.output.removesuffix('\n')

    def get_volume(self):
        """ Get global volume. """
        print("current global volume:")
        self.output = self.__run(["get-sink-volume", "0"])
        print(self.output)
        return

    def set_volume(self, value_="0"):
        """ Set global volume. """
        value_ = str(value_)+"%"
        print("setting global volume to {} ...".format(value_))
        self.output = self.__run(["set-sink-volume", "0", value_])
        return


def main():
    PACtl().get_volume()

    PACtl().set_volume()
    PACtl().get_volume()

    PACtl().set_volume(30)
    PACtl().get_volume()

    return


if __name__ == "__main__":
    main()

