"""
    Jakob Janzen
    jakob.janzen80@gmail.com
    2023-02-25

    Synchronize User Configurations - Core - Logging.
"""
import logging as _log


class Log(object):
    def __init__(self, GlobalVars_):
        """Distinguish loggers through name."""
        self.__logger = _log.getLogger(GlobalVars_.module_name)
        self.__logger.setLevel(_log.INFO)
        self.__format = GlobalVars_.logformat
        self.__formatter = _log.Formatter(self.__format)
        # Log-file with only date timestamp, avoid files overkill by omitting time.
        self.__logfile = "{}_{}.log".format(
            GlobalVars_.module_name, GlobalVars_.timestamp_logfile
        )
        # Avoid multiple times logging by creating handlers only if required.
        if not self.__logger.handlers:
            self.__file_handler = self.__output_file_handler()
            self.__console_handler = self.__output_console_handler()

    def __output_file_handler(self):
        file_handler = _log.FileHandler(self.__logfile)
        file_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(file_handler)
        return file_handler

    def __output_console_handler(self):
        console_handler = _log.StreamHandler()
        console_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(console_handler)
        return console_handler

    def info(self, message_="________"):
        self.__logger.info(message_)

    def warning(self, message_="________"):
        self.__logger.warning(message_)

    def error(self, message_="________"):
        self.__logger.error(message_)

    def critical(self, message_="________"):
        self.__logger.critical(message_)

    def section(self, message_="________", level_=1):
        self.info("{} {} {}".format("*" * level_, message_, "*" * level_))

    def exception(self, message_="________"):
        self.__logger.exception(message_)
