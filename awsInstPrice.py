import boto3
import json
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

instance_dict=dict()

instance_dict['ap-south-1']=ec2_instance_types(region_code='ap-south-1')


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

