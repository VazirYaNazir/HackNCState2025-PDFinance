import math
from PyPDF2.generic import NullObject
from openai import OpenAI
import DB
import os
import vectorfunctions as vf
from dotenv import load_dotenv
from src.DB import retrieve_pdf

load_dotenv()

import vector_functions
import GUIR

question = ""
limit = GUIR.global_value

def api_(question: str, limit: int) -> str:
    """
    Gets ids, stored itter.
    Gets all pdf ids
    """
    question_obj = vector_functions.StringFunctions(pages= [question], vector=[], id=-1)

    string_object_list: list[vector_functions.StringFunctions] = []
    for id_ in range(1, DB.get_last_id()):
        retrieved_pages = DB.retrieve_pdf(id_)
        string_object_list.append(vector_functions.StringFunctions(pages=retrieved_pages,vector=[], id=id_))

    list_of_numerics = []
    for obj in string_object_list:
        list_of_numerics.append(obj.create_vector())

    q_ = question_obj.create_vector()
    _q = vector_functions.VectorFunctions(vector=[q_])

    list_of_vector_obj: list[vector_functions.VectorFunctions]= []
    for obj in list_of_numerics:
        list_of_vector_obj.append(vector_functions.VectorFunctions(vector=obj))

    list_of_pdf_angles = []
    for obj in list_of_vector_obj:
        list_of_pdf_angles.append(obj.calculate_vector_angle(obj.vector, _q.vector))

    print(list_of_pdf_angles)

    # [[angle, id], [angle,id]]
    smallest_n = []
    for index, angle in enumerate(list_of_pdf_angles):
        smallest_n.append([angle,index+1])
    smallest_n.sort(key=lambda x: x[0])
    smallest_n = smallest_n[:limit]

    output_pages = []
    for pair in smallest_n:
        list_of_page_angles = []
        pages = retrieve_pdf(pair[1])
        for page in pages:
            pageObj = vector_functions.StringFunctions(pages=[page], vector = [], id = 0)
            pageObj.vector = pageObj.create_vector()
            angle = vector_functions.VectorFunctions.calculate_vector_angle(pageObj, _q)
            list_of_page_angles.append([angle, page])

        list_of_page_angles.sort(key = lambda x : x[0])
        list_of_page_angles = list_of_pdf_angles[:limit]

        for page in range(limit):
            output_pages.append(page[1])



    # Ensure API key is set
    api_key = os.getenv("OPEN_AI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key. Set it as an environment variable.")

    client = OpenAI(api_key=api_key)

    # Efficiently join context strings
    context_string = "".join(output_pages)

    # Construct prompt
    prompt_string = f"{question}\nAnswer the question above with the following context:\n{context_string}"

    # Make API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt_string},
        ],
        stream=False
    )
    #delete once running
    print(prompt_string)
    return response.choices[0].message.content