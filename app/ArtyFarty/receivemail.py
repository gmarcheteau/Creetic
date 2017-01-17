import imaplib
import email
import os
import random
from config import IMAP_LOGIN,IMAP_PASSWORD, WTF_CSRF_ENABLED,SECRET_KEY

file_extensions = ('.jpg','.JPG','.png','.PNG','.jpeg','.JPEG','.gif','.GIF')

def getMsgs():
  servername="imap.gmail.com"
  usernm = IMAP_LOGIN
  passwd = IMAP_PASSWORD
  #subject = 'Test'
  conn = imaplib.IMAP4_SSL(servername)
  conn.login(usernm,passwd)
  conn.select('Inbox')
  typ, data = conn.search(None,'(UNSEEN)')
  #typ, data = conn.search(None,'(UNSEEN SUBJECT "%s")' % subject)
  for num in data[0].split():
    typ, data = conn.fetch(num,'(RFC822)')
    msg = email.message_from_string(data[0][1])
    #typ, data = conn.store(num,'-FLAGS','\\Seen')
    yield msg

def getAttachment(msg,check):
  for part in msg.walk():
    if part.get_content_type() == 'image/jpeg':
      if check(part.get_filename()):
        return part.get_payload(decode=1)

def checkNewMailWithImages():
  newMessages = []
  for msg in getMsgs():
    fromaddr = email.utils.parseaddr(msg['From'])[1]
    print "Message from: %s" %fromaddr
    payload = getAttachment(msg,lambda x: x.endswith(file_extensions))
    if not payload:
      print "No image attachment."
      continue
    try:
      rand = random.randint(0,999999)
      filename = "image%d.jpg" %rand
      filepath = os.path.abspath("static/images/%s" %filename)
      while os.path.exists(filepath):
        rand += 1
        print "%s already existed, trying the next number" % filepath
        filename = "image%d.jpg" %rand
        filepath = os.path.abspath("static/images/%s" %filename)
      
      open(filepath,'w').write(payload)
      print "Writing to %s" % filepath
      newMessages.append(
        {"fromaddr":fromaddr,"imageurl":filepath})
    except Exception as err:
      print str(err)
  print newMessages
  return newMessages