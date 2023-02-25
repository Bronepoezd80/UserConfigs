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
    timestamp_logfile = core.Timestamp().logfile()
    timestamp_backup = core.Timestamp().backup()
    backup_directory = ".backup_userconfigs"


def main():
    # Version().check()
    core.Version(GlobalVars).check()

    GlobalVars.name = GlobalVars.module_name
    class Main:
        log = core.Log(GlobalVars)
    Main.log.section("{} USER CONFIGURATIONS".format(GlobalVars.module_name).upper(), 5)

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
    options.userhome = os.path.abspath(options.userhome)

    if options.userhome is None:
        parser.print_help()
        return
    if not os.path.isdir(options.userhome):
        parser.print_help()
        raise core.SyncError("directory {} invalid!".format(options.userhome))

    cwd = os.getcwd()
    Main.log.info("current working directory: {}".format(cwd))

    # source = os.path.join(cwd, "userhome")
    source = options.userhome
    Main.log.info("source: {}".format(source))

    target = str(Path.home())
    Main.log.info("target: {}".format(target))

    if os.path.isdir(source):
        Main.log.section("WALKING THE SOURCE", 3)
        for root, directories, files in os.walk(source):
            sync = core.Sync(GlobalVars, root, directories, files)
            sync.directories(source, target)
            sync.files(source, target)
            Main.log.info()
    else:
        error = "path {} not found!"
        raise core.SyncError(error.format(source))

    return


if __name__ == "__main__":
    try:
        log = core.Log(GlobalVars)
        main()
        sys.exit(0)

    except core.SyncError as e:
        log.exception(e)
    except core.SyncMakeDirError as e:
        log.exception(e)
    except core.SyncCopyFileError as e:
        log.exception(e)
    except core.SyncCopySymlinkError as e:
        log.exception(e)

    sys.exit(1)
