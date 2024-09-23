import sqlite3
from generate_questions import get_completion
from config import DATABASE

prompt = [{"role":"system","content":"""Your role is to rank the candidate based on their response of the questionnaire, job description, his resume and Designation. STRICTLY FOLLOW: rating scale is from 1-10. For each candidate profile just give one rating. The questionnaire is as follows: <QUESTIONNAIRE> and the job designation is <DESIGNATION>. The candidate resume is <RESUME>. The job description is <JD>.
           your response should only be a rating number and nothing else."""}]

# def rate_candidate(job_id):
#     conn = sqlite3.connect(DATABASE)  # Create or connect to the database
#     cursor = conn.cursor()

#     cursor.execute('SELECT * FROM questionnaire')
#     rows = cursor.fetchall()

#     for row in rows:
#         print("ID:", row[0])
#         prompt[0]["content"] = prompt[0]["content"].replace("<QUESTIONNAIRE>", row[4]).replace("<DESIGNATION>", row[5])
#         response = get_completion(prompt)
#         print(response)
#         cursor.execute('update questionnaire set rating = ? where id = ?', (response, row[0]))
#         conn.commit()
#     conn.close()

def rate_candidate(job_id):
    conn = sqlite3.connect(DATABASE)  # Create or connect to the database
    cursor = conn.cursor()

    # Step 1: Fetch all candidates and their resume data, questionnaire data, and job description for the given job_id
    cursor.execute('''
        SELECT c.id, c.name, c.email, c.resume_data, q.questions, q.job_title, jm.job_description
        FROM candidates c
        JOIN questionnaire q ON c.id = q.id
        JOIN job_metadata jm ON c.job_id = jm.job_id
        WHERE c.job_id = ? AND q.job_id = ?
    ''', (job_id, job_id))
    
    rows = cursor.fetchall()

    # Step 2: Process each candidate's questionnaire entry
    for row in rows:
        candidate_id = row[0]         # Candidate ID from the 'candidates' table
        candidate_name = row[1]       # Candidate Name
        candidate_email = row[2]      # Candidate Email
        resume_data = row[3]          # Resume Data (in JSON format)
        questionnaire_data = row[4]   # Questionnaire Data
        designation = row[5]          # Designation
        job_description = row[6]      # Job Description from job_metadata

        # Step 3: Prepare and update the prompt for completion (rating)
        prompt[0]["content"] = prompt[0]["content"].replace("<QUESTIONNAIRE>", questionnaire_data).replace("<DESIGNATION>", designation).replace("<JD>", job_description).replace("<RESUME>", resume_data)

        # Step 4: Get the rating response from some function
        response = get_completion(prompt)
        print(f"Rating for Candidate {candidate_name} (Email: {candidate_email}): {response}")

        # Step 5: Update the rating in both the questionnaire and candidates table
        cursor.execute('UPDATE questionnaire SET rating = ? WHERE id = ?', (response, candidate_id))
        cursor.execute('UPDATE candidates SET rating = ? WHERE id = ?', (response, candidate_id))

    # Commit all updates at once
    conn.commit()

    # Close the database connection
    conn.close()

def fetch_candidate_profiles():
    conn = sqlite3.connect(DATABASE)  # Create or connect to the database
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM questionnaire')
    rows = cursor.fetchall()
    conn.close()
    return rows
