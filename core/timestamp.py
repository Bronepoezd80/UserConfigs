"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-21

    Synchronize User Configurations - Core - Timestamp.
"""
from datetime import datetime as _dt


class Timestamp(object):
    def __init__(self):
        self.__now = _dt.now()
        return

    def logfile(self):
        return self.__now.strftime("%Y%m%d")

    def backup(self):
        return self.__now.strftime("%Y%m%d%H%M%S")
