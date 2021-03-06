# -*- coding: UTF-8 -*-

import shelve
import urllib2
import json
import logging

# Persist an object to shelve based on a key
def persist(p_key, p_content, bname):
	logging.debug("persisting " + p_key)

	bucket = shelve.open(bname, writeback = True) 

	# It is a new key, just persist
	if not bucket.has_key(p_key):
		bucket[p_key] = p_content
	else:
	# Otherwise, we merge
		for c_key in p_content.keys():
			bucket[p_key][c_key] = p_content[c_key]


	bucket.close()

def process(input_url, bname):
	url_set = set([input_url])

	while len(url_set) > 0:
		url = url_set.pop()

		# Read from the URL given
		logging.debug("reading: " + url)
		response = urllib2.urlopen(urllib2.Request(url))

		r = response.read()
		j = json.loads(r.replace('\r\n', ''))

		for o in j:
			if "@type" in o.keys():
				# Should we find a reference to another URL, process it asynchronously
				if o["@type"] == "http://meta.eesti.ee/tyyp/SDF/SDFReference":
					logging.debug('Found a reference ' + o["@value"])
					url_set.add(o["@value"])
					continue

			persist(o["@id"].encode('utf-8'),o, bname)


BUCKET_NAME = "eeservice"
SEED_URL = "https://raw.githubusercontent.com/andreskytt/ee_service/master/reference.json"

#Set up log level
logging.basicConfig(level=logging.DEBUG)

process(SEED_URL, BUCKET_NAME)

