# Homelab Helper
![alt text](https://img.shields.io/badge/Version-v0.1.1-blue.svg)

[![Build Status](https://travis-ci.org/reschouw/HomelabHelper.svg?branch=master)](https://travis-ci.org/reschouw/HomelabHelper) - Master Branch

[![Build Status](https://travis-ci.org/reschouw/HomelabHelper.svg?branch=dev)](https://travis-ci.org/reschouw/HomelabHelper) - Development branch
#### A modular homelab helper integrated with Slack


This project is a small Slack bot designed to run on a Raspberry Pi inside a home network. By sending the bot commands over Slack, the Raspberry Pi can then perform actions not otherwise possible from outside home networks.

Version 0.1.0 will be the first "stable" version. From there I hope to implement some CI practices and work to make this a more robust, feature-rich project. 

#### Currently available features are as follows:
- Can't remember the MAC of one of your servers? Pull that information from the bot's host inventory file.
- Use Wake-On-LAN  commands to wake specified hosts, or by using "wol all", wake all WOL-capable hosts.
- Ping specified hosts that may not be accessible from outside your network.


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

#### Installation:

To install, start by cloning [the repository](https://github.com/reschouw/HomelabHelper)

You will likely want to install `virtualenv` in order to keep your python dependencies from interfering with one another. After installing via 

`apt install virtualenv`

(or your respective package manager), run the following:

`virtualenv helper`

"helper is simply the name of the virtual environment. To reactivate the environment, do the following from the project directory:

`source ./helper/bin/activate`

Run the following command to install dependencies.

`python -m pip install -r requirements.txt`

You can then start the bot by running:

`python3 homelabhelper.py`

This will start the bot in the foreground and any diagnostic messages will print to the terminal.
The first time the program is run, it will create example config and hosts files. Edit these to your satisfaction, rename them to `config` and `hosts` and start the bot again.

In the `config` file, there is a commented-out line for `bot_token`. This is the key that will allow the bot into your Slack workspace. Find instructions for creating a bot user [here](https://get.slack.help/hc/en-us/articles/115005265703-Create-a-bot-for-your-workspace). After creating the bot, paste the API token that starts with `-xoxb` into this configuration option.

Automatically running the bot as a system service is a planned feature, but until then you can use the following command to run the bot in the background even if you close the terminal window.

`nohup python3 homelabhelper.py &`