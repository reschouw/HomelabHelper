# Homelab Helper
# Command handlers
# Ryan Schouweiler
# A modular homelab helper
# https://github.com/reschouw/HomelabHelper

import os
import urllib.request

from wakeonlan import send_magic_packet

def help():
    """
       Print available commands and options
    """
    return "List of available commands:\n" + \
           "       - help: list available commands\n" + \
           "       - wol [host]: wake up all or specifies host\n" + \
           "       - ping [host]: ping specified host and return response\n" + \
           "       - info [option]: retreive specified information" + \
           "Type the name of a command to see more specific usage info"
           
def wol(command, hosts): 
    """
        Wake specified host(s)
    """
    def isup(host):
        """
            Returns True if host is reachable, else False
        """
        pong = os.system("ping -c 1 -q " + host + " > /dev/null")
        if pong == 0:
            return True
        else:
            return False
    
    
    command = command.split(" ")
    response = ""
    success = True
    if len(command) > 1:
        #Valid usage
        if command[1] == "all":
            #Wake all hosts
            for hostname in hosts.sections():
                if hosts[hostname].getboolean('wol_ready'):
                    if isup(hostname):
                        response = response + "Host \'" + hostname + \
                                              "\' is already up.\n"
                    else:
                        send_magic_packet(hosts[hostname]['mac_address'])
                        print('wol:', hosts[hostname]['mac_address'])
                        response = response + "Waking \'" + hostname + "\'.\n"
        else:
            #Wake specified hosts
            for i in range (1, len(command)):
                try:
                    hostname = command[i]
                    if hosts[hostname].getboolean('wol_ready'):
                        send_magic_packet(hosts[hostname]["mac_address"])
                        print('wol:', hosts[hostname]['mac_address'])
                        response = response + "Waking \'" + hostname + "\'.\n"
                    else:
                        response = response + "Host \'" + hostname + \
                                              "\' is not WOL ready.\n"
                        success = False
                except KeyError:
                    response = response + "Unknown host: \'" + \
                                          hostname + "\'.\n"
                    success = False
        if success :
            #All hosts woken successfully
            return response + "Task complete."
        else:
            #Some hosts not wol ready or unknown
            return response + "Not all hosts wol ready or were not known.\n" + \
                              "Check your host file or your capitalization."
    else:
        #Invalid usage
        return "No host specified. Use \'wol all\' to wake all hosts."

def ping(command, hosts):
    """
        Pings specified host(s)
    """
    
    def doping(host):
        """
            Performs actual pinging of a host and returns status
        """
        pong = os.system("ping -c 1 -q " + host + " > /dev/null")
        print("ping:" + host)
        if pong == 0:
            print("Host up!")
            return host + ": Host reachable.\n"
        else:
            print("Host down!")
            return host + ": Host not reachable.\n"
            
            
    command = command.split(" ")
    if len(command) > 1:
        #Valid usage (probably)
        response = ""
        if command[1] == "all":
            #Ping all hosts
            for host in hosts.sections():
                target = hosts[host]['host_or_ip']
                response = response + doping(target)
        elif command[1] == "host":
            if len(command) < 3:
                return "Please specify a host."
            else:
                #Ping specific targets from hosts file
                for i in range(2, len(command)):
                    host = command[i]
                    try:
                        target = hosts[host]['host_or_ip']
                        response = response + doping(target)
                    except KeyError:
                        #Host not in hosts file
                        response = response + "Host \'" + host + "\' not found.\n"
        else:
            #Wake specified targets
            for i in range (1, len(command)):
                target = command[i]
                response = response + doping(target)
        return response + "Task complete."
    else:
        #Invalid usage
        return "No host specified. Use \'ping all\' to ping all hosts or " + \
               "\'ping host [target(s)]\' to ping hosts from the hosts file"

def info(command, hosts):
    """
        Returns external IP using https://ident.me
    """
    command = command.split(" ")
    if len(command) == 2:
        #Valid usage
        if command[1] == "ip":
            ext_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
            return "Your external IP is " + ext_ip
        else:
            return "Unknown option."
    else:
        #No options given
        return "No option specified. Available options: \n" + \
               "    - \'ip\' : return public IP address"
    
        
    
    
    
    
    
    