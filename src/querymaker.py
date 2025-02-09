import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate



# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key
# Change environment variable name from "OPENAI_API_KEY" to the name given in
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

def main(question : str, limit):
    vector_function = OpenAIEmbeddings()
    vector = vector_function.embed()

    vector_database = Chroma(persist_directory=CHROMA_PATH, embedding_function=vector_function)
    results = db.similarity_search_with_relevance_scores(question, k=limit)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return


