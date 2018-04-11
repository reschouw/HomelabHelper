# Homelab Helper
# Command handlers
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import os

from wakeonlan import send_magic_packet

def help():
    """
       Print available commands and options
    """
    return "List of available commands:\n" + \
           "       - help: list available commands\n" + \
           "       - wol [host]: wake up all or specifies host\n" + \
           "       - ping [host]: ping specified host and return response\n" + \
           "Type the name of a command to see more specific usage info"
           
def wol(command, hosts): 
    """
        Wake specified host(s)
    """
    command = command.split(" ")
    response = ""
    success = True
    if len(command) > 1:
        #Valid usage
        if command[1] == "all":
            #Wake all hosts
            for hostname in hosts.sections():
                if hosts[hostname].getboolean('wol_ready'):
                    send_magic_packet(hosts[hostname]['mac_address'])
                    print('wol:', hosts[hostname]['mac_address'])
                    response = response + "Waking " + hostname + "\n"
        else:
            #Wake specified hosts
            for i in range (1, len(command)):
                try:
                    hostname = command[i]
                    if hosts[hostname].getboolean('wol_ready'):
                        send_magic_packet(hosts[hostname]["mac_address"])
                        print('wol:', hosts[hostname]['mac_address'])
                        response = response + "Waking " + hostname + "\n"
                    else:
                        response = response + "Host " + hostname + \
                                              " is not WOL ready\n"
                        success = False
                except KeyError:
                    response = response + "Unknown host: '" + hostname + "'\n"
                    success = False
        if success :
            #All hosts woken successfully
            return response + "Finished sending wake-up packets"
        else:
            #Some hosts not wol ready or unknown
            return response + "Not all hosts wol ready or were not known.\n" + \
                              "Check your host file or your capitalization"
    else:
        #Invalid usage
        return "No host specified. Use \'wol all\' to wake all hosts."
    
def ping(command, hosts):
    """
        Pings specified host(s)
    """
    command = command.split(" ")
    if len(command) > 1:
        #Valid usage
        if command[1] == "all":
            #Ping all hosts
            response = ""
            for host in hosts.sections():
                hostname = hosts[host]['host_or_ip']
                pong = os.system("ping -c 1 -q " + hostname + " > /dev/null")
                print("ping:" + hostname)
                if pong == 0:
                    print("Host up!")
                    response = response + hostname + ": Host up!\n"
                else:
                    print("Host down!")
                    response = response + hostname + ": Host down!\n"
        else:
            #Wake specified hosts
            response = ""
            for i in range (1, len(command)):
                hostname = command[i]
                pong = os.system("ping -c 1 -q " + hostname + " > /dev/null")
                print("ping:" + hostname)
                if pong == 0:
                    print("Host up!")
                    response = response + hostname + ": Host up!\n"
                else:
                    print("Host down!")
                    response = response + hostname + ": Host down!\n"
        return response + "Task complete!"
    else:
        #Invalid usage
        return "No host specified. Us \'ping all\' to ping all hosts"