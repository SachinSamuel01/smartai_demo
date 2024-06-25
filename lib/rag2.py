from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
import time
import os
from langchain.text_splitter import CharacterTextSplitter



llm = Ollama(model="mistral")  
embeddings = OllamaEmbeddings(model="mistral")
parser= StrOutputParser()


def create_vec_db(prompt, files):

    print(1)
    p=prompt

    print(2)

    all_doc=[]
    for file in files:
        loader = PyPDFLoader(file)
        doc = loader.load_and_split()
        all_doc.extend(doc)

    print(3)
    
    persist_directory = r'./db/chroma1'
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    # Assuming 'all_splits' is your texts and 'embeddings' is your embedding function/model
    vector_store = Chroma.from_documents(all_doc, embedding=embeddings)

    # Initialize the retriever with the vector store
    retriever = vector_store.as_retriever()
    return retriever, p




def get_response(prompt_for_llm,retriever,  query):

    
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)

    

    return qa_chain.run(query) #, context=prompt_for_llm)