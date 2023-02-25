"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-22

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
        self.__backup_timestamp_dir = "BAK{}".format(GlobalVars_.timestamp_backup)
        self.__backup_target_dir = _osp.join(
            self.__userhome, self.__backup_dir, self.__backup_timestamp_dir
        )
        return

    def directory(self, target_):
        target_dir = _osp.join(
            self.__backup_target_dir, target_.removeprefix(self.__userhome + "/")
        )
        self.__log.info("making backup of directory {}".format(target_dir))
        self.__dirs.make(target_dir)
        return

    def file(self, source_):
        source_suffix = source_.removeprefix(self.__userhome + "/")
        target = _osp.join(self.__backup_target_dir, source_suffix)
        self.__log.info("making backup of file {}".format(source_))
        self.__copy.file(source_, target)
        return
