# Homelab Helper
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/PacketParser

import configparser

print("Homelab Helper starting...")

config = configparser.ConfigParser()

print(config.read('blah'))

if config['test'].getboolean('Active'):
    print('Test')

if config['test2'].getboolean('Active'):
    print('Test2')
