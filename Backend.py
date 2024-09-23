import flask
from flask import Flask, request, jsonify
from resume_parser import pdf_to_base64,extract_text,get_details
from config import output_folder_name, ip_config, config, environment
from werkzeug.utils import secure_filename
import os
from generate_questions import generate_questions, format_questions
from question_link import generate_link
from send_email import send_email

app = flask.Flask(__name__)

# @app.route('/upload', methods=['POST'])
# def upload():
#     data = request.json
#     print("***************************************")
#     print(data)
#     pdf_file_name = os.path.basename(data["file"]).split(".pdf")[0] + ".json"
#     base64_string = pdf_to_base64(data["file"])
#     # print(base64_string)
#     file_name = os.path.join(output_folder_name, pdf_file_name) # Path to store the output JSON file
#     # file_name = r"resume_parser\piyush.json"
#     # print(file_name)
#     status = extract_text(file_name,base64_string)
#     status = "200"
#     if status == "400":
#         result = {"message": "error in extracting text from resume","status":"400","file_name":file_name}
#         return jsonify(result)
#     else:
#         result = {"message": "extracted text from resume successfully","status":"200","file_name":file_name}
#         return jsonify(result)


@app.route('/send_details', methods=['POST'])
def send_details():
    data = request.json
    file_name = data["file"].replace("\\","/")
    print("file_name*****************:",file_name)
    data = get_details(file_name)
    return jsonify({"message": "Details sent successfully","data":data})

@app.route('/fetch_email', methods=['POST'])
def fetch_email():
    data = request.json
    # print("data:",data)
    # print(data)
    email = data['data']["personal_info"]["email"]
    return jsonify({"message": "Details sent successfully","email":email})

@app.route("/fetch_questions", methods=['POST'])
def generate_questionnaire():
    data = request.json
    print("data:",data)
    job_description = data["job_description"]
    designation = data["designation"]
    email = data["email"]
    print(email)
    question_list = generate_questions(job_description, designation)
    form_data = format_questions(question_list)
    form_link = generate_link(form_data)
    send_email(form_link, email)
    return jsonify({"message": "Questions sent successfully"})    
    
@app.route("/extract_text", methods=['POST'])
def extract_text_from_resume(): 
    '''Extract text from resume using base64 string and store in db'''
    try:
        data = request.json
        base64_string = data.get('file')
        job_id = data.get('job_id')
        if not base64_string:
            return jsonify({'error': 'No base64 string provided'}), 400
        else:
            extracted_text = extract_text(base64_string,job_id)
            return jsonify({'extracted_text': extracted_text}), 200
    except Exception as e:
        print("Error in extracting text from resume:",e)



    
if __name__ == '__main__':
    # IP = ip_config[environment]
    response_port = config['ResumeApplication']['Backend']  # response API
    app.run(host='0.0.0.0', port=response_port)