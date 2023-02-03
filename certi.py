from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.message import EmailMessage
import pandas as pd
import os

os.chdir('/Users/Joy/Desktop/Python_Projects/Certificate') # Current directory path

def send_mail(certificate, recipient):

    E_MAIL = os.environ.get('TEST_E-MAIL') # e-mail and password stored in environment varaibles
    PASSWORD = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'Certificate of Participation'
    msg['From'] =  E_MAIL
    msg['To'] = recipient
    msg.set_content("Here's your certificate of Participation for Deep learning using python")

    file = f'{certificate}.pdf'
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(E_MAIL, PASSWORD)
        smtp.send_message(msg)


df = pd.read_csv('data.csv')
df['full_name'] = df['first_name'] + " " + df['last_name']
df['full_name'] = df['full_name'].str.title()

for i, e_mail in zip(df["full_name"], df['e-mail']):

    img = Image.open('Base_Template.jpg')
    draw = ImageDraw.Draw(img)

    location = (1015, 650)
    color = (1,21,99)

    font = ImageFont.truetype("DancingScript-VariableFont_wght.ttf", 150)
    draw.text(location, i, fill=color, font=font, anchor="mm", align="center") 
    img.save("PDFs/{}.pdf".format(i.replace(" ", "_")))

    os.chdir('/Users/Joy/Desktop/Python_Projects/Certificate/PDFs') # path where you want to save the pdf's
    certi_file_name = i.replace(" ", "_")

    send_mail(certi_file_name, e_mail)
    print(f'E-mail sent to {e_mail}')
    os.chdir('/Users/Joy/Desktop/Python_Projects/Certificate') # back to current directory
