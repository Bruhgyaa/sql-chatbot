import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from snowflake.sqlalchemy import URL
import sqlalchemy as sa
import pandas as pd

OPENAI_API_KEY = "OPENAI_API_KEY"
SF_USER = 'SF_USER'
SF_PASSWORD = 'SF_PASSWORD'
SF_ACCOUNT = 'SF_ACCOUNT'
SF_WAREHOUSE = 'SF_WAREHOUSE'
SF_DATABASE = 'SF_DATABASE'
SF_SCHEMA = 'SF_SCHEMA'
SF_ROLE = 'SF_ROLE'

conn_url = URL(
    account=SF_ACCOUNT,
    user=SF_USER,
    password=SF_PASSWORD,
    database=SF_DATABASE,
    schema=SF_SCHEMA,
    role=SF_ROLE,
    warehouse=SF_WAREHOUSE
)

engine = sa.create_engine(conn_url)

def execute_query(query):
    with engine.connect() as conn:
        result = conn.execute(sa.text(query))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

def query_page():
    st.header("SQL Query")
    user_input = st.text_area("Enter your question in natural language")
    if st.button("Submit"):
        response = conversation.predict(input=user_input)
        st.write(f"SQL Query: {response}")

def answer_page():
    st.header("Answer")
    user_input = st.text_area("Enter your question in natural language")
    if st.button("Submit"):
        response = conversation.predict(input=user_input)
        try:
            result = execute_query(response)
            st.write(result)
        except Exception as e:
            st.write(f"Error executing query: {e}")

def visualization_page():
    st.header("Data Visualization")
    user_input = st.text_area("Enter your question in natural language")
    if st.button("Submit"):
        response = conversation.predict(input=user_input)
        try:
            result = execute_query(response)
            st.write(result)
            # Add data visualization code here
        except Exception as e:
            st.write(f"Error executing query: {e}")

st.title("AI SQL Assistant")

pages = {
    "SQL Query": query_page,
    "Answer": answer_page,
    "Data Visualization": visualization_page,
}

selection = st.sidebar.selectbox("Go to", list(pages.keys()))

if selection == "SQL Query":
    query_page()
elif selection == "Answer":
    answer_page()
else:
    visualization_page()
    inputs() 