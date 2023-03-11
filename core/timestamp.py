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

    def logfile(self, format_):
        return self.__now.strftime(format_)

    def backup(self, format_):
        return self.__now.strftime(format_)
