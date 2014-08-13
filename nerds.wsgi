#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/nerds/")

from nerds import app as application
application.secret_key = 'Not so secret key'
