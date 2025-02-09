from PyPDF2.generic import NullObject
from openai import OpenAI
import DB
import vectorfunctions as vf

def find_page(question, filter):
    # Filter is an integer which serves as a limit for the amount of documents searched
    # find the best PDFs
    pdf_vectors = []

    for i in range(1,DB.get_last_id()+1):
        pages = DB.retrieve_pdf(i)
        pdf_vectors.append(vf.make_pdf_vector_with_question(pages,question))

    angles = []
    for pdf_vector in pdf_vectors:
        question_vector = pdf_vector.pop()
        angles.append(vf.angle_between_vectors(pdf_vector, question_vector))

    smallest_n = []
    for index, angle in enumerate(angles):
        smallest_n.append([angle,index+1])
    smallest_n.sort(key=lambda x: x[0])
    smallest_n = smallest_n[:filter]

    # find the best page in each of our best pdfs
    pageStrings = []
    for pdf_id in smallest_n[1]:
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
            pdf = vf.retrieve_pdf(id)
            pageStrings.append(pdf[smallest_j[1]])

    return makePromptToDeepSeek(question, pageStrings)

def makePromptToDeepSeek(question, pageStrings):
    client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

    contextstring = ""
    for i in pageStrings:
        contextstring += i

    promptString = f"{question}\nAnswer the question above with the following context:\n {contextstring}"

    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful financial assistant"},
        {"role": "user", "content": promptString},
    ],
    stream=False
    )

    return response.choices[0].message.content



