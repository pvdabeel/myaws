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
import time
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
    print ('|image=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')

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
        images = json.loads(subprocess.check_output("/usr/local/bin/aws ec2 describe-images --owners "+aws_owner_id+" --query 'Images[*].{ImageId:ImageId,Name:Name,SnapshotId:BlockDeviceMappings[0].Ebs.SnapshotId}'", shell=True))
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
       current_image_snapshot_id = image['SnapshotId']
 
       # Create a submenu for every AMI
       print ('%sImage: %s | color=%s' % (prefix, image['Name'], color))
       prefix = '--'
       
       # print menu with relevant info and actions

       print ('%sDeploy new Virtual Machine | color=%s' % (prefix, color))
       print ('%s--t2.micro		(  1 vcpu, 1Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t2.micro --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.small		(  1 vcpu, 2Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t2.small --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.medium	(  2 vcpu, 4Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t2.medium --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.large		(  2 vcpu, 8Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t2.large --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.xlarge	(  4 vcpu, 16Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t2.xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t2.2xlarge 	(  8 vcpu, 32Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t2.2xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s-----' % prefix)
       print ('%s--t3.micro		(  2 vcpu, 1Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t3.micro --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t3.small		(  2 vcpu, 2Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t3.small --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t3.medium	(  2 vcpu, 4Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t3.medium --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t3.large		(  2 vcpu, 8Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t3.large --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t3.xlarge	(  4 vcpu, 16Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t3.xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--t3.2xlarge 	(  8 vcpu, 32Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type t3.2xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s-----' % prefix)
       print ('%s--m4.4xlarge	( 16 vcpu, 64Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type m4.4xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--m4.16xlarge	( 64 vcpu, 256Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type m4.16xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s-----' % prefix)
       print ('%s--m5.4xlarge	( 16 vcpu, 64Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type m5.4xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--m5.12xlarge	( 48 vcpu, 192Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type m5.12xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--m5.24xlarge	( 96 vcpu, 384Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type m5.24xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s-----' % prefix)
       print ('%s--c5.4xlarge	( 16 vcpu, 32Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type c5.4xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--c5.9xlarge	( 36 vcpu, 72Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type c5.9xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s--c5.18xlarge	( 72 vcpu, 144Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type c5.18xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))
       print ('%s-----' % prefix)
       print ('%s--x1.32xlarge	( 128 vcpu, 1952Gb vram ) | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 run-instances --image-id "+current_image_id+" --instance-type x1.32xlarge --key-name gentoo --security-group-ids sg-bce547d1", color))

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
                 print ('%s--Create image | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 create-image --instance-id "+current_instance_id+" --name Linux-"+time.strftime("%Y%m%d-%Hh%M"), color))
              if state == 'running':
                 print ('%s--Stop | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 stop-instances --instance-ids "+current_instance_id+" --force", color))
              if (state == 'running') or (state == 'stopped'):
                 print ('%s--Terminate | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 terminate-instances --instance-ids "+current_instance_id, color))
              if state == 'running': 
                 print ('%s-----' % (prefix))
                 print ('%s--Console | color=%s' % (prefix, color))
                 console = json.loads(subprocess.check_output("/usr/local/bin/aws ec2 get-console-screenshot --instance-id "+current_instance_id, shell=True))['ImageData']
                 print ('%s----|image="%s" | color=%s' % (prefix, console, color))
       
       if len(image_instance_list) > 0: 
          print ('%s---' % prefix)
          print ('%sTerminate all Virtual Machines | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 terminate-instances --instance-ids "+" ".join(image_instance_list), color))
       print ('%s---' % prefix)
       if len(images) > 1:
          print ('%sDestroy image | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 deregister-image --image-id "+current_image_id + " && /usr/local/bin/aws ec2 delete-snapshot --snapshot-id "+current_image_snapshot_id, color))
       else:
          print ('%sDestroy image | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "/usr/local/bin/aws", "ec2 deregister-image --image-id "+current_image_id + " --dry-run && /usr/local/bin/aws ec2 delete-snapshot --dry-run --snapshot-id "+current_image_snapshot_id, color))
       prefix = ''

def run_script(script):
    return subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()

if __name__ == '__main__':
    main(sys.argv)
