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



class test_ping(unittest.TestCase):
    
    hosts = configparser.ConfigParser()
    hosts['host1'] = {'host_or_ip' : '1.1.1.1'}
    hosts['host2'] = {'host_or_ip' : 'host2'}
    hosts['host3'] = {'host_or_ip' : 'host3.domain.com'}
    hosts['host4'] = {'host_or_ip' : '4.4.4.4'}
    
    def test_ping_none(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            response = ping("ping", self.hosts)
            self.assertEqual(mock_system.call_count, 0)
            self.assertIs(type(response), str)
    
    def test_ping_host_single(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            ping("ping host host1", self.hosts)
            self.assertEqual(mock_system.call_count, 1)
            self.assertEqual(mock_system.call_args, 
                             (('ping -c 1 -q 1.1.1.1 > /dev/null',),))
            mock_system.return_value = False
            ping("ping host host2", self.hosts)
            self.assertEqual(mock_system.call_count, 2)
            self.assertEqual(mock_system.call_args, 
                             (('ping -c 1 -q host2 > /dev/null',),))

    def test_ping_host_multiple(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            ping("ping host host2 host3 host4", self.hosts)
            self.assertEqual(mock_system.call_count, 3)
            expected = [(('ping -c 1 -q host2 > /dev/null',),),
                        (('ping -c 1 -q host3.domain.com > /dev/null',),),
                        (('ping -c 1 -q 4.4.4.4 > /dev/null',),)]
            self.assertEqual(mock_system.call_args_list, expected)
    
    def test_ping_host_none(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            response = ping("ping host", self.hosts)
            self.assertIs(type(response), str)
            self.assertEqual(mock_system.call_count, 0)
        
    def test_ping_all(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            ping("ping all", self.hosts)
            self.assertEqual(mock_system.call_count, 4)
            expected = [(('ping -c 1 -q 1.1.1.1 > /dev/null',),),
                        (('ping -c 1 -q host2 > /dev/null',),),
                        (('ping -c 1 -q host3.domain.com > /dev/null',),),
                        (('ping -c 1 -q 4.4.4.4 > /dev/null',),)]
            self.assertEqual(mock_system.call_args_list, expected)
    
    def test_ping_other_ip(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            ping("ping other 1.1.1.1", self.hosts)
            self.assertEqual(mock_system.call_count, 1)
            self.assertEqual(mock_system.call_args, 
                             (('ping -c 1 -q 1.1.1.1 > /dev/null',),))
            mock_system.return_value = False
            ping("ping other 2.2.2.2", self.hosts)
            self.assertEqual(mock_system.call_count, 2)
            self.assertEqual(mock_system.call_args, 
                             (('ping -c 1 -q 2.2.2.2 > /dev/null',),))
    
    def test_ping_other_url(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            ping("ping other <https://test.com|test.com>", self.hosts)
            self.assertEqual(mock_system.call_count, 1)
            self.assertEqual(mock_system.call_args, 
                             (('ping -c 1 -q test.com > /dev/null',),))
            mock_system.return_value = False
            ping("ping other <https://google.com|google.com>", self.hosts)
            self.assertEqual(mock_system.call_count, 2)
            self.assertEqual(mock_system.call_args, 
                             (('ping -c 1 -q google.com > /dev/null',),))
        
    def test_ping_other_multiple(self):
        with patch('os.system') as mock_system:
            mock_system.return_value = True
            ping("ping other test.com google.com 1.1.1.1", self.hosts)
            self.assertEqual(mock_system.call_count, 3)
            expected = [(('ping -c 1 -q test.com > /dev/null',),),
                        (('ping -c 1 -q google.com > /dev/null',),),
                        (('ping -c 1 -q 1.1.1.1 > /dev/null',),),]
            self.assertEqual(mock_system.call_args_list, expected)
    
if __name__ == '__main__':
    unittest.main()