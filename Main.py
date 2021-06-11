#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2021 Denis Meyer
#

"""Main"""

__prog__ = 'telegram-impf-msg'
__version__ = '1.0'

import logging
import sys
import os
from time import sleep

from urllib.request import urlopen
import json
import threading

import telegram

from lib.Settings import Settings
from lib.GracefulKiller import GracefulKiller

IDLE_SLEEP_S = 30
config_impfzentren_str = 'impfzentren_config.json'

def initialize_logger(settings):
    """Initializes the logger
    :param settings: The settings
    """
    if settings.log_to_file:
        basedir = os.path.dirname(settings.log_filename)

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    logger = logging.getLogger()
    logger.setLevel(settings.log_level)
    logger.propagate = False

    logger.handlers = []

    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.setLevel(settings.log_level)
    handler_console.setFormatter(logging.Formatter(
        fmt=settings.log_format, datefmt=settings.log_dateformat))
    logger.addHandler(handler_console)

    if settings.log_to_file:
        handler_file = logging.FileHandler(
            settings.log_filename, mode='w', encoding=None, delay=False)
        handler_file.setLevel(settings.log_level)
        handler_file.setFormatter(logging.Formatter(
            fmt=settings.log_format, datefmt=settings.log_dateformat))
        logger.addHandler(handler_file)


def load_config(config_name):
    with open(config_name, 'r') as f:
        config = json.load(f)
    return config


def getJson(url, object_hook=None):
    with urlopen(url) as resource:
        return json.load(resource, object_hook=object_hook)


def is_vax_available(url):
    try:
        json_response = getJson(url)
    except:
        logging.error('Failed to get URL')
        return False, 0
    try:
        at_least_one_in_stock = False
        nr_in_stock = 0
        result_list = json_response['resultList']
        logging.debug('Got {} result(s)'.format(len(result_list)))
        for result in json_response['resultList']:
            logging.debug(result)
            found = (not result['outOfStock']) if 'outOfStock' in result else False
            if found:
                logging.info(result)
                at_least_one_in_stock = True
            nr_in_stock += result['freeSlotSizeOnline'] if 'freeSlotSizeOnline' in result else 0
    except:
        logging.error('Failed to parse JSON')
        return False, 0

    return at_least_one_in_stock, nr_in_stock

if __name__ == '__main__':
    settings = Settings()
    initialize_logger(settings)

    logging.info('{} starting'.format(__prog__))

    logging.info('Loading config')
    config = load_config(config_impfzentren_str)
    logging.debug(config)
    logging.info('Config loaded')

    logging.info('Initializing telegram bot(s)')
    for c in config:
        c['telegram']['bot'] = telegram.Bot(token=c['telegram']['token'])
        bot_info = c['telegram']['bot'].get_me()
        logging.info('Bot info: {}'.format(bot_info))
        logging.info('Sending messages to chat[ID={}]'.format(c['telegram']['chat_id']))
        if c['telegram']['send']:
            c['telegram']['bot'].send_message(chat_id=c['telegram']['chat_id'], text='Ich bin online und suche im {} nach Terminen für dich.'.format(c['name']))
    logging.info('Telegram bot(s) initialized')

    logging.info('Starting polling')
    g_killer = GracefulKiller()
    while not g_killer.kill_now:
        try:
            for c in config:
                if c['poll']:
                    logging.info('Polling {}...'.format(c['name']))
                    avail = is_vax_available(c['url'])
                    if avail[0]:
                        logging.info('{} Impfungen(en) im {} verfügbar - jetzt auf {} prüfen!'.format(avail[1], c['name'], c['main_url']))
                        if c['telegram']['send']:
                            c['telegram']['bot'].send_message(chat_id=c['telegram']['chat_id'], text='{} Impfungen(en) im {} verfügbar - jetzt auf {} prüfen!'.format(avail[1], c['name'], c['main_url']))
                    else:
                        logging.info('Nothing found...')
            sleep(IDLE_SLEEP_S)
        except Exception as e:
            logging.error('Something went wrong:')
            logging.error(e)
    logging.info('Stopping polling')

    logging.info('Shutting down telegram bot(s)')
    for c in config:
        if c['telegram']['send']:
            c['telegram']['bot'].send_message(chat_id=c['telegram']['chat_id'], text='Ich bin nun offline.')
    logging.info('Telegram bot(s) shut down')

    logging.info('Quitting')
    sys.exit(0)
