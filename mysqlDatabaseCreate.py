import mysql.connector
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = '1234') #insert your own host, user and password
mycursor=mydb.cursor()
query="CREATE database cpa"
mycursor.execute(query)
query="use cpa"
mycursor.execute(query)
mydb.commit()

query="create table awsPrice(Instance_name varchar(20), Instance_Price float, vCPU int, Memory int, Storage varchar(20), Instance_Family varchar(40))"
mycursor.execute(query)
query="create table azurePrice(Instance_name varchar(40), Linux_Price float, Windows_Price float, vCPU int, Memory int, Storage int, Instance_Family varchar(40))"
mycursor.execute(query)
mydb.commit()
