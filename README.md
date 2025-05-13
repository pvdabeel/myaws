
# MyAWS - MacOS Menubar plugin

Displays information regarding your AWS EC2 virtual machines in the MacOS menubar. 
Allows you to create, connect to and terminate EC2 virtual machines.
Create and destroy EC2 images from virtual machines. Check storage consumption


Start, connect to and terminate virtual machines
![Imgur](https://i.imgur.com/yR5iPQy.jpg)

See console output in Menu Bar
![Imgur](https://i.imgur.com/UpZnhNa.jpg)

Create new virtual machines and retrieve up to date EC2 prices
![Imgur](https://i.imgur.com/ZnsKTTo.jpg)

Check your current EC2 spending 
![Imgur](https://i.imgur.com/n2FEdT1.jpg)


## Licence: GPL v3

## Installation instructions: 

1. Ensure you have [aws command line tools](https://docs.aws.amazon.com/cli/latest/userguide/cli-install-macos.html) installed (AWS CLI 1 or 2 are both fine)
2. Execute 'sudo pip install tinydb awspricing currencyconverter' in Terminal.app
3. Ensure you have [xbar](https://github.com/matryer/xbar/releases/latest) installed.
4. Copy [myaws.15m.py](myaws.15m.py) to your bitbar plugins folder and chmod +x the file from your terminal in that folder
5. Run 'myaws.15m.py update' in Terminal.app to retrieve latest pricing
6. Run xbar (version 2.1.7-beta or higher)
