import smtplib
import email.mime.text
import email.utils
import email.mime.image
import email.mime.multipart
import random
import kim_photo
import pickle
import os

PATH = os.getcwd()
FILE = PATH + "/test.jpg"

subject = ['FYI',
           'Just FYI',
           'Interesting',
           'See attached',
           'Photo',
           'Classic Kim']

salutation = ['Mate',
              'Champ',
              'Fella',
              'Hombre',
              'Chief',
              ]

first_line = ['Thought this might interest you. ',
              'Please see attached. ',
              'You may already have seen this but, in case not... ',
              'May be of interest. ',
              'Fascinating stuff. ',
              'Really thought-provoking. ',
              'You ought to take a look at this. ']

sign_off = ['Have a good one, ',
            'Best regards, ',
            'Regards, ',
            'See you anon, ',
            'We must do lunch some time soon, ',
            'All the best, ']



class KimMail:
    def __init__(self,
                 mail_photo,
                 recipient,
                 recipient_email,
                 sender,
                 sender_email,
                 sender_server,
                 sender_password):
        
        self.mail_photo = mail_photo
        self.sender_server = sender_server
        self.sender_password = sender_password
        self.recipient = recipient
        self.sender = sender
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['To'] = email.utils.formataddr((recipient, recipient_email))
        self.msg['From'] = email.utils.formataddr((sender, sender_email))
        self.msg['Subject'] = random.choice(subject)
        
        msgText = email.mime.text.MIMEText(
            "{},\n\n{}\n\nAs you'll see, it's a picture of Kim Jong Un {}.\n\n{}\n\n{}".format(
                random.choice(salutation),
                random.choice(first_line),
                mail_photo.title,
                random.choice(sign_off),
            self.sender))
        
        self.msg.attach(msgText)
        
        with open(FILE, "rb") as f:
            pic = f.read()
   
        att = email.mime.image.MIMEImage(pic)
        self.msg.attach(att)        
        
        pass
    
    def send(self):
        '''Send the KimMail'''
        print("[+]\tConnecting to {}...".format(self.sender_server))
        server = smtplib.SMTP(self.sender_server)
        server.starttls()
        print("[+]\tConnected to {}".format(self.sender_server))
        print("[+]\tLogging in to {}...".format(self.sender_server))
        server.login(self.sender_email, self.sender_password)
        print("[+]\tLogged in to {}".format(self.sender_server))
        print("[+]\tSending {} to {}...".format(self.mail_photo.__str__, self.recipient))
        server.sendmail(self.sender_email, self.recipient_email, self.msg.as_string())
        print("[+]\tMessage sent. Quitting server")
        server.quit()
        self.update_cache()
        
    def update_cache(self):
        if os.path.isfile(PATH+"/hist.log"):
            with open(PATH+"/hist.log", "rb") as f:
                log = pickle.load(f)
                log[self.recipient_email] = self.mail_photo.src
            with open(PATH+"/hist.log", "wb") as f:
                pickle.dump(log, f)
        else:
            log={}
            log[self.recipient_email] = self.mail_photo.src
            with open(PATH+"/hist.log", "wb") as f:
                pickle.dump(log, f)            

