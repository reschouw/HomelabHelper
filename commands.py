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
           "       - wol [host]: wake up all or specifies host" + \
           "Type the name of a command to see more specific usage info"
           
def wol(command, hosts): 
    """
        Wake specified host(s)
    """
    command = command.split(" ")
    if len(command) > 1:
        #Valid usage
        if command[1] == "all":
            #Wake all hosts
            for host in hosts.sections():
                send_magic_packet(hosts[host]['mac_address'])
                print('wol:', hosts[host]['mac_address'])
        else:
            #Wake specified hosts
            for i in range (1, len(command)):
                try:
                    send_magic_packet(hosts[command[i]]["mac_address"])
                    print('wol:', hosts[command[i]]['mac_address'])
                except KeyError:
                    return "Unknown host: " + command[i] + \
                           ". Hostnames are case-sensitive"

        return "Sent!"
    else:
        #Invalid usage
        return "No host specified. use \'wol all\' to wake all hosts."
    