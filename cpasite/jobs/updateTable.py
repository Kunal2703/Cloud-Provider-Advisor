import mysql.connector

def main():
    mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = '1234') #insert your own host, user and password
    mycursor=mydb.cursor()

    query="use cpa"
    mycursor.execute(query)


    query="insert into allinstanceprice1(Instance_name, Linux_Price, Windows_Price, vCPU, Memory, Storage, Instance_Family, region, Provider) select Instance_name, Linux_Price, Windows_Price, vCPU, memory, storage, Instance_Family, region, 'AWS' from awsprice"
    mycursor.execute(query)

    query="insert into allinstanceprice1(Instance_name, Linux_Price, Windows_Price, vCPU, Memory, Storage, Instance_Family, region, Provider) select Instance_name, Linux_Price, Windows_Price, vCPU, memory, storage, Instance_Family, region, 'Azure' from azureprice"
    mycursor.execute(query)

    query="insert into allinstanceprice1(Instance_name, Linux_Price, Windows_Price, vCPU, Memory, Storage, Instance_Family, region, Provider) select Instance_name, Instance_Price, Instance_Price, vcpu, Memory, 'Customizable', Instance_Family, Region, 'GCP' from gcpprice"
    mycursor.execute(query)

    query="truncate allInstancePrice"
    mycursor.execute(query)

    query="insert into allInstancePrice select * from allInstancePrice1"
    mycursor.execute(query)

    mydb.commit()
    mydb.close()

if __name__=='__main__':
    main()