import requests
import json

REST = "http://localhost:5005/conversations/user123/trigger_intent?output_channel=latest"

#payload = {"name": "greet"}
payload = {"name": "find_feature", "entities": {"features": "GPS Navigation"}}
headers = {'content-type': 'application/json'}
r = requests.post(REST, json=payload, headers=headers)
print(r.text)