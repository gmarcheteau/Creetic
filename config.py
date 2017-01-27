  #!/usr/bin/env python
# settings.py
import os

#non-sensitive stuff
MIN_CLUSTERS = 3
MAX_CLUSTERS = 5
DEFAULT_URL = "https://upload.wikimedia.org/wikipedia/commons/6/69/VanGogh-starry_night_edit.jpg"
#DEFAULT_URL = "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"

#check if running on Heroku
IS_HEROKU = os.environ.get('IS_HEROKU', None)

#if running on Heroku
if IS_HEROKU:
  print "Heroku env -- importing variables"
  IMAP_LOGIN = os.environ.get('IMAP_LOGIN', None)
  IMAP_PASSWORD = os.environ.get('IMAP_PASSWORD', None)
  WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', True)
  SECRET_KEY = os.environ.get('SECRET_KEY', True)
  #TWITTER
  TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', None)
  TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', None)
  TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', None)
  TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', None)
  

else:
  print "local env -- importing localconfig.py"
  from localconfig import IMAP_LOGIN,IMAP_PASSWORD, WTF_CSRF_ENABLED,SECRET_KEY,TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET