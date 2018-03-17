# Homelab Helper
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper


import configparser

def createConfig():
    """Creates example config file"""
    print('No existing config file. Creating example.')
    config['test'] = {'Active' : 'yes'}
    config['test2'] = {'Active' : 'yes'}
    with open('example.cfg', 'w') as configfile:
        config.write(configfile)
    print('Please rename the example.cfg file to helper.cfg after reviewing settings')

    

# Main entry point
print("Homelab Helper starting...")

config = configparser.ConfigParser()

config.read('helper.cfg')
if not config.sections():
    createConfig()
    exit()

if config['test'].getboolean('Active'):
    print('Test')

if config['test2'].getboolean('Active'):
    print('Test2')
