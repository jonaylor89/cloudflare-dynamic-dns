#!/usr/bin/env python
import CloudFlare 
import os
import requests

def getCurrentIp():
    r = requests.get(r'http://jsonip.com')
    ip=r.json()['ip']
    return ip

def main():
    email = os.environ['CF_EMAIL']
    token = os.environ['CF_TOKEN']
    zone = os.environ['CF_ZONE_ID']
    target_record = os.environ['TARGET_RECORD']
    cf=CloudFlare.CloudFlare(email=email,token=token)
    dns_record={'name':target_record,'type':'A','content':getCurrentIp()}
    r = cf.zones.dns_records.post(zone, data=dns_record)
    exit(0)

if __name__ == '__main__':
    main()
