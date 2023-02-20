#!/bin/env python
"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-20

    Synchronize User Configurations.
"""
import os
import sys
import os.path
import shutil
import filecmp
import logging
from pathlib import Path
from datetime import datetime
from optparse import OptionParser


class SyncError(Exception):
    def __init__(self, message_):
        self.__message = message_
        super().__init__(self.__message)
        return


class SyncMakeDirError(SyncError):
    pass


class SyncCopyFileError(SyncError):
    pass


class SyncCopySymlinkError(SyncError):
    pass


class Timestamp(object):
    def __init__(self):
        self.__now = datetime.now()
        return

    def logfile(self):
        return self.__now.strftime("%Y%m%d")

    def backup(self):
        return self.__now.strftime("%Y%m%d%H%M%S")


# GLOBAL VARIABLES
module_name = os.path.basename(str(__file__)).split(".")[0]
backup_directory = ".backup_userconfigs"
# Required Python version.
version_major_required = 3
version_minor_required = 8
# Global time stamps.
timestamp_logfile = Timestamp().logfile()
timestamp_backup = Timestamp().backup()


class Log(object):
    def __init__(self, name_):
        """ Distinguish loggers through name. """
        self.__logger = logging.getLogger(name_)
        self.__logger.setLevel(logging.INFO)
        self.__format = "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s"
        self.__formatter = logging.Formatter(self.__format)
        # Log-file with only date timestamp, avoid files overkill by omitting time.
        self.__logfile = "{}_{}.log".format(module_name, timestamp_logfile)
        # Avoid multiple times logging by creating handlers only if required.
        if not self.__logger.handlers:
            # Output to file handler.
            self.__file_handler = logging.FileHandler(self.__logfile)
            self.__file_handler.setFormatter(self.__formatter)
            self.__logger.addHandler(self.__file_handler)
            # Output to console handler.
            self.__console_handler = logging.StreamHandler()
            self.__console_handler.setFormatter(self.__formatter)
            self.__logger.addHandler(self.__console_handler)
        return

    def info(self, message_="________"):
        self.__logger.info(message_)
        return

    def warning(self, message_="________"):
        self.__logger.warning(message_)
        return

    def error(self, message_="________"):
        self.__logger.error(message_)
        return

    def critical(self, message_="________"):
        self.__logger.critical(message_)
        return

    def section(self, message_="________", level_=1):
        self.info("{} {} {}".format("*"*level_, message_, "*"*level_))
        return

    def exception(self, message_="________"):
        self.__logger.exception(message_)
        return


class Version(object):
    def __init__(self):
        self.complete = "{}.{}".format(sys.version_info.major,
                                       sys.version_info.minor)
        self.major_required = version_major_required
        self.minor_required = version_minor_required
        self.major = int(sys.version_info.major)
        self.minor = int(sys.version_info.minor)
        return

    def check_major(self):
        ismajor = self.major != self.major_required
        if ismajor:
            error = "Python {}: major version {} is required!"
            raise SyncError(error.format(self.complete, self.major_required))
        return

    def check_minor(self):
        ismajor = self.major == self.major_required
        isminor = self.minor < self.minor_required
        if ismajor and isminor:
            error = "Python {}: minor version minimum {} is required!"
            raise SyncError(error.format(self.complete, self.minor_required))
        return

    def check(self):
        self.check_major()
        self.check_minor()
        return


class Dirs(object):
    def __init__(self, parent_name_):
        self.__name = "{} :: MakeDirs".format(parent_name_)
        self.__log = Log(self.__name)
        return

    def make(self, target_):
        """ Making directories recursively with checking. """
        try:
            os.makedirs(target_)
        except FileExistsError:
            self.__log.info("directory {} synchronized".format(target_))
        else:
            if os.path.isdir(target_):
                self.__log.info("made target directory {}".format(target_))
            else:
                error = "failed to make target directory {} !"
                raise SyncMakeDirError(error.format(target_))
        return


class Copy(object):
    def __init__(self, parent_name_):
        self.__name = "{} :: Copy".format(parent_name_)
        self.__log = Log(self.__name)
        return

    def __remove(self, file_):
        """ Ensuring removal of file or symbolic link. """
        if os.path.isfile(file_) or os.path.islink(file_):
            self.__log.info("removing {}".format(file_))
            # Ensure copying source by removing target first.
            os.remove(file_)
            if not os.path.isfile(file_):
                self.__log.info("removed {}".format(file_))
            else:
                error = "failed to remove {}"
                raise SyncCopySymlinkError(error.format(file_))

    def __filecmp_before(self, source_, target_):
        """ Checking before copying. """
        if os.path.isfile(source_) and os.path.isfile(target_):
            if filecmp.cmp(source_, target_):
                self.__log.info("source and target are equal")
        return

    def __filecmp_after(self, source_, target_):
        """ Checking after copying. """
        if not filecmp.cmp(source_, target_):
            error = "failed to copy {} to {}"
            raise SyncCopyFileError(error.format(source_, target_))
        self.__log.info("file {} synchronized".format(target_))
        return

    def __symlink(self, source_, target_):
        """ Copying symbolic link with checking. """
        if os.path.islink(source_):
            self.__log.info("{} is a symbolic link".format(source_))
            self.__remove(target_)
            # Preserve as symbolic link.
            shutil.copy(source_, target_, follow_symlinks=False)
            return True
        return False

    def file(self, source_, target_):
        """ Copying file or symbolic link with checking. """
        try:
            self.__log.info("copying {} to {}".format(source_, target_))
            if self.__symlink(source_, target_):
                return
            self.__filecmp_before(source_, target_)
            shutil.copy(source_, target_, follow_symlinks=True)
            self.__filecmp_after(source_, target_)
        except FileNotFoundError as e:
            self.__log.warning(str(e))
        return


class Backup(object):
    def __init__(self, parent_name_, userhome_):
        self.__name = "{} :: Backup".format(parent_name_)
        self.__log = Log(self.__name)
        self.__userhome = userhome_
        self.__backup_dir = backup_directory
        self.__backup_timestamp_dir = "BAK{}".format(timestamp_backup)
        self.__backup_target_dir = os.path.join(self.__userhome,
                                                self.__backup_dir,
                                                self.__backup_timestamp_dir)
        return

    def directory(self, target_):
        target_dir = os.path.join(self.__backup_target_dir,
                                  target_.removeprefix(self.__userhome + "/"))
        self.__log.info("making backup of directory {}".format(target_dir))
        Dirs(self.__name).make(target_dir)
        return

    def file(self, source_, target_):
        source_suffix = source_.removeprefix(self.__userhome + "/")
        target_prefix = target_.removesuffix(source_suffix)
        target = os.path.join(self.__backup_target_dir, source_suffix)
        self.__log.info("making backup of file {}".format(source_))
        Copy(self.__name).file(source_, target)
        return


class Sync(object):
    def __init__(self, parent_name_, root_, directories_, files_):
        self.__userhome = str(Path.home())

        self.__root = root_
        self.__directories = directories_
        self.__files = files_

        self.__source = None
        self.__target = None

        self.__name = "{} :: Sync".format(parent_name_)
        self.__log = Log(self.__name)
        return

    def __set_source(self, path_, type_):
        self.__source = os.path.join(self.__root, path_)
        self.__log.info("source {}: {}".format(type_, self.__source))
        return

    def __set_target(self, source_, target_, type_):
        self.__target= os.path.join(target_, self.__source.removeprefix(source_ + "/"))
        self.__log.info("target {}: {}".format(type_, self.__target))
        return

    def __set_paths(self, path_, source_, target_, type_):
        self.__set_source(path_, type_)
        self.__set_target(source_, target_, type_)

    def directories(self, source_, target_):
        """ Handling directory synchronization. """
        self.__log.section("DIRECTORIES", 1)
        for directory in self.__directories:
            self.__set_paths(directory, source_, target_, "directory")
            Backup(self.__name, self.__userhome).directory(self.__target)
            Dirs(self.__name).make(self.__target)
            self.__log.info()
        return

    def files(self, source_, target_):
        """ Handling file synchronization. """
        self.__log.section("FILES", 1)
        for file in self.__files:
            self.__set_paths(file, source_, target_, "file")
            Backup(self.__name, self.__userhome).file(self.__target, self.__source)
            Copy(self.__name).file(self.__source, self.__target)
            self.__log.info()
        return


def main():
    Version().check()

    log = Log(module_name)
    log.section("{} USER CONFIGURATIONS".format(module_name).upper(), 5)

    # Command line options:
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--userhome", dest="userhome", action="store", type="string",
                      help="folder with configurations in the user home",
                      metavar="USERHOME")
    (options, args) = parser.parse_args()

    if options.userhome is None:
        parser.print_help()
        return
    if not os.path.isdir(options.userhome):
        parser.print_help()
        raise SyncError("directory {} invalid!".format(options.userhome))

    cwd = os.getcwd()
    log.info("current working directory: {}".format(cwd))

    source = os.path.join(cwd, "userhome")
    log.info("source: {}".format(source))

    target = str(Path.home())
    log.info("target: {}".format(target))

    if os.path.isdir(source):
        log.section("WALKING THE SOURCE", 3)
        for root, directories, files in os.walk(source):
            sync = Sync(module_name, root, directories, files)
            sync.directories(source, target)
            sync.files(source, target)
            log.info()
    else:
        error = "path {} not found!"
        raise SyncError(error.format(source))

    return


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)

    except SyncError as e:
        Log("SyncError").exception(e)
    except SyncMakeDirError as e:
        Log("SyncMakeDirError").exception(e)
    except SyncCopyFileError as e:
        Log("SyncCopyFileError").exception(e)
    except SyncCopySymlinkError as e:
        Log("SyncCopySymlinkError").exception(e)

    sys.exit(1)

