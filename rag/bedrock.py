import os
import sys
import boto3
import pinecone
from dotenv import load_dotenv
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.llms import Bedrock

load_dotenv()


def get_bedrock_client():
    return boto3.client(
        "bedrock-runtime",
        region_name="eu-central-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def load_vectorstore(index_name, embeddings):
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENV"),
    )
    return Pinecone.from_existing_index(index_name, embeddings)


def build_chain():
    bedrock_client = get_bedrock_client()
    embeddings = BedrockEmbeddings(client=bedrock_client)
    llm = Bedrock(
        client=bedrock_client,
        model_id="amazon.titan-text-express-v1",
        model_kwargs={"temperature": 0}
    )
    vectorstore = load_vectorstore("my-index", embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt_template = """
    Assistant: OK, got it, I'll be a talkative truthful AI assistant.

    Human: Here are a few documents in <documents> tags:
    <documents>
    {context}
    </documents>
    Based on the above documents, provide a detailed answer for, {question} 
    Answer "don't know" if not present in the document. 

    Assistant:

    """

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    condense_qa_template = """

    Given the following conversation and a follow up question, rephrase
    the follow up question to be a standalone question.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:

    """

    standalone_question_prompt = PromptTemplate.from_template(
        condense_qa_template)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        condense_question_prompt=standalone_question_prompt,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    return qa


def run_chain(chain, prompt: str, history=[]):
    return chain({"question": prompt, "chat_history": history})


def main():
    history = []
    qa = build_chain()
    print("Hello! How can I help you?")
    print("Ask a question, start a New search: or CTRL-D to exit.")
    print(">", end=" ", flush=True)
    for query in sys.stdin:
        if (query.strip().lower().startswith("new search:")):
            query = query.strip().lower().replace("new search:", "")
            history = []
        elif (len(history) == 5):
            history.pop(0)
        result = run_chain(qa, query, history)
        history.append((query, result["answer"]))
        print(result["answer"])
        if "source_documents" in result:
            print("Sources: ")
            for d in result["source_documents"]:
                print(d.metadata["source"])
        print("Ask a question, start a New search: or CTRL-D to exit.")
        print(">", end=" ", flush=True)
    print("Bye")


if __name__ == "__main__":
    main()
