from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.subscription import SubscriptionClient
import time

import requests
import json
import mysql.connector
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = '1234', database='cpa')
mycursor=mydb.cursor()
query="delete from azureprice"
mycursor.execute(query)
mydb.commit()


compute_client = ComputeManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id='54a5ea51-c07c-4503-9757-fd6e935b14e4'
)

subs_client= SubscriptionClient(
    credential=DefaultAzureCredential(),
    subscription_id='54a5ea51-c07c-4503-9757-fd6e935b14e4'
)

def azure_instance_types(location):
    instance_types= compute_client.virtual_machine_sizes.list(location)
    instances=dict()
    for i, r in enumerate(instance_types):
        instance_name=r.name.strip()
        if "D" in r.name or "B" in r.name or "A" in r.name:
            family="General Purpose"
        elif "F" in r.name:
            family="Compute Optimized"
        elif "E" in r.name or "M" in r.name or "Gs" in r.name:
            family="Memory Optimized"
        elif "L" in r.name:
            family="Storage Optimized"
        elif "N" in r.name:
            family="GPU"
        elif "H" in r.name:
            family="HPC"
        LinuxPrice, WindowsPrice =getAzureInstancePrice(instance_name,location)
        if LinuxPrice==0 and WindowsPrice==0:
            continue
        try:
            instances[instance_name]={"LinuxPrice":LinuxPrice,"WindowsPrice":WindowsPrice,"VCpuInfo":r.number_of_cores, "MemoryInfo":r.memory_in_mb/1024, "InstanceStorageInfo":r.resource_disk_size_in_mb/1024, "instanceFamily": family}
        except:
            print(instance_name,"is causing error")
        query="insert into azurePrice values(%s,%s,%s,%s,%s,%s,%s,%s)"
        tup=(instance_name,LinuxPrice,WindowsPrice,r.number_of_cores,r.memory_in_mb/1024,r.resource_disk_size_in_mb/1024,family, location)
        mycursor.execute(query,tup)
        print(instance_name+" ",instances[instance_name])
        mydb.commit()
    return instances


def getAzureInstancePrice(instance_name,location):
    api_url="https://prices.azure.com/api/retail/prices"
    query = "armRegionName eq '"+location+"' and armSkuName eq '"+instance_name+"' and priceType eq 'Consumption'"
    try:
        response = requests.get(api_url, params={'$filter': query})
    except:
        time.sleep(10)
        response = requests.get(api_url, params={'$filter': query})
    
    json_result=json.loads(response.text)

    for item in json_result['Items']:
        if 'Spot' in item['meterName'] or 'Low Priority' in item['meterName'] or "Virtual Machines" not in item['productName']:
            continue
        if 'Windows' in item['productName']:
            price2=item['retailPrice']
        else:
            price1=item['retailPrice']
        

    nextPage=json_result['NextPageLink']

    while(nextPage):
        response=requests.get(nextPage.text)
        json_result=json.loads(response)
        for item in json_result['Items']:
            if 'Spot' in item['meterName'] or 'Low Priority' in item['meterName'] or "Virtual Machines" not in item['productName']:
                continue
            if 'Windows' in item['productName']:
                price2=item['retailPrice']
            else:
                price1=item['retailPrice']
        nextPage=json_result['NextPageLink']
    try:
        return price1, price2
    except UnboundLocalError:
        return 0,0


def insertIntoTable(instance_dict):
    for region in instance_dict.keys():
        instances=instance_dict[region]
        for i in instances:
            instance_name=i
            LinuxPrice=instances[i]["LinuxPrice"]
            WindowsPrice=instances[i]["WindowsPrice"]
            vcpu=instances[i]["VCpuInfo"]
            memory=instances[i]["MemoryInfo"]
            storage=instances[i]["InstanceStorageInfo"]
            family=instances[i]["instanceFamily"]
            query="insert into azurePrice values(%s,%s,%s,%s,%s,%s,%s)"
            tup=(instance_name,LinuxPrice,WindowsPrice,vcpu,memory,storage,family)
            mycursor.execute(query,tup)
    
    mydb.commit()

def main():
    print('azureInstPrice is executing')
    # Get the prices for each instance type
    instance_dict=dict()
    region_list=['eastus', 'eastus2', 'westus', 'centralus', 'northcentralus', 'southcentralus', 'northeurope', 'westeurope', 'eastasia', 'southeastasia', 'japaneast', 'japanwest', 'australiaeast', 'australiasoutheast', 'australiacentral', 'brazilsouth', 'southindia', 'centralindia', 'westindia', 'canadacentral', 'canadaeast', 'westus2', 'westcentralus', 'uksouth', 'ukwest', 'koreacentral', 'koreasouth', 'francecentral', 'southafricanorth', 'uaenorth', 'switzerlandnorth', 'germanywestcentral', 'norwayeast', 'jioindiawest', 'westus3', 'swedencentral', 'qatarcentral', 'polandcentral']
    #region_list=['eastus', 'eastus2', 'westus', 'centralus', 'northcentralus', 'southcentralus', 'northeurope', 'westeurope', 'eastasia', 'southeastasia', 'japaneast', 'japanwest', 'australiaeast', 'australiasoutheast', 'australiacentral', 'brazilsouth', 'southindia', 'centralindia', 'westindia', 'canadacentral', 'canadaeast', 'westus2', 'westcentralus', 'uksouth', 'ukwest', 'koreacentral', 'koreasouth', 'francecentral', 'southafricanorth', 'uaenorth', 'switzerlandnorth', 'germanywestcentral', 'jioindiawest', 'westus3']
    for region in region_list:
        instance_dict[region]=azure_instance_types(region)

if __name__=='__main__':
    main()


#insertIntoTable(instance_dict)
#print(instance_dict["westus2"])