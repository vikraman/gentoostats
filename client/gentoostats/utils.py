
import json
import httplib

headers = {'Accept': 'application/json'}

def GET(server, url, headers, https=True):
    if https:
        conn = httplib.HTTPSConnection(server)
    else:
        conn = httplib.HTTPConnection(server)
    try:
        conn.request('GET', url=url, headers=headers)
        data = conn.getresponse().read()
    except httplib.HTTPException:
        return None
    return data

def deserialize(object):
    try:
        decoded = json.JSONDecoder().decode(object)
    except (ValueError, TypeError):
        return None
    return decoded
