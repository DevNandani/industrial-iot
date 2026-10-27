import json
import urllib.request
import urllib.error

url = "http://127.0.0.1:8000/api/machines/TEST201/"

data = {"temperature": 85}
body = json.dumps(data).encode("utf-8")

request = urllib.request.Request(
    url,
    data=body,
    headers={"Content-Type": "application/json"},
    method="PATCH"
)

try:
    response = urllib.request.urlopen(request)
    print("HTTP Status:", response.status)
    print(response.read().decode("utf-8"))
except urllib.error.HTTPError as error:
    print("HTTP Status:", error.code)
    print(error.read().decode("utf-8"))
except urllib.error.URLError as error:
    print("Connection error:", error.reason)
