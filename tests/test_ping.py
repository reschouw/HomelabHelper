# Homelab Helper
# Testing module for ping command
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

#Used for unit testing
import unittest
from unittest.mock import patch

#Modules used to create test environment
import configparser

#Modules to be tested
from commands import ping



class test_help(unittest.TestCase):
    
    hosts = configparser.ConfigParser()
    hosts['host1'] = {'host_or_ip' : '1.1.1.1'}
    hosts['host2'] = {'host_or_ip' : 'host2'}
    hosts['host3'] = {'host_or_ip' : 'host2.domain.com'}
    hosts['host4'] = {'host_or_ip' : '4.4.4.4'}
    
    def test_ping_host_single(self):
        pass

    def test_ping_host_multiple(self):
        pass
    
    def test_ping_host_none(self):
        pass
        
    def test_ping_all(self):
        pass
    
    def test_ping_other_ip(self):
        pass
    
    def test_ping_other_url(self):
        pass
        
    def test_ping_other_multiple(self):
        pass
if __name__ == '__main__':
    unittest.main()