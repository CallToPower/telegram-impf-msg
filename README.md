# telegram-impf-msg

Polls vaccination centers for available dates and sends a telegram message if found.
It's possible to configure multiple vaccination centers that get updated to multiple telegram groups.

Copyright (C) 2021 Denis Meyer

## Prerequisites

* Python 3
* Windows
  * Add Python to PATH variable in environment

## TODO before using

* Create a token
** https://t.me/botfather ( https://core.telegram.org/bots#6-botfather )
* Get chat ID
** Add the Telegram bot to the group
** Get the list of updates for your BOT: https://api.telegram.org/bot<botToken>/getUpdates
** Look for the "chat" object
* Fill in the token and chat ID in Main.py

## Usage

* Start shell
  * Windows
    * Start shell as administrator
    * `Set-ExecutionPolicy Unrestricted -Force`
* Create a virtual environment
  * `python -m venv venv`
* Activate the virtual environment
  * Mac/Linux
    * `source venv/bin/activate`
  * Windows
    * `.\venv\scripts\activate`
* Install the required libraries
  * `pip install -r requirements.txt`
* Configure
  * `impfzentren_config.json`
* Run the app
  * `python Main.py`
