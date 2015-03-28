# -*- coding: UTF-8 -*-

import shelve
import json
import logging

def extract(bucket_name):
	b = shelve.open(bucket_name)
	output = [b[k] for k in b.keys()]
	s = json.dumps(output, encoding='utf-8', indent = True)
	b.close()
	return s

BUCKET_NAME = "eeservice"

#Set up log level
logging.basicConfig(level=logging.DEBUG)

print extract(BUCKET_NAME)

