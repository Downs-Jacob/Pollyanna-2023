import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(subject, body, to_email, file_path):
    from_email = "familypollyannajpd@gmail.com"  
    password = "lzur rpbc kysq vkso"          
    # Setting up the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Attaching the file
    attachment = open(file_path, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % file_path.split('/')[-1])
    message.attach(p)

    # SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_email, password)
    text = message.as_string()
    s.sendmail(from_email, to_email, text)
    s.quit()

    print("Email sent successfully!")