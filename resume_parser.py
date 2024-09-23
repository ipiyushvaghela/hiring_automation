import http.client
import json
import base64
import os
from resume_db import store_resume

def pdf_to_base64(pdf_path):
    # Open the PDF file in binary mode
    with open(pdf_path, "rb") as pdf_file:
        # Read the content of the file
        pdf_content = pdf_file.read()
        # Encode the content to base64
        base64_string = base64.b64encode(pdf_content)
        # Convert the base64 bytes to a string
        base64_string = base64_string.decode('utf-8')
        return base64_string

# def extract_text(file_name,base64_string):

#     try:
#         conn = http.client.HTTPSConnection("resume-parsing-api2.p.rapidapi.com")
#         payload_dict = {
#             "extractionDetails": {
#                 "name": "Resume - Extraction",
#                 "language": "English",
#                 "fields": [
#                     {
#                         "key": "personal_info",
#                         "description": "personal information of the person",
#                         "type": "object",
#                         "properties": [
#                             {
#                                 "key": "name",
#                                 "description": "name of the person",
#                                 "example": "Alex Smith",
#                                 "type": "string"
#                             },
#                             {
#                                 "key": "email",
#                                 "description": "email of the person",
#                                 "example": "alex.smith@gmail.com",
#                                 "type": "string"
#                             },
#                             {
#                                 "key": "phone",
#                                 "description": "phone of the person",
#                                 "example": "0712 123 123",
#                                 "type": "string"
#                             },
#                             {
#                                 "key": "address",
#                                 "description": "address of the person",
#                                 "example": "Bucharest, Romania",
#                                 "type": "string"
#                             }
#                         ]
#                     },
#                     {
#                         "key": "work_experience",
#                         "description": "work experience of the person",
#                         "type": "array",
#                         "items": {
#                             "type": "object",
#                             "properties": [
#                                 {
#                                     "key": "title",
#                                     "description": "title of the job",
#                                     "example": "Software Engineer",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "start_date",
#                                     "description": "start date of the job",
#                                     "example": "2022",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "end_date",
#                                     "description": "end date of the job",
#                                     "example": "2023",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "company",
#                                     "description": "company of the job",
#                                     "example": "Fastapp Development",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "location",
#                                     "description": "location of the job",
#                                     "example": "Bucharest, Romania",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "description",
#                                     "description": "description of the job",
#                                     "example": "Designing and implementing server-side logic to ensure high performance and responsiveness of applications.",
#                                     "type": "string"
#                                 }
#                             ]
#                         }
#                     },
#                     {
#                         "key": "education",
#                         "description": "school education of the person",
#                         "type": "array",
#                         "items": {
#                             "type": "object",
#                             "properties": [
#                                 {
#                                     "key": "title",
#                                     "description": "title of the education",
#                                     "example": "Master of Science in Computer Science",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "start_date",
#                                     "description": "start date of the education",
#                                     "example": "2022",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "end_date",
#                                     "description": "end date of the education",
#                                     "example": "2023",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "institute",
#                                     "description": "institute of the education",
#                                     "example": "Bucharest Academy of Economic Studies",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "location",
#                                     "description": "location of the education",
#                                     "example": "Bucharest, Romania",
#                                     "type": "string"
#                                 },
#                                 {
#                                     "key": "description",
#                                     "description": "description of the education",
#                                     "example": "Advanced academic degree focusing on developing a deep understanding of theoretical foundations and practical applications of computer technology.",
#                                     "type": "string"
#                                 }
#                             ]
#                         }
#                     },
#                     {
#                         "key": "languages",
#                         "description": "languages spoken by the person",
#                         "type": "array",
#                         "items": {
#                             "type": "string",
#                             "example": "English"
#                         }
#                     },
#                     {
#                         "key": "skills",
#                         "description": "skills of the person",
#                         "type": "array",
#                         "items": {
#                             "type": "string",
#                             "example": "NodeJS"
#                         }
#                     },
#                     {
#                         "key": "certificates",
#                         "description": "certificates of the person",
#                         "type": "array",
#                         "items": {
#                             "type": "string",
#                             "example": "AWS Certified Developer - Associate"
#                         }
#                     }
#                 ]
#             },
#             "file": base64_string
#         }

#         # Convert the dictionary to a JSON string
#         payload_json = json.dumps(payload_dict)

#         # print(payload_json)
#         headers = {
#             'x-rapidapi-key': "6e2b605f73msh1686a021a37cc83p1e1e7djsn037f4052cc94",
#             'x-rapidapi-host': "resume-parsing-api2.p.rapidapi.com",
#             'Content-Type': "application/json"
#         }

#         conn.request("POST", "/processDocument", payload_json, headers)

#         res = conn.getresponse()
#         data = res.read()

#         print(data.decode("utf-8"))

#         with open(file_name, 'w') as f:
#             f.write(data.decode("utf-8"))
            
#         status = "200"
#         # get_details(data.decode("utf-8"))
#         return status
        
#     except Exception as e:
#         status = "400"
#         print(e)
#         return status



def extract_text(base64_string,job_id):

    try:
        conn = http.client.HTTPSConnection("resume-parsing-api2.p.rapidapi.com")
        payload_dict = {
            "extractionDetails": {
                "name": "Resume - Extraction",
                "language": "English",
                "fields": [
                    {
                        "key": "personal_info",
                        "description": "personal information of the person",
                        "type": "object",
                        "properties": [
                            {
                                "key": "name",
                                "description": "name of the person",
                                "example": "Alex Smith",
                                "type": "string"
                            },
                            {
                                "key": "email",
                                "description": "email of the person",
                                "example": "alex.smith@gmail.com",
                                "type": "string"
                            },
                            {
                                "key": "phone",
                                "description": "phone of the person",
                                "example": "0712 123 123",
                                "type": "string"
                            },
                            {
                                "key": "address",
                                "description": "address of the person",
                                "example": "Bucharest, Romania",
                                "type": "string"
                            }
                        ]
                    },
                    {
                        "key": "work_experience",
                        "description": "work experience of the person",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": [
                                {
                                    "key": "title",
                                    "description": "title of the job",
                                    "example": "Software Engineer",
                                    "type": "string"
                                },
                                {
                                    "key": "start_date",
                                    "description": "start date of the job",
                                    "example": "2022",
                                    "type": "string"
                                },
                                {
                                    "key": "end_date",
                                    "description": "end date of the job",
                                    "example": "2023",
                                    "type": "string"
                                },
                                {
                                    "key": "company",
                                    "description": "company of the job",
                                    "example": "Fastapp Development",
                                    "type": "string"
                                },
                                {
                                    "key": "location",
                                    "description": "location of the job",
                                    "example": "Bucharest, Romania",
                                    "type": "string"
                                },
                                {
                                    "key": "description",
                                    "description": "description of the job",
                                    "example": "Designing and implementing server-side logic to ensure high performance and responsiveness of applications.",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "key": "education",
                        "description": "school education of the person",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": [
                                {
                                    "key": "title",
                                    "description": "title of the education",
                                    "example": "Master of Science in Computer Science",
                                    "type": "string"
                                },
                                {
                                    "key": "start_date",
                                    "description": "start date of the education",
                                    "example": "2022",
                                    "type": "string"
                                },
                                {
                                    "key": "end_date",
                                    "description": "end date of the education",
                                    "example": "2023",
                                    "type": "string"
                                },
                                {
                                    "key": "institute",
                                    "description": "institute of the education",
                                    "example": "Bucharest Academy of Economic Studies",
                                    "type": "string"
                                },
                                {
                                    "key": "location",
                                    "description": "location of the education",
                                    "example": "Bucharest, Romania",
                                    "type": "string"
                                },
                                {
                                    "key": "description",
                                    "description": "description of the education",
                                    "example": "Advanced academic degree focusing on developing a deep understanding of theoretical foundations and practical applications of computer technology.",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    {
                        "key": "languages",
                        "description": "languages spoken by the person",
                        "type": "array",
                        "items": {
                            "type": "string",
                            "example": "English"
                        }
                    },
                    {
                        "key": "skills",
                        "description": "skills of the person",
                        "type": "array",
                        "items": {
                            "type": "string",
                            "example": "NodeJS"
                        }
                    },
                    {
                        "key": "certificates",
                        "description": "certificates of the person",
                        "type": "array",
                        "items": {
                            "type": "string",
                            "example": "AWS Certified Developer - Associate"
                        }
                    }
                ]
            },
            "file": base64_string
        }

        # Convert the dictionary to a JSON string
        payload_json = json.dumps(payload_dict)

        # print(payload_json)
        headers = {
            'x-rapidapi-key': "6e2b605f73msh1686a021a37cc83p1e1e7djsn037f4052cc94",
            'x-rapidapi-host': "resume-parsing-api2.p.rapidapi.com",
            'Content-Type': "application/json"
        }

        conn.request("POST", "/processDocument", payload_json, headers)
        try:
            res = conn.getresponse()
            data = res.read()
            parsed_data = json.loads(data.decode("utf-8"))
            store_resume(parsed_data,job_id)
        except Exception as e:
            print(e)

        status = "200"
        return status
        
    except Exception as e:
        status = "400"
        print(e)
        return status
    
    
def get_details(file_name):
   with open(file_name, 'r') as file:
    data = json.load(file)
    return data
    
    
    
# pdf_path = r"resumes\VISHESH.pdf"
# base64_string = pdf_to_base64(pdf_path)
# output_file_name  = pdf_path.split("\\")[1] + ".json"
# output_folder_name = "resume_parser"
# file_name = os.path.join(output_folder_name, output_file_name)
# extract_text(file_name)