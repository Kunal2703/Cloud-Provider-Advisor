import boto3
import json
import mysql.connector
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = '1234', database='cpa')
mycursor=mydb.cursor()

pricing = boto3.client('pricing')
ec2=boto3.client('ec2')


def ec2_instance_types(region_code):

    instances=dict()

    ec2 = boto3.client('ec2', 
        region_name=region_code,
    )

    describe_args = {
    }
    
    while True:
        describe_result = ec2.describe_instance_types(**describe_args)
        for i in describe_result['InstanceTypes']:
            instanceName=i['InstanceType']
            instances[instanceName]=i
            try:
                instanceFamily, linuxPrice, windowsPrice=getInstancePrice(instanceName,region_code)
                instances[instanceName]['InstanceFamily']=instanceFamily
                instances[instanceName]['LinuxPrice']=linuxPrice
                instances[instanceName]['WindowsPrice']=windowsPrice
            except:
                continue

        if 'NextToken' not in describe_result:
            break
        describe_args['NextToken'] = describe_result['NextToken']
    
    
    return instances


def getInstancePrice(instance_name, regionCode):
    Filters = '[{{"Field": "tenancy", "Value": "shared", "Type": "TERM_MATCH"}},'\
    '{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},'\
    '{{"Field": "preInstalledSw", "Value": "NA", "Type": "TERM_MATCH"}},'\
    '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},'\
    '{{"Field": "regionCode", "Value": "{r}", "Type": "TERM_MATCH"}},'\
    '{{"Field": "capacitystatus", "Value": "Used", "Type": "TERM_MATCH"}},'\
    '{{"Field": "licenseModel", "Value": "No License required", "Type": "TERM_MATCH"}}]'

    f = Filters.format(r=regionCode, t=instance_name, o='Linux')
    response = pricing.get_products(
        ServiceCode='AmazonEC2', 
        Filters=json.loads(f))
    on_demand = json.loads(response['PriceList'][0])['terms']['OnDemand']
    key1 = list(on_demand)[0]
    key2 = list(on_demand[key1]['priceDimensions'])[0]
    linuxPrice=on_demand[key1]['priceDimensions'][key2]['pricePerUnit']['USD']
    linuxPrice=float(linuxPrice)
    instanceFamily=json.loads(response['PriceList'][0])['product']['attributes']['instanceFamily']

    f = Filters.format(r=regionCode, t=instance_name, o='Windows')
    response = pricing.get_products(
        ServiceCode='AmazonEC2', 
        Filters=json.loads(f))
    on_demand = json.loads(response['PriceList'][0])['terms']['OnDemand']
    key1 = list(on_demand)[0]
    key2 = list(on_demand[key1]['priceDimensions'])[0]
    windowsPrice=on_demand[key1]['priceDimensions'][key2]['pricePerUnit']['USD']
    windowsPrice=float(windowsPrice)

    return instanceFamily, linuxPrice, windowsPrice

def insertIntoTable(instance_dict):
    query="delete from awsprice"
    mycursor.execute(query)
    for region in instance_dict.keys():
        for i in instance_dict[region]:
            instance=instance_dict[region][i]
            instance_name=i
            try:
                linuxPrice=instance['LinuxPrice']
                windowsPrice=instance['WindowsPrice']
            except:
                continue
            vcpu=instance['VCpuInfo']['DefaultVCpus']
            memory=instance['MemoryInfo']['SizeInMiB']/1024
            family=instance['InstanceFamily']
            query="insert into awsprice values(%s, %s, %s, %s, %s, %s)"
            if 'InstanceStorageInfo' in instance.keys():
                storage=instance['InstanceStorageInfo']['TotalSizeInGB']
            else:
                storage='EBS only'

            query="insert into awsprice values(%s, %s, %s, %s, %s, %s, %s, %s)"
            tup=(instance_name, linuxPrice, windowsPrice, vcpu, memory, storage, family, region)
            mycursor.execute(query,tup)
            mydb.commit()


def main():
    print('awsInstPrice is executing')

    region_list= [region['RegionName']for region in ec2.describe_regions(AllRegions=True)['Regions']]
    instance_dict=dict()

    for region in region_list:
        instance_dict[region]=ec2_instance_types(region_code=region)

    insertIntoTable(instance_dict)
    mydb.close()
    print("updated aws")

if __name__=='__main__':
    main()
