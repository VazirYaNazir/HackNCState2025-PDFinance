from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from dotenv import load_dotenv
import os
import shutil
import DB

# Load environment variables
load_dotenv()

# ---- Set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OpenAI API key. Set it as an environment variable.")

openai.api_key = api_key  # Correct initialization

# Set up Chroma DB
CHROMA_PATH = "chroma"
DATA_PATH = "data/books"

# Main function
def generatevectors():
    generate_data_store()

# Create documents using load documents
def generate_data_store():
    loader = []
    for i in range(1, DB.get_last_id() + 1):
        text = DB.retrieve_pdf(i)
        loader.append(text)

    # Convert to list of Document objects
    documents = [Document("".join(text)) for text in loader]
    chunks = split_text(documents)
    save_to_chroma(chunks)

# Split text using RecursiveCharacterTextSplitter
def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

# Save text chunks to Chroma vector store
def save_to_chroma(chunks: list[Document]):
    if not chunks:
        raise ValueError("Cannot save empty chunks to Chroma DB.")

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
