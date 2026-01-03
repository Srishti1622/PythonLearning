from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


model=ChatGroq(model='')

user_input=input("enter user question: ")

prompt=ChatPromptTemplate([
    ('system',"You are a expert in content writing. You will get user query based on that you need to provide the content."),
    ('user',user_input)
])

chain=prompt|model

if user_input:
    res=chain.invoke(user_input)
    print(res)