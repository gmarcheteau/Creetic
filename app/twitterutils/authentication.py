import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET

class authentication:

  def __init__(self):
      # Go to http://apps.twitter.com and create an app.
      # The consumer key and secret will be generated for you after
      self.consumer_key = TWITTER_CONSUMER_KEY
      self.consumer_secret = TWITTER_CONSUMER_SECRET

      # After the step above, you will be redirected to your app's page.
      # Create an access token under the the "Your access token" section
      self.access_token = TWITTER_ACCESS_TOKEN
      self.access_token_secret = TWITTER_ACCESS_TOKEN_SECRET
      
  def getconsumer_key(self):
      return self.consumer_key
  def getconsumer_secret(self):
      return self.consumer_secret
  def getaccess_token(self):
      return self.access_token
  def getaccess_token_secret(self):
      return self.access_token_secret