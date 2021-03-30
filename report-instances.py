#!/usr/bin/python3
import boto3
import json
import os
import csv
from datetime import datetime
from os import environ
import sys
from pyzabbix import ZabbixAPI

regions = ["us-east-1"]
#regions = ["us-east-1","sa-east-1"]
zurl = ""
zuser = ""
zpass= ""
regiao= list()
status = list()
instancias = list()
now = datetime.now()
date =datetime(now.year,now.month,now.day).strftime('%Y-%m-%d')
zabbix_ip=[]
arquivoOutput = ""
if len(sys.argv) > 4:
    zurl = sys.argv[3]
    zuser = sys.argv[4]
    zpass = sys.argv[5]
    arquivoOutput = sys.argv[6]
    zapi = ZabbixAPI(zurl)
    zapi.login(zuser,zpass)
        
    for host in zapi.host.get(output="extend"):
        ips = zapi.hostinterface.get(output="extend", hostids = str(host['hostid']))
        if ips[0]['ip'] != "127.0.0.1":
            zabbix_ip.append(ips[0]['ip'])
else:
    arquivoOutput= sys.argv[3]

for region in regions:
    print('\n'+region)
    ec2 = boto3.client('ec2',aws_access_key_id=sys.argv[1],
    aws_secret_access_key=sys.argv[2], region_name=region)
    response = ec2.describe_instances()
    for r in response['Reservations']:
        for instance in r['Instances']:
            zabbix = ""
            if len(sys.argv) > 4:
                zabbix = "Não"
            for tag in instance.get('Tags',[]):
                if tag['Key'] == 'Name':
                    name=tag['Value']
            publicip=''
            keyname=instance.get('KeyName','')
            privateip=instance.get('PrivateIpAddress','')
            if privateip in zabbix_ip:
                zabbix = "Sim"
            try:
                img=ec2.describe_images(ImageIds=[imgid])['Images'][0]
            except:
                img={}
            for network in instance['NetworkInterfaces']:
                pubip=network.get('Association',{}).get('PublicIp')
                if pubip:
                    publicip = pubip
                    if publicip in zabbix_ip:
                        zabbix = "Sim"
                    break
            result={
                "Region": region,
                "State": instance['State'].get('Name'),
                "Name": name,
                "InstanceId": instance['InstanceId'],
                "InstanceType": instance['InstanceType'],
                "PrivateIpAddress": privateip,
                "PublicIp": publicip,
                "KeyName" : keyname,
                "Zabbix": zabbix
            }
            instancias.append(result)
            print('.', end='')
print(json.dumps(instancias,indent=4,default=str))
regiao.append(region)  

with open(arquivoOutput, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Region','State','Name','InstanceId','PrivateIpAddress','KeyName','Zabbix'])
    for i in instancias:
        spamwriter.writerow([i['Region'],i['State'],i['Name'],i['InstanceId'],i['PrivateIpAddress'],i['KeyName'],i['Zabbix']])
print('Arquivo gerado: ' + arquivoOutput)        
