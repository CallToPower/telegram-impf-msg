#!/bin/bash

if [[ -e /tmp/telegram-impf-msg.py.pid ]]; then
    echo "telegram-impf-msg is running, stopping..."
    kill `cat /tmp/telegram-impf-msg.py.pid`
    rm /tmp/telegram-impf-msg.py.pid
    echo "telegram-impf-msg has been stopped"
else
    echo "telegram-impf-msg is not running"
fi