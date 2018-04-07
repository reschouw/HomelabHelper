# Homelab Helper
# Slack Integration
# Ryan Schouweiler
# Credit to Matt Makai @fullstackpython for starter code
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import re
from slackclient import SlackClient

from commands import *



class Slack_Bot:
    
    def __init__(self, bot_token, require_mention, hosts):
        """
            Creates slack client with given bot token and settings
        """
        self.slack_client = SlackClient(bot_token)
        self.bot_id = None
        self.require_mention = require_mention
        self.hosts = hosts
        
            
    def connect(self):
        """
            Connects slack client and gets assigned bot id
        """
        if self.slack_client.rtm_connect(with_team_state=False,
                                         auto_reconnect=True):
            # Read bot's user ID by calling Web API method `auth.test`
            self.bot_id = self.slack_client.api_call("auth.test")["user_id"]
            return True
        else:
            return False
    
    def read_command(self):
        """
            Checks for new messages on slack and handles them appropriately
        """
        command, channel = self.parse_bot_commands(self.slack_client.rtm_read())
        if command:
            self.handle_command(command, channel)
    
    def parse_bot_commands(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event['type'] == 'message':
                if self.require_mention:
                    user_id, message = parse_direct_mention(event['text'])
                    if user_id == self.bot_id:
                        return message, event['channel']
                else:
                    #Prevent bot responding to it's own messages
                    if 'user' in event and event['user'] != self.bot_id:
                        return event['text'], event['channel']
        return None, None

    def parse_direct_mention(self, message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search("^<@(|[WU].+?)>(.*)", message_text)
        # The first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip())\
                if matches else (None, None)

    def handle_command(self, command, channel):
        """
            Executes bot command if the command is known
        """
        # Default response is help text for the user
        default_response = "Not sure what you mean. Try *{}*.".format('help')

        # Finds and executes the given command, filling in response
        response = None
        if command.startswith('help'):
            response = help()
        elif command.startswith('wol'):
            response = wol(command, self.hosts)
        elif command.startswith('ping'):
            response = ping(command, self.hosts)

        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )