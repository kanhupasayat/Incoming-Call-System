# API Examples - Formatted JSON Responses

## 🎯 Naye Formatted Endpoints

### 1. Saari Calls (Clean JSON Format)

```
GET http://127.0.0.1:8000/api/calls/formatted/
```

**Response:**
```json
{
  "success": true,
  "total_calls": 5,
  "message": "Calls retrieved successfully",
  "data": [
    {
      "call_info": {
        "call_id": "CALL-001",
        "call_sid": "SID-123456",
        "status": "completed",
        "start_time": "2025-11-07 10:30:00",
        "end_time": "2025-11-07 10:35:00",
        "duration_seconds": 300,
        "duration_formatted": "5m 0s",
        "recording_url": "https://example.com/recording.mp3"
      },
      "caller_info": {
        "phone_number": "+919876543210",
        "name": "Raj Kumar"
      },
      "staff_info": {
        "name": "Amit Sharma",
        "id": "EMP001"
      },
      "customer_info": {
        "name": "Raj Kumar",
        "email": "raj.kumar@example.com",
        "address": "Delhi, India"
      },
      "disposition": {
        "code": "SALES_INQ",
        "name": "Sales Inquiry",
        "category": "sales",
        "notes": "Customer interested in Nexon EV"
      },
      "vehicle_interest": {
        "model": "Nexon EV",
        "variant": "Max"
      },
      "lead_info": {
        "is_lead": true,
        "quality": "hot",
        "quality_label": "Hot Lead - High Priority"
      },
      "notes": [
        {
          "note": "Customer will visit tomorrow",
          "created_by": "Amit Sharma",
          "created_at": "2025-11-07 10:36:00"
        }
      ],
      "metadata": {
        "created_at": "2025-11-07 10:35:10",
        "updated_at": "2025-11-07 10:36:05"
      }
    }
  ]
}
```

---

### 2. Single Call Detail (Clean JSON Format)

```
GET http://127.0.0.1:8000/api/calls/1/formatted_detail/
```

**Response:**
```json
{
  "success": true,
  "message": "Call details retrieved successfully",
  "data": {
    "call_info": {
      "call_id": "CALL-001",
      "call_sid": "SID-123456",
      "status": "completed",
      "start_time": "2025-11-07 10:30:00",
      "end_time": "2025-11-07 10:35:00",
      "duration_seconds": 300,
      "duration_formatted": "5m 0s",
      "recording_url": "https://example.com/recording.mp3"
    },
    "caller_info": {
      "phone_number": "+919876543210",
      "name": "Raj Kumar"
    },
    "staff_info": {
      "name": "Amit Sharma",
      "id": "EMP001"
    },
    "customer_info": {
      "name": "Raj Kumar",
      "email": "raj.kumar@example.com",
      "address": "Delhi, India"
    },
    "disposition": {
      "code": "SALES_INQ",
      "name": "Sales Inquiry",
      "category": "sales",
      "notes": "Customer interested in Nexon EV Max variant"
    },
    "vehicle_interest": {
      "model": "Nexon EV",
      "variant": "Max"
    },
    "lead_info": {
      "is_lead": true,
      "quality": "hot",
      "quality_label": "Hot Lead - High Priority"
    },
    "notes": [
      {
        "note": "Customer will visit showroom tomorrow",
        "created_by": "Amit Sharma",
        "created_at": "2025-11-07 10:36:00"
      },
      {
        "note": "Follow-up required for finance options",
        "created_by": "Neha Gupta",
        "created_at": "2025-11-07 11:00:00"
      }
    ],
    "metadata": {
      "created_at": "2025-11-07 10:35:10",
      "updated_at": "2025-11-07 11:00:05"
    }
  }
}
```

---

## 🔍 Filters bhi kaam karenge

### Sirf Leads (Hot quality ke)
```
GET http://127.0.0.1:8000/api/calls/formatted/?is_lead=true&lead_quality=hot
```

### Specific Date Range
```
GET http://127.0.0.1:8000/api/calls/formatted/?start_date=2025-11-01&end_date=2025-11-07
```

### Phone Number se Search
```
GET http://127.0.0.1:8000/api/calls/formatted/?search=9876543210
```

### Status ke basis par
```
GET http://127.0.0.1:8000/api/calls/formatted/?status=completed
```

---

## 📊 Statistics (Formatted)

### Call Stats
```
GET http://127.0.0.1:8000/api/calls/stats/
```

**Response:**
```json
{
  "total_calls": 150,
  "answered_calls": 120,
  "missed_calls": 30,
  "total_duration": 45000,
  "average_duration": 300,
  "total_leads": 80,
  "hot_leads": 25,
  "warm_leads": 35,
  "cold_leads": 20
}
```

---

### Disposition ke basis par grouping
```
GET http://127.0.0.1:8000/api/calls/by_disposition/
```

**Response:**
```json
[
  {
    "disposition__code": "SALES_INQ",
    "disposition__name": "Sales Inquiry",
    "disposition__category": "sales",
    "count": 45
  },
  {
    "disposition__code": "TEST_DRIVE",
    "disposition__name": "Test Drive Request",
    "disposition__category": "test_drive",
    "count": 30
  },
  {
    "disposition__code": "SERVICE",
    "disposition__name": "Service Request",
    "disposition__category": "service",
    "count": 25
  }
]
```

---

## 🆕 Main Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/calls/formatted/` | GET | Saari calls (clean JSON) |
| `/api/calls/{id}/formatted_detail/` | GET | Single call detail (clean JSON) |
| `/api/calls/` | GET | Saari calls (standard format) |
| `/api/calls/stats/` | GET | Call statistics |
| `/api/calls/recent/` | GET | Recent calls (last 24 hours) |
| `/api/calls/by_disposition/` | GET | Disposition wise grouping |
| `/api/webhook/` | POST | Webhook receiver (Tata Dealer) |

---

## 🎨 JSON Structure Explained

### call_info
- Call ki basic details
- Duration, timing, status, recording

### caller_info
- Caller ka phone number aur naam

### staff_info
- Kis staff ne handle kiya

### customer_info
- Customer ki complete details

### disposition
- Kis liye call aayi thi
- Category aur notes

### vehicle_interest
- Kaunsi gaadi me interested hai

### lead_info
- Lead hai ya nahi
- Quality (hot/warm/cold)
- Priority label

### notes
- Additional notes array

### metadata
- Created aur updated timestamps

---

## 💡 Tips

### Python me use karo:
```python
import requests

response = requests.get('http://127.0.0.1:8000/api/calls/formatted/')
data = response.json()

for call in data['data']:
    print(f"Call ID: {call['call_info']['call_id']}")
    print(f"Caller: {call['caller_info']['name']}")
    print(f"Lead: {call['lead_info']['is_lead']}")
    print("---")
```

### JavaScript me use karo:
```javascript
fetch('http://127.0.0.1:8000/api/calls/formatted/')
  .then(response => response.json())
  .then(data => {
    data.data.forEach(call => {
      console.log('Call ID:', call.call_info.call_id);
      console.log('Caller:', call.caller_info.name);
      console.log('Lead:', call.lead_info.is_lead);
    });
  });
```

### cURL se test karo:
```bash
curl http://127.0.0.1:8000/api/calls/formatted/ | python -m json.tool
```

---

**Ye clean, organized aur easy-to-use JSON format hai!** 🎯
