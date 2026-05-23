#!/usr/bin/env PYTHONIOENCODING=UTF-8 /opt/local/bin/python
# -*- coding: utf-8 -*-
#
# <xbar.title>MyAWS</xbar.title>
# <xbar.version>v4.0</xbar.version>
# <xbar.author>pvdabeel@mac.com</xbar.author>
# <xbar.author.github>pvdabeel</xbar.author.github>
# <xbar.desc>Create, connect to and terminate Amazon EC2 virtual machines from the OS X menubar</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
#
# Licence: GPL v3

# Installation instructions: 
# -------------------------- 
# Ensure you have the Amazon EC2 CLI installed (see Readme for link)
# Run 'sudo pip install tinydb boto3 currencyconverter' in Terminal.app
# Ensure you have xbar installed https://github.com/matryer/xbar-plugins
# Copy this file to your xbar plugins folder and chmod +x the file from your terminal in that folder
# Run xbar

import warnings

warnings.filterwarnings("ignore")

aws_owner_id = '615416975922'
aws_key_name = 'pvdabeel@mac.com'
aws_security = 'sg-bce547d1'
aws_command  = '/opt/local/bin/aws' # Full path needed
aws_region   = 'eu-central-1'
aws_ostype   = 'Linux'

# AWS Pricing API uses verbose location names instead of region codes.
# Extend this map if you switch aws_region to something not listed here.
aws_region_to_location = {
    'us-east-1':      'US East (N. Virginia)',
    'us-east-2':      'US East (Ohio)',
    'us-west-1':      'US West (N. California)',
    'us-west-2':      'US West (Oregon)',
    'eu-central-1':   'EU (Frankfurt)',
    'eu-west-1':      'EU (Ireland)',
    'eu-west-2':      'EU (London)',
    'eu-west-3':      'EU (Paris)',
    'eu-north-1':     'EU (Stockholm)',
    'eu-south-1':     'EU (Milan)',
    'ap-northeast-1': 'Asia Pacific (Tokyo)',
    'ap-northeast-2': 'Asia Pacific (Seoul)',
    'ap-southeast-1': 'Asia Pacific (Singapore)',
    'ap-southeast-2': 'Asia Pacific (Sydney)',
    'ap-south-1':     'Asia Pacific (Mumbai)',
    'ca-central-1':   'Canada (Central)',
    'sa-east-1':      'South America (Sao Paulo)',
}

vm_cheap     = 1
vm_expensive = 2 

preferred_currency = 'EUR' # or 'USD' (or any currency supported by currencyconvertor)


aws_vmtypes  = [#('t2', [ ('.micro',   '(   1 vcpu, 1Gb ram )\t'),
                #         ('.small',   '(   1 vcpu, 2Gb ram )\t'),
                #         ('.medium',  '(   2 vcpu, 4Gb ram )\t'),
                #         ('.large',   '(   2 vcpu, 8Gb ram )\t'), 
                #         ('.xlarge',  '(   4 vcpu, 16Gb ram )\t'), 
                #         ('.2xlarge', '(   8 vcpu, 32Gb ram )\t')  ]),
                #('t3', [ ('.micro',   '(   2 vcpu, 1Gb ram )\t'), 
                #         ('.small',   '(   2 vcpu, 2Gb ram )\t'), 
                #         ('.medium',  '(   2 vcpu, 4Gb ram )\t'), 
                #         ('.large',   '(   2 vcpu, 8Gb ram )\t'), 
                #         ('.xlarge',  '(   4 vcpu, 16Gb ram )\t'), 
                #         ('.2xlarge', '(   8 vcpu, 32Gb ram )\t')  ]), 
                #('m4', [ ('.4xlarge', '(  16 vcpu, 64Gb ram )\t'), 
                #         ('.16xlarge','(  64 vcpu, 256Gb ram )\t') ]), 
                #('m5', [ ('.4xlarge', '(  16 vcpu, 64Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 384Gb ram )\t') ]),
                #         ('.metal',   '(  96 vcpu, 384Gb ram )\t') ]), 
                #('m5d',[ ('.4xlarge', '(  16 vcpu, 64Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 384Gb ram )\t'), 
                #         ('.metal',   '(  96 vcpu, 384Gb ram )\t') ]), 
                #('m5zn',[('.large',   '(   2 vcpu, 8Gb ram )\t'), 
                #         ('.xlarge',  '(   4 vcpu, 16Gb ram )\t'), 
                #         ('.2xlarge', '(   8 vcpu, 32Gb ram )\t'), 
                #         ('.3xlarge', '(  12 vcpu, 48Gb ram )\t'), 
                #         ('.6xlarge', '(  24 vcpu, 96Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'), 
                #         ('.metal',   '(  48 vcpu, 192Gb ram )\t') ]), 
                #('m6i',[ ('.4xlarge', '(  16 vcpu, 64Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 384Gb ram )\t'), 
                #         ('.32xlarge','( 128 vcpu, 512Gb ram )\t') ]),
                #         ('.metal',   '( 128 vcpu, 512Gb ram )\t') ]), 
                #('m6id',[('.4xlarge', '(  16 vcpu, 64Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 384Gb ram )\t'), 
                #         ('.32xlarge','( 128 vcpu, 512Gb ram )\t'),
                #         ('.metal',   '( 128 vcpu, 512Gb ram )\t') ]), 
                #('m7i',[ ('.4xlarge', '(  16 vcpu, 64Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 384Gb ram )\t'), 
                #         ('.48xlarge','( 192 vcpu, 768Gb ram )\t') ]),
                #('m7id',[('.4xlarge', '(  16 vcpu, 64Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 384Gb ram )\t'), 
                #         ('.32xlarge','( 128 vcpu, 512Gb ram )\t'),
                #         ('.metal',   '( 128 vcpu, 512Gb ram )\t') ]), 
                #('c5', [ ('.4xlarge', '(  16 vcpu, 32Gb ram )\t'), 
                #         ('.9xlarge', '(  36 vcpu, 72Gb ram )\t'), 
                #         ('.18xlarge','(  72 vcpu, 144Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 192Gb ram )\t') ]),
                #        ('.metal',   '(  96 vcpu, 192Gb ram )\t') ]),
                #('c5d',[ ('.4xlarge', '(  16 vcpu, 32Gb ram )\t'), 
                #         ('.9xlarge', '(  36 vcpu, 72Gb ram )\t'), 
                #         ('.18xlarge','(  72 vcpu, 144Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 192Gb ram )\t'),
                #         ('.metal',   '(  96 vcpu, 192Gb ram )\t') ]),
                #('c5n',[ ('.4xlarge', '(  16 vcpu, 42Gb ram )\t'), 
                #         ('.9xlarge', '(  36 vcpu, 96Gb ram )\t'), 
                #         ('.18xlarge','(  72 vcpu, 192Gb ram )\t'),
                #         ('.metal',   '(  72 vcpu, 192Gb ram )\t') ]),
                #('c6i',[ ('.4xlarge', '(  16 vcpu, 32Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 96Gb ram )\t'), 
                #         ('.24xlarge','(  96 vcpu, 192Gb ram )\t'),
                #         ('.32xlarge','( 128 vcpu, 256Gb ram )\t') ]),
                #         ('.metal',   '( 128 vcpu, 256Gb ram )\t') ]),
                ('c7i',[ ('.4xlarge', '(  16 vcpu, 32Gb ram )\t'), 
                         ('.12xlarge','(  48 vcpu, 96Gb ram )\t'), 
                         ('.24xlarge','(  96 vcpu, 192Gb ram )\t'),
                         ('.48xlarge','( 192 vcpu, 384Gb ram )\t') ]),

                ('c8i',[ ('.4xlarge', '(  16 vcpu, 32Gb ram )\t'), 
                         ('.12xlarge','(  48 vcpu, 96Gb ram )\t'), 
                         ('.24xlarge','(  96 vcpu, 192Gb ram )\t'),
                         ('.48xlarge','( 192 vcpu, 384Gb ram )\t'),
                         ('.96xlarge','( 384 vcpu, 768Gb ram )\t') ]),

                ('m8i',[ ('.4xlarge', '(  16 vcpu, 64bGb ram )\t'), 
                         ('.12xlarge','(  48 vcpu, 192Gb ram )\t'),
                         ('.24xlarge','(  96 vcpu, 384Gb ram )\t'),
                         ('.48xlarge','( 192 vcpu, 768Gb ram )\t'),
                         ('.96xlarge','( 384 vcpu, 1536Gb ram )') ]) ]
 
                #         ('.metal',   '( 128 vcpu, 256Gb ram )\t') ]) ]
                #('u-6tb1', [ ('.112xlarge', '( 448 vcpu, 6Tb ram )') ]) ]
                #         ('.8xlarge', '(  32 vcpu, 244Gb ram )'), 
                #         ('.16xlarge','(  64 vcpu, 488Gb ram )')  ]), 
                #('x1', [ ('.16xlarge','(  64 vcpu, 976Gb ram )\t'),
                #         ('.32xlarge','( 128 vcpu, 1952Gb ram )')  ]), 
                #('x1e',[ ('.16xlarge','(  64 vcpu, 1952Gb ram )'),
                #         ('.32xlarge','( 128 vcpu, 3904Gb ram )')  ]), 
                #('u-6tb1',[('.metal',  '( 448 vcpu, 6144Gb ram )')  ]), 
                #('z1d',[ ('.2xlarge', '(   8 vcpu, 64Gb ram )\t'),
                #         ('.3xlarge', '(  12 vcpu, 96Gb ram )\t'), 
                #         ('.6xlarge', '(  24 vcpu, 192Gb ram )\t'), 
                #         ('.12xlarge','(  48 vcpu, 384Gb ram )\t'), 
                #         ('.metal',   '(  48 vcpu, 384Gb ram )\t')  ]), 
                #('i3', [ ('.metal',   '(  72 core, 512Gb ram )\t') ]),
                #('mac1',[('.metal',   '(  12 core, 32Gb ram )\t') ]),
                #('mac2',[('.metal',   '(   8 core, 16Gb ram )\t') ]),
                #('mac2-m2',[('.metal', '(   8 core, 24Gb ram )\t') ]) ]
                #('mac2-m2pro',[('.metal',   '(  12 core, 32Gb ram )\t') ]) ]


aws_default_vmtype_update  = 'c8i.12xlarge'
aws_default_vmtype_rebuild = 'c8i.48xlarge'
aws_default_vmtype_tinder  = 'm8i.96xlarge'

# Command to be called inside instance to update it

cmd_update  = 'update'
cmd_rebuild = 'fullupdate'
cmd_tinder  = 'tinder'

# Ephemeral tinder worker: full manifest-all --build matrix.
tinder_env = (
    'TINDER_MANIFEST=manifest-all.txt'
    ' TINDER_MATRIX_MODE=--build'
    ' TINDER_JOBS=64'
    ' NPROC=32'
)

# Smoke test example (manifest-100 --pretend on m8i.48xlarge):
# aws_default_vmtype_tinder = 'm8i.48xlarge'
# tinder_env = (
#     'TINDER_MANIFEST=manifest-100.txt'
#     ' TINDER_MATRIX_MODE=--pretend'
#     ' TINDER_JOBS=32'
#     ' NPROC=32'
# )

# aws ec2 describe-images --owners 615416975922 --query 'Images[*].{ID:ImageId}'
# aws ec2 run-instances --image-id ami-089fc69c2ca496809 --count 1 --ebs-optimized --instance-type t2.micro --key-name gentoo --security-group-ids sg-bce547d1
# aws ec2 describe-instances --query 'Reservations[*].Instances[*].{ID:PublicDnsName,State:State}'
# aws ec2 terminate-instances --instance-ids i-0de69865f64ebd6ad
# aws ec2 stop-instances --instance-ids --force
# aws ec2 describe-instances --instance-id i-0c27fcf159ec94d0d --query 'Reservations[*].Instances[*].LaunchTime'
# aws ec2 get-console-output --instance-id i-0ed95956c74a187ac --output text
# aws ce get-cost-and-usage --time-period Start=2018-09-01,End=2018-09-23 --granularity MONTHLY --metrics BlendedCost UnblendedCost UsageQuantity --group-by Type=DIMENSION,Key=SERVICE

import json
import sys
import datetime
import base64
import time
import os
import subprocess
import shlex
import requests
import decimal
import boto3
from concurrent.futures import ThreadPoolExecutor

from tinydb import TinyDB

from os.path import expanduser

# Location where to store state files
home         = expanduser("~")
state_dir    = home+'/.state/myaws'

if not os.path.exists(state_dir):                                               
    os.makedirs(state_dir)    

# The full path to this file

cmd_path = os.path.realpath(__file__)

# Tiny DB to store pricing
database = TinyDB(state_dir+'/myawspricing.json')

# Nice ANSI colors
CEND    = '\33[0m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[36m'
CGRAY   = '\33[37m'
CDGRAY  = '\33[37m'

# ANSI styles

CBOLD   = '\033[01m'
CNORMAL = '\033[00m'

# Support for OS X Dark Mode                                                    
DARK_MODE=True if os.getenv('XBARDarkMode','false') == 'true' else False  


# Logo for both dark mode and regular mode
def app_print_logo():
    print ('|image=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')
    print('---')


def clear_tinydb(db):
    # Newer TinyDB (v4+)
    if hasattr(db, "drop_tables"):
        db.drop_tables()
        return

    # Older TinyDB (v1-v3)
    if hasattr(db, "purge_tables"):
        db.purge_tables()
        return

    # Fallback: clear the default table (older APIs)
    if hasattr(db, "purge"):
        db.purge()
        return

    raise RuntimeError(f"Don't know how to clear TinyDB for {type(db)}")


# ---------------------------------------------------------------------------
# Lazy boto3 session + clients (single Session per process, reused across calls)
# ---------------------------------------------------------------------------

_boto_session = None
_boto_clients = {}

def _aws_session():
    global _boto_session
    if _boto_session is None:
        _boto_session = boto3.Session(region_name=aws_region)
    return _boto_session

def _aws_client(service, **kwargs):
    key = (service, tuple(sorted(kwargs.items())))
    client = _boto_clients.get(key)
    if client is None:
        client = _aws_session().client(service, **kwargs)
        _boto_clients[key] = client
    return client

def ec2_client():
    return _aws_client('ec2')

def ce_client():
    return _aws_client('ce')

def pricing_client():
    # AWS Pricing API is only served from us-east-1 / ap-south-1.
    return _aws_client('pricing', region_name='us-east-1')


# ---------------------------------------------------------------------------
# Lazy CurrencyConverter (constructor parses an embedded ECB CSV; only pay
# that cost the first time we actually need to format a price).
# ---------------------------------------------------------------------------

_currency_converter = None

def get_converter():
    global _currency_converter
    if _currency_converter is None:
        from currency_converter import CurrencyConverter
        _currency_converter = CurrencyConverter()
    return _currency_converter


# ---------------------------------------------------------------------------
# File-backed TTL cache for read-only AWS describe-* calls. Keeps consecutive
# xbar refreshes (e.g. "refresh" submenu clicks) snappy. Datetimes are stored
# as ISO strings so cached and fresh data look identical to consumers.
# ---------------------------------------------------------------------------

class _DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        return super().default(o)

def cached_call(name, ttl_seconds, fn):
    cache_path = state_dir + '/cache-' + name + '.json'
    try:
        if time.time() - os.path.getmtime(cache_path) < ttl_seconds:
            with open(cache_path) as f:
                return json.load(f)
    except (OSError, ValueError):
        pass
    data = fn()
    serialized = json.dumps(data, cls=_DateTimeEncoder)
    try:
        with open(cache_path, 'w') as f:
            f.write(serialized)
    except OSError:
        pass
    return json.loads(serialized)


# Pretty printing
def color_state(state):
    if state == 'running':
        return CGREEN + justify(state,14) + CEND
    if state == 'stopped':
        return CRED + justify(state,14) + CEND
    if state == 'pending':
        return CGREEN + justify('starting',16) + CEND
    if state == 'terminated':
        return justify('deleted',14)
    if state == 'shutting-down':
        return CRED + justify('stopping',14) + CEND
    if state == 'stopping':
        return CRED + justify('stopping',14) + CEND
    else:
        return state

def color_cost(unconverted_cost,desc,rate):
    if preferred_currency == 'EUR':
        short_rate = u"€"
    else:
        short_rate = '$'
    if unconverted_cost == 'n/a':
       return 'Per hour:  '+CGRAY + ' n/a ' + CEND
    cost     = float(get_converter().convert(unconverted_cost, rate, preferred_currency))
    amount   = justify(str(cost_format(round(cost, 4))), 8)
    body     = short_rate + ' ' + amount
    if desc == 'Tax':
       return CRED + body + '\t ' + CEND + ' - ' + desc
    elif desc == 'Total':
       return CGREEN + body + '\t ' + CEND + ' - ' + desc
    elif desc == 'Hourly':
       if cost < vm_cheap:
          color = CGREEN
       elif cost <= vm_expensive:
          color = CYELLOW
       else:
          color = CRED
       return 'Per hour:  ' + color + body + ' ' + CEND
    elif desc == '':
       return CGREEN + body + '\t ' + CEND
    else:
       return CBLUE + body + '\t ' + CEND + ' - ' + desc

def cost_format(x):
    digits = 4
    temp = str(decimal.Decimal(str(x) + '0' * digits))
    return temp[:temp.find('.') + digits + 1]


def justify(string, number=10):
    length = len(string)
    quot   = (number - length ) // 4
    rem    = (number - length )  % 4
    return string.ljust(length+rem,' ').ljust(length+rem+quot,'\t')

def important(string):
    return CRED + string + CEND

# The init function: Called to store your AWS access keys
def init():
    print ('Please run \'aws configure\'')


# The update-pricing function: Retrieve EC2 pricing
#
# Uses the AWS Pricing API (boto3) instead of downloading the full EC2 offer
# file via awspricing. Each instance type only needs a small filtered query,
# and we run them in parallel and write the TinyDB once at the end.
def update_pricing():
    pricing = pricing_client()
    location = aws_region_to_location.get(aws_region, 'EU (Frankfurt)')

    def fetch_one(item):
        aws_vmgroup, aws_vmtype = item
        instance_type = aws_vmgroup + aws_vmtype
        try:
            resp = pricing.get_products(
                ServiceCode='AmazonEC2',
                Filters=[
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType',    'Value': instance_type},
                    {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': aws_ostype},
                    {'Type': 'TERM_MATCH', 'Field': 'tenancy',         'Value': 'Shared'},
                    {'Type': 'TERM_MATCH', 'Field': 'location',        'Value': location},
                    {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw',  'Value': 'NA'},
                    {'Type': 'TERM_MATCH', 'Field': 'capacitystatus',  'Value': 'Used'},
                    {'Type': 'TERM_MATCH', 'Field': 'licenseModel',    'Value': 'No License required'},
                ],
                MaxResults=1,
            )
            product = json.loads(resp['PriceList'][0])
            term         = next(iter(product['terms']['OnDemand'].values()))
            price_dim    = next(iter(term['priceDimensions'].values()))
            aws_pricing  = price_dim['pricePerUnit']['USD']
        except Exception:
            aws_pricing = 'n/a'
        return {'type': instance_type, 'pricing': aws_pricing}

    items = [(g, t) for (g, tl) in aws_vmtypes for (t, _) in tl]

    with ThreadPoolExecutor(max_workers=min(16, max(1, len(items)))) as pool:
        records = list(pool.map(fetch_one, items))

    clear_tinydb(database)
    if records:
        database.insert_multiple(records)
    database.insert({'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})


# The update-image function: Update an EC2 image
def update_image(cmd=cmd_update):
    if (len(sys.argv) != 4):
        print ('Please provide an ami name and ami snapshot id as argument')
        return
    ami_to_update = sys.argv[2]
    ami_snap_id   = sys.argv[3]

    ec2 = ec2_client()

    print ('')
    print (CYELLOW+CBOLD+'>>> Updating image:         '+CNORMAL+CGREEN+ami_to_update+CEND)
    print ('')
    if (cmd == cmd_update):
        aws_default_vmtype = aws_default_vmtype_update
    else:
        aws_default_vmtype = aws_default_vmtype_rebuild

    # for the given AMI image, spawn an instance
    print ('--- Deploying instance:     '+CGREEN+aws_default_vmtype+CEND)
    try:
        run_resp = ec2.run_instances(
            ImageId=ami_to_update,
            InstanceType=aws_default_vmtype,
            EbsOptimized=True,
            KeyName=aws_key_name,
            SecurityGroupIds=[aws_security],
            MinCount=1,
            MaxCount=1,
        )
        instance_id = run_resp['Instances'][0]['InstanceId']
    except Exception:
        print (CRED+'!!! Failed to deploy instance'+CEND)
        return
    print ('--- Instance deployed:      '+CGREEN+instance_id+CEND)

    def _terminate_quietly():
        try:
            ec2.terminate_instances(InstanceIds=[instance_id])
        except Exception:
            pass

    # wait until instance is up and running
    print ('--- Checking instance:      ', end="")
    try:
        ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        print (CGREEN+'running'+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Instance failed to reach running state'+CEND)
        _terminate_quietly()
        return

    print ('--- Instance dnsname:       ', end="")
    try:
        desc = ec2.describe_instances(InstanceIds=[instance_id])
        instance_dns = desc['Reservations'][0]['Instances'][0]['PublicDnsName']
        print (CGREEN+instance_dns+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Failed to get instance dnsname'+CEND)
        _terminate_quietly()
        return

    # execute update (still uses ssh; no boto3 equivalent)
    print ('--- Updating instance:', end="")
    print ('')
    try:
        updateoutcome = subprocess.call(
            "sleep 60 && ssh -q -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=~/.ssh/amazon-vms root@"
            + instance_dns + " \"bash -icl " + cmd + "\"", shell=True)
        print ('')
    except Exception:
        print (CRED+'!!! Failed to update instance'+CEND)
        _terminate_quietly()
        print ('')
        return

    if (updateoutcome):
        print (CRED+'!!! Failed to update instance'+CEND)
        _terminate_quietly()
        print ('')
        return

    # create new image
    print ('--- Creating new image:    ', end="")
    new_image_id = None
    try:
        updated_ami = ec2.create_image(
            InstanceId=instance_id,
            Name='Linux-' + time.strftime("%Y%m%d-%Hh%M"),
        )
        new_image_id = updated_ami['ImageId']
        print (CGREEN+'ok'+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Failed to create image'+CEND)

    # wait until image is available
    print ('--- Checking new image:    ', end="")
    try:
        if new_image_id:
            ec2.get_waiter('image_available').wait(ImageIds=[new_image_id])
        else:
            ec2.get_waiter('image_available').wait(Owners=['self'])
        print (CGREEN+'available'+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Image failed to reach available state'+CEND)
        return

    # Cleanup instance
    print ('--- Cleanup instance:      ', end="")
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        print (CGREEN+'ok'+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Instance cleanup failed'+CEND)

    # Cleanup old image
    print ('--- Cleanup old image:     ', end="")
    try:
        ec2.deregister_image(ImageId=ami_to_update)
        ec2.delete_snapshot(SnapshotId=ami_snap_id)
        print (CGREEN+'ok'+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Image cleanup failed'+CEND)

    print ('')
    print (CYELLOW+CBOLD+'>>> New image created'+CNORMAL+CEND)
    print ('')
    return


# Ephemeral tinderbox-ng matrix: spawn worker, run tinder, terminate.
# No new AMI is created; worker is always destroyed afterward.
def tinder_image():
    if (len(sys.argv) != 3):
        print ('Please provide an ami id as argument')
        return
    ami_id = sys.argv[2]

    ec2 = ec2_client()

    print ('')
    print (CYELLOW+CBOLD+'>>> Tinder run (manifest-all --build): '+CNORMAL+CGREEN+ami_id+CEND)
    print ('')
    print ('--- Instance type:          '+CGREEN+aws_default_vmtype_tinder+' (384 vCPU, 1536 GiB)'+CEND)
    print ('--- Matrix:                 '+CGREEN+'manifest-all.txt --build --jobs 64'+CEND)
    print ('')

    try:
        run_resp = ec2.run_instances(
            ImageId=ami_id,
            InstanceType=aws_default_vmtype_tinder,
            EbsOptimized=True,
            KeyName=aws_key_name,
            SecurityGroupIds=[aws_security],
            MinCount=1,
            MaxCount=1,
        )
        instance_id = run_resp['Instances'][0]['InstanceId']
    except Exception:
        print (CRED+'!!! Failed to deploy instance'+CEND)
        return
    print ('--- Instance deployed:      '+CGREEN+instance_id+CEND)

    def _terminate_quietly():
        try:
            ec2.terminate_instances(InstanceIds=[instance_id])
        except Exception:
            pass

    print ('--- Checking instance:      ', end="")
    try:
        ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        print (CGREEN+'running'+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Instance failed to reach running state'+CEND)
        _terminate_quietly()
        return

    print ('--- Instance dnsname:       ', end="")
    try:
        desc = ec2.describe_instances(InstanceIds=[instance_id])
        instance_dns = desc['Reservations'][0]['Instances'][0]['PublicDnsName']
        print (CGREEN+instance_dns+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Failed to get instance dnsname'+CEND)
        _terminate_quietly()
        return

    print ('--- Running tinder:           (bootstrap + matrix; long-running)')
    print ('')
    tinder_rc = 1
    try:
        remote_cmd = 'bash -icl ' + shlex.quote(tinder_env.strip() + ' ' + cmd_tinder)
        tinder_rc = subprocess.call(
            "sleep 60 && ssh -q -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=~/.ssh/amazon-vms root@"
            + instance_dns + " " + shlex.quote(remote_cmd),
            shell=True)
        print ('')
    except Exception:
        print (CRED+'!!! Failed to run tinder on instance'+CEND)
        _terminate_quietly()
        print ('')
        return

    print ('--- Cleanup instance:      ', end="")
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        print (CGREEN+'ok'+CEND)
    except Exception:
        print (CRED+'failed'+CEND)
        print (CRED+'!!! Instance cleanup failed'+CEND)

    print ('')
    if tinder_rc:
        print (CRED+'!!! Tinder finished with errors (rc='+str(tinder_rc)+')'+CEND)
    else:
        print (CYELLOW+CBOLD+'>>> Tinder run complete'+CNORMAL+CEND)
    print ('')
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

    # CASE 1e: ephemeral tinderbox-ng matrix (manifest-all --build)
    if 'tinder_image' in argv:
       tinder_image()
       return


    # CASE 2: nor init nor update were called, AWS not available
    if bool(DARK_MODE):                                                         
        color = '#FFFFFE'                                                       
        info_color = '#C0C0C0'                                                  
    else:                                                                       
        color = '#00000E'                                                       
        info_color = '#616161' 

    
    # CASE 3a: no internet connection
    try:
        requests.get('http://www.google.com',timeout=2)
    except:
       app_print_logo()
       print ('No internet connection | refresh=true terminal=false shell="%s" param1="%s" color=%s' % (cmd_path, 'true', color))
       return



    try:
        todayDate = datetime.date.today()
        monthDate = todayDate.replace(day=1)

        if (todayDate == monthDate):
           monthDate = monthDate - datetime.timedelta(days=1)
           monthDate = monthDate.replace(day=1)

        ec2 = ec2_client()
        ce  = ce_client()

        # Short-TTL cache for read-only describe calls so consecutive xbar
        # refreshes (e.g. clicking "refresh=true" items) stay snappy.
        DESCRIBE_TTL = 30  # seconds

        images_resp    = cached_call('describe-images',    DESCRIBE_TTL,
                                     lambda: ec2.describe_images(Owners=[aws_owner_id]))
        instances_resp = cached_call('describe-instances', DESCRIBE_TTL,
                                     lambda: ec2.describe_instances())
        volumes_resp   = cached_call('describe-volumes',   DESCRIBE_TTL,
                                     lambda: ec2.describe_volumes())
        snapshots_resp = cached_call('describe-snapshots', DESCRIBE_TTL,
                                     lambda: ec2.describe_snapshots(OwnerIds=[aws_owner_id]))

        # Normalise images so existing consumers can keep using
        # image['ImageId'] / image['Name'] / image['SnapshotId'].
        images = []
        for img in images_resp.get('Images', []):
            snap_id = None
            for bdm in img.get('BlockDeviceMappings') or []:
                ebs = bdm.get('Ebs') or {}
                if ebs.get('SnapshotId'):
                    snap_id = ebs['SnapshotId']
                    break
            images.append({
                'ImageId':    img.get('ImageId'),
                'Name':       img.get('Name'),
                'SnapshotId': snap_id,
            })

        # Flatten reservations -> single list of instance dicts.
        instances = [i for r in instances_resp.get('Reservations', [])
                       for i in r.get('Instances', [])]
        volumes   = volumes_resp.get('Volumes', [])
        snapshots = snapshots_resp.get('Snapshots', [])

        # Cost data is cached per-day. Use boto3 instead of the CLI when we
        # actually have to fetch (saves ~1s of CLI cold-start each call).
        def _fetch_cost(granularity):
            return ce.get_cost_and_usage(
                TimePeriod={'Start': monthDate.strftime("%Y-%m-%d"),
                            'End':   todayDate.strftime("%Y-%m-%d")},
                Granularity=granularity,
                Metrics=['BlendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}],
            )

        monthly_path = state_dir+'/myaws-costs-monthly'+todayDate.strftime("%Y%m%d")+'.json'
        try:
            with open(monthly_path) as json_file:
                monthly_cost = json.load(json_file)
        except (OSError, ValueError):
            monthly_cost = _fetch_cost('MONTHLY')
            with open(monthly_path, 'w') as json_file:
                json.dump(monthly_cost, json_file, cls=_DateTimeEncoder)

        daily_path = state_dir+'/myaws-costs-daily'+todayDate.strftime("%Y%m%d")+'.json'
        try:
            with open(daily_path) as json_file:
                daily_cost = json.load(json_file)
        except (OSError, ValueError):
            daily_cost = _fetch_cost('DAILY')
            with open(daily_path, 'w') as json_file:
                json.dump(daily_cost, json_file, cls=_DateTimeEncoder)
    except Exception:
       app_print_logo()
       print ('Failed to get data from EC2 | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (cmd_path, 'init', color))
       return

    # Build an in-memory pricing index once instead of scanning TinyDB
    # len(images) * len(vmtypes) times inside the loop below.
    price_by_type = {}
    db_last_updated = None
    for row in database.all():
        if 'type' in row:
            price_by_type[row['type']] = row['pricing']
        elif 'timestamp' in row:
            db_last_updated = row['timestamp']

    # CASE 3b: all ok, all other cases
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

       for (aws_vmgroup,aws_vmtypelist) in aws_vmtypes:
          for (aws_vmtype,aws_vmdesc) in aws_vmtypelist:
             instance_type = aws_vmgroup + aws_vmtype
             aws_pricing   = price_by_type.get(instance_type, 'n/a')
             print ('%s--%16s\t%30s\t%s | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, justify(instance_type,17), justify(aws_vmdesc,30), color_cost(aws_pricing,'Hourly','USD'), aws_command, "ec2 run-instances --image-id "+current_image_id+" --instance-type "+instance_type+" --ebs-optimized --key-name "+aws_key_name+" --security-group-ids "+aws_security, color))

          print ('%s-----' % prefix)


       if db_last_updated:
          print ('%s--Last updated:\t\t     %s | color=%s' % (prefix, db_last_updated, color))
          print ('%s----%s | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, 'Update AWS pricing',cmd_path, "update_pricing", color))
       else:
          print ('%s--%s | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, important('Update AWS pricing'),cmd_path, "update_pricing", color))

       print ('%s---' % prefix)


       # loop through instances
       image_instance_list = []

       for instance_json in instances:

           current_instance_id = instance_json['InstanceId']

           if instance_json['ImageId'] == current_image_id:
              image_instance_list.append(current_instance_id)
              state      = instance_json['State']['Name']
              dnsname    = instance_json.get('PublicDnsName', '') or ''
              vmtype     = instance_json['InstanceType']
              ipaddress  = instance_json.get('PublicIpAddress', '') or ''
              # LaunchTime arrives as an ISO string (cached_call serialises
              # boto3 datetimes via _DateTimeEncoder.isoformat()).
              launchtime = datetime.datetime.strptime(instance_json['LaunchTime'][:19],'%Y-%m-%dT%H:%M:%S')
              uptime     = datetime.datetime.utcnow() - launchtime
              uptime_d   = divmod(uptime.total_seconds(),86400)
              uptime_h   = divmod(uptime_d[1], 3600)
              uptime_m   = divmod(uptime_h[1], 60)

              print ('%s%14s %02dd : %02dh : %02dm\t%s ip: %s ' % (prefix, color_state(state), int(uptime_d[0]),int(uptime_h[0]),int(uptime_m[0]), justify(vmtype,24), ipaddress ))

              if state == 'running':
                 print ('%s--Connect | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, "ssh", "-q -o StrictHostKeyChecking=no -o UserKnownHostsFile=~/.ssh/amazon-vms root@"+dnsname, color))
              if state == 'stopped':
                 print ('%s--Start | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 start-instances --instance-ids "+current_instance_id, color))
              if (state == 'stopped'):
                 print ('%s--Create image | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 create-image --instance-id "+current_instance_id+" --name Linux-"+time.strftime("%Y%m%d-%Hh%M"), color))
              if state == 'running':
                 print ('%s--Stop | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 stop-instances --instance-ids "+current_instance_id+" --force", color))
              if (state == 'running') or (state == 'stopped'):
                 print ('%s--Terminate | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 terminate-instances --instance-ids "+current_instance_id, color))
              if state == 'running':
                 print ('%s-----' % (prefix))
                 print ('%s--Screenshot| color=%s' % (prefix, color))
                 try:
                    console = ec2.get_console_screenshot(InstanceId=current_instance_id)['ImageData']
                    print ('%s----|image="%s" | color=%s' % (prefix, console, color))
                 except Exception:
                    print ('%s----|Unable to get a screenshot | color=%s' % (prefix, color))
              if state != 'terminated':
                 print ('%s-----' % (prefix))
                 print ('%s--Serial Console Log| refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, "cat", state_dir+"/myaws-"+current_instance_id+".console.log", color))
                 try:
                    raw_output = ec2.get_console_output(InstanceId=current_instance_id).get('Output', '')
                    serial = base64.b64decode(raw_output).decode('utf-8', errors='replace') if raw_output else ''
                 except Exception:
                    serial = ''
                 with open(state_dir+"/myaws-"+current_instance_id+".console.log",'w') as console_file:
                    console_file.write(serial)
       
       if len(image_instance_list) > 0: 
          print ('%s---' % prefix)
          print ('%sTerminate all Virtual Machines | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 terminate-instances --instance-ids "+" ".join(image_instance_list), color))

       print ('%s---' % prefix)
       print ('%sImage' % prefix) 
       print ('%s--Update | refresh=true terminal=true shell="%s" param1="%s" param2="%s" param3="%s" color=%s' % (prefix, cmd_path, "update_image", current_image_id, current_image_snapshot_id, color))
       print ('%s--Rebuild | refresh=true terminal=true shell="%s" param1="%s" param2="%s" param3="%s" color=%s' % (prefix, cmd_path, "rebuild_image", current_image_id, current_image_snapshot_id, color))
       print ('%s--Tinder | refresh=true terminal=true shell="%s" param1="%s" param2="%s" color=%s' % (prefix, cmd_path, "tinder_image", current_image_id, color))

       if (len(images) > 1):
          print ('%s--Destroy | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 deregister-image --image-id "+current_image_id + " && "+aws_command+" ec2 delete-snapshot --snapshot-id "+current_image_snapshot_id, color))
       else:
          print ('%s--Destroy | refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 deregister-image --image-id "+current_image_id + " --dry-run && "+aws_command+" ec2 delete-snapshot --dry-run --snapshot-id "+current_image_snapshot_id, info_color))
          print ('%s--Destroy | alternate=true refresh=true terminal=true shell="%s" param1="%s" color=%s' % (prefix, aws_command, "ec2 deregister-image --image-id "+current_image_id + " --dry-run && "+aws_command+" ec2 delete-snapshot --snapshot-id "+current_image_snapshot_id, color))
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
        my_snapshots_consumption += snapshot.get('VolumeSize', 0)

    print ('Volumes:  \t\t\t %s objects, %s Gb total | color=%s' % (my_volumes, my_volumes_consumption, info_color))
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
       print ('--%s | color=%s' % (color_cost(group['Metrics']['BlendedCost']['Amount'],group['Keys'][0],group['Metrics']['BlendedCost']['Unit']),color))
    print ('-----')
    print ('--%s | color=%s' % (color_cost(totalcost,'Total','USD'),color))
    totalcost = 0
    
    # daily 
    dailycost = 0
    for day in daily_cost['ResultsByTime']:
       for group in day['Groups']:
          dailycost += float(group['Metrics']['BlendedCost']['Amount'])
       print ('----%s : %s | color=%s' % (day['TimePeriod']['Start'],color_cost(dailycost,'','USD'),color))
       for group in day['Groups']:
          if group['Keys'][0] == 'Tax':
             print('---------')
          print ('------%s | color=%s' % (color_cost(group['Metrics']['BlendedCost']['Amount'],group['Keys'][0],group['Metrics']['BlendedCost']['Unit']),color))
       print ('---------')
       print ('------%s | color=%s' % (color_cost(dailycost,'Total','USD'),color))
       dailycost = 0
 



def run_script(script):
    return subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()

if __name__ == '__main__':
    main(sys.argv)
