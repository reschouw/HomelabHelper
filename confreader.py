# Homelab Helper
# Configuration reader
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import configparser


def createExConfig(config):
    """Creates example config file"""
    #config['Module1'] = {'Active' : 'yes'}
    config['Slack Integration'] = {'require_mention' : 'yes',
                                   'refresh_rate' : '0.3',
                                   '#bot_token' : ''}
    with open('exampleconfig', 'w') as configfile:
        config.write(configfile)
    print('Please rename the \'exampleconfig\' file to \'config\' after reviewing settings')

def createExHosts(hosts):
    """Creates example hosts file"""
    hosts['Example_Host_Entry'] = {'host_or_ip' : 'localhost',
                                   'mac_address' : 'ff:ff:ff:ff:ff:ff',
                                   'wol_ready' : 'yes'}
    with open('examplehosts', 'w') as hostsfile:
        hosts.write(hostsfile)
    print('Please rename the \'examplehosts\' file to \'hosts\' after reviewing settings')

def verifyConfigs(config, hosts):
    
    #Verify Hosts file
    print("Verifying hosts file...")
    for host in hosts.sections():
        verified = True
        try:
            hosts[host]['host_or_ip']
            hosts[host]['mac_address']
            hosts[host].getboolean('wol_ready')
        except KeyError:
            verified = False
        except ValueError:
            verified = False
        if len(hosts[host]['mac_address']) != 17:
            verified = False
        
        if not verified:
            print("Error found in " + host + " section of hosts file.")
            exit(1)
       
    #Verify config file
    print("Verifying config file...")
    verified = True
    try:
        config['Slack Integration'].getfloat('refresh_rate')
        config['Slack Integration'].getboolean('require_mention')
        config['Slack Integration']['bot_token']
    except KeyError:
        verified = False
    except ValueError:
        verified = False
    if not verified:
        print("Error found in Slack Integreaton section of config file.")
        exit(1)
    
    print("Verified!")
        

def openConfigs():
    """
        Verifies config files and opens them.
        Missing config files cause examples to be created and the program exited
    """
    config = configparser.ConfigParser()
    hosts = configparser.ConfigParser()
    
    config.read('config')
    hosts.read('hosts')
    
    #Create missing config files and exit
    if not config.sections() and not hosts.sections():
        print('Cannot find configuration files. Creating examples.')
        createExConfig(config)
        createExHosts(hosts)
        exit(0)
    elif not config.sections():
        print('Cannot find config file. Creating example.')
        createExConfig(config)
        exit(0)
    elif not hosts.sections():
        print('Cannot find hosts file. Creating example.')
        createExHosts(hosts)
        exit(0)
    
    verifyConfigs(config, hosts)
    
    return config, hosts