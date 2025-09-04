import inspect
import logging
import os
from test.conftest import *

from dotenv import load_dotenv
load_dotenv()

class BaseClass:
        def getlogger(self):
            loggerName = inspect.stack()[1][3]
            logger = logging.getLogger(loggerName)

            if not logger.hasHandlers():  # Check if logger already has handlers to avoid duplication
                formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")

            fileHandler = logging.FileHandler("test_logs.log")
            formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
            logger.addHandler(streamHandler)

            logger.setLevel(logging.DEBUG)
            return logger
