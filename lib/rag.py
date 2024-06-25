from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
import time
import os
from langchain.text_splitter import CharacterTextSplitter

# pdf1=r'D:\projects\VS_code\project\RAG_with_Open_Source_LLM_and_LangChain\pdfs\1_Ramırez-Duque_.pdf'
# pdf2=r'D:\projects\VS_code\project\RAG_with_Open_Source_LLM_and_LangChain\pdfs\Asd_Cry_patterns.pdf'
# pdf3=r'D:\projects\VS_code\project\RAG_with_Open_Source_LLM_and_LangChain\pdfs\carpenter2020 (1).pdf'

# loader = PyPDFLoader(pdf2)
# pages = loader.load_and_split()

# tt=' '
# for page in pages:

#     tt=tt+page.page_content

# parser= StrOutputParser()


# llm = Ollama(model="mistral")  
# embeddings = OllamaEmbeddings(model="mistral")

# template= """
# Use the following pieces of context to answer the question at the end.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.
# Use three sentences maximum and keep the answer as concise as possible.

# Context: {context}

# Question: {question}
# """

# query="Tell me how to deal with autisim with machine learning and robotics give me a detail answer"


# prompt= ChatPromptTemplate.from_template(template)

# text_splitter= RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# all_splits = text_splitter.split_text(tt)

# db= Chroma.from_texts(texts=all_splits, embedding=embeddings)


# docs = db.similarity_search(query)

# # print(type(docs[0].page_content))

# docs=[x.page_content for x in docs ]

# if len(docs)>=3:
#     content=docs[-1] +' '+ docs[-2] +' '+ docs[-3]
    
# else:
#     docs= docs[-1::-1]
#     content=' '.join(docs)

# chain= prompt | llm | parser

# print("Calling Invoke ######################################################################")
# start = time.time()
# print(chain.invoke({
#     'context': content,
#     'question' : query
# }))

# print("End Time : " + str(time.time() - start))


#######################################################


llm = Ollama(model="mistral")  
embeddings = OllamaEmbeddings(model="mistral")
parser= StrOutputParser()


def create_vec_db(prompt, files):

    print(1)
    template= prompt + """
    Content: {content}

    Query: {query}
    """
    prompt_for_llm= ChatPromptTemplate.from_template(template)

    print(2)

    texts=' '
    for file in files:
        loader = PyPDFLoader(file)
        pages = loader.load_and_split()
        for page in pages:
            texts= page.page_content

    print(3)
    
#    text_splitter= RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1500, chunk_overlap=100)


    all_splits = text_splitter.split_text(texts)
    print(all_splits)
  #  db= Chroma.from_texts(persist_directory=r'../db/chroma1', texts=all_splits, embedding=embeddings)
    persist_directory = r'./db/chroma1'
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    # Assuming 'all_splits' is your texts and 'embeddings' is your embedding function/model
    db = Chroma.from_texts(persist_directory=persist_directory, texts=all_splits, embedding=embeddings)
    print(5)
    return db, prompt_for_llm




def get_response(prompt_for_llm,db,  query):

    
    docs = db.similarity_search(query)

    print(type(docs[0].page_content))

    docs=[x.page_content for x in docs ]

    if len(docs)>=3:
        content=docs[-1] +' '+ docs[-2] +' '+ docs[-3]
        
    else:
        
        content=' '.join(docs)
    
    print(content)

    chain= prompt_for_llm | llm | parser

    return chain.invoke({
        'content': content,
        'query': query 
    })
    
    