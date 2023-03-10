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
from pathlib import Path
from optparse import OptionParser
import core

# GLOBAL VARIABLES
class GlobalVars:
    version_major_required = 3
    version_minor_required = 8
    name = None
    module_name = os.path.basename(str(__file__)).split(".")[0]
    logformat = "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s"
    timestamp_logfile = core.Timestamp().logfile("%Y%m%d")
    timestamp_backup = core.Timestamp().backup("%Y%m%d%H%M%S")
    backup_directory = ".backup_userconfigs"


def main():
    core.Version(GlobalVars).check()

    GlobalVars.name = GlobalVars.module_name

    log = core.Log(GlobalVars)
    log.section("{} USER CONFIGURATIONS".format(GlobalVars.module_name).upper(), 5)

    # Command line options:
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option(
        "-u",
        "--userhome",
        dest="userhome",
        action="store",
        type="string",
        help="folder with configurations in the user home",
        metavar="USERHOME",
    )
    (options, args) = parser.parse_args()
    if options.userhome is None:
        parser.print_help()
        return 1
    options.userhome = os.path.abspath(options.userhome)

    if not os.path.isdir(options.userhome):
        parser.print_help()
        raise core.SyncError("directory {} invalid!".format(options.userhome))

    cwd = os.getcwd()
    log.info("current working directory: {}".format(cwd))

    source = options.userhome
    log.info("source: {}".format(source))
    target = str(Path.home())
    log.info("target: {}".format(target))

    if os.path.isdir(source):
        log.section("WALKING THE SOURCE", 3)
        for root, directories, files in os.walk(source):
            sync = core.Sync(GlobalVars, root, directories, files)
            sync.directories(source, target)
            sync.files(source, target)
            log.info()
    else:
        error = "path {} not found!"
        raise core.SyncError(error.format(source))
    return 0


if __name__ == "__main__":
    try:
        log = core.Log(GlobalVars)
        exitcode = main()
        sys.exit(exitcode)

    except PermissionError as e:
        print(str(e), file=sys.stderr)
    except core.SyncError as e:
        log.exception(e)
    except core.SyncMakeDirError as e:
        log.exception(e)
    except core.SyncCopyFileError as e:
        log.exception(e)
    except core.SyncCopySymlinkError as e:
        log.exception(e)

    sys.exit(1)
