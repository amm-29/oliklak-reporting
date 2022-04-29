# Import modules
import smtplib
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
## The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd
import ssl


def attach_file_to_email(email_message, filename, extra_headers=None):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    # Add header/name to the attachments
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)
    # Attach the file to the message
    email_message.attach(file_attachment)


def send_mail(link, name_school, date_report, email_to):
    # Define the HTML document
    html = '''
        <html>
            <body>
                <h1><center>L' Informe CLAKI {}</center></h1>
                <h2><center>Centre: {} </center></h2>
                <p><center>Aquest es un correu de prova.</center></p>
                <p><center>Per accedir a l' informe heu de fer click i descarregar l' arxiu del següent enllaç <a href={}>AQUÍ</a></center></p>
                <p><center>Per visualitzar l' informe,  es necessari obrir el fitxer .html mitjançant un cercador com Google Chrome o Firefox.</center></p>
                <p><center>Per poder imprimir o guardar-lo com a .pdf, al cercador, fer click dret al arxiu i esocllir l' opció "imprimir".
                Serà necessari establir el tamany de paper a "A1" i, si cal, l' escala entre 110 i 115. </center></p>
                <p><center>Gràcies per recollir amb Claki!</center></p>
                <p><center>Fins el mes vinent :)</center></p>
                <img src='cid:myimageid' width="700">
            </body>
        </html>
        '''.format(date_report.replace("_", "-"), name_school, link)

    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = 'alejandro.oliklak@gmail.com'
    password = 'Cocacola1995'
    # email_to = 'alejandro.oliklak@gmail.com'

    # Generate today's date to be included in the email Subject
    # date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Test email informe Claki ({date_report.replace("_", "-")})'

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))
    # attach_file_to_email(email_message, './images/header.png', {'Content-ID': 'myimageid'})
    # attach_file_to_email(email_message, filename)
    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)
