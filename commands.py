# Homelab Helper
# Command handlers
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

from wakeonlan import send_magic_packet

def help(command):
    """
       Print available commands and options
    """
    return "List of available commands:\n" + \
           "       - help: list available commands\n" + \
           "       - wol [host]: wake up all or specifies host"
           
def wol(command, hosts): 
    """
        Wake specified host or all hosts if no host specified
    """
    for host in hosts.sections():
        send_magic_packet(hosts[host]['mac_address'])
        print('wol:', hosts[host]['mac_address'])
    return "Sent!"