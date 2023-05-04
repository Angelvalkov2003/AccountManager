import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

class EmailSender:
    def __init__(self, email_address, email_password):
        self.SMTP_SERVER = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.EMAIL_ADDRESS = email_address
        self.EMAIL_PASSWORD = email_password
    
    def send_email(self, to_email_address, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = to_email_address
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        
        text = body
        msg.attach(MIMEText(text))
        
        server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
        
        server.sendmail(self.EMAIL_ADDRESS, to_email_address, msg.as_string())
        server.quit()

# Example usage