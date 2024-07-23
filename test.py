import json

with open('firebase-credentials.json') as f:
    service_account_info = json.load(f)
encoded_credentials = json.dumps(service_account_info)
print(encoded_credentials)
