
from openai import AzureOpenAI
import os
import ast

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version='2024-03-01-preview',#'2023-07-01 preview',
    azure_endpoint = "https://dxfactor-openai.openai.azure.com/")

def get_completion(history):
    completion = client.chat.completions.create(model='DXF-POC-GPT35-16k',
    messages=history,
    temperature=0.7,
    timeout=10)
    return completion.choices[0].message.content

def generate_questions(job_description, designation):
    messages = [{"role":"system","content":"""Your role is to generate questionnaire. For the given job description and designation, generate a list of questions that can be asked to the candidate to evaluate best fit for further interview process. 
    Questions Example:
    1. How many years of experience do you have in this field? #Specific to the Designation
    2. What is your notice period? #General
    3. What are your salary expectations? #General
    4. What is your current location? #General
    5. What is your current job title? #General
    6. What is your current salary? #General
    7. Do you have experience with <Specific Technology>? #Specific to the Job Description
    These are just examples, you can generate more questions based on the job description and designation provided. Your response should be in the form of a list of questions. Do not generate more than 10 questions.
    The job description is as follows: <JOB_DESCRIPTION> and the designation is <DESIGNATION>""".replace("<JOB_DESCRIPTION>",job_description).replace("<DESIGNATION>",designation)}]
    response = get_completion(messages)
    return response

def generate_jd(filters,designation):
    messages = [{"role":"system","content":"""Your role is to generate job description. For the given filters and designation, generate a job description that can be used to attract candidates for the job role. Filters are: <FILTERS> and Designation is <DESIGNATION>""".replace("<FILTERS>",str(filters)).replace("<DESIGNATION>",designation)}]
    response = get_completion(messages)
    return response


job_description = """
As a Data Scientist at [Company Name], you will play a key role in analyzing complex data sets, developing predictive models, and providing actionable insights to drive strategic decisions. You will work closely with cross-functional teams to understand business needs and deliver data-driven solutions that impact the company's growth and success.

Key Responsibilities:

Data Analysis & Modeling:

Analyze large and complex data sets to identify trends, patterns, and insights.
Develop and implement statistical models, machine learning algorithms, and predictive analytics to support business objectives.
Perform data mining, feature engineering, and data wrangling to prepare data for analysis.
Insights & Reporting:

Create detailed reports, dashboards, and visualizations to communicate findings to stakeholders.
Translate analytical results into actionable recommendations and strategic plans.
Present complex data insights in a clear and compelling manner to both technical and non-technical audiences.
Collaboration:

Work with product managers, engineers, and business analysts to define data requirements and deliver solutions.
Collaborate with team members to design experiments, conduct A/B testing, and evaluate the performance of data models.
Continuous Improvement:

Stay up-to-date with the latest industry trends, tools, and technologies in data science and analytics.
Identify opportunities to improve existing processes, models, and tools.
Requirements:

Education & Experience:

Bachelor’s or Master’s degree in Data Science, Statistics, Computer Science, Mathematics, or a related field.
 years of experience in data science, analytics, or a related role.
Technical Skills:

Proficiency in programming languages such as Python, R, or SQL.
Experience with data visualization tools (e.g., Tableau, Power BI) and statistical analysis software.
Strong understanding of machine learning algorithms, statistical modeling, and data mining techniques.
Soft Skills:

Excellent problem-solving skills and the ability to think critically and analytically.
Strong communication skills with the ability to convey complex data insights to diverse audiences.
Proven ability to work collaboratively in a team environment and manage multiple priorities.
Desired Skills:

Experience with big data technologies (e.g., Hadoop, Spark) is a plus.
Knowledge of cloud platforms (e.g., AWS, Azure, Google Cloud) and data engineering practices.
Experience in GenAI"""
desigantion = "Data Scientist"

filters = {
    "title": "Data Scientist",
    "location": "Work from office",
    "experience": "2-4 years",
    "skills": ["Python", "AWS", "SQL", "Machine Learning", "Pandas","tensorflow","web scrapping"]}


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
        {
            "title": "Phone",
            "type": "phone_number"
        },
    ] } 

    print(response)
    questions = list(response.split("\n"))
    form_data["fields"].extend([{"title":q,"type":"short_text"} for q in questions])
    # print(form_data)

    return form_data


    # response = generate_questions(job_description, desigantion)
    # response = generate_jd(filters,desigantion)