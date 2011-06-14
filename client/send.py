#!/usr/bin/env python

from payload import Payload
import json
import urllib, httplib

def getAuthInfo():
  #TODO: Return public uuid and md5sum of password
  auth_info = {
      "UUID": "254e308c-d6a0-405c-aa1f-f21d9c1ea6e1",
      "PASSWD": "5f4dcc3b5aa765d61d8327deb882cf99"
      }
  return auth_info

def serialize(object, human=False):
  if human:
    indent = 2
    sort_keys = True
  else:
    indent = None
    sort_keys = False
  return json.JSONEncoder(indent=indent, sort_keys=sort_keys).encode(object)

def main():
  pl = Payload()
  pl.dump(human=True)
  post_data = pl.get()
  post_data['AUTH'] = getAuthInfo()
  post_body = serialize(post_data,human=True)
  post_headers = {"Content-type": "application/json"}
  myuuid = getAuthInfo()['UUID']
  conn = httplib.HTTPConnection("127.0.0.1:8080")
  conn.request('POST', '/host/' + myuuid, headers=post_headers, body=post_body)
  #TODO: Handle exceptions
  response = conn.getresponse()
  print response.status, response.reason
  print 'Server response: ' + response.read()

if __name__ == "__main__":
  main()
