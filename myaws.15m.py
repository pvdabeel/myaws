#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python
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
# Run 'sudo easy_install tinydb awspricing' in Terminal.app
# Ensure you have bitbar installed https://github.com/matryer/bitbar/releases/latest
# Ensure your bitbar plugins directory does not have a space in the path (known bitbar bug)
# Copy this file to your bitbar plugins folder and chmod +x the file from your terminal in that folder
# Run bitbar

aws_owner_id = '615416975922'
aws_key_name = 'gentoo'
aws_security = 'sg-bce547d1'
aws_command  = '/usr/local/bin/aws'
aws_region   = 'eu-central-1'
aws_ostype   = 'Linux' 

vm_cheap     = 0.25
vm_expensive = 1.0 

preferred_currency = 'EUR' # or 'USD' (or any currency supported by currencyconvertor)


aws_vmtypes  = [('t2', [ ('.micro',   '(   1 vcpu, 1Gb vram )\t'),
                         ('.small',   '(   1 vcpu, 2Gb vram )\t'),
                         ('.medium',  '(   2 vcpu, 4Gb vram )\t'),
                         ('.large',   '(   2 vcpu, 8Gb vram )\t'), 
                         ('.xlarge',  '(   4 vcpu, 16Gb vram )\t'), 
                         ('.2xlarge', '(   8 vcpu, 32Gb vram )\t')  ]),
                ('t3', [ ('.micro',   '(   2 vcpu, 1Gb vram )\t'), 
                         ('.small',   '(   2 vcpu, 2Gb vram )\t'), 
                         ('.medium',  '(   2 vcpu, 4Gb vram )\t'), 
                         ('.large',   '(   2 vcpu, 8Gb vram )\t'), 
                         ('.xlarge',  '(   4 vcpu, 16Gb vram )\t'), 
                         ('.2xlarge', '(   8 vcpu, 32Gb vram )\t')  ]), 
                ('m4', [ ('.4xlarge', '(  16 vcpu, 64Gb vram )\t'), 
                         ('.16xlarge','(  64 vcpu, 256Gb vram )\t') ]), 
                ('m5', [ ('.4xlarge', '(  16 vcpu, 64Gb vram )\t'), 
                         ('.12xlarge','(  48 vcpu, 192Gb vram )\t'), 
                         ('.24xlarge','(  96 vcpu, 384Gb vram )\t'),
                         ('.metal',   '(  96 vcpu, 384Gb vram )\t') ]), 
                ('m5d',[ ('.4xlarge', '(  16 vcpu, 64Gb vram )\t'), 
                         ('.12xlarge','(  48 vcpu, 192Gb vram )\t'), 
                         ('.24xlarge','(  96 vcpu, 384Gb vram )\t'), 
                         ('.metal',   '(  96 vcpu, 384Gb vram )\t') ]), 
                ('c5', [ ('.4xlarge', '(  16 vcpu, 32Gb vram )\t'), 
                         ('.9xlarge', '(  36 vcpu, 72Gb vram )\t'), 
                         ('.18xlarge','(  72 vcpu, 144Gb vram )\t'), 
                         ('.24xlarge','(  96 vcpu, 192Gb vram )\t'),
                         ('.metal',   '(  96 vcpu, 192Gb vram )\t') ]),
                ('c5d',[ ('.4xlarge', '(  16 vcpu, 32Gb vram )\t'), 
                         ('.9xlarge', '(  36 vcpu, 72Gb vram )\t'), 
                         ('.18xlarge','(  72 vcpu, 144Gb vram )\t'), 
                         ('.24xlarge','(  96 vcpu, 192Gb vram )\t'),
                         ('.metal',   '(  96 vcpu, 192Gb vram )\t') ]),
                ('c5n',[ ('.4xlarge', '(  16 vcpu, 42Gb vram )\t'), 
                         ('.9xlarge', '(  36 vcpu, 96Gb vram )\t'), 
                         ('.18xlarge','(  72 vcpu, 192Gb vram )\t'),
                         ('.metal',   '(  72 vcpu, 192Gb vram )\t') ]),
                ('p3', [ ('.2xlarge', '(   8 vcpu, 61Gb vram )\t'),
                         ('.8xlarge', '(  32 vcpu, 244Gb vram )'), 
                         ('.16xlarge','(  64 vcpu, 488Gb vram )')  ]), 
                ('x1', [ ('.16xlarge','(  64 vcpu, 976Gb vram )\t'),
                         ('.32xlarge','( 128 vcpu, 1952Gb vram )')  ]), 
                ('x1e',[ ('.16xlarge','(  64 vcpu, 1952Gb vram )'),
                         ('.32xlarge','( 128 vcpu, 3904Gb vram )')  ]), 
                ('u-6tb1',[('.metal',  '( 448 vcpu, 6144Gb vram )')  ]), 
                ('z1d',[ ('.2xlarge', '(   8 vcpu, 64Gb vram )\t'),
                         ('.3xlarge', '(  12 vcpu, 96Gb vram )\t'), 
                         ('.6xlarge', '(  24 vcpu, 192Gb vram )\t'), 
                         ('.12xlarge','(  48 vcpu, 384Gb vram )\t'), 
                         ('.metal',   '(  48 vcpu, 384Gb vram )\t')  ]), 
                ('i3', [ ('.metal',   '(  72 core, 512Gb ram )\t') ]) ] 


aws_default_vmtype_update  = 'c5d.4xlarge'
aws_default_vmtype_rebuild = 'c5d.24xlarge'

# Command to be called inside instance to update it

cmd_update  = 'update' 
cmd_rebuild = 'fullupdate' 

# aws ec2 describe-images --owners 615416975922 --query 'Images[*].{ID:ImageId}'
# aws ec2 run-instances --image-id ami-089fc69c2ca496809 --count 1 --ebs-optimized --instance-type t2.micro --key-name gentoo --security-group-ids sg-bce547d1
# aws ec2 describe-instances --query 'Reservations[*].Instances[*].{ID:PublicDnsName,State:State}'
# aws ec2 terminate-instances --instance-ids i-0de69865f64ebd6ad
# aws ec2 stop-instances --instance-ids --force
# aws ec2 describe-instances --instance-id i-0c27fcf159ec94d0d --query 'Reservations[*].Instances[*].LaunchTime'
# aws ec2 get-console-output --instance-id i-0ed95956c74a187ac --output text
# aws ce get-cost-and-usage --time-period Start=2018-09-01,End=2018-09-23 --granularity MONTHLY --metrics BlendedCost UnblendedCost UsageQuantity --group-by Type=DIMENSION,Key=SERVICE

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
import decimal
import awspricing
import six

from datetime import date
from tinydb import TinyDB, Query
from currency_converter import CurrencyConverter


from os.path import expanduser

# Location where to store state files
home         = expanduser("~")
state_dir    = home+'/.state/myaws'

if not os.path.exists(state_dir):                                               
    os.makedirs(state_dir)    

# Tiny DB to store pricing
database = TinyDB(state_dir+'/myawspricing.json')

# Cost convertor
converter = CurrencyConverter()

# Nice ANSI colors
CEND    = '\33[0m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CGRAY   = '\33[30m'
CDGRAY  = '\33[90m'

# ANSI styles

CBOLD   = '\033[01m'
CNORMAL = '\033[00m'

# Support for OS X Dark Mode
DARK_MODE=os.getenv('BitBarDarkMode',0)


# Logo for both dark mode and regular mode
def app_print_logo():
    print ('|image=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')
    print('---')


# Pretty printing
def color_state(state):
    if state == 'running':
        return CGREEN + justify(state,10) + CEND
    if state == 'stopped':
        return CRED + justify(state,10) + CEND
    if state == 'pending':
        return CGREEN + justify('starting',10) + CEND
    if state == 'terminated':
        return justify('deleted',10)
    if state == 'shutting-down':
        return CRED + justify('stopping',10) + CEND
    if state == 'stopping':
        return CRED + justify('stopping',10) + CEND
    else:
        return state

def color_cost(unconverted_cost,desc,rate):
    if preferred_currency == 'USD': 
        short_rate = '$'
    elif preferred_currency == 'EUR':
        short_rate = u"€" 
    else:
        short_rate = '$'
    if unconverted_cost == 'n/a':
       return CBLUE + '           n/a ' + CEND + '  per hour'
    cost = converter.convert(unconverted_cost,rate,preferred_currency) 
    if desc == 'Tax':
       return CRED + short_rate + ' ' + justify(str(cost_format(round(float(cost),4))),7) + '\t ' + CEND + ' - ' + desc
    elif desc == 'Total': 
       return CGREEN + short_rate + ' ' + justify(str(cost_format(round(float(cost),4))),7) + '\t ' + CEND + ' - ' + desc
    elif desc == 'Hourly':
       if (float(cost) < vm_cheap):
          return CGREEN + short_rate + ' ' + justify(str(cost_format(round(float(cost),4))),7) + ' ' + CEND + ' per hour'
       if (float(cost) >= vm_cheap) and (float(cost) <= vm_expensive):
          return CYELLOW + short_rate + ' ' + justify(str(cost_format(round(float(cost),4))),7) + ' ' + CEND + ' per hour'
       if (float(cost) > vm_expensive ):
          return CRED + short_rate + ' ' + justify(str(cost_format(round(float(cost),4))),7) + ' ' + CEND + ' per hour'
    elif desc == '': 
       return CGREEN + short_rate + ' ' + justify(str(cost_format(round(float(cost),4))),7) + '\t ' + CEND
    else:
       return CBLUE + short_rate + ' ' + justify(str(cost_format(round(float(cost),4))),7) + '\t ' + CEND + ' - ' + desc

def cost_format(x):
    digits = 4
    temp = str(decimal.Decimal(str(x) + '0' * digits))
    return temp[:temp.find('.') + digits + 1]


def justify(string):
    return justify(string,10)

def justify(string,number):
    length = len(string)
    quot   = (number - length ) // 4
    rem    = (number - length )  % 4
    return string.ljust(length+rem,' ').ljust(length+rem+quot,'\t')

def important(string):
    return CRED + string + CEND

# The init function: Called to store your AWS access keys
def init():
    print 'Please run \'aws configure\''


# The update-pricing function: Retrieve EC2 pricing 
def update_pricing(): 
    # Purge existing database
    database.purge()
    # Get an EC2 price list from amazon
    ec2_offer = awspricing.offer('AmazonEC2')
    # Retrieve latest pricing for vm and insert in database
    for (aws_vmgroup,aws_vmtypelist) in aws_vmtypes:
       for (aws_vmtype,aws_vmdesc) in aws_vmtypelist:
          try:
             # DB format change (bug in awspricing) aws_pricing = ec2_offer.ondemand_hourly(aws_vmgroup+aws_vmtype,operating_system=aws_ostype,region=aws_region)
             # Ondemand makes a distinction between Used, ReservationBox, ...
             sku = ec2_offer.search_skus(instance_type=aws_vmgroup+aws_vmtype,operating_system=aws_ostype,tenancy='Shared',location='EU (Frankfurt)',licenseModel='No License required', preInstalledSw='NA',capacitystatus='Used').pop()
             print ec2_offer._offer_data[sku]['terms']['OnDemand']
             aws_pricing = next(six.itervalues(next(six.itervalues(ec2_offer._offer_data[sku]['terms']['OnDemand']))['priceDimensions']))['pricePerUnit']['USD']
             print aws_pricing
          except:
             aws_pricing = 'n/a'
             pass 
          database.insert({'type':aws_vmgroup+aws_vmtype,'pricing':aws_pricing})
    # Store timestamp
    database.insert({'timestamp':str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))})


# The update-image function: Update an EC2 image
def update_image(cmd=cmd_update):
    if (len(sys.argv) != 4): 
        print ('Please provide an ami name and ami snapshot id as argument')
        return
    ami_to_update = sys.argv[2]
    ami_snap_id   = sys.argv[3]

    print
    print (CYELLOW+CBOLD+'>>> Updating image:         '+CNORMAL+CGREEN+ami_to_update+CEND)
    print
    if (cmd == cmd_update): 
        aws_default_vmtype = aws_default_vmtype_update
    else:
        aws_default_vmtype = aws_default_vmtype_rebuild

    # for the given AMI image, spawn an instance
    print ('--- Deploying instance:     '+CGREEN+aws_default_vmtype+CEND)
    try: 
        instance_id = json.loads(subprocess.check_output(aws_command+" ec2 run-instances --image-id "+ami_to_update+" --instance-type "+aws_default_vmtype+" --ebs-optimized --key-name "+aws_key_name+" --security-group-ids "+aws_security, shell=True))['Instances'][0]['InstanceId']
    except: 
        print (CRED+'!!! Failed to deploy instance'+CEND) 
        return
    print ('--- Instance deployed:      '+CGREEN+instance_id+CEND)

    # wait until instance is up and running 
    print ('--- Checking instance:     '),
    try:
        subprocess.check_output(aws_command+" ec2 wait instance-running --instance-ids "+instance_id, shell=True)
        print (CGREEN+'running'+CEND)
    except: 
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Instance failed to reach running state'+CEND)
        # Destroy instance
        json.loads(subprocess.check_output(aws_command+" ec2 terminate-instances --instance-ids "+instance_id, shell=True))
        return

    print ('--- Instance dnsname:      '),
    try:
        instance_dns = json.loads(subprocess.check_output(aws_command+" ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].{PublicDnsName:PublicDnsName,State:State}'", shell=True))[0][0]['PublicDnsName']
        print (CGREEN+instance_dns+CEND)
    except: 
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Failed to get instance dnsname'+CEND)
         # Destroy instance
        json.loads(subprocess.check_output(aws_command+" ec2 terminate-instances --instance-ids "+instance_id, shell=True))
        return

    # execute update
    print ('--- Updating instance:')
    print
    try:
        updateoutcome = subprocess.call("sleep 60 && ssh -q -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=~/.ssh/amazon-vms root@"+instance_dns+ " \"bash -icl "+cmd+"\"", shell=True)
        print
    except:
        print (CRED+'!!! Failed to update instance'+CEND)
        # Destroy instance
        json.loads(subprocess.check_output(aws_command+" ec2 terminate-instances --instance-ids "+instance_id, shell=True))
        print
        return

    if (updateoutcome):
        print (CRED+'!!! Failed to update instance'+CEND)
        json.loads(subprocess.check_output(aws_command+" ec2 terminate-instances --instance-ids "+instance_id, shell=True))
        print
        return

    # create new image
    print ('--- Creating new image:    '),
    try:
        updated_ami = json.loads(subprocess.check_output(aws_command+" ec2 create-image --instance-id "+instance_id+" --name Linux-"+time.strftime("%Y%m%d-%Hh%M"), shell=True))
        print (CGREEN+'ok'+CEND) 
    except: 
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Failed to create image'+CEND)

    # Cleanup instance
    print ('--- Cleanup instance:      '),
    try: 
        json.loads(subprocess.check_output(aws_command+" ec2 terminate-instances --instance-ids "+instance_id, shell=True))
        print (CGREEN+'ok'+CEND)
    except:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Instance cleanup failed'+CEND)

    # wait until image is available 
    print ('--- Checking new image:    '),
    try:
        subprocess.check_output(aws_command+" ec2 wait image-available --owners self", shell=True)
        print (CGREEN+'available'+CEND)
    except: 
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Image failed to reach available state'+CEND)
        return

    # Cleanup old image 
    print ('--- Cleanup old image:     '),
    try: 
        subprocess.check_output(aws_command+" ec2 deregister-image --image-id "+ami_to_update+" && /usr/local/bin/aws ec2 delete-snapshot --snapshot-id "+ami_snap_id, shell=True)
        print (CGREEN+'ok'+CEND)
    except:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Image cleanup failed'+CEND)

    print
    print (CYELLOW+CBOLD+'>>> New image created'+CNORMAL+CEND)
    print
    return


# The main function
def main(argv):

    # CASE 1a: init was called 
    if 'init' in argv:
       init()
       return
 
    # CASE 1b: update_pricing was called 
    if 'update_pricing' in argv:
       update_pricing()
       return

    # CASE 1c: update-image was called
    if 'update_image' in argv:
       update_image(cmd_update)
       return
 
    # CASE 1d: 
    if 'rebuild_image' in argv:
       update_image(cmd_rebuild)
       return


    # CASE 2: nor init nor update were called, AWS not available
    if DARK_MODE:
        color = '#FFDEDEDE'
        info_color = '#808080'
    else:
        color = 'black' 
        info_color = '#808080'

    try: 
        todayDate = datetime.date.today()
        monthDate = todayDate.replace(day=1)

        if (todayDate == monthDate):
           monthDate = monthDate - datetime.timedelta(days=1)
           monthDate = monthDate.replace(day=1)

        images       = json.loads(subprocess.check_output(aws_command+" ec2 describe-images --owners "+aws_owner_id+" --query 'Images[*].{ImageId:ImageId,Name:Name,SnapshotId:BlockDeviceMappings[0].Ebs.SnapshotId}'", shell=True))
        instances    = json.loads(subprocess.check_output(aws_command+" ec2 describe-instances --query 'Reservations[*].Instances[*].{PublicDnsName:PublicDnsName,State:State,InstanceType:InstanceType,PublicIpAddress:PublicIpAddress,InstanceId:InstanceId,ImageId:ImageId,LaunchTime:LaunchTime}'", shell=True))
        volumes      = json.loads(subprocess.check_output(aws_command+" ec2 describe-volumes --query 'Volumes[*].{Size:Size}'", shell=True))
        snapshots    = json.loads(subprocess.check_output(aws_command+" ec2 describe-snapshots --owner-ids "+aws_owner_id+" --query 'Snapshots[*].{Size:VolumeSize}'", shell=True))

        try:
            with open(state_dir+'/myaws-costs-monthly'+todayDate.strftime("%Y%m%d")+'.json') as json_file:
                monthly_cost = json.load(json_file)
                json_file.close()
        except: 
            with open(state_dir+'/myaws-costs-monthly'+todayDate.strftime("%Y%m%d")+'.json','w') as json_file:
                monthly_cost = json.loads(subprocess.check_output(aws_command+" ce get-cost-and-usage --time-period Start="+monthDate.strftime("%Y-%m-%d")+",End="+todayDate.strftime("%Y-%m-%d")+" --granularity MONTHLY --metrics BlendedCost --group-by Type=DIMENSION,Key=SERVICE", shell=True))
                json.dump(monthly_cost,json_file)
                json_file.close()
        try:
            with open(state_dir+'/myaws-costs-daily'+todayDate.strftime("%Y%m%d")+'.json') as json_file:
                daily_cost = json.load(json_file)
                json_file.close()
        except: 
            with open(state_dir+'/myaws-costs-daily'+todayDate.strftime("%Y%m%d")+'.json','w') as json_file:
                daily_cost   = json.loads(subprocess.check_output(aws_command+" ce get-cost-and-usage --time-period Start="+monthDate.strftime("%Y-%m-%d")+",End="+todayDate.strftime("%Y-%m-%d")+" --granularity DAILY --metrics BlendedCost --group-by Type=DIMENSION,Key=SERVICE", shell=True))
                json.dump(daily_cost,json_file)
                json_file.close()
    except: 
       app_print_logo()
       print ('Failed to get data from EC2 | refresh=true terminal=true bash="\'%s\'" param1="%s" color=%s' % (sys.argv[0], 'init', color))
       return

    # CASE 3: all ok, all other cases
    app_print_logo()
    prefix = '' 
   
    # -------------------
    # image menu
    # -------------------

    # loop through images, list all instances and print menu for creating new vm from image
    for image in images: 

       current_image_id = image['ImageId']
       current_image_snapshot_id = image['SnapshotId']

       # create a submenu for every AMI which whose underlying storage is ready
       if (current_image_snapshot_id):
           print ('%sImage :\t\t\t\t %s | color=%s' % (prefix, image['Name'], color))
           prefix = '--'
       else:
           print ('%sImage :\t\t\t\t %s | color=%s' % (prefix, image['Name'], info_color))
           continue


       # print menu with relevant info and actions
       print ('%sDeploy new Virtual Machine | color=%s' % (prefix, color))

       aws_pricing = 'n/a'
       
       for (aws_vmgroup,aws_vmtypelist) in aws_vmtypes:
          for (aws_vmtype,aws_vmdesc) in aws_vmtypelist:
             Q = Query()
             try: 
                aws_pricing = database.search(Q.type==aws_vmgroup+aws_vmtype)[0]['pricing']
             except:
                aws_pricing = 'n/a'
                pass 
             print ('%s--%s\t%s\t%s | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, justify(aws_vmgroup+aws_vmtype,14), justify(aws_vmdesc,18), color_cost(aws_pricing,'Hourly','USD'), aws_command, "ec2 run-instances --image-id "+current_image_id+" --instance-type "+aws_vmgroup+aws_vmtype+" --ebs-optimized --key-name "+aws_key_name+" --security-group-ids "+aws_security, color))
          print ('%s-----' % prefix)


       db_last_updated = False

       try:
          db_last_updated = database.search(Q.timestamp)[0]['timestamp']
          print ('%s--Last updated:\t%s | color=%s' % (prefix, db_last_updated, color))
          print ('%s----%s | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, 'Update AWS pricing',sys.argv[0], "update_pricing", color))
       except: 
          print ('%s--%s | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, important('Update AWS pricing'),sys.argv[0], "update_pricing", color))

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
              launchtime = datetime.datetime.strptime(instance_json['LaunchTime'][:19],'%Y-%m-%dT%H:%M:%S')
              uptime = datetime.datetime.utcnow() - launchtime
              uptime_d = divmod(uptime.total_seconds(),86400)
              uptime_h = divmod(uptime_d[1], 3600)
              uptime_m = divmod(uptime_h[1], 60)

              print ('%s%s\t%sd:%sh%sm\t\t%s\t\tip: %s ' % (prefix, color_state(state), int(uptime_d[0]),int(uptime_h[0]),int(uptime_m[0]), justify(vmtype,10), ipaddress ))

              if state == 'running': 
                print ('%s--Connect | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "ssh", "-q -o StrictHostKeyChecking=no -o UserKnownHostsFile=~/.ssh/amazon-vms root@"+dnsname, color))
              if state == 'stopped':
                 print ('%s--Start | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 start-instances --instance-ids "+current_instance_id, color))
                 print ('%s--Create image | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 create-image --instance-id "+current_instance_id+" --name Linux-"+time.strftime("%Y%m%d-%Hh%M"), color))
              if state == 'running':
                 print ('%s--Stop | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 stop-instances --instance-ids "+current_instance_id+" --force", color))
              if (state == 'running') or (state == 'stopped'):
                 print ('%s--Terminate | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 terminate-instances --instance-ids "+current_instance_id, color))
              if state == 'running': 
                 print ('%s-----' % (prefix))
                 print ('%s--Screenshot| color=%s' % (prefix, color))
                 try:
                    console = json.loads(subprocess.check_output("/usr/local/bin/aws ec2 get-console-screenshot --instance-id "+current_instance_id, shell=True))['ImageData']
                    print ('%s----|image="%s" | color=%s' % (prefix, console, color))
                 except:
                    print ('%s----|Unable to get a screenshot | color=%s' % (prefix, color))
              if state != 'terminated':
                 print ('%s-----' % (prefix))
                 print ('%s--Serial Console Log| refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, "cat", state_dir+"/myaws-"+current_instance_id+".console.log", color))
                 with open(state_dir+"/myaws-"+current_instance_id+".console.log",'w') as console_file:
                    serial  = str(subprocess.check_output("/usr/local/bin/aws ec2 get-console-output --output text --instance-id "+current_instance_id, shell=True))
                    console_file.write(serial)
                    console_file.close()
       
       if len(image_instance_list) > 0: 
          print ('%s---' % prefix)
          print ('%sTerminate all Virtual Machines | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 terminate-instances --instance-ids "+" ".join(image_instance_list), color))

       print ('%s---' % prefix)
       print ('%sImage' % prefix) 
       print ('%s--Update | refresh=true terminal=true bash="%s" param1="%s" param2="%s" param3="%s" color=%s' % (prefix, sys.argv[0], "update_image", current_image_id, current_image_snapshot_id, color))
       print ('%s--Rebuild | refresh=true terminal=true bash="%s" param1="%s" param2="%s" param3="%s" color=%s' % (prefix, sys.argv[0], "rebuild_image", current_image_id, current_image_snapshot_id, color))

       if (len(images) > 1):
          print ('%s--Destroy | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 deregister-image --image-id "+current_image_id + " && /usr/local/bin/aws ec2 delete-snapshot --snapshot-id "+current_image_snapshot_id, color))
       else:
          print ('%s--Destroy | refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 deregister-image --image-id "+current_image_id + " --dry-run && /usr/local/bin/aws ec2 delete-snapshot --dry-run --snapshot-id "+current_image_snapshot_id, info_color))
          print ('%s--Destroy | alternate=true refresh=true terminal=true bash="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 deregister-image --image-id "+current_image_id + " --dry-run && /usr/local/bin/aws ec2 delete-snapshot --snapshot-id "+current_image_snapshot_id, color))
       prefix = ''


    # -------------------
    # storage menu
    # -------------------

    print ('---')
    
    my_volumes = 0
    my_volumes_consumption = 0

    my_snapshots = 0
    my_snapshots_consumption = 0

    for volume in volumes: 
        my_volumes += 1
        my_volumes_consumption += volume['Size']
    
    for snapshot in snapshots:
        my_snapshots +=1 
        my_snapshots_consumption += snapshot['Size']

    print ('Volumes:\t\t\t %s objects, %s Gb total | color=%s' % (my_volumes, my_volumes_consumption, info_color))
    print ('Snapshots:\t\t\t %s objects, %s Gb total | color=%s' % (my_snapshots, my_snapshots_consumption, info_color))

    # -------------------
    # cost and usage menu
    # -------------------

    # monthly 
    print ('---')
    totalcost = 0
    for group in monthly_cost['ResultsByTime'][0]['Groups']:
       totalcost += float(group['Metrics']['BlendedCost']['Amount'])
    print ('Cost this month:\t\t %s | color=%s' % (color_cost(totalcost,'','USD'),color))
    for group in monthly_cost['ResultsByTime'][0]['Groups']:
       if group['Keys'][0] == 'Tax':
          print('-----')
       print '--%s | color=%s' % (color_cost(group['Metrics']['BlendedCost']['Amount'],group['Keys'][0],group['Metrics']['BlendedCost']['Unit']),color)
    print ('-----')
    print ('--%s | color=%s' % (color_cost(totalcost,'Total','USD'),color))
    totalcost = 0
    
    # daily 
    dailycost = 0
    for day in daily_cost['ResultsByTime']:
       for group in day['Groups']:
          dailycost += float(group['Metrics']['BlendedCost']['Amount'])
       print ('----%s : \t%s | color=%s' % (day['TimePeriod']['Start'],color_cost(dailycost,'','USD'),color))
       for group in day['Groups']:
          if group['Keys'][0] == 'Tax':
             print('---------')
          print '------%s | color=%s' % (color_cost(group['Metrics']['BlendedCost']['Amount'],group['Keys'][0],group['Metrics']['BlendedCost']['Unit']),color)
       print ('---------')
       print ('------%s | color=%s' % (color_cost(dailycost,'Total','USD'),color))
       dailycost = 0
 



def run_script(script):
    return subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()

if __name__ == '__main__':
    main(sys.argv)
