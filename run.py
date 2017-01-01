#!flask/bin/python
from app import app
import os
port = int(os.getenv('PORT', 5000))
print "Starting app on port %d" % port
app.run(debug=True)
