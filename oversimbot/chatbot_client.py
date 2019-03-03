
import httplib, urllib
import sys

if len(sys.argv) == 2:
    message = sys.argv[1]
    # print(message)
    params = urllib.urlencode({'message': message})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", "8000")
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    # print response.status, response.reason
    data = response.read()
    print(data)
