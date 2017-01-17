#!/usr/bin/env python
# settings.py

IS_HEROKU = os.environ.get('IS_HEROKU', None)

#if running on Heroku
if IS_HEROKU:
  username = os.environ.get('IMAP_LOGIN', None)
  password = os.environ.get('IMAP_PASSWORD', None)

else:
  print "local env -- importing localconfig.py"
  from localconfig import ENVIRONMENT,IMAP_LOGIN,IMAP_PASSWORD
  username = IMAP_LOGIN
  password = IMAP_PASSWORD
