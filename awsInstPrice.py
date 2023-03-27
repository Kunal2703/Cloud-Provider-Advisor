import boto3
import json
import mysql.connector
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = '1234', database='cpa')
mycursor=mydb.cursor()

pricing = boto3.client('pricing')



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
                instanceFamily, price=getInstancePrice(instanceName,region_code)
                instances[instanceName]['InstanceFamily']=instanceFamily
                instances[instanceName]['Price']=price
            except:
                continue
            
        if 'NextToken' not in describe_result:
            break
        describe_args['NextToken'] = describe_result['NextToken']
    
    
    return instances


def getInstancePrice(instance_name, regionCode):

    if instance_name.startswith('p2'):
        response = pricing.get_products(
                ServiceCode='AmazonEC2',
                Filters=[
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_name},
                    {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                    {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                    {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': regionCode},
                    {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
                ],
                FormatVersion='aws_v1',
            )
    else:
        response = pricing.get_products(
                ServiceCode='AmazonEC2',
                Filters=[
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_name},
                    {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                    {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                    {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': regionCode},
                    {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
                    {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'UnusedCapacityReservation'},
                ],
                FormatVersion='aws_v1',
            )

    for result in response['PriceList']:
        json_result=json.loads(result)
        for i in json_result['terms']['OnDemand'].values():
            for j in i['priceDimensions'].values():
                for k in j['pricePerUnit'].values():
                    continue
        price=float(k)
        instanceFamily=json_result['product']['attributes']['instanceFamily']
        
        return instanceFamily, price

def insertIntoTable(instance_dict):
    query="delete from awsprice"
    mycursor.execute(query)
    for region in instance_dict.keys():
        for i in instance_dict[region]:
            instance=instance_dict[region][i]
            instance_name=i
            try:
                price=instance['Price']
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

            query="insert into awsprice values(%s, %s, %s, %s, %s, %s)"
            tup=(instance_name, price, vcpu, memory, storage, family)
            mycursor.execute(query,tup)
            mydb.commit()


instance_dict=dict()

instance_dict['ap-south-1']=ec2_instance_types(region_code='ap-south-1')

insertIntoTable(instance_dict)

'''

for i in instance_dict['ap-south-1']:
    instance=instance_dict['ap-south-1'][i]
    if 'InstanceStorageInfo' in instance.keys():
        try:
            print(i," $",instance['Price'], instance['VCpuInfo']['DefaultVCpus'], instance['MemoryInfo']['SizeInMiB']/1024,"GB", instance['InstanceStorageInfo']['TotalSizeInGB'],"GB SSD ", instance['InstanceFamily'])
        except KeyError:
            continue
    else:
        try:
            print(i," $",instance['Price'], instance['VCpuInfo']['DefaultVCpus'], instance['MemoryInfo']['SizeInMiB']/1024,"GB", "EBS only", instance['InstanceFamily'])
        except KeyError:
            continue

'''
