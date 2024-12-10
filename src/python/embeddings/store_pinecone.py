from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, WebBaseLoader, YoutubeLoader, DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from openai import OpenAI
import numpy as np
import tiktoken
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()



pinecone_api_key = os.environ.get("PINECONE_API_KEY")

groq_api_key = os.environ.get("GROQ_API_KEY")


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def process_directory(directory_path):
    data = []
    f_data = open(directory_path[0], "r")
    f_urls = open(directory_path[1], "r")
    f_index = open("./src/python/embeddings/embedded_idx.txt", "r")
    content = f_data.read()
    urls = f_urls.read()
    idx = int(f_index.read())
    while idx < len(urls):
        data.append(f"{urls[idx]}: {[idx]}")
        idx += 1
    f_data.close()
    f_urls.close()
    f_index.close()
    f_index = open("./src/python/embeddings/embedded_idx.txt", "w")
    f_index.write(str(idx))
    f_index.close()


    return data

directory_path = ["./src/python/embeddings/research.csv", "./src/python/embeddings/sites.csv"]
documents = process_directory(directory_path)





# Make sure to create a Pinecone index with 384 dimensions

index_name = "ai-research-automation"

namespace = "main"

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)







# Prepare the text for embedding
document_data = []
for document in documents:

    document_source = document['Data'][0].metadata['source']
    document_content = document['Data'][0].page_content

    file_name = document_source.split("/")[-1]
    folder_names = document_source.split("/")[2:-1]

    doc = Document(
        page_content = f"\n{document_source}\n\n\n\n{document_content}\n",
    )
    document_data.append(doc)
     



# Insert documents into Pinecone
vectorstore_from_documents = PineconeVectorStore.from_documents(
    document_data,
    embeddings,
    index_name=index_name,
    namespace=namespace
)




# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Connect to your Pinecone index
pinecone_index = pc.Index(index_name)

