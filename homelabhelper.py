# Homelab Helper
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import os
import time
import re
import configparser
from slackclient import SlackClient


def createExConfig():
    """Creates example config file"""
    #config['Module1'] = {'Active' : 'yes'}
    config['Slack Integration'] = {'#bot_token' : '',
                                   'refresh_rate' : '1'}
    with open('exampleconfig', 'w') as configfile:
        config.write(configfile)
    print('Please rename the \'exampleconfig\' file to \'config\' after reviewing settings')

def createExHosts():
    """Creates example hosts file"""
    #config['Host1'] = {'Active' : 'yes'}
    with open('examplehosts', 'w') as hostsfile:
        config.write(hostsfile)
    print('Please rename the \'examplehosts\' file to \'hosts\' after reviewing settings')

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event['type'] == 'message':
            user_id, message = parse_direct_mention(event['text'])
            if user_id == bot_id:
                return message, event['channel']
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search("^<@(|[WU].+?)>(.*)", message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format('help')

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith('help'):
        response = "List of available commands:\n" + \
                   "    - help: list available commands"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

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
        createExConfig()
        createExHosts()
        exit(0)
    elif not config.sections():
        print('Cannot find config file. Creating example.')
        createExConfig()
        exit(0)
    elif not hosts.sections():
        print('Cannot find hosts file. Creating example.')
        createExHosts()
        exit(0)
    
    #Read in important config values
    try:
        refresh_rate = config['Slack Integration'].getfloat('refresh_rate')
        if not refresh_rate:
            raise TypeError('Invalid refresh_rate value', refresh_rate)
    except TypeError as err:
        print (err.args)
        exit(1)
            
    #Connect to Slack and start bot
    #Credit to Matt Makai @fullstackpython for starter code
    if 'bot_token' in config['Slack Integration']:
        slack_client = SlackClient(config['Slack Integration']['bot_token'])
    else:
        slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    bot_id = None
    if slack_client.rtm_connect(with_team_state=False):
        print("Homelab Helper Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(refresh_rate)
    else:
        print("Connection failed. Exception traceback printed above.")
        
        
        
        
        
        
        