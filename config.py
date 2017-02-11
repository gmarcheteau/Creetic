  #!/usr/bin/env python
# settings.py
import os

#non-sensitive stuff
MIN_CLUSTERS = 3
MAX_CLUSTERS = 6
DEFAULT_URLS = [
  "https://upload.wikimedia.org/wikipedia/commons/6/69/VanGogh-starry_night_edit.jpg",
  "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg/687px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg",
  "http://www.ibiblio.org/wm/paint/auth/munch/munch.scream.jpg",
  "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg/802px-Retrato_del_Papa_Inocencio_X._Roma%2C_by_Diego_Vel%C3%A1zquez.jpg",
  "https://upload.wikimedia.org/wikipedia/en/2/23/Pablo_Picasso%2C_1901-02%2C_Femme_au_caf%C3%A9_%28Absinthe_Drinker%29%2C_oil_on_canvas%2C_73_x_54_cm%2C_Hermitage_Museum%2C_Saint_Petersburg%2C_Russia.jpg",
  "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Pablo_Picasso%2C_1905%2C_Au_Lapin_Agile_%28At_the_Lapin_Agile%29%2C_oil_on_canvas%2C_99.1_x_100.3_cm%2C_Metropolitan_Museum_of_Art.jpg/768px-Pablo_Picasso%2C_1905%2C_Au_Lapin_Agile_%28At_the_Lapin_Agile%29%2C_oil_on_canvas%2C_99.1_x_100.3_cm%2C_Metropolitan_Museum_of_Art.jpg",
  "https://upload.wikimedia.org/wikipedia/en/a/a3/Pablo_Picasso%2C_1919%2C_Sleeping_Peasants%2C_gouache%2C_watercolor_and_pencil_on_paper%2C_31.1_x_48.9_cm%2C_Museum_of_Modern_Art%2C_New_York.jpg",
  "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg",
  "http://www.fondationlouisvuitton.fr/content/flvinternet/fr/expositions/exposition-les-clefs-d-une-passion/la-danse-d-henri-matisse/_jcr_content/content/columncontrol_8b3e/leftG6/image_2398.flvcrop.980.5000.jpeg"
  
  ]
#DEFAULT_URL = "http://www.telegraph.co.uk/content/dam/art/2016/10/04/picasso-large_trans++qVzuuqpFlyLIwiB6NTmJwbKTcqHAsmNzJMPMiov7fpk.jpg"

#check if running on Heroku
IS_HEROKU = os.environ.get('IS_HEROKU', None)

#if running on Heroku
if IS_HEROKU:
  print "Heroku env -- importing variables"
  IMAP_LOGIN = os.environ.get('IMAP_LOGIN', None)
  IMAP_PASSWORD = os.environ.get('IMAP_PASSWORD', None)
  WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', True)
  SECRET_KEY = bool(os.environ.get('SECRET_KEY', True))
  #TWITTER
  TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', None)
  TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', None)
  TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', None)
  TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', None)
  TWITTER_ON = bool(os.environ.get('TWITTER_ON', False))
  

else:
  print "local env -- importing localconfig.py"
  from localconfig import IMAP_LOGIN,IMAP_PASSWORD, WTF_CSRF_ENABLED,SECRET_KEY,TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET,TWITTER_ON

####
print "TWITTER_ON type: %s" %str(type(TWITTER_ON))
if TWITTER_ON:
  print "TWITTER_ON -- will be sending tweets"
if not TWITTER_ON:
  print "TWITTER DISABLED -- should not be sending tweets"