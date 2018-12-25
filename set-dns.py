#!/usr/bin/env python
import CloudFlare 
import os
import requests
import socket
import time

def get_ip_by_dns(domain_name):
    return socket.gethostbyname(domain_name)

def get_current_ip():
    r = requests.get(r'http://jsonip.com')
    ip=r.json()['ip']
    return ip

def search_zone_for_record(cf, zone_id, target_record):
    dns_records = cf.zones.dns_records.get(zone_id)
    for record in dns_records:
        if record['name'] == target_record:
            return record['id']
    return False

def main(cf, zone, target_record):
    current_ip = get_current_ip()
    
    while True:
        print("checking for record")
        record_id = search_zone_for_record(cf,zone,target_record)
        if record_id:
            if current_ip == get_ip_by_dns(target_record):
          
                dns_record={'name':target_record,'type':'A','content':current_ip}
                cf.zones.dns_records.delete(zone,record_id)         
                r = cf.zones.dns_records.post(zone, data=dns_record)
            else:
                print("not changing the record since its already correct")
        else:
            dns_record={'name':target_record,'type':'A','content':current_ip}
            r = cf.zones.dns_records.post(zone, data=dns_record)

        time.sleep(30)


if __name__ == '__main__':
    email = os.environ['CF_EMAIL']
    token = os.environ['CF_TOKEN']
    zone = os.environ['CF_ZONE_ID']
    target_record = os.environ['TARGET_RECORD']
    cf=CloudFlare.CloudFlare(email=email, token=token)
    main(cf,zone,target_record)
