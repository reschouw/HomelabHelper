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
    
    print("Copyright (C) 2018  Ryan Schouweiler")
    
    print("This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.")

    #Open and verify config files
    config, hosts = openConfigs()

    #Read in important config values
    refresh_rate = config['Slack Integration'].getfloat('refresh_rate')
    require_mention = config['Slack Integration'].getboolean('require_mention')
            
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
        
        
        
        
        
        
        