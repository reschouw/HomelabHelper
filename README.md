# Homelab Helper
----------
#### A modular homelab helper integrated with Slack

This project is designed to help manage homelabs from outside of home networks. It will change forms as I work on it and hopefully in the end it will be a useful piece of software.

This project is a small Slack bot designed to run on a Raspberry Pi inside a home network. By sending the bot commands over Slack, the Raspberry Pi can then perform actions not otherwise possible from outside home networks.

Version 0.1.0 will be the first "stable" version. From there I hope to implement some CI practices and work to make this a more robust, feature-rich project. 

###Currently available features are as follows:
Can`t remember the MAC of one of your servers? Pull that information from the bot`s host inventory file.
Use Wake-On-LAN  commands to wake specified hosts, or by using "wol all", wake all WOL-capable hosts.
Ping specified hosts that may not be accessible from outside your network.


#### Major Feature ToDo List:
- [X] Slack integration
- [X] Configuration files
- [X] Wol Module
- [X] Ping Module
- [X] Info Module
- [ ] Wake Module
- [ ] Queue Module
- [ ] Host Inventory Labels
- [ ] Run as Daemon or system service

Installation:

To install, start by cloning this repository [https://github.com/reschouw/HomelabHelper](https://github.com/reschouw/HomelabHelper)

Then, in the cloned repository, run the following command to install dependencies:
```pip3 install -r requirements.txt```

You can then start the bot using:
```python3 homelabhelper.py```

This will start the bot in the foreground and any diagnostic messages will print to the terminal.
The first time the program is run, it will create example config and hosts files. Edit these to your satisfaction, rename them to `config` and `hosts` and start the bot again.

Automatically running the bot as a system service is a planned feature, but until then you can use the following command to run the bot in the background even if you close the terminal window:
```nohup python3 homelabhelper.py &```
