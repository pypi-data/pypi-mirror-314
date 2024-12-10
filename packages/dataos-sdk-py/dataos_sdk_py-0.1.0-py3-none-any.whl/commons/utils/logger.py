import logging
from logging.config import fileConfig
from os import path
import sys

# file_path = path.join(path.dirname(path.dirname(sys.modules['__main__'].__file__)), 'logging_config.ini')
# fileConfig(file_path)


def get(name):
    logger = logging.getLogger(name)
    return logger
