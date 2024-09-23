import streamlit as st
from prompts import jd_prompt
from docx import Document
from io import BytesIO
from generate_questions import generate_questions, format_questions, get_completion
from Frontend import *
from resume_db import insert_metadata, create_resume_table, fetch_job_metadata_and_emails
from send_email import send_report,send_email
from question_link import generate_link, get_questionnaire_response
from candidate_ranking import rate_candidate, fetch_candidate_profiles
from apscheduler.schedulers.background import BackgroundScheduler
import schedule
from functools import partial
import time
from threading import Thread
import webbrowser
from web_search import *
from fetch_resume import *

scheduler_running = False

def scheduled_job(form_url,job_title,job_id):

    try:
        if form_url and job_title:
            get_questionnaire_response(form_url, job_title,job_id)
            rate_candidate(job_id)
            candidate_rank_data = fetch_candidate_profiles()

            # Prepare the CSV file and send the report
            csv_file_name = send_profile(candidate_rank_data)
            # send_report(csv_file_name, "pankti@dxfactor.com")

            # Optionally log or store the candidate data somewhere if needed
            print("Daily task executed successfully.")
        else:
             print("form_url or job_title not set.")
             
    except Exception as e:
        print(f"Error in scheduled task: {e}")

def start_scheduler(form_url, job_title, job_id):
    global scheduler_running
    
    if not scheduler_running:
        scheduled_job_with_args = partial(scheduled_job, form_url, job_title, job_id)

        # Schedule the job every minute for testing purposes
        schedule.every(1).minutes.do(scheduled_job_with_args)

        scheduler_running = True

        while scheduler_running:
            schedule.run_pending()
            time.sleep(60)  # Check the schedule every minute to reduce CPU usage
    else:
        print("Scheduler already running.")

def run_scheduler_in_background(form_url, job_title, job_id):
    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=start_scheduler, args=(form_url, job_title, job_id))
    scheduler_thread.daemon = True  # Ensure the thread closes when the main program ends
    scheduler_thread.start()

# Call this function in Streamlit only when necessary
def trigger_scheduler(form_url, job_title, job_id):
    global scheduler_running

    # Only start the scheduler if it isn't already running
    if not scheduler_running:
        st.write("Starting the scheduler...")
        run_scheduler_in_background(form_url, job_title, job_id)
    else:
        st.write("Scheduler is already running.")
        
        
# App title
st.title("Candidate Profile Solution")


# Sidebar options
option = st.sidebar.radio(
    "Choose an option:",
    ("Upload Resume", "Generate JD", "Send Test", "Extract Resume")
)


if option == "Upload Resume":
    st.header("Upload Resume")
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "zip"])
    job_title = st.text_input("Enter Designation")
    job_description = st.text_area("Enter Job Description")
    
    if st.button("Submit"):
        if uploaded_file is not None:
            if uploaded_file.type in ['application/zip', 'application/x-zip-compressed']:
                st.write("ZIP file uploaded.")
                # zip_file_path = save_uploaded_file(uploaded_file)
                # print(zip_file_path)
                # extract_dir = extract_zip_file(zip_file_path)
                # create_resume_table()
                # job_id = insert_metadata(job_title, job_description, extract_dir)
                extract_dir = r"uploaded_data\extracted_files\resume"
                job_id = "1"
                job_title = "Data Scientist Intern"
                try:
                    # for file in os.listdir(extract_dir):
                    #     if file.endswith(".pdf"):
                    #         file_path = os.path.join(extract_dir, file)
                    #         base64_string = pdf_to_base64(file_path)
                    #         #Extract text and store in db with job_id
                    #         process_resumes(base64_string, job_id)
                      
                    job_details = fetch_job_metadata_and_emails()
                    for job_id, details in job_details.items():
                        job_title = details['job_title']
                        job_description = details['job_description']
                        emails = details['emails']
                        
                    question_list = generate_questions(job_description, job_title)
                    print(question_list)
                    form_data = format_questions(question_list)
                    form_url = generate_link(form_data)
                    print(form_url)
                    for email in emails:
                        send_email(form_url, email)
                    
                    
                    #### call scheduler
                    
                    form_url = "https://qz4atdkbo71.typeform.com/to/JrdCQB01"
                    run_scheduler_in_background(form_url, job_title, job_id)
                    
                    # get_questionnaire_response(form_url,job_title,job_id)
                    # rate_candidate(job_id)
                    # candiate_rank_data = fetch_candidate_profiles()
                    # st.title("Candidate Profiles")
                    # st.write("Below are the details of candidates:")
                    # csv_file_name = send_profile(candiate_rank_data)
                    # # send_report(csv_file_name, "pankti@dxfactor.com")
                    # for profile in candiate_rank_data:
                    #     st.write(f"ID: {profile[0]}")
                    #     st.write(f"Name: {profile[1]}")
                    #     st.write(f"Email: {profile[2]}")
                    #     st.write(f"Phone: {profile[3]}")
                    #     st.write(f"Job_title: {profile[5]}")
                    #     st.write(f"Job_id: {profile[6]}")
                    #     st.write(f"Rating: {profile[7]}")
                    #     st.write("---")
       
                except Exception as e:
                    st.error(f"Error processing resumes: {e}")
            else:
                st.warning("Please Upload zip file")
         

elif option == "Generate JD":
 
    # Sidebar filters for Generate JD
    with st.sidebar:
        st.subheader("Filter Options")
        job_title = st.text_input("Job Title")
        location = st.text_input("Location")
        experience = st.slider("Years of Experience", 0, 20, 3)
        skills_input = st.text_area("Enter Skills (comma-separated)")
        skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
        technologies = st.sidebar.text_area("Technologies")
        other = st.sidebar.text_area("Other Details")


    if st.sidebar.button("Generate JD"):
        data = {
            "job_title": job_title,
            "location": location,
            "experience": f"{experience} years",
            "skills": ", ".join(skills),
            "technologies": technologies,
            "other": other
        }
        jd_prompt[0]["content"] = jd_prompt[0]["content"].replace("<FILTERS>",str(data)).replace("<DESIGNATION>",job_title)
        
        response = get_completion(jd_prompt)
        st.success("Job Description generated successfully!")
        
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown(f"**Generated Job Description:**\n\n{response}")

        
        # Create a .docx file for download
        docx_file = create_docx(response)
        
        st.download_button(
            label="Download as DOCX",
            data=docx_file,
            file_name="job_description.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
     # data = {"location":"Ahmedabad","experience":"5 years","skills":"python, tableu, my sql","technologies":"Genai","other":"should be good at communication"}
     
     
elif option == "Send Test":
    new_candidate_data = []
    candidate_rank_data = fetch_candidate_profiles()
    filtered_data = [(profile[1], profile[2], profile[5], profile[6], profile[7]) for profile in candidate_rank_data if profile]
    print(filtered_data)
        
    # Display candidate data in the Streamlit app
    for profile in candidate_rank_data:
        st.write(f"ID: {profile[0]}, Name: {profile[1]}, Email: {profile[2]}")
    
    # When the button is clicked, send data to Flask and open the front-end URL
    if st.button('Send Candidates to Web Page'):
        # Send candidate data to Flask backend
        response = requests.post('http://127.0.0.1:5001/api/candidates', json=filtered_data)
        
        if response.status_code == 200:
            st.success('Candidates sent successfully!')
            
            # Redirect to the front-end page served by Flask
            front_end_url = 'http://127.0.0.1:5001/'  # Replace with your actual URL if different
            webbrowser.open(front_end_url)  # This opens the front-end page in the user's default web browser
        else:
            st.error('Failed to send candidates.')
    # for profile in candiate_rank_data:
    #     st.write(f"ID: {profile[0]}")
    #     st.write(f"Name: {profile[1]}")
    #     st.write(f"Email: {profile[2]}")
    #     st.write(f"Phone: {profile[3]}")
    #     st.write(f"Job_title: {profile[5]}")
    #     st.write(f"Job_id: {profile[6]}")
    #     st.write(f"Rating: {profile[7]}")
    #     st.write("---")
    
    
elif option == "Extract Resume":
    location = st.text_input('Enter Location:', placeholder="e.g., Ahmedabad")
    year = st.text_input('Enter Year of Experience:', placeholder="e.g., 1 year")
    post = st.text_input('Enter Post:', placeholder="e.g., Data Scientist")
    if st.button('Submit'):
        query = f"site:linkedin.com/in intitle:{location}+{year}+{post}"
        profile_urls = fetch_profile(query)
        st.write(profile_urls)
        # scrape_resume(profile_urls)
