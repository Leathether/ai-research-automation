
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity
from langchain_pinecone import PineconeVectorStore
import pinecone as pc
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from openai import OpenAI
import numpy as np
import tiktoken
import os
from groq import Groq
from dotenv import load_dotenv
import numpy as np

load_dotenv()




embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


pinecone_api_key = os.environ.get("PINECONE_API_KEY")

groq_api_key = os.environ.get("GROQ_API_KEY")





index_name = "ai-research-agent"

namespace = "master"

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)



import ast


def process_directory(directory_path):
    data = []
    for root, _, files in os.walk(directory_path):
        for file in files:

            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            loader = open(f"./src/python/embeddings/research/{file}", "r")
            loader = loader.read()
            loader = ast.literal_eval(loader)
            data.append({"File": file, "Data": loader['text']})

    return data


directory_path = "./src/python/embeddings/research"
documents = process_directory(directory_path)



# Prepare the text for embedding
document_data = []
for document in documents:

    document_source = document['File']
    document_content = document['Data']

    file_name = document_source

    doc = Document(
        page_content = f"\n{document_source}\n\n\n\n{document_content}\n",
        metadata = {
            "file_name": file_name,
        }
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






