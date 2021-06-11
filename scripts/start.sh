#!/bin/bash

cd src
if [[ ! -e /tmp/telegram-impf-msg.py.pid ]]; then
    echo "Starting telegram-impf-msg..."
    # python3 raspi-sapis.py <username>:<password> &
    source venv/bin/activate
    python Main.py &
    echo $! > /tmp/telegram-impf-msg.py.pid
    echo "telegram-impf-msg has been started with pid "
    cat /tmp/telegram-impf-msg.py.pid
else
    echo -n "ERROR: telegram-impf-msg seems to be running with pid "
    cat /tmp/telegram-impf-msg.py.pid
    echo
fi