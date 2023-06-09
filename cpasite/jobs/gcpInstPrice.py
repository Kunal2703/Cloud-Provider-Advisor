import requests
from google.cloud import compute_v1
import mysql.connector
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = '1234', database='cpa')
mycursor=mydb.cursor()


def getPrice(instanceName, regionCode):
    headers = {
        'X-Api-Key': 'ico-GnVxKvhdSo033YEthR0CVH6GTlbiwe9p',    
    }

    json_data = {
    'query': '{ products(filter: {vendorName: "gcp", service: "Compute Engine", productFamily: "Compute Instance", region: "'+regionCode+'", attributeFilters: [{key: "machineType", value: "'+instanceName+'"}]}) { prices(filter: {purchaseOption: "on_demand"}) { USD } } } ',
    }

    response = requests.post('https://pricing.api.infracost.io/graphql', headers=headers, json=json_data)
    response=response.json()
    try:
        price=response['data']['products'][0]['prices'][0]['USD']
        price=float(price)
        return price

    except:
        #print(instanceName, regionCode, response)    
        return 0
    


def getInstance(regionCode):
    machine_client=compute_v1.MachineTypesClient()
    if regionCode=='europe-west1':
        zoneCode=regionCode+'-b'
    else:
        zoneCode=regionCode+'-a'
    machine_list=machine_client.list(project='cloud-provider-advisor',zone=zoneCode)
    instances=dict()
    for i in machine_list:
        
        instanceName=i.name
        instancePrice=getPrice(instanceName,regionCode)
        if instancePrice==0:
            continue
        else:
            instances[instanceName]=dict()
            instancePrice=getPrice(instanceName,regionCode)
            instances[instanceName]['price']=instancePrice
            instances[instanceName]['vCPU']=i.guest_cpus
            instances[instanceName]['memory']=i.memory_mb/1024
       

        if "e2" in instanceName or "n2" in instanceName or "t2" in instanceName or "n1" in instanceName or "f1" in instanceName or "g1" in instanceName:
            family="General purpose"
        elif "c2" in instanceName:
            family="Compute optimized"
        elif "m1" in instanceName or "m2" in instanceName or "m3" in instanceName:
            family="Memory optimized"
        elif "a2" in instanceName or "g2" in instanceName:
            family="GPU instance" 
        
        instances[instanceName]['instanceFamily']=family
        
       
    return instances

def getRegions():

    regionClient=compute_v1.RegionsClient()
    regionListPager=regionClient.list(project='cloud-provider-advisor')
    regionList=list()
    for region in regionListPager:
        regionList.append(region.name)
    return regionList

def insertIntoTable(instance_dict):
    query="delete from gcpprice"
    mycursor.execute(query)
    for region in instance_dict.keys():
        for i in instance_dict[region]:
            instance=instance_dict[region][i]
            instance_name=i
            price=instance['price']
            vcpu=instance['vCPU']
            memory=instance['memory']
            family=instance['instanceFamily']

            query="insert into gcpprice values(%s, %s, %s, %s, %s, %s)"
            tup=(instance_name, price, vcpu, memory, family, region)
            mycursor.execute(query,tup)
            mydb.commit()


def main():
    print('gcpInstPrice is executing')
    regionList=getRegions()

    instanceDict=dict()

    for region in regionList:
        instanceDict[region]=getInstance(region)

    #instanceDict['us-west1']=getInstance('us-west1')
    insertIntoTable(instanceDict)
    mydb.close()
    print("updated gcp")

if __name__=='__main__':
    main()