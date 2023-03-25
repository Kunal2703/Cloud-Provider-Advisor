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
    return instance_types

def getAzureInstancePrice(instance_name,location):
    #api_url= "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview"
    api_url="https://prices.azure.com/api/retail/prices"
    query = "armRegionName eq '"+location+"' and armSkuName eq '"+instance_name+"' and priceType eq 'Consumption'"
    response = requests.get(api_url, params={'$filter': query})
    json_result=json.loads(response.text)

    for item in json_result['Items']:
        if 'Spot' in item['meterName'] or 'Low Priority' in item['meterName'] or "Virtual Machines" not in item['productName']:
            continue
        print(instance_name+" ",item['retailPrice'])

    nextPage=json_result['NextPageLink']
    #print(json_result)
    while(nextPage):
        response=requests.get(nextPage.text)
        json_result=json.loads(response)
        for item in json_result['Items']:
            if 'Spot' in item['meterName'] or 'Low Priority' in item['meterName']:
                continue
            print(instance_name+" ",item['retailPrice'])
        nextPage=json_result['NextPageLink']
        #print(json_result)

# Get the prices for each instance type

instance_types=azure_instance_types('westus2')
for i, r in enumerate(instance_types):
   #getAzureInstancePrice(instance_name= r.name, location='westus2')
   print(r)