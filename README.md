
# MyAWS - OS X Menubar plugin

Displays information regarding your AWS EC2 virtual machines in the Mac OS X menubar. 
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
2. Execute 'sudo easy_install tinydb==3.9 awspricing currencyconverter' in Terminal.app
3. Ensure you have [bitbar](https://github.com/matryer/bitbar/releases/latest) installed.
4. Ensure your bitbar plugins directory does not have a space in the path (A known bitbar bug)
5. Copy [myaws.15m.py](myaws.15m.py) to your bitbar plugins folder and chmod +x the file from your terminal in that folder
6. Run 'myaws.15m.py update' in Terminal.app to retrieve latest pricing
7. Run bitbar (version 1.9 or <2.0-beta9, xbar not yet supported)
