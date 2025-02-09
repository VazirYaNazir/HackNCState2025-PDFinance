from PyPDF2.generic import NullObject
from openai import OpenAI
import DB
import os
import vectorfunctions as vf
from dotenv import load_dotenv

load_dotenv()

def find_page(question, filter):
    # Filter is an integer which serves as a limit for the amount of documents searched
    # find the best PDFs
    pdf_vectors = []

    for i in range(1,DB.get_last_id()+1):
        pages = DB.retrieve_pdf(i)
        #print(vf.make_pdf_vector_with_question(pages,question))
        pdf_vectors.append(vf.make_pdf_vector_with_question(pages,question))
        print(pdf_vectors)
        print(type(pdf_vectors))

    angles = []


    question_vector = pdf_vectors[-1]
    del pdf_vectors[-1]
    for pdf_vector in pdf_vectors:
        angles.append(vf.angle_between_vectors(question_vector, pdf_vector))
    print(angles)

    smallest_n = []
    for index, angle in enumerate(angles):
        smallest_n.append([angle,index+1])
    smallest_n.sort(key=lambda x: x[0])
    smallest_n = smallest_n[:filter]
    # [[angle, id], [angle,id]]
    print(smallest_n)

    # find the best page in each of our best pdfs
    page_strings = []
    for i in range(0, range(len(smallest_n))):
        pdf_pages = DB.retrieve_pdf(smallest_n[i][1])
        page_vectors = vf.make_page_vectors(PDFpages, question)

        page_angles = []
        #find best page vector in pdf by looping through pageVectors, adding the angle to pageAngles
        for vector in page_vectors:
            page_angles.append(vf.angle_between_vectors(vector, pageVectors[-1]))

        #for angle in page_angles:
        #




    """
    for pdf_id in range(1, len(smallest_n)):
        best_pdf_pages = DB.retrieve_pdf(pdf_id)
        page_vectors = vf.make_page_vectors(best_pdf_pages, question)
        question_vector = page_vectors.pop()
        page_angles = []
        for page_vector in page_vectors:
            page_angles.append(vf.angle_between_vectors(page_vector, question_vector))

        smallest_j = []
        for index, angle in enumerate(angles):
            smallest_j.append([angle, index + 1])
        smallest_j.sort(key=lambda x: x[0])
        smallest_j = smallest_j[:filter]

        for id in smallest_n[1]:
            pdf = DB.retrieve_pdf(id)
            page_strings.append(pdf[smallest_j[1]])

    return make_prompt_to_chat_gpt(question, page_strings)
    """

def make_prompt_to_chat_gpt(question, page_strings):
    client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"), base_url=os.getenv("OPEN_AI_URL"))

    context_string = ""
    for i in page_strings:
        context_string += i

    prompt_string = f"{question}\nAnswer the question above with the following context:\n {context_string}"

    response = client.chat.completions.create(
    model="chatgpt-4o-latest",
    messages=[
        {"role": "system", "content": "You are a helpful financial assistant"},
        {"role": "user", "content": prompt_string},
    ],
    stream=False
    )
    #delete once running
    print(prompt_string)
    return response.choices[0].message.content



