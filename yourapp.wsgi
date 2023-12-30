#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/root/youtube/youtubesearch")

from code import app as application  # Adjust 'you' to the name of your Flask script

