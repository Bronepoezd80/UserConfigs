"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-25

    Synchronize User Configurations - Core - Backup.
"""
import os.path as _osp
from core import logging as _log
from core import directories as _dirs
from core import copying as _cp


class Backup(object):
    def __init__(self, GlobalVars_, userhome_):
        GlobalVars_.name = "{} :: Backup".format(GlobalVars_.name)
        self.__log = _log.Log(GlobalVars_)
        self.__dirs = _dirs.Dirs(GlobalVars_)
        self.__copy = _cp.Copy(GlobalVars_)
        self.__userhome = userhome_
        self.__backup_dir = GlobalVars_.backup_directory
        self.__backup_timestamp_dir = self.__timestamp_dir(GlobalVars_)
        self.__backup_target_dir = self.__target_dir()

    def __timestamp_dir(self, GlobalVars_):
        return "BAK{}".format(GlobalVars_.timestamp_backup)

    def __target_dir(self):
        return _osp.join(
            self.__userhome, self.__backup_dir, self.__backup_timestamp_dir
        )

    def __format_target_dir(self, target_):
        return _osp.join(
            self.__backup_target_dir, target_.removeprefix(self.__userhome + "/")
        )

    def __format_source_file(self, source_):
        return source_.removeprefix(self.__userhome + "/")

    def __format_target_file(self, target_):
        return _osp.join(self.__backup_target_dir, target_)

    def directory(self, target_):
        target = self.__format_target_dir(target_)
        self.__log.info("making backup of directory {}".format(target))
        self.__dirs.make(target)

    def file(self, source_):
        source = self.__format_source_file(source_)
        target = self.__format_target_file(source)
        self.__log.info("making backup of file {}".format(source_))
        self.__copy.file(source_, target)
