import mysql.connector
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = '1234') #insert your own host, user and password
mycursor=mydb.cursor()
query="CREATE database cpa"
mycursor.execute(query)
query="use cpa"
mycursor.execute(query)
mydb.commit()

query="create table awsPrice(Instance_name varchar(20), Linux_Price float, Windows_Price float, vCPU int, Memory float, Storage varchar(20), Instance_Family varchar(40), Region varchar(20))"
mycursor.execute(query)
query="create table azurePrice(Instance_name varchar(40), Linux_Price float, Windows_Price float, vCPU int, Memory float, Storage int, Instance_Family varchar(40), Region varchar(20))"
mycursor.execute(query)
query="create table gcpPrice(Instance_name varchar(40), Instance_Price float, vCPU int, Memory float, Instance_Family varchar(40), Region varchar(40))"
mycursor.execute(query)
query="create table allInstancePrice(Instance_name varchar(40), Linux_Price float, Windows_Price float, vCPU int, Memory varchar(20), Storage varchar(20), Instance_Family varchar(40), Region varchar(40), Provider varchar(20))"
mycursor.execute(query)
mydb.commit()
