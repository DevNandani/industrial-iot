import json
import urllib.request
import urllib.error

url = "http://127.0.0.1:8000/api/machines/TEST201/"

data = {
    "machine_id": "TEST201",
    "name": "Updated Test Motor",
    "location": "Factory Floor 4",
    "temperature": 55,
    "status": "RUNNING"
}

request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="PUT"
)

try:
    with urllib.request.urlopen(request) as response:
        print("HTTP Status:", response.status)
        print(response.read().decode("utf-8"))
except urllib.error.HTTPError as error:
    print("HTTP Error:", error.code)
    print(error.read().decode("utf-8"))
except urllib.error.URLError as error:
    print("Connection error:", error.reason)
