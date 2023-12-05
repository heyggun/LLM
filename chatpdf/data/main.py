__import__('pysqlite3')
import sys
sys.modules['sqlite3']=sys.modules.pop('pysqlite3')

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import chromadb
import streamlit as st
import tempfile
import os

# title 
st.title('chatPDF')
st.write('---')

# file upload
uploaded_file = st.file_uploader('Choose a file')
st.write('----')

def pdf_to_document(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    return pages

# successed upload 
if uploaded_file is not None:
    pages = pdf_to_document(uploaded_file)
    pass


    #Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
        length_function = len,
        is_separator_regex = False
    )

    texts = text_splitter.split_documents(pages)

    #Embedding
    embeddings_model = OpenAIEmbeddings()

    #load it into the vector store.
    db = Chroma.from_documents(texts, OpenAIEmbeddings())

    #question
    st.header('PDF에게 질문해보세요')
    question = st.text_input('질문을 입력하세요')

    if st.button('질문하기'):
        with st.spinner('Wait for it...'):
            llm = ChatOpenAI(temperature=0) #temperature : 무작위성, 0이면 일관성 있음
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever())
            result = qa_chain({"query":question})
            st.write(result['result'])
