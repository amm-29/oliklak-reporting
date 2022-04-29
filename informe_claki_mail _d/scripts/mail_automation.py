from datetime import datetime, date
import os
import smtplib
import pathlib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase

from utils import *

from sqlalchemy import create_engine


'''# save the plot with date as filename in ./results/
filename = "./plots/" + str(date.today()) + ".png"
# working directory
dir = pathlib.Path(__file__).parent.absolute()
# folder where the plots should be saved
folder = r"/reports/"
# path to image
path_plot = str(dir) + folder + filename
'''
# Settings
# from_mail = os.environ['MAIL1']  # "test.name@googlemail.com"
# from_password = os.environ['G-PW']  # "password123"
from_mail = "alejandro.oliklak@protonmail.com"
from_password = "Zeldalink22955"
to_mail = "link4255@protonmail.com"
smtp_server = "localhost"
smtp_port = 1025


def send_email(smtp_server, smtp_port, from_mail, from_password, to_mail):
    '''
        Send results via mail
    '''

    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = 'Informe de Claki'
    msg['From'] = from_mail
    COMMASPACE = ', '
    msg['To'] = COMMASPACE.join([from_mail, to_mail])
    msg.preamble = 'Simple Data Report: Time analysis'

    '''# Open the files in binary mode and attach to mail
    with open(path_plot, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='hours_plot.png')
        img.add_header('X-Attachment-Id', '0')
        img.add_header('Content-ID', '<0>')
        fp.close()
        msg.attach(img)'''

    message_html = pd.read_html("/Users/alejandro/Desktop/work/informe-claki/reports/report_curso_08940E015_2021-07-15.html")
    print(message_html)
    # Attach HTML body
    msg.attach(MIMEText(message_html, 'html', 'utf-8'))
    print(msg)

    # Send mail
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.ehlo()
    server.login(from_mail, from_password)

    server.sendmail(from_mail, [from_mail, to_mail], msg.as_string())
    server.quit()


send_email(smtp_server, smtp_port, from_mail, from_password, to_mail)

