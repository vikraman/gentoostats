
import uuid
import json
import unittest
from main import app

class TestHost(unittest.TestCase):

  def setUp(self):
	self.b = app.browser()

  def test_basic(self):
	self.b.open('/host')
	self.assertEqual(self.b.path, '/host')
	self.assertEqual(self.b.status, 404)
  
  def test_get(self):
	uri = '/host/' + str(uuid.uuid4())
	self.b.open(uri)
	self.assertEqual(self.b.path, uri)

	# This has a probability of failing of
	# 1 - exp(-((n+1)**2)/2**123)
	# where n is the no. of uuids already in the db
	self.assertEqual(self.b.status, 404)

  def test_post_empty(self):
	str_uuid = str(uuid.uuid4())
	uri = '/host/' + str_uuid
	# post with empty string
	self.b.open(uri, '')
	self.assertEqual(self.b.path, uri)
	self.assertEqual(self.b.status, 500)
	# post with empty json string
	data = json.JSONEncoder().encode('')
	self.b.open(uri, data)
	self.assertEqual(self.b.path, uri)
	self.assertEqual(self.b.status, 500)
	# post with empty payload
	payload = {
		'AUTH':{'UUID':str_uuid,'PASSWD':'test'},
		'PROTOCOL':1
		}
	data = json.JSONEncoder().encode(payload)
	self.b.open(uri, data)
	self.assertEqual(self.b.path, uri)
	self.assertEqual(self.b.status, 500)
  
  def test_post_bad(self):
	str_uuid = str(uuid.uuid4())
	uri = '/host/' + str_uuid
	# different uuid in payload
	payload = {
		'AUTH':{'UUID':str(uuid.uuid4()),'PASSWD':'test'},
		'PROTOCOL':1
		}
	data = json.JSONEncoder().encode(payload)
	self.b.open(uri,data)
	self.assertEqual(self.b.path, uri)
	self.assertEqual(self.b.status, 200)
	self.assertTrue('Invalid uuid' in self.b.data)

  def test_post_get(self):
	str_uuid = str(uuid.uuid4())
	uri = '/host/' + str_uuid
	payload = {
		'AUTH':{'UUID':str_uuid,'PASSWD':'test'},
		'PROTOCOL':1
		}
	for var in ['PLATFORM','PROFILE','LASTSYNC']:
	  payload[var] = 'Unknown'
	for var in ['ARCH','CHOST','CFLAGS','CXXFLAGS','FFLAGS','LDFLAGS','MAKEOPTS','SYNC']:
	  payload[var] = None
	for var in ['ACCEPT_KEYWORDS','LANG','GENTOO_MIRRORS','FEATURES','USE']:
	  payload[var] = []
	payload['PACKAGES'] = {}
	data = json.JSONEncoder().encode(payload)
	self.b.open(uri,data)
	self.assertEqual(self.b.path, uri)
	self.assertEqual(self.b.status, 200)
	self.assertTrue('POST for ' + str_uuid + ' successful' in self.b.data)
