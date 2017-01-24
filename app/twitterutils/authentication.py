class authentication:

  def __init__(self):
      # Go to http://apps.twitter.com and create an app.
      # The consumer key and secret will be generated for you after
      self.consumer_key ="t04snnb6CZPhSDnm5Cs3ryy2M"
      self.consumer_secret="u1CVC8miydKxPB51jzhjXE2SW9meu0jj60TFzubZ6Wa2Z9Nr1V"

      # After the step above, you will be redirected to your app's page.
      # Create an access token under the the "Your access token" section
      self.access_token="803878154695745536-ALcodoPprkwYePTXj48MAJjXWkNfhK2"
      self.access_token_secret="8aEadXRb2u8PXhUONQUA7M3GQRJfZAE6eiJueta4v6JGg"
      
  def getconsumer_key(self):
      return self.consumer_key
  def getconsumer_secret(self):
      return self.consumer_secret
  def getaccess_token(self):
      return self.access_token
  def getaccess_token_secret(self):
      return self.access_token_secret