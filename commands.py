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
           "       - ping [host|other] [host/url/IP]: ping and return response\n" + \
           "       - info [option]: retreive specified information\n" + \
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
        #Return usage
        return "Usage:\n" + \
               "    \'wol [host1 host2 ...]' to wake specified host(s)\n" + \
               "    \'wol all\' will wake all WOL capable hosts"

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
        elif command[1] == "other":
            if len(command) < 3:
                return "Please specify a host/url/IP."
            for i in range (2, len(command)):
                #Check for links. Slack will wrap them and 
                if "|" in command[i]:
                    print ("Link detected!")
                    link = command[i]
                    target = link[link.find("|")+1:link.rfind(">")]
                    print (target)
                    response = response + doping(target)
                else:
                    response = response + doping(command[i])
        else:
            #No valid option specified
            response = response + "Invalid option. Type \'ping\' for available options.\n"
        return response + "Task complete."
    else:
        #Return usage
        return "Usage: \n" + \
               "    \'ping all\' to ping all hosts\n" + \
               "    \'ping host [host1 host 2 ...]\' to ping specific" + \
                                 "hosts from the hosts file\n" + \
               "    \'ping other [host1 host 2 ...]\' Ping hosts/urls/IP addresses not in hosts file."

def info(command, hosts):
    """
        Returns config info, hosts info, or external IP using https://ident.me
    """
    command = command.split(" ")
    if len(command) > 1:
        #Valid usage (probably)
        if command[1] == "ip":
            try:
                ext_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
                return "Your external IP is " + ext_ip
            except:
                return "Unable to retreive public IP address. Check your internet connection."
        elif command[1] == "hosts":
            response = "Available hosts:\n"
            for host in hosts:
                if host == "DEFAULT":
                    continue
                response = response + "    - " + host + "\n"
            return response
        elif command[1] == "host" and len(command) < 4:
            try:
                host = hosts[command[2]]
            except:
                return "Unknown host!"
            response = "Config information for " + command[2] + ":\n"
            for line in host:
                response = response + "    " + line + " : " + host[line] + "\n"
            return response
        else:
            return "Unknown option."
    else:
        #Return usage
        return "Usage: \n" + \
               "    info ip : return public IP address\n" + \
               "    info hosts : list configured hosts\n" + \
               "    info host [hostname] : list info about configured host"
    
        
    
    
    
    
    
    