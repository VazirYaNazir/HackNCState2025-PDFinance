import argparse
import openai
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key
# Change environment variable name from "OPENAI_API_KEY" to the name given in
# your .env file.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OpenAI API key. Set it as an environment variable.")

openai.api_key = api_key

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}

"""


def askPrompt(question : str, limit):
    vector_function = OpenAIEmbeddings()
    vector_database = Chroma(persist_directory=CHROMA_PATH, embedding_function=vector_function)


    results = vector_database.similarity_search_with_relevance_scores(question, k=limit)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)

    client = OpenAI(api_key=openai.api_key)
    # Make API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    return response.choices[0].message.content

