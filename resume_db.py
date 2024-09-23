import sqlite3
import json  

DATABASE_PATH = "resume_details.db"
# with open(r"resume_parser\Karan_CV.pdf.json", 'r') as file:
#     data = json.load(file)


def store_resume(data,job_id):

    print(type(data))
    conn = sqlite3.connect('resume_details.db')  # Create or connect to the database
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    resume_data TEXT,
    job_id TEXT,
    rating INTEGER DEFAULT 0
    )
    ''')
    
    name, email, phone = None, None, None
    if "personal_info" in data:
        personal_info = data["personal_info"]
        name = personal_info.get("name")
        email = personal_info.get("email")
        phone = personal_info.get("phone")
    

    cursor.execute('''
    INSERT INTO candidates (name, email, phone, resume_data, job_id)
    VALUES (?, ?, ?, ?,?)
    ''', (name, email, phone, json.dumps(data), job_id))

    # Commit and close
    conn.commit()
    conn.close()

    print("Data inserted successfully!")

def store_questions(data):
    print(data)
    conn = sqlite3.connect('resume_details.db')  # Create or connect to the database
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questionnaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    questions TEXT,
    job_title TEXT,
    job_id INTEGER,         -- Added job_id here
    rating INTEGER DEFAULT 0
    )
    ''')

    try:
        cursor.execute('''
        SELECT id FROM questionnaire WHERE name = ?
        ''', (data.get('Name', None),))
        existing_record = cursor.fetchone()

        if existing_record:
            print(f"Record already exists for name: {data.get('Name', None)}")
        else:
            questions_str = '\n'.join(data.get('Questions', []))
            cursor.execute('''
            INSERT INTO questionnaire (name, email, phone, questions, job_title, job_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data.get('Name', None),
                data.get('Email', None),
                data.get('Phone', None),
                questions_str,
                data.get('job_title', None),
                data.get('job_id', None)  # Insert the job_id here as well
            ))
            print("Data inserted successfully in questionnaire!")
    except Exception as e:
        print(f"Error inserting data: {e}")

    finally:
        # Commit and close
        conn.commit()
        conn.close()

def create_resume_table():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_titles (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT UNIQUE
        )
        """)
        
        # Create job metadata table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_metadata (
            submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            job_description TEXT,
            zip_file_path TEXT,
            FOREIGN KEY (job_id) REFERENCES job_titles (job_id)
        )
        """)
        conn.commit()

# def insert_metadata(job_title, job_description, zip_file_path):
#     with sqlite3.connect(DATABASE_PATH) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#         INSERT INTO job_metadata (job_title, job_description, zip_file_path)
#         VALUES (?, ?, ?)
#         """, (job_title, job_description, zip_file_path))
#         conn.commit()
#         job_id = cursor.lastrowid
#     return job_id

def insert_metadata(job_title, job_description, zip_file_path):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        
        # Check if the job_title already exists in job_titles table
        cursor.execute("""
        SELECT job_id FROM job_titles WHERE job_title = ?
        """, (job_title,))
        row = cursor.fetchone()
        
        if row:
            # Job title exists, get the existing job_id
            job_id = row[0]
            print(f"Job title '{job_title}' already exists with job_id {job_id}.")
        else:
            # If job title doesn't exist, insert into job_titles table
            cursor.execute("""
            INSERT INTO job_titles (job_title)
            VALUES (?)
            """, (job_title,))
            conn.commit()
            job_id = cursor.lastrowid  # Get the newly inserted job_id
            print(f"Inserted new job title '{job_title}' with job_id {job_id}.")

        # Now insert the submission into the job_metadata table using job_id
        cursor.execute("""
        INSERT INTO job_metadata (job_id, job_description, zip_file_path)
        VALUES (?, ?, ?)
        """, (job_id, job_description, zip_file_path))
        conn.commit()

    return job_id


def fetch_candidate_email():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT email FROM candidates
        """)
        results = cursor.fetchall()
        emails = [row[0] for row in results]
    return emails


def fetch_job_metadata_and_emails():
    conn = sqlite3.connect('resume_details.db')
    cursor = conn.cursor()

    # Step 1: Fetch all distinct job IDs from the candidates table
    cursor.execute("SELECT DISTINCT job_id FROM candidates")
    job_ids = [row[0] for row in cursor.fetchall()]
    job_metadata = {}
    
    # Step 2: Fetch job metadata (job title and job description) for those job IDs
    if job_ids:
        placeholders = ', '.join('?' * len(job_ids))
        query = f"""
        SELECT jt.job_id, jt.job_title, jm.job_description
        FROM job_titles jt
        JOIN job_metadata jm ON jt.job_id = jm.job_id
        WHERE jt.job_id IN ({placeholders})
        """
        cursor.execute(query, job_ids)

        # Step 3: Store job metadata in a dictionary
        for row in cursor.fetchall():
            job_metadata[str(row[0])] = {
                'job_title': row[1],
                'job_description': row[2]
            }
    
    # Step 4: Fetch emails and associate them with job metadata
    result = {}
    for job_id in job_ids:
        if str(job_id) in job_metadata:
            cursor.execute("SELECT email FROM candidates WHERE job_id = ?", (job_id,))
            emails = [row[0] for row in cursor.fetchall()]
            job_info = job_metadata[str(job_id)]
            result[job_id] = {
                'job_title': job_info['job_title'],
                'job_description': job_info['job_description'],
                'emails': emails
            }
    
    conn.close()
    return result

# def fetch_job_metadata_and_emails():
#     conn = sqlite3.connect('resume_details.db')
#     cursor = conn.cursor()

#     # Step 1: Fetch all job IDs from the candidates table
#     cursor.execute("SELECT DISTINCT job_id FROM candidates")
#     job_ids = [row[0] for row in cursor.fetchall()]
#     job_metadata = {}
    
#     # Step 2: Fetch job metadata for those job IDs
#     if job_ids:
#         placeholders = ', '.join('?' * len(job_ids))
#         # query = f"SELECT job_id, job_title, job_description FROM job_metadata WHERE job_id IN ({placeholders})"
#         query = f"SELECT job_id, job_description FROM job_metadata WHERE job_id IN ({placeholders})"
        
#         cursor.execute(query, job_ids)
        
#         title_query = f"SELECT job_title FROM job_titles WHERE job_id IN ({placeholders})"
        
#         cursor.execute(title_query, job_ids)
        
#         # Step 3: Store job metadata in a dictionary
#         for row in cursor.fetchall():
#             job_metadata[str(row[0])] = {
#                 'job_title': row[1],
#                 'job_description': row[2]
#             }
#     # Step 4: Fetch emails and job details
#     result = {}
#     for job_id in job_ids:
#         if job_id in job_metadata:
#             cursor.execute("SELECT email FROM candidates WHERE job_id = ?", (job_id,))
#             emails = [row[0] for row in cursor.fetchall()]
#             job_info = job_metadata[job_id]
#             result[job_id] = {
#                 'job_title': job_info['job_title'],
#                 'job_description': job_info['job_description'],
#                 'emails': emails
#             }
    
#     conn.close()
#     return result

# store_resume(data)
# fetch_questions()