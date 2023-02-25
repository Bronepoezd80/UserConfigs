"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-22

    Synchronize User Configurations - Core - Synchronize.
"""
import os.path as _osp
from pathlib import Path as _Path
from core import logging as _log
from core import directories as _dirs
from core import backup as _bak
from core import copying as _cp


class Sync(object):
    def __init__(self, GlobalVars_, root_, directories_, files_):
        GlobalVars_.name = "{} :: Sync".format(GlobalVars_.name)
        self.__userhome = str(_Path.home())
        self.__root = root_
        self.__directories = directories_
        self.__files = files_
        self.__source = None
        self.__target = None
        self.__backup = _bak.Backup(GlobalVars_, self.__userhome)
        self.__dirs = _dirs.Dirs(GlobalVars_)
        self.__copy = _cp.Copy(GlobalVars_)
        self.__log = _log.Log(GlobalVars_)
        return

    def __set_source(self, path_, type_):
        self.__source = _osp.join(self.__root, path_)
        self.__log.info("source {}: {}".format(type_, self.__source))
        return

    def __set_target(self, source_, target_, type_):
        self.__target = _osp.join(
            target_, self.__source.removeprefix(source_ + "/")
        )
        self.__log.info("target {}: {}".format(type_, self.__target))
        return

    def __set_paths(self, path_, source_, target_, type_):
        self.__set_source(path_, type_)
        self.__set_target(source_, target_, type_)

    def directories(self, source_, target_):
        """Handling directory synchronization."""
        self.__log.section("DIRECTORIES", 1)
        for directory in self.__directories:
            self.__set_paths(directory, source_, target_, "directory")
            self.__backup.directory(self.__target)
            self.__dirs.make(self.__target)
            self.__log.info()
        return

    def files(self, source_, target_):
        """Handling file synchronization."""
        self.__log.section("FILES", 1)
        for file in self.__files:
            self.__set_paths(file, source_, target_, "file")
            self.__backup.file(self.__target)
            self.__copy.file(self.__source, self.__target)
            self.__log.info()
        return
