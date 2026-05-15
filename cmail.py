import smtplib  #sending mail
from email.message import EmailMessage   #mail formatting
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)    
    server.login('annaladasubindubabu@gmail.com','hsqs dztc glxf pdmc')
    msg=EmailMessage()
    msg['FROM']='annaladasubindubabu@gmail.com'
    msg['SUBJECT']=subject
    msg['TO']=to
    msg.set_content(body)
    server.send_message(msg)
    server.close()