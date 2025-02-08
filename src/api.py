from openai import OpenAI
import DB
import vectorfunctions
from src.vectorfunctions import make_pdf_vector_with_question, angle_between_vectors

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

def find_page(question):
    pdf_vectors = []

    for i in range(1,DB.get_last_id()+1):
        pages = DB.retrieve_pdf(i)
        pdf_vectors.append(make_pdf_vector_with_question(pages))

    minimum_angle = 
    for pdf_vector in pdf_vectors:
        question_vector = pdf_vector.pop()
        if minimum_angle <= angle_between_vectors(pdf_vector, question_vector):
            hi = 1

