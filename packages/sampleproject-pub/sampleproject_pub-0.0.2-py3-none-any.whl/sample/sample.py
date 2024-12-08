def add_one(number):
    return number + 1

import requests

response = requests.get("https://www.google.com")

print(response.content)