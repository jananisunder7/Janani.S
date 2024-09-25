from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os 
import sqlite3

import google.generativeai as genai

#configuring api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load google gemini model and provide sql query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

#to retrieve query from sql database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    column_names = [description[0] for description in cur.description ]
    conn.close()
    return column_names,rows

#defining prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name cust and has the following columns - Name,customer_id , 
    Salary,job_position,City \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM customer ;
    \nExample 2 - Tell me all the names containing the City  Berlin?, 
    the SQL command will be something like this SELECT * FROM customer
    where City="Berlin"; 
    also the sql code should not have ``` in beginning or end and sql word in output

"""
]

#streamlit app


st.set_page_config(page_title="Text to SQL using gemini")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input your questions for query",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    st.subheader(" SQL Query")
    st.code(response,language='sql')

    try:
        db_name='Car_Database.db'
        conn=sqlite3.connect(db_name)
        cursor=conn.cursor()

        cursor.execute("PRAGMA table_info(customer)")
        column_info=cursor.fetchall()
        column_names,data=read_sql_query(response,db_name)
        st.subheader("Result: ")

        if len(data)>0:
            data_with_columns = [dict(zip(column_names,row)) for row in data]
            st.table(data_with_columns)
        else:
           st.write("No result found")
        cursor.close()
        conn.close()

    except Exception as e:
        pass