#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2021 Denis Meyer
#

"""Waits for the kill signal and sets a flag when it fires"""

import logging
import signal

class GracefulKiller:

    def __init__(self):
        """Initializes the graceful killer state"""
        self.kill_now = False
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _exit_gracefully(self, signum, frame):
        """Sets the graceful killer state to exit

        :param signum The exit signal
        :param frame: The frame
        """
        logging.info('Received exit signal {}. Please wait a moment to shut down gracefully...'.format(signum))
        self.kill_now = True
