# Homelab Helper
# Testing module for help command
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

#Used for unit testing
import unittest

#Modules to be tested
from commands import help



class test_help(unittest.TestCase):
    
    def test_help_none(self):
        response = help()
        self.assertIs(type(response), str)

        
if __name__ == '__main__':
    unittest.main()