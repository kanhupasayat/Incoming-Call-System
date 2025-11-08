import requests
import json

# Tata ki tarah JSON ko form data ke key me bhejte hain
url = "http://localhost:8000/api/webhook/"

# Sample data with disposition
tata_data = {
    "call_id": "TEST-DISPOSITION-123",
    "caller_id_number": "+919999888777",
    "start_stamp": "2025-11-07T22:30:00+05:30",
    "end_stamp": "2025-11-07T22:31:00+05:30",
    "duration": "60",
    "agent": {
        "name": "Test Agent",
        "id": "TEST001"
    },
    "disposition": {
        "name": "Customer Follow Up",
        "code": "D99",
        "note": "Testing disposition save"
    },
    "call_status": "Answered",
    "recording_url": "https://example.com/recording.mp3"
}

# Send as form data (jaise Tata bhejta hai)
# The JSON becomes the key itself
response = requests.post(url, data={json.dumps(tata_data): ""})

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
