#!/usr/bin/env python
import CloudFlare 
import os
import requests
import socket
def get_ip_by_dns(domain_name):
    return socket.gethostbyname(domain_name)
def get_current_ip():
    r = requests.get(r'http://jsonip.com')
    ip=r.json()['ip']
    return ip

def main():
    email = os.environ['CF_EMAIL']
    token = os.environ['CF_TOKEN']
    zone = os.environ['CF_ZONE_ID']
    target_record = os.environ['TARGET_RECORD']
    cf=CloudFlare.CloudFlare(email=email,token=token)
    current_ip = get_current_ip()
    if current_ip == get_ip_by_dns(target_record):
        dns_record={'name':target_record,'type':'A','content':current_ip}
        r = cf.zones.dns_records.post(zone, data=dns_record)
    else:
        print("not changing the record sicne its already correct")
    exit(0)

if __name__ == '__main__':
    main()
