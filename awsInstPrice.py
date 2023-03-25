import boto3
import json
pricing = boto3.client('pricing')
#instance_type_name="t2.nano"

location='Asia Pacific (Mumbai)'

#loc_params=pricing.get_attribute_values(ServiceCode='AmazonEC2',AttributeName='location')
#print(loc_params)
def ec2_instance_types(region_name, cpu_architecture="x86_64", default_cores=2, default_threads_per_core=1, gpu=True):

    workload_wise_instance=dict()
    workload_wise_instance['gen_purpose']=dict()

    ec2 = boto3.client('ec2', 
        region_name=region_name,
    )

    describe_args = {
    }
    gen_purpose_prefix=['m7g','mac','m6g','m6i','m6in','m6a','m5','m5n','m5zn','m5a','m4','a1','t4g','t3','t3a','t2']
    
    while True:
        describe_result = ec2.describe_instance_types(**describe_args)
        for i in describe_result['InstanceTypes']:
            if(i['InstanceType'].startswith(tuple(gen_purpose_prefix))):
                workload_wise_instance['gen_purpose'][i['InstanceType']]=i
        if 'NextToken' not in describe_result:
            break
        describe_args['NextToken'] = describe_result['NextToken']
        
    return workload_wise_instance


def getInstancePrice(instance_name, location):

    response = pricing.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_name},
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': location},
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
        return price

#getInstancePrice("t2.micro",location)

instance_dict=dict()
instance_dict['ap-south-1']=ec2_instance_types(region_name='ap-south-1')

l=instance_dict['ap-south-1']['gen_purpose']

for i in l:
    l[i]['Price']=getInstancePrice(i,location)

for i in l:
    print(i,l[i]['Price'])