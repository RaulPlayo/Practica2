import json
from urllib import request

url = 'http://localhost:3000/api/login'
data = json.dumps({'username':'admin','password':'admin123'}).encode('utf-8')
req = request.Request(url, data=data, headers={'Content-Type':'application/json'})
try:
    resp = request.urlopen(req)
    print(resp.status)
    print(resp.read().decode())
except Exception as e:
    print('Error:', e)
    if hasattr(e, 'read'):
        print(e.read().decode())
