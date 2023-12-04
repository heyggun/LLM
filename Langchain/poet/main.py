from dotenv import load_dotenv
load_dotenv()

# from langchain.llms import OpenAI
# llm = OpenAI()
# result = llm.predict('내가 좋아하는 동물은 ')
# print(result)

from langchain.chat_models import ChatOpenAI
chat_model = ChatOpenAI()
content = '코딩'
result = chat_model.predict(content + '에 대한 시를 써줘')
print(result)

