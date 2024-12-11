"""
Simple module for demonstrating the log.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import scilogger

# create the logger
LOGGER = scilogger.get_logger(__name__, "mod_b")


def display():
    LOGGER.info("module_b")
    with LOGGER.BlockIndent():
        LOGGER.debug("debug level log")
        LOGGER.info("info level log")
        LOGGER.error("error level log")
