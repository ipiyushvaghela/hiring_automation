import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(form_link, recipient_email):
    sender_email = "pankti_15@outlook.com"
    sender_password = "Pankti@@99"

    subject = "DXFactor - Job Application Form"
    body = f"Hi,\n\nPlease fill out the form using the following link:\n{form_link}\n This will help us understand more about your skills.\n\nThank you!"

    
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
        
        
def send_report(csv_file_name, recipient_email):
    sender_email = "pankti_15@outlook.com"
    sender_password = "Pankti@@99"

    subject = "Candidate Profiles"
    body = f"Hi,\n\nPlease find the attached candidate profiles.\n\nThank you!" 

    print("Sending email from:", sender_email)
    
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach the email body
    message.attach(MIMEText(body, "plain"))
    
    # Attach the CSV file
    with open(csv_file_name, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(csv_file_name)}',
        )
        message.attach(part)

    try:
        # Connect to the server and send the email
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()  # Start TLS for security
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
        
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# form_link = "https://qz4atdkbo71.typeform.com/to/JrdCQB01"
# recipient_email = "nishant@dxfactor.com"
# send_email(form_link, recipient_email)
