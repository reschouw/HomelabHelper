# Homelab Helper
# Testing module for wol command
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

#Used for unit testing
import unittest
from unittest.mock import patch

#Modules used to create test environment
import configparser

#Modules to be tested
from commands import wol



class test_commands(unittest.TestCase):
    
    hosts = configparser.ConfigParser()
    hosts['host1'] = {'wol_ready' : True,  'mac_address' : '11:11:11:11:11:11'}
    hosts['host2'] = {'wol_ready' : True,  'mac_address' : '22:22:22:22:22:22'}
    hosts['host3'] = {'wol_ready' : False, 'mac_address' : '33:33:33:33:33:33'}
    hosts['host4'] = {'wol_ready' : True,  'mac_address' : '44:44:44:44:44:44'}
    
    def test_wol_none(self):
        with patch('commands.send_magic_packet') as mock_send_magic_packet:
            response = wol("wol", self.hosts)
            self.assertEqual(mock_send_magic_packet.call_count, 0)
            self.assertIs(type(response), str)
            
    
    def test_wol_single(self):
        with patch('commands.send_magic_packet') as mock_send_magic_packet:
            response = wol("wol host2", self.hosts)
            self.assertIs(type(response), str)
            response = wol("wol host3", self.hosts)
            self.assertIs(type(response), str)
            self.assertEqual(mock_send_magic_packet.call_count, 1)
            self.assertEqual(mock_send_magic_packet.call_args,
                             (('22:22:22:22:22:22',),)
                            )
            
    def test_wol_multiple(self):
        with patch('commands.send_magic_packet') as mock_send_magic_packet:
            response = wol("wol host1 host3 host4", self.hosts)
            self.assertIs(type(response), str)
            self.assertEqual(mock_send_magic_packet.call_count, 2)
            expected = [(('11:11:11:11:11:11',),),
                        (('44:44:44:44:44:44',),),]
            self.assertEqual(mock_send_magic_packet.call_args_list, expected)
            
            
    def test_wol_all(self):
        with patch('commands.send_magic_packet') as mock_send_magic_packet:
            with patch('os.system', return_value=1) as mock_system:
                wol("wol all", self.hosts)
                self.assertEqual(mock_system.call_count, 3)
                self.assertEqual(mock_send_magic_packet.call_count, 3)
        
        
        
if __name__ == '__main__':
    unittest.main()