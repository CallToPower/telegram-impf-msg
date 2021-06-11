#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2021 Denis Meyer
#
# This file is part of raspi-sapis
#

"""Settings - The settings storage"""


import logging
import time
import os

class Settings:

    _FOLDER_LOG_OUT = 'logs'
    _FILE_LOG_OUT_TMPL = 'telegram-impf-msg.application-{}.log'

    def __init__(self,
                    log_out_foldername=_FOLDER_LOG_OUT,
                    log_out_filename_tmpl=_FILE_LOG_OUT_TMPL):
        """Initializes the class

        :param log_out_foldername: The log output folder name
        :param log_out_filename_tmpl: The log output file name
        """
        logging.info('Initializing')

        self.log_filename = os.path.join(
            os.getcwd(),
            log_out_foldername, log_out_filename_tmpl.format(time.strftime('%d-%m-%Y-%H-%M-%S')))

        self.log_to_file = True
        self.log_level = logging.INFO
        self.log_format = '[%(asctime)s] [%(levelname)-7s] [%(module)-20s:%(lineno)-4s] %(message)s'
        self.log_dateformat = '%d-%m-%Y %H:%M:%S'
