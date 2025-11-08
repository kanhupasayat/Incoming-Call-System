# Tata Dealer Webhook Integration Guide

## 🔗 Webhook URL

```
https://85db735a6b8d.ngrok-free.app/api/webhook/
```

⚠️ **Important:** Ye URL temporary hai. Production ke liye permanent URL diya jayega.

---

## 📤 Request Format

### **Method:**
```
POST
```

### **Headers:**
```
Content-Type: application/json
```

### **Body (JSON):**

---

## ✅ **Option 1: Minimum Required Fields** (Testing ke liye)

```json
{
  "call_id": "UNIQUE-CALL-ID",
  "caller_number": "+919876543210",
  "call_start_time": "2025-11-07T16:30:00Z"
}
```

**Required Fields:**
- `call_id` - Unique identifier for the call (String)
- `caller_number` - Phone number with country code (String)
- `call_start_time` - ISO 8601 format datetime (String)

---

## 🎯 **Option 2: Complete Fields** (Production ke liye)

```json
{
  "call_id": "TATA-CALL-12345",
  "call_sid": "SID-ABC123",
  "caller_number": "+919876543210",
  "caller_name": "Rohit Kumar",
  "call_start_time": "2025-11-07T16:30:00Z",
  "call_end_time": "2025-11-07T16:35:30Z",
  "call_duration": 330,
  "call_status": "completed",
  "staff_name": "Priya Sharma",
  "staff_id": "EMP-101",
  "recording_url": "https://example.com/recordings/call-12345.mp3",
  "disposition_code": "SALES_INQ",
  "disposition_notes": "Customer interested in Harrier Dark Edition, Budget 25L",
  "customer_name": "Rohit Kumar",
  "customer_email": "rohit.kumar@gmail.com",
  "customer_address": "Mumbai, Maharashtra",
  "vehicle_model": "Harrier",
  "vehicle_variant": "Dark Edition",
  "is_lead": true,
  "lead_quality": "hot"
}
```

---

## 📋 Field Descriptions

### **Required Fields:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `call_id` | String | Unique call identifier | "TATA-CALL-12345" |
| `caller_number` | String | Phone with country code | "+919876543210" |
| `call_start_time` | DateTime | ISO 8601 format | "2025-11-07T16:30:00Z" |

### **Optional Fields:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `call_sid` | String | System call ID | "SID-ABC123" |
| `caller_name` | String | Caller's name | "Rohit Kumar" |
| `call_end_time` | DateTime | ISO 8601 format | "2025-11-07T16:35:00Z" |
| `call_duration` | Integer | Duration in seconds | 330 |
| `call_status` | String | ringing/answered/completed/no-answer/busy/failed | "completed" |
| `staff_name` | String | Staff member name | "Priya Sharma" |
| `staff_id` | String | Staff ID | "EMP-101" |
| `recording_url` | String | Call recording URL | "https://..." |
| `disposition_code` | String | Disposition code | "SALES_INQ" |
| `disposition_notes` | String | Additional notes | "Customer wants..." |
| `customer_name` | String | Customer name | "Rohit Kumar" |
| `customer_email` | String | Email address | "rohit@example.com" |
| `customer_address` | String | Customer address | "Mumbai, Maharashtra" |
| `vehicle_model` | String | Vehicle model | "Harrier" |
| `vehicle_variant` | String | Vehicle variant | "Dark Edition" |
| `is_lead` | Boolean | Is this a lead? | true / false |
| `lead_quality` | String | hot/warm/cold | "hot" |

---

## 🏷️ Available Disposition Codes

| Code | Name | Category |
|------|------|----------|
| `GEN_INQ` | General Inquiry | inquiry |
| `SALES_INQ` | Sales Inquiry | sales |
| `TEST_DRIVE` | Test Drive Request | test_drive |
| `BOOKING` | Vehicle Booking | booking |
| `SERVICE` | Service Request | service |
| `FINANCE` | Finance Inquiry | finance |
| `COMPLAINT` | Complaint | complaint |
| `FOLLOWUP` | Follow-up Call | followup |
| `EXCHANGE` | Exchange Inquiry | sales |
| `PRICE` | Price Inquiry | inquiry |

---

## ✅ Success Response

**Status Code:** `201 Created`

```json
{
  "status": "success",
  "message": "Call data received successfully",
  "call_id": "TATA-CALL-12345",
  "created": true
}
```

---

## ❌ Error Response

**Status Code:** `400 Bad Request`

```json
{
  "status": "error",
  "message": "Invalid data received",
  "errors": {
    "call_id": ["This field is required."],
    "caller_number": ["This field is required."],
    "call_start_time": ["Datetime has wrong format. Use ISO 8601."]
  }
}
```

---

## 🧪 Testing Examples

### **Example 1: Curl Command**

```bash
curl -X POST https://85db735a6b8d.ngrok-free.app/api/webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "TEST-001",
    "caller_number": "+919876543210",
    "call_start_time": "2025-11-07T16:30:00Z",
    "call_status": "completed",
    "staff_name": "Test Staff",
    "disposition_code": "SALES_INQ",
    "vehicle_model": "Nexon",
    "is_lead": true,
    "lead_quality": "hot"
  }'
```

### **Example 2: Python**

```python
import requests
import json
from datetime import datetime

webhook_url = "https://85db735a6b8d.ngrok-free.app/api/webhook/"

data = {
    "call_id": "TEST-001",
    "caller_number": "+919876543210",
    "call_start_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "call_status": "completed",
    "staff_name": "Test Staff"
}

response = requests.post(webhook_url, json=data)
print(response.status_code)
print(response.json())
```

### **Example 3: JavaScript/Node.js**

```javascript
const axios = require('axios');

const webhookUrl = 'https://85db735a6b8d.ngrok-free.app/api/webhook/';

const data = {
  call_id: 'TEST-001',
  caller_number: '+919876543210',
  call_start_time: new Date().toISOString(),
  call_status: 'completed',
  staff_name: 'Test Staff'
};

axios.post(webhookUrl, data)
  .then(response => {
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.response.data);
  });
```

---

## 📝 Important Notes

### **Date/Time Format:**
- ✅ Use ISO 8601 format: `2025-11-07T16:30:00Z`
- ❌ Don't use: `07-11-2025 4:30 PM` or `2025/11/07 16:30:00`

### **Phone Numbers:**
- ✅ Include country code: `+919876543210`
- ❌ Don't send: `9876543210` (without +91)

### **Call ID:**
- Must be **unique** for each call
- Use consistent format (e.g., `TATA-CALL-12345`)

### **Boolean Values:**
- Use lowercase: `true` or `false` (not `True` or `False`)

---

## 🔍 Troubleshooting

### **400 Bad Request**
- Check all required fields are present
- Verify date format is ISO 8601
- Ensure JSON is valid (no trailing commas, proper quotes)

### **404 Not Found**
- Verify webhook URL is correct
- Check ngrok is running (for testing)

### **500 Server Error**
- Contact technical support
- Provide call_id and timestamp

---

## 📞 Support

For technical issues or questions:
- Check Django server logs
- Verify ngrok is running
- Test with minimal payload first

---

**Last Updated:** 2025-11-07
