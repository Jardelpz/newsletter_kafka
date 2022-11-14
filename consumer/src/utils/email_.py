import smtplib
import ssl
import re


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.settings import EMAIL, EMAIL_PASSWORD


def is_valid_email(email) -> bool:
    return email if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email) else False


def send_email(to_email, subject, message):
    html = "<html><body>"
    for paragraph in message:
        if subtitle := paragraph.get('subtitle'):
            html += "".join(f"<h1>{subtitle}</h1>")

        if content := paragraph.get('content'):
            html += "".join(f"<p>{content}</p>")

        if image := paragraph.get('image'):
            html += "".join(f'<img alt="" src="{image}" width=150" height="70">')

        html += "".join("<br><br>")

    html += "".join("</body></html>")

    email_message = MIMEMultipart()
    email_message['From'] = EMAIL
    email_message['To'] = to_email
    email_message['Subject'] = subject
    email_message.attach(MIMEText(html, "html"))
    email_string = email_message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, to_email, email_string)


