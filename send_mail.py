import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from decouple import config
from dotenv import load_dotenv
load_dotenv()


def send_email(file_path):
    sender_email = config("SENDER_EMAIL")
    sender_password = config("SENDER_PASSWORD")
    receiver_email = "milenov556@gmail.com"                #input("Add the email receiver:")

    subject = "Fibank Branches Info"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    attachment = open(file_path, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)

    filename = os.path.basename(file_path)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())