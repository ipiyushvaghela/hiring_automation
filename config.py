import os
output_folder_name = "resume_parser"

environment = os.environ.get("ENV")  # local / prod / dev

ip_config = {'prod': "54.67.61.89", 
             'dev' : os.environ.get("FSF_DEV_HOST"),
             'local': "127.0.0.1"}

protocol = os.environ.get("FSF_PROTOCOL")  # http / https

config = {"ResumeApplication": {
    "Backend": 7004,   # port needs to be public - 8001
    "Frontend": 8002,  # port needs to be public - 8002
    "Embedding":7003
    }
}

DATABASE = "resume_details.db"
TEXT_EXTRACTION_API_URL = f"http://{ip_config[environment]}:{config['ResumeApplication']['Backend']}/extract_text"
TEST_API_URL = f"http://{ip_config[environment]}:{config['ResumeApplication']['Backend']}/send_test"
