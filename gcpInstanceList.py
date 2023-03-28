from google.cloud import compute_v1, billing

machine_client=compute_v1.MachineTypesClient()

machine_list=machine_client.list(project='cloud-provider-advisor',zone='us-east4-c')
for i in machine_list:
    #print(i.name+" "+i.description)
    print(i.name)