from dotenv import load_dotenv
import streamlit as st
from langchain.llms import OpenAI

load_dotenv()
llm = OpenAI()
result = llm.predict('내가 좋아하는 동물은 ')
print(result)