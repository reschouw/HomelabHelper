# Homelab Helper
# Testing module for info command
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

#Used for unit testing
import unittest
from unittest.mock import patch

#Modules used to create test environment
import configparser

#Modules to be tested
from commands import info



class test_wol(unittest.TestCase):
    
    hosts = configparser.ConfigParser()
    hosts['host1'] = {'wol_ready' : True,  'mac_address' : '11:11:11:11:11:11'}
    hosts['host2'] = {'wol_ready' : True,  'mac_address' : '22:22:22:22:22:22'}
    hosts['host3'] = {'wol_ready' : False, 'mac_address' : '33:33:33:33:33:33'}
    hosts['host4'] = {'wol_ready' : True,  'mac_address' : '44:44:44:44:44:44'}
    
    def test_info_none(self):
        response = info("info", self.hosts)
        self.assertIs(type(response), str)
    
    def test_info_ip(self):
        response = info("info ip", self.hosts)
        self.assertIs(type(response), str)
        
    def test_info_hosts(self):
        response = info("info hosts", self.hosts)
        self.assertIs(type(response), str)
    
    def test_info_host(self):
        response = info("info host MiniVerse", self.hosts)
        self.assertIs(type(response), str)
        response = info("info host host1", self.hosts)
        self.assertIs(type(response), str)