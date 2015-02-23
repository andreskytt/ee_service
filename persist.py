# Import S3 SDK
import boto
import urllib2
import json
import logging

# Initialize the S3 connection unless already present
def get_connection():
	global s3 
	if(s3 == None):
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
def persist(p_key, p_content):
	from boto.s3.key import Key
	c = get_connection()
	
	bucket = c.get_bucket(BUCKET_NAME)
	k = Key(bucket)
	k.key = p_key
	logging.debug("persisting " + p_key)
	k.set_contents_from_string(p_content)
	logging.debug("done")

s3 = None
BUCKET_NAME = "eeservice"

#Set up log level
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('boto').propagate = False

response = urllib2.urlopen(urllib2.Request("https://raw.githubusercontent.com/andreskytt/ee_service/master/sample_service.json"))
j = json.loads(response.read())

for o in j:
	persist(o["@id"],json.dumps(o))
