import json
import urllib.request
import urllib.error

url = "http://127.0.0.1:8000/api/machines/"

data = {
    "machine_id": "TEST201",
    "name": "Test Motor",
    "location": "Factory Floor 3",
    "temperature": 45,
    "status": "RUNNING"
}

body = json.dumps(data).encode("utf-8")
request = urllib.request.Request(
    url,
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST"
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
