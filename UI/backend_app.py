from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)

candidate_data_store = []


def send_email(form_link, recipient_email):
    sender_email = "pankti_15@outlook.com"
    sender_password = "Pankti@@99"

    subject = "DXFactor - Proctored Test"
    body = f"Hi,\n\nPlease take your test:\n{form_link}\nThis will help us understand more about your skills.\n\nThank you!"

    print(f"Sending email to {recipient_email}...")
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
        
        print(f"Email sent successfully to {recipient_email}!")
        return True
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")
        return False
    
@app.route('/send-emails', methods=['POST'])
def send_emails():
    data = request.json  # Get the JSON data from the front-end
    emails = data.get('emails', [])
    print(emails)
    form_link = data.get('form_link', 'https://qz4atdkbo71.typeform.com/to/ztMqoegE')  # Default link to the test
    
    if not emails:
        return jsonify({"error": "No emails provided"}), 400
    
    success_count = 0
    for email in emails:
        if send_email(form_link, email):
            success_count += 1
    
    return jsonify({"status": "success", "message": f"Emails sent to {success_count}/{len(emails)} candidates."}), 200

# Endpoint to receive candidate data from Streamlit
@app.route('/api/candidates', methods=['POST'])
def receive_candidates():
    global candidate_data_store
    candidate_data_store = request.json
    return jsonify({'status': 'success', 'message': 'Candidates received'}), 200

# Endpoint to serve candidate data to the front-end page
@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    return jsonify(candidate_data_store), 200

@app.route('/')
def index():
    return render_template('exam.html')

if __name__ == '__main__':
    # app.run(127.0.0.1,5001,debug=True)
    app.run(host='127.0.0.1', port=5001, debug=True)
