import sqlite3

#connect to sqlite
connection=sqlite3.connect("cust.db")

#create a cursor to insert,create,retrieve table
cursor=connection.cursor()

#create table
table_info="""
create table customer(Name VARCHAR(25),
customer_id int PRIMARY KEY,
Salary int,
job_position VARCHAR(25),
City VARCHAR(25));
"""
cursor.execute(table_info)

#insert some records

cursor.execute('''INSERT INTO CUSTOMER VALUES('John',001,40000,'Sales person','Berlin')''')
cursor.execute('''Insert Into CUSTOMER values('Amir',002,50000,'Data Analyst','Texas')''')
cursor.execute('''Insert Into CUSTOMER values('Johnny',008,60000,'Full Stack','Berlin')''')
cursor.execute('''Insert Into CUSTOMER values('Rahim',010,35000,'Manager','Delhi')''')
cursor.execute('''Insert Into CUSTOMER values('Anbu',004,55000,'Data Scientist','kerala')''')

## Disspaly ALl the records

print("The inserted records are")
data=cursor.execute('''Select * from CUSTOMER''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()