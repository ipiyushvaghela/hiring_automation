from openai import AzureOpenAI
import os
import requests, json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version='2024-03-01-preview',#'2023-07-01 preview',
    azure_endpoint = "https://dxfactor-openai.openai.azure.com/")

access_token = 'tfp_7DQbEn2mUGQydYjTZ4oR2EsSDwtDpa2843RG63JPv9Ro_3peHGepWqkxhGe'


def get_completion(history):
    completion = client.chat.completions.create(model='DXF-POC-GPT35-16k',
    messages=history,
    temperature=0.7,
    timeout=10)
    return completion.choices[0].message.content
  
  
def generate_questions(designation):
    messages = [{"role":"system","content":"""Your role is to generator exam questions for candidate hiring. Your role is to generate questions for given job role <JOB_ROLE>. Generate 5 questions. Difficulty level should be decided based on the job role. 
                 Your response should only be the list of questions and nothing else.""".replace("<JOB_ROLE>",designation)}]
    response = get_completion(messages)
    return response
  
  
def format_questions(response):
    
    form_data = { 
    "title": "Job Application Form",
    "fields": [
        {
            "title": "Name",
            "type": "short_text"
        },
        {
            "title": "Email",
            "type": "email"
        },
    ] } 

    # print(response)
    questions = list(response.split("\n"))
    form_data["fields"].extend([{"title":q,"type":"short_text"} for q in questions])
  
    return form_data
  
  
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
  
  
def send_email(form_link, recipient_email):
    sender_email = "pankti_15@outlook.com"
    sender_password = "Pankti@@99"

    subject = "DXFactor - Proctored Test"
    body = f"Hi,\n\nPlease take your test:\n{form_link}\n This will help us understand more about your skills.\n\nThank you!"

    
    print("Sending email...:",sender_email)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()  # Start TLS for security
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
        
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
  
desigantion = "Data Scientist Intern"
recipient_email = ""
response = generate_questions(desigantion)
form_data = format_questions(response)
form_link = generate_link(form_data)
# send_email(form_link, recipient_email)
print(form_link)