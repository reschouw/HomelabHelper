# Homelab Helper
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import os
import time

from slackint import Slack_Bot
from confreader import *



# Main entry point
if __name__ == "__main__":
    print("Homelab Helper starting...")

    #Open and verify config files
    config, hosts = openConfigs()

    #Read in important config values
    try:
        refresh_rate = config['Slack Integration'].getfloat('refresh_rate')
        if not refresh_rate:
            raise TypeError('Invalid refresh_rate value', refresh_rate)
        require_mention = config['Slack Integration']\
                                 .getboolean('require_mention')
        if require_mention is None:
            raise TypeError('Invalid require_mention value', require_mention)
    except TypeError as err:
        print(err.args)
        exit(1)
            
    #Connect to Slack, start, and run bot
    if 'bot_token' in config['Slack Integration']:
        slack_bot = Slack_Bot(config['Slack Integration']['bot_token'],
                              require_mention,
                              hosts)
    else:
        slack_bot = Slack_Bot(os.environ.get('SLACK_BOT_TOKEN'),
                                             require_mention,
                                             hosts)
    if slack_bot.connect():
        print("Homelab Helper Bot connected and running!")
        while True:
            slack_bot.read_command()
            time.sleep(refresh_rate)
    else:
        print("Connection failed. Exception traceback printed above.")
        exit(1)
        
        
        
        
        
        
        