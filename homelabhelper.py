# Homelab Helper
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import os
import time
import configparser

from slackint import Slack_Bot

def createExConfig(config):
    """Creates example config file"""
    #config['Module1'] = {'Active' : 'yes'}
    config['Slack Integration'] = {'require_mention' : 'yes',
                                   'refresh_rate' : '0.3',
                                   '#bot_token' : ''}
    with open('exampleconfig', 'w') as configfile:
        config.write(configfile)
    print('Please rename the \'exampleconfig\' file to \'config\' after reviewing settings')

def createExHosts(hosts):
    """Creates example hosts file"""
    hosts['Example_Host_Entry'] = {'mac_address' : 'ff:ff:ff:ff:ff:ff'}
    with open('examplehosts', 'w') as hostsfile:
        hosts.write(hostsfile)
    print('Please rename the \'examplehosts\' file to \'hosts\' after reviewing settings')

# Main entry point
if __name__ == "__main__":
    print("Homelab Helper starting...")

    #Open config files
    config = configparser.ConfigParser()
    hosts = configparser.ConfigParser()

    config.read('config')
    hosts.read('hosts')

    if not config.sections() and not hosts.sections():
        print('Cannot find configuration files. Creating examples.')
        createExConfig(config)
        createExHosts(hosts)
        exit(0)
    elif not config.sections():
        print('Cannot find config file. Creating example.')
        createExConfig(config)
        exit(0)
    elif not hosts.sections():
        print('Cannot find hosts file. Creating example.')
        createExHosts(hosts)
        exit(0)
    
    #Read in important config values
    try:
        refresh_rate = config['Slack Integration'].getfloat('refresh_rate')
        if not refresh_rate:
            raise TypeError('Invalid refresh_rate value', refresh_rate)
        require_mention = config['Slack Integration'].getboolean('require_mention')
        if require_mention is None:
            raise TypeError('Invalid require_mention value', require_mention)
    except TypeError as err:
        print (err.args)
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
        
        
        
        
        
        
        