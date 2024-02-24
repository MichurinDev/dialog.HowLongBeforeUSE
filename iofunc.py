from main import handler
import json

with open("test_request.json", encoding="utf-8") as f:
    event = json.loads(f.read())

print(handler(event, None)['response']['text'])