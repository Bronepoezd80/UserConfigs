"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-25

    Synchronize User Configurations - Core - Copying.
"""
import os as _os
import os.path as _osp
import shutil as _shtl
import filecmp as _fcmp
from core import exceptions as _exc
from core import logging as _log


class Copy(object):
    def __init__(self, GlobalVars_):
        GlobalVars_.name = "{} :: Copy".format(GlobalVars_.name)
        self.__log = _log.Log(GlobalVars_)
        return

    def __remove(self, file_):
        """Ensuring removal of file or symbolic link."""
        if _osp.isfile(file_) or _osp.islink(file_):
            self.__log.info("removing {}".format(file_))
            # Ensure copying source by removing target first.
            _os.remove(file_)
            if not _osp.isfile(file_):
                self.__log.info("removed {}".format(file_))
            else:
                error = "failed to remove {}"
                raise _exc.SyncCopySymlinkError(error.format(file_))

    def __filecmp_before(self, source_, target_):
        """Checking before copying."""
        if (
            _osp.isfile(source_)
            and _osp.isfile(target_)
            and _fcmp.cmp(source_, target_)
        ):
            self.__log.info("source and target are equal")
        return

    def __filecmp_after(self, source_, target_):
        """Checking after copying."""
        if not _fcmp.cmp(source_, target_):
            error = "failed to copy {} to {}"
            raise _exc.SyncCopyFileError(error.format(source_, target_))
        self.__log.info("file {} synchronized".format(target_))
        return

    def __symlink(self, source_, target_):
        """Copying symbolic link with checking."""
        if _osp.islink(source_):
            self.__log.info("{} is a symbolic link".format(source_))
            self.__remove(target_)
            # Preserve as symbolic link.
            _shtl.copy(source_, target_, follow_symlinks=False)
            return True
        return False

    def file(self, source_, target_):
        """Copying file or symbolic link with checking."""
        try:
            self.__log.info("copying {} to {}".format(source_, target_))
            if self.__symlink(source_, target_):
                return
            self.__filecmp_before(source_, target_)
            _shtl.copy(source_, target_, follow_symlinks=True)
            self.__filecmp_after(source_, target_)
        except FileNotFoundError as e:
            self.__log.warning(str(e))
        return
