import math
import os
import DB
import vector_functions as vf
from dotenv import load_dotenv
from src.DB import retrieve_pdf
import string
load_dotenv()

# Global variables
question = "Hello my name is Jordan"
limit = 5  # Set a limit value here for testing (can be set dynamically in your actual GUI)
#
# def api_(question: str, limit: int) -> str:
#     """
#     Given a query question, find the most relevant PDF pages based on vector similarity.
#     """
#     # Create vector for the question
#     question_vector = vf.create_vector([question])
#
#     # List to store vectors for all retrieved PDFs
#     vector_objects = []
#
#     # Retrieve and process PDFs
#     for id_ in range(1, DB.get_last_id() + 1):
#         retrieved_pages = DB.retrieve_pdf(id_)
#         vector_object = vf.create_vector(retrieved_pages)
#         vector_objects.append((id_, vector_object, retrieved_pages))
#
#     # Compute vector angles between the question and each PDF
#     angle_results = []
#     for id_, vector, pages in vector_objects:
#         angle = vf.calculate_vector_angle(question_vector, vector)
#         angle_results.append((angle, id_, pages))
#
#     # Sort PDFs by the smallest angle (most similar)
#     angle_results.sort(key=lambda x: x[0])
#
#     # Select the top N (defined by `limit`)
#     closest_pdfs = angle_results[:limit]
#
#     # Prepare final output pages
#     output_pages = []
#     for _, id_, pages in closest_pdfs:
#         for page in pages:
#             page_create_vector([page])
#             page_angle = vf.calculate_vector_angle(question_vector, page_vector)
#             output_pages.append((page_angle, page))
#
#     # Sort pages by their angle to the query
#     output_pages.sort(key=lambda x: x[0])
#
#     # Get the most relevant pages from the sorted list
#     top = [page for _, page in output_pages[:limit]]
#     return top
#
# question = "Hello my name is Jordan"
# limit = 5
# print(api_(question, limit))



# load_dotenv()
#
list_of_raw_pdfs = []

question = ""
def set_raw_pdfs():
    for x in range(1, DB.get_last_id() + 1):
        a = remove_punctuation(DB.retrieve_pdf(x))
        list_of_raw_pdfs.append(a)


def remove_punctuation(data):
    if isinstance(data, str):
        return ''.join(char for char in data if char not in string.punctuation)

    # If data is a list, recursively remove punctuation from each item.
    elif isinstance(data, list):
        return [remove_punctuation(item) for item in data]

    # If data is a dictionary, recursively process both keys and values.
    elif isinstance(data, dict):
        return {remove_punctuation(key): remove_punctuation(value) for key, value in data.items()}

    # For other data types, return as-is.
    else:
        return data
set_raw_pdfs()

dict_store = []
for x in list_of_raw_pdfs:
    di = count_words_and_transform_dict(x)
    dict_store.append(di)

vectors_list = []
for x in dict_store:
    vectors_ = create_vector(x)
    vectors_list.append(vectors_)

question = ["Given the rapid advancements in machine learning and deep learning, particularly in object detection, how can we optimize models such as YOLO to accurately identify items in diverse real-world environments, such as recycling bins, where the quality of images may vary due to lighting conditions, occlusion, and varying object types? Moreover, considering the importance of reducing waste and promoting sustainability, how can we integrate these models into a larger system that not only detects objects but also provides actionable, context-specific feedback on how to dispose of or reuse the identified items, while addressing challenges related to user experience, privacy, and data management?"]


question_dict = (count_words_and_transform_dict(remove_punctuation(question)))
print(question_dict)
question_vector = create_vector(question_dict)


angles_list = []
for x in vectors_list:
    angle = calculate_vector_angle(x, question_vector)
    angles_list.append(angle)

def update_gui_() -> str:

    return ""



#
# def api_(question: str, limit: int) -> str:
#     """
#     Gets ids, stored itter.
#     Gets all pdf ids
#     """
#
#     string_object_list: list[vector_functions.StringFunctions] = [
#         vector_functions.StringFunctions(pages=DB.retrieve_pdf(id_), vector=[], id=id_)
#         for id_ in range(1, DB.get_last_id())
#         if DB.retrieve_pdf(id_)
#     ]
#
#     list_of_numerics = [obj.create_vector() for obj in string_object_list]
#
#     question_obj = vector_functions.StringFunctions(pages=[question], vector=[], id=-1)
#
#     string_object_list: list[vector_functions.StringFunctions] = []
#     for id_ in range(1, DB.get_last_id()):
#         retrieved_pages = DB.retrieve_pdf(id_)
#         string_object_list.append(vector_functions.StringFunctions(pages=retrieved_pages,vector=[], id=id_))
#
#
#     q_ = question_obj.create_vector()5
#     q = vector_functions.VectorFunctions(vector=[q_])
#
#     list_of_vector_obj: list[vector_functions.VectorFunctions]= []
#     for obj in list_of_numerics:
#         list_of_vector_obj.append(vector_functions.VectorFunctions(vector=obj))
#
#     list_of_pdf_angles = []
#     for obj in list_of_vector_obj:
#         list_of_pdf_angles.append(obj.calculate_vector_angle(obj.vector, q.vector))
#
#     print(list_of_pdf_angles)
#
#     # [[angle, id], [angle,id]]
#     smallest_n = []
#     for index, angle in enumerate(list_of_pdf_angles):
#         smallest_n.append([angle,index+1])
#     smallest_n.sort(key=lambda x: x[0])
#     smallest_n = smallest_n[:limit]
#
#     output_pages = []
#     for pair in smallest_n:
#         list_of_page_angles = []
#         pages = retrieve_pdf(pair[1])
#         for page in pages:
#             pageObj = vector_functions.StringFunctions(pages=[page], vector = [], id = 0)
#             pageObj.vector = pageObj.create_vector()
#             angle = pageObj.calculate_vector_angle(q.vector, pageObj.vector)
#             list_of_page_angles.append([angle, page])
#
#         list_of_page_angles.sort(key = lambda x : x[0])
#         trimmed_list_of_pages = list_of_pdf_angles[:limit]
#
#         for page in trimmed_list_of_pages:
#             output_pages.append(page[1])

#
    #
    #
    # # Ensure API key is set
    # api_key = os.getenv("OPEN_AI_API_KEY")
    # if not api_key:
    #     raise ValueError("Missing OpenAI API key. Set it as an environment variable.")
    #
    # client = OpenAI(api_key=api_key)
    #
    # # Efficiently join context strings
    # context_string = "".join(output_pages)
    #
    # # Construct prompt
    # prompt_string = f"{question}\nAnswer the question above with the following context:\n{context_string}"
    #
    # # Make API call
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful financial assistant."},
    #         {"role": "user", "content": prompt_string},
    #     ],
    #     stream=False
    # )
    # #delete once running
    # print(prompt_string)
    # return response.choices[0].message.content