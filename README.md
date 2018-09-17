
# MyAWS - OS X Menubar plugin

Displays information regarding your AWS EC2 virtual machines in the Mac OS X menubar. 
Allows you to create, connect to and terminate EC2 virtual machines.
Create and destroy EC2 images from virtual machines.


Start, connect to and terminate virtual machines
![Imgur](https://i.imgur.com/1MTAvlX.png)

See console output in Menu Bar
![Imgur](https://i.imgur.com/B17Q9hy.jpg)

Create new virtual machines 

![Imgur](https://i.imgur.com/YRpszUT.png)


## Licence: GPL v3

## Installation instructions: 

1. Execute in terminal.app before running : sudo easy_install keyring boto
2. Ensure you have [aws command line tools](https://docs.aws.amazon.com/cli/latest/userguide/cli-install-macos.html) installed
3. Ensure you have [bitbar](https://github.com/matryer/bitbar/releases/latest) installed.
4. Ensure your bitbar plugins directory does not have a space in the path (A known bitbar bug)
5. Copy [myaws.15m.py](myaws.15m.py) to your bitbar plugins folder and chmod +x the file from your terminal in that folder
6. Run bitbar
