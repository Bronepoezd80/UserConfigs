"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-22

    Synchronize User Configurations - Core - Directories.
"""
import os as _os
import os.path as _osp
from core import logging as _log
from core import exceptions as _exc


class Dirs(object):
    def __init__(self, GlobalVars_):
        GlobalVars_.name = "{} :: MakeDirs".format(GlobalVars_.name)
        self.__log = _log.Log(GlobalVars_)
        return

    def make(self, target_):
        """Making directories recursively with checking."""
        try:
            _os.makedirs(target_)
        except FileExistsError:
            self.__log.info("directory {} synchronized".format(target_))
        else:
            if _osp.isdir(target_):
                self.__log.info("made target directory {}".format(target_))
            else:
                error = "failed to make target directory {} !"
                raise _exc.SyncMakeDirError(error.format(target_))
        return
