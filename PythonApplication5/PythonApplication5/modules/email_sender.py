from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import config

def send_recommendation_email(name, email, papers):
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL_SENDER
    msg['To'] = email
    msg['Subject'] = 'Research Paper Recommendations'

    # Create email body content with paper information
    email_content = f"Dear {name},\n\nHere are some research papers you might find interesting:\n\n"
    for paper in papers:
        email_content += f"Title: {paper['title']}\n"
        email_content += f"Abstract: {paper['abstract']}\n"
        email_content += f"Download Link: {paper['download_link']}\n\n"

    msg.attach(MIMEText(email_content, 'plain'))

    try:
        # Connect to SMTP server and send the email
        smtp_server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        smtp_server.send_message(msg)
        smtp_server.quit()
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}. Error: {str(e)}")
