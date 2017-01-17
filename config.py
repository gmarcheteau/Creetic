#!/usr/bin/env python
# settings.py
import os

IS_HEROKU = os.environ.get('IS_HEROKU', None)

#if running on Heroku
if IS_HEROKU:
  print "Heroku env -- importing variables"
  IMAP_LOGIN = os.environ.get('IMAP_LOGIN', None)
  IMAP_PASSWORD = os.environ.get('IMAP_PASSWORD', None)
  WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', True)
  SECRET_KEY = os.environ.get('SECRET_KEY', True)

else:
  print "local env -- importing localconfig.py"
  from localconfig import IMAP_LOGIN,IMAP_PASSWORD, WTF_CSRF_ENABLED,SECRET_KEY