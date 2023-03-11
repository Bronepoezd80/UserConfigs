"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-22

    Synchronize User Configurations - Core - Exceptions.
"""


class SyncError(Exception):
    def __init__(self, message_):
        self.__message = message_
        super().__init__(self.__message)


class SyncMakeDirError(SyncError):
    pass


class SyncCopyFileError(SyncError):
    pass


class SyncCopySymlinkError(SyncError):
    pass
