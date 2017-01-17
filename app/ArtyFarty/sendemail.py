# Found most ofthis at http://ryrobes.com/python/python-snippet-sending-html-email-with-an-attachment-via-google-apps-smtp-or-gmail/
# Adapted to accept a list of files for multiple file attachments
# From other stuff I googled, a little more elegant way of converting html to plain text
# This works in 2.7 and my brain gets it.

######### Setup your stuff here #######################################
from config import IMAP_LOGIN,IMAP_PASSWORD, WTF_CSRF_ENABLED,SECRET_KEY

attachments = []

host = 'smtp.gmail.com:587' # specify port, if required, using this notations

fromaddr = 'artomatic2000@gmail.com' # must be a vaild 'from' address in your GApps account
default_toaddr  = 'gregoire.marcheteau@gmail.com'
replyto = fromaddr # unless you want a different reply-to

msgsubject = 'Artomatic 2000'

htmlmsgtext = """<h2>This is my message body in HTML</h2>"""

######### In normal use nothing changes below this line ###############

import smtplib, os, sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
from HTMLParser import HTMLParser

# A snippet - class to strip HTML tags for the text version of the email

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

########################################################################

def sendEmail(htmlmessage, toaddr):
  try:
      # necessary mimey stuff
      msg = MIMEMultipart()
      msg.preamble = 'This is a multi-part message in MIME format.\n'
      msg.epilogue = ''
  
      body = MIMEMultipart('alternative')
      #body.attach(MIMEText(msgtext))
      body.attach(MIMEText(htmlmessage, 'html'))
      msg.attach(body)
  
      if 'attachments' in globals() and len('attachments') > 0: # are there attachments?
          for filename in attachments:
              f = filename
              part = MIMEBase('application', "octet-stream")
              part.set_payload( open(f,"rb").read() )
              Encoders.encode_base64(part)
              part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
              msg.attach(part)
  
      msg.add_header('From', fromaddr)
      msg.add_header('To', toaddr)
      msg.add_header('Subject', msgsubject)
      msg.add_header('Reply-To', replyto)
  
      # The actual email sendy bits
      server = smtplib.SMTP(host)
      server.set_debuglevel(False) # set to True for verbose output
      try:
          # gmail expect tls
          server.starttls()
          server.login(username,password)
          server.sendmail(msg['From'], [msg['To']], msg.as_string())
          print 'Email sent'
          server.quit() # bye bye
      except:
          # if tls is set for non-tls servers you would have raised an exception, so....
          server.login(username,password)
          server.sendmail(msg['From'], [msg['To']], msg.as_string())
          print 'Email sent'
          server.quit() # sbye bye
  except:
      print ('Email NOT sent to %s successfully. %s ERR: %s %s %s ', str(toaddr), 'tete', str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2]) )
      #just in case