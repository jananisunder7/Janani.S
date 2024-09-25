import sqlite3

#connect to sqlite
connection=sqlite3.connect("student.db")

#create a cursor to insert,create,retrieve table
cursor=connection.cursor()

#create table
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)

#insert some records

cursor.execute('''Insert Into STUDENT values('Janani','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Dhanya','Data Science','A',100)''')
cursor.execute('''Insert Into STUDENT values('mythili','Data Science','B',86)''')
cursor.execute('''Insert Into STUDENT values('Vinoth','CS','B',50)''')
cursor.execute('''Insert Into STUDENT values('Dinesh','CS','A',35)''')

## Disspaly ALl the records

print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()