#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/cs373-idb/")

from app import app as application
#application.secret_key = 'Add your secret key'
