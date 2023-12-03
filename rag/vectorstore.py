import os
import boto3
import requests
import nest_asyncio
import pinecone
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.document_loaders import WebBaseLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings import BedrockEmbeddings

load_dotenv()


def get_bedrock_client():
    return boto3.client(
        "bedrock-runtime",
        region_name="eu-central-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def get_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [p.find("a")["href"] for p in soup.find_all("p", class_="job-title pb-2 m-0")]


def load_docs():
    # nest_asyncio.apply()
    # loader = WebBaseLoader(urls)
    loader = DirectoryLoader('data/', glob='*.txt')
    # loader.requests_per_second = 3
    return loader.load()


def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(docs)


def create_vectorstore(docs, embeddings):
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENV"),
    )
    index_name = "mock-jobs"
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
    Pinecone.from_documents(docs, embeddings, index_name=index_name)


def main():
    bedrock_client = get_bedrock_client()
    embeddings = BedrockEmbeddings(client=bedrock_client)
    docs = load_docs()
    print(docs[0])
    create_vectorstore(docs, embeddings)


if __name__ == "__main__":
    main()
