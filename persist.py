# -*- coding: UTF-8 -*-

# Import S3 SDK
import boto
import urllib2
import json
import logging
import pp

# Initialize the S3 connection unless already present
def get_connection():
	logging.debug("Connecting to S3")
	s3 = boto.connect_s3()
	logging.debug("Done")
	# create the bucket if it does not exist
	if(not s3.lookup(BUCKET_NAME)):
		logging.debug("Creating bucket " + BUCKET_NAME)
		s3.create_bucket(BUCKET_NAME)
		logging.debug("Done")
	return s3

# Persist a blob to S3 based on a key
def persist(p_key, p_content, c,bname):
	from boto.s3.key import Key
	
	bucket = c.get_bucket(bname)
	k = bucket.get_key(bname)
	j = p_content

	if k == None:
		k = Key(bucket)
		k.key = p_key
	else:
		j = json.loads(k.get_contents_as_string())
		for c_key in p_content.keys():
			j[c_key] = p_content[c_key]

	logging.debug("persisting " + p_key)
	k.set_contents_from_string(j)

def process(url, s3, bname):
	jobs = []
	js = None

	response = urllib2.urlopen(urllib2.Request(url))
	logging.getLogger('boto').propagate = False 

	logging.basicConfig(level=logging.DEBUG)
	logging.debug("reading: " + url)
	r = response.read()
	j = json.loads(r.replace('\r\n', ''))

	for o in j:
		if "@type" in o.keys():
			if o["@type"] == "http://meta.eesti.ee/tyyp/SDF/SDFReference":
				if not js:
					js = pp.Server()
				jobs.append((o["@value"], js.submit(process,(o["@value"],s3,bname),(persist,),("urllib2", "boto", "logging", "json", "pp"))))
				continue

		persist(o["@id"],json.dumps(o),s3, bname)

	for (input, job) in jobs:
		j = job()

	return True


BUCKET_NAME = "eeservice"
#SEED_URL = "https://raw.githubusercontent.com/andreskytt/ee_service/master/mkm_sample.json"
SEED_URL = "https://raw.githubusercontent.com/andreskytt/ee_service/master/reference.json"

#Set up log level
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('boto').propagate = False

process(SEED_URL, get_connection(), BUCKET_NAME)

