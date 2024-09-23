import requests
import json
import re
from generate_questions import format_questions
from resume_db import store_questions

access_token = 'tfp_7DQbEn2mUGQydYjTZ4oR2EsSDwtDpa2843RG63JPv9Ro_3peHGepWqkxhGe'

def get_form_questions(form_id, access_token):
    url = f"https://api.typeform.com/forms/{form_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        questions = {}
        fields = response.json().get("fields", [])
        for field in fields:
            questions[field["id"]] = field["title"]
        return questions
    else:
        print("Failed to retrieve form details.")
        return {}
def generate_link(form_data):
# Replace with your Typeform personal access token

    # Endpoint for creating a form
    url = "https://api.typeform.com/forms"

    # Headers with authorization token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Send a POST request to create the form
    response = requests.post(url, headers=headers, data=json.dumps(form_data))

    # Check if the form was created successfully
    if response.status_code == 201:
        form_url = response.json()["_links"]["display"]
        print(f"Form created successfully! Access it here: {form_url}")
    else:
        print(f"Failed to create form: {response.status_code}, {response.text}")
    return form_url


def extract_form_id(url):
    # Regular expression pattern to match the form ID
    pattern = r'to/([a-zA-Z0-9_]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def get_questionnaire_response(form_url,job_title,job_id):

    # Extract the form ID from the form URL
    form_id = extract_form_id(form_url)
    print(f"Form ID: {form_id}")

    url = f"https://api.typeform.com/forms/{form_id}/responses"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        responses = response.json()["items"]

        questions = get_form_questions(form_id, access_token)
        for response in responses:
            response_info = {'Questions': []} 
            for answer in response["answers"]:
                question_id = answer["field"]["id"]
                question_text = questions.get(question_id, "Unknown question")
                if question_text not in ["Email", "Phone", "Name"]:
                    response_info['Questions'].append(question_text + ": " + answer.get('text', ''))
                elif question_text == "Name":
                    response_info[question_text] = answer.get('text', '')
                elif question_text == "Email":
                    response_info[question_text] = answer.get('text', '')
                elif question_text == "Phone":
                    response_info[question_text] = answer.get('text', '')
                response_info["job_title"] = job_title
                response_info["job_id"] = job_id
                
                
                # print(response_info)
            store_questions(response_info)
    else:
        print(f"Failed to fetch responses: {response.status_code}, {response.text}")
 
 
# form_data = { 
#     "title": "Job Application Form",
#     "fields": [
#         {
#             "title": "Name",
#             "type": "short_text"
#          },
#         {
#             "title": "Email",
#             "type": "email"
#         },
#         {
#             "title": "Phone",
#             "type": "phone_number"
#         },
#         {
#             "title": "Resume",
#             "type": "file_upload"
#         }
#     ] }      

# form_data = create_questions()
# form_url = generate_link(form_data)
# print(form_url)
# form_url = "https://qz4atdkbo71.typeform.com/to/JrdCQB01"


# get_questionnaire_response(form_url)


