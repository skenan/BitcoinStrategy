#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging.config
import os.path


class Log:
    def __init__(self):
        LOGGING_CONF = os.path.join(os.path.dirname(__file__), "../logging.ini")
        logging.config.fileConfig(LOGGING_CONF)
        self.log = logging.getLogger("bitcoin")

    def info(self, message):

        self.log.info(message)

    def warning(self, message):
        self.log.warning(message)

    def debug(self, message):
        self.log.debug(message)




if __name__ == '__main__':
    log = Log()
    log.info("fdsfds")