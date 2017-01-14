#!flask/bin/python
from app import app
import argparse
import os
port = int(os.getenv('PORT', 5000))
print "Starting app on port %d" % port

#parse arguments
p = argparse.ArgumentParser()
p.add_argument("--debug", help="FALSE to run in debug mode. Default: False")
args = p.parse_args()
DEBUG_MODE = True if args.debug == "TRUE" else False

if DEBUG_MODE:
  print "DEBUG MODE ON"
  app.run(debug=True)
else:
  app.run(debug=False, port=port, host='0.0.0.0')