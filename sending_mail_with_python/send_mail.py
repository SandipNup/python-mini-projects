import os
import smtplib
import imghdr
from email.mime.text import MIMEText

from email.message import EmailMessage
import logging

logger = logging.getLogger('root')


EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def send_mail(subject, to, html_file, images=[], files=[]):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(to)

    msg.set_content("If html is not visible this will be visible ")
    with open(html_file) as html:
        msg.add_alternative(html.read(), subtype='html')

    if images:
        for image in images:
            with open(image, 'rb') as attach_file:
                image_name = attach_file.name
                image_type = imghdr.what(attach_file.name)
                image_data = attach_file.read()
            msg.add_attachment(image_data, maintype="image", subtype=image_type, filename=image_name)

    if files:
        for file in files:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = f.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    logger.info("mail_was send successfully")



