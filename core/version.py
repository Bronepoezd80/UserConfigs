"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-21

    Synchronize User Configurations - Core - Version.
"""
import sys as _sys
from core import exceptions as _exc


class Version(object):
    def __init__(self, GlobalVars_):
        self.complete = "{}.{}".format(_sys.version_info.major,
                                       _sys.version_info.minor)
        self.GlobalVars = GlobalVars_
        self.major = int(_sys.version_info.major)
        self.minor = int(_sys.version_info.minor)
        return

    def check_major(self):
        ismajor = self.major != self.GlobalVars.version_major_required
        if ismajor:
            error = "Python {}: major version {} is required!"
            raise _exc.SyncError(error.format(
                self.complete, self.GlobalVars.version_major_required))
        return

    def check_minor(self):
        ismajor = self.major == self.GlobalVars.version_major_required
        isminor = self.minor < self.GlobalVars.version_minor_required
        if ismajor and isminor:
            error = "Python {}: minor version minimum {} is required!"
            raise _exc.SyncError(error.format(
                self.complete, self.GlobalVars.version_minor_required))
        return

    def check(self):
        self.check_major()
        self.check_minor()
        return
