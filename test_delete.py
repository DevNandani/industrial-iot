import urllib.request
import urllib.error

url = "http://127.0.0.1:8000/api/machines/TEST201/"

request = urllib.request.Request(url, method="DELETE")

try:
    with urllib.request.urlopen(request) as response:
        print("HTTP Status:", response.status)
        print("Machine deleted successfully.")
except urllib.error.HTTPError as error:
    print("HTTP Error:", error.code)
    print(error.read().decode("utf-8"))
except urllib.error.URLError as error:
    print("Connection error:", error.reason)
