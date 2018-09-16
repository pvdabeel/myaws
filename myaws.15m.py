#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# <bitbar.title>MyAWS</bitbar.title>
# <bitbar.version>v3.0</bitbar.version>
# <bitbar.author>pvdabeel@mac.com</bitbar.author>
# <bitbar.author.github>pvdabeel</bitbar.author.github>
# <bitbar.desc>Create, connect to and terminate Amazon EC2 virtual machines from the OS X menubar</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# Licence: GPL v3

# Installation instructions: 
# -------------------------- 
# Ensure you have the Amazon EC2 CLI installed (see Readme for link)
# Ensure you have bitbar installed https://github.com/matryer/bitbar/releases/latest
# Ensure your bitbar plugins directory does not have a space in the path (known bitbar bug)
# Copy this file to your bitbar plugins folder and chmod +x the file from your terminal in that folder
# Run bitbar


aws_owner_id = '615416975922'
aws_key_name = 'gentoo'
aws_security = 'sg-bce547d1'

# aws ec2 describe-images --owners 615416975922 --query 'Images[*].{ID:ImageId}'
# aws ec2 run-instances --image-id ami-089fc69c2ca496809 --count 1 --instance-type t2.micro --key-name gentoo --security-group-ids sg-bce547d1
# aws ec2 describe-instances --query 'Reservations[*].Instances[*].{ID:PublicDnsName,State:State}'
# aws ec2 terminate-instances --instance-ids i-0de69865f64ebd6ad
# aws ec2 stop-instances --instance-ids --force


try:   # Python 3 dependencies
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen, build_opener
    from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, HTTPError, URLError
except: # Python 2 dependencies
    from urllib import urlencode
    from urllib2 import Request, urlopen, build_opener
    from urllib2 import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, HTTPError, URLError


import ast
import json
import sys
import datetime
import calendar
import base64
import math
import time
import os
import subprocess
import requests

from datetime import date


# Nice ANSI colors
CEND    = '\33[0m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CGRAY   = '\33[30m'

# Support for OS X Dark Mode
DARK_MODE=os.getenv('BitBarDarkMode',0)


# Logo for both dark mode and regular mode
def app_print_logo():
    if bool(DARK_MODE):
        print ('|image=iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAAAXNSR0IArs4c6QAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAFU2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICAgICAgICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgICAgICAgICB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+CiAgICAgICAgIDxkYzp0aXRsZT4KICAgICAgICAgICAgPHJkZjpBbHQ+CiAgICAgICAgICAgICAgIDxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCI+dGVzbGFfVF9CVzwvcmRmOmxpPgogICAgICAgICAgICA8L3JkZjpBbHQ+CiAgICAgICAgIDwvZGM6dGl0bGU+CiAgICAgICAgIDx4bXBNTTpEZXJpdmVkRnJvbSByZGY6cGFyc2VUeXBlPSJSZXNvdXJjZSI+CiAgICAgICAgICAgIDxzdFJlZjppbnN0YW5jZUlEPnhtcC5paWQ6NjFlOGM3OTktZDk2Mi00Y2JlLWFiNDItY2FmYjlmOTYxY2VlPC9zdFJlZjppbnN0YW5jZUlEPgogICAgICAgICAgICA8c3RSZWY6ZG9jdW1lbnRJRD54bXAuZGlkOjYxZThjNzk5LWQ5NjItNGNiZS1hYjQyLWNhZmI5Zjk2MWNlZTwvc3RSZWY6ZG9jdW1lbnRJRD4KICAgICAgICAgPC94bXBNTTpEZXJpdmVkRnJvbT4KICAgICAgICAgPHhtcE1NOkRvY3VtZW50SUQ+eG1wLmRpZDpCNkM1NEUzNDlERTAxMUU3QTRFNEExMTMwMUY5QkJBNTwveG1wTU06RG9jdW1lbnRJRD4KICAgICAgICAgPHhtcE1NOkluc3RhbmNlSUQ+eG1wLmlpZDpCNkM1NEUzMzlERTAxMUU3QTRFNEExMTMwMUY5QkJBNTwveG1wTU06SW5zdGFuY2VJRD4KICAgICAgICAgPHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD51dWlkOjI3MzY3NDg0MTg2QkRGMTE5NjZBQjM5RDc2MkZFOTlGPC94bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+QWRvYmUgSWxsdXN0cmF0b3IgQ0MgMjAxNSAoTWFjaW50b3NoKTwveG1wOkNyZWF0b3JUb29sPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KI5WHQwAAANVJREFUOBHtU8ENwjAMTBADdJRuACMwUjdgBEaAEcoEgQlSJmCEcJYS6VzlYVfiV0snn6/na5SqIez17xuIvReUUi7QT8AInIFezRBfwDPG+OgZlIbQL5BrT7Xf0YcK4eJpz7LMKqQ3wDSJEViXBArWJd6pl6U0mORkVyADchUBXVXVRogZuAGDCrEOWExAq2TZO1hM8CzkY06yptbgN60xJ1lTa/BMa8xJ1tQavNAac5I30vblrOtHqxG+2eENnmD5fc3lCf6YU2H0BLtO7DnE7t12Az8xb74dVbfynwAAAABJRU5ErkJggg==')
    else:
        print ('|image=iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA/xpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ1dWlkOjI3MzY3NDg0MTg2QkRGMTE5NjZBQjM5RDc2MkZFOTlGIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkI2QzU0RTM0OURFMDExRTdBNEU0QTExMzAxRjlCQkE1IiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkI2QzU0RTMzOURFMDExRTdBNEU0QTExMzAxRjlCQkE1IiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIElsbHVzdHJhdG9yIENDIDIwMTUgKE1hY2ludG9zaCkiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDo2MWU4Yzc5OS1kOTYyLTRjYmUtYWI0Mi1jYWZiOWY5NjFjZWUiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6NjFlOGM3OTktZDk2Mi00Y2JlLWFiNDItY2FmYjlmOTYxY2VlIi8+IDxkYzp0aXRsZT4gPHJkZjpBbHQ+IDxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCI+dGVzbGFfVF9CVzwvcmRmOmxpPiA8L3JkZjpBbHQ+IDwvZGM6dGl0bGU+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+ux4+7QAAALlJREFUeNpi/P//PwMtABMDjcDQM5gFmyAjI2MAkLIHYgMgdsCh9wAQXwDig8B42oAhC4o8ZAwE74H4PpQ+D6XXA7EAFK9HkwOrxTAHi8ENUA3/0fB6KEYXB6ltIMZgkKv6oS4xgIqhGAYVM4CqmQ/SQ9BgbBjqbZjB54nRQ2yqeICDTXFyu4iDTbHBB3CwKTaY5KBgJLYQAmaa/9B0z0h2ziMiOKhq8AVaGfxwULiYcbQGobnBAAEGADCCwy7PWQ+qAAAAAElFTkSuQmCC')
    print('---')


# Pretty printing

def color_state(state):
    if state == 'running':
        return CGREEN + justify(state) + CEND
    if state == 'stopped':
        return CRED + justify(state) + CEND
    if state == 'pending':
        return CGREEN + justify('starting') + CEND
    if state == 'terminated':
        return justify('deleted')
    if state == 'shutting-down':
        return CRED + justify('stopping') + CEND
    else:
        return state

def justify(string):
    return string.ljust(10)


# The init function: Called to store your AWS access keys

def init():
    print 'Please run \'aws configure\''


# The main function

def main(argv):

    # CASE 1: init was called 
    if 'init' in argv:
       init()
       return
  
    # CASE 2: init was not called, AWS not available
    if DARK_MODE:
        color = '#FFDEDEDE'
        info_color = '#808080'
    else:
        color = 'black' 
        info_color = '#808080'

    try: 
        images = json.loads(subprocess.check_output("/usr/local/bin/aws ec2 describe-images --owners "+aws_owner_id+" --query 'Images[*].{ImageId:ImageId,Name:Name}'", shell=True))
        instances = json.loads(subprocess.check_output("/usr/local/bin/aws ec2 describe-instances --query 'Reservations[*].Instances[*].{PublicDnsName:PublicDnsName,State:State,InstanceType:InstanceType,PublicIpAddress:PublicIpAddress,InstanceId:InstanceId,ImageId:ImageId}'", shell=True))
    except: 
       app_print_logo()
       print ('Failed to get AMI from EC2 | refresh=true terminal=true bash="\'%s\'" param1="%s" color=%s' % (sys.argv[0], 'init', color))
       return

    # CASE 3: all ok, all other cases
    app_print_logo()
    prefix = ''
    
    # loop through images, list all instances and menu for creating new vm

    for image in images: 

       current_image_id = image['ImageId']
 
       # Create a submenu for every AMI
       print ('%sImage: %s | color=%s' % (prefix, image['Name'], color))
       prefix = '--'
       
       # print menu with relevant info and actions

       print ('%sDeploy new Virtual Machine | color=%s' % (prefix, color))
       print ('%s--t2.micro		(  1 vcpu, 1Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type t2.micro --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.small		(  1 vcpu, 2Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type t2.small --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.medium	(  2 vcpu, 4Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type t2.medium --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.large		(  4 vcpu, 16Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type t2.large --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.2xlarge 	(  8 vcpu, 32Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type t2.2xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s-----' % prefix)
       print ('%s--m4.4xlarge	( 16 vcpu, 64Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type m4.4xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--m4.16xlarge	( 64 vcpu, 256Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type m4.16xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s-----' % prefix)
       print ('%s--x1.32xlarge	( 128 vcpu, 1952Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id ami-089fc69c2ca496809 --instance-type x1.32xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))

       print ('%s---' % prefix)

       # loop through instances, 

       image_instance_list = []

       for instance in instances:

           instance_json=instance[0]
           
           current_instance_id = instance_json['InstanceId']

           if instance_json['ImageId'] == current_image_id: 
              image_instance_list.append(current_instance_id)
              state = instance_json['State']['Name'] 
              dnsname = instance_json['PublicDnsName']
              vmtype = instance_json['InstanceType']
              ipaddress = instance_json['PublicIpAddress']

              print ('%s%s		%s		ip: %s ' % (prefix, color_state(state), justify(vmtype), ipaddress))
              if state == 'running': 
                 print ('%s--Connect | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "ssh", "-q -o StrictHostKeyChecking=no -o UserKnownHostsFile=~/.ssh/amazon-vms root@"+dnsname, color))
              if state == 'stopped':
                 print ('%s--Start | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 start-instances --instance-ids "+current_instance_id, color))
              if state == 'running':
                 print ('%s--Stop | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 stop-instances --instance-ids "+current_instance_id+" --force", color))
              if (state == 'running') or (state == 'stopped'):
                 print ('%s--Terminate | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 terminate-instances --instance-ids "+current_instance_id, color))
       
       if len(instances) > 0: 
          print ('%s---' % prefix)
          print ('%sTerminate all Virtual Machines | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 terminate-instances --dry-run --instance-ids "+" ".join(image_instance_list), color))
       print ('%s---' % prefix)
       print ('%sDestroy image | color=%s' % (prefix, color))


def run_script(script):
    return subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()

if __name__ == '__main__':
    main(sys.argv)
