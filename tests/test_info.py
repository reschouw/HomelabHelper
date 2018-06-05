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
from commands import wol



class test_wol(unittest.TestCase):

    def test_info_none(self):
        pass