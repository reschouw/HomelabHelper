# Homelab Helper
# Testing module for bot commands
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import unittest
from unittest.mock import patch

import slack_commands
from slack_commands import *


class test_commands(unittest.TestCase):
    hosts = {
             'host1' : {'wol_ready' : True,  'mac_address' : '11:11:11:11:11:11'},
             'host2' : {'wol_ready' : True,  'mac_address' : '22:22:22:22:22:22'},
             'host3' : {'wol_ready' : True,  'mac_address' : '33:33:33:33:33:33'},
             'host4' : {'wol_ready' : False, 'mac_address' : '44:44:44:44:44:44'},
            }
         
         
    def test_example(self):
        print ("Hello World!")
        
    def test_help(self):
        return isinstance(help(), str)

    def test_wol_all(self):
        with patch('slack_commands.wakeonlan.send_magic_packet') as mock_send_magic_packet:
            wol(["wol", "all"], self.hosts)
            assertEqual(mock_send_magic_packet, 3)
        
        
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()