from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.billing import BillingManagementClient
import requests
import json


compute_client = ComputeManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id='54a5ea51-c07c-4503-9757-fd6e935b14e4'
)

billing_client= BillingManagementClient(
    credential=DefaultAzureCredential(), 
    subscription_id='54a5ea51-c07c-4503-9757-fd6e935b14e4'
)
def azure_instance_types(location):
    instance_types= compute_client.virtual_machine_sizes.list(location)
    instances=dict()
    for i, r in enumerate(instance_types):
        name=r.name.strip()
        if "D" in r.name or "B" in r.name:
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
        price1, price2 =getAzureInstancePrice(name,location)
        if price1==0 and price2==0:
            continue
        instances[name]={"LinuxPrice":price1,"WindowsPrice":price2,"VCpuInfo":r.number_of_cores, "MemoryInfo":r.memory_in_mb/1024, "InstanceStorageInfo":r.resource_disk_size_in_mb/1024, "instanceFamily": family}
        print(name+" ",instances[name])
    return instances


def getAzureInstancePrice(instance_name,location):
    #api_url= "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview"
    api_url="https://prices.azure.com/api/retail/prices"
    query = "armRegionName eq '"+location+"' and armSkuName eq '"+instance_name+"' and priceType eq 'Consumption'"
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


# Get the prices for each instance type
instance_dict=dict()

instance_dict['westus2']=azure_instance_types('westus2')
print(instance_dict["westus2"])
