import requests
r = requests.get("http://localhost:8000?lastname=Hoppe")
r.close()
print r.headers
print r.content
