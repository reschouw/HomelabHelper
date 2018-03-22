# Homelab Helper
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper


import configparser

def createExConfig():
    """Creates example config file"""
    #config['Module1'] = {'Active' : 'yes'}
    with open('exampleconfig', 'w') as configfile:
        config.write(configfile)
    print('Please rename the \'exampleconfig\' file to \'config\' after reviewing settings')

def createExHosts():
    """Creates example hosts file"""
    #config['host1'] = {'Active' : 'yes'}
    with open('examplehosts', 'w') as hostsfile:
        config.write(hostsfile)
    print('Please rename the \'examplehosts\' file to \'hosts\' after reviewing settings')

    

# Main entry point
print("Homelab Helper starting...")

config = configparser.ConfigParser()
hosts = configparser.ConfigParser()

config.read('config')
hosts.read('hosts')

if not config.sections() and not hosts.sections():
    print('Cannot find configuration files. Creating examples.')
    createExConfig()
    createExHosts()
    exit()
elif not config.sections():
    print('Cannot find config file. Creating example.')
    createExConfig()
    exit()
elif not hosts.sections():
    print('Cannot find hosts file. Creating example.')
    createExHosts()
    exit()