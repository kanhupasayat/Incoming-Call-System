# Tata Dealer Incoming Call Management System - Setup Guide (हिंदी)

## तेज़ Setup (Quick Setup)

### Windows के लिए:

1. **Setup चलाएं:**
   ```
   setup.bat
   ```
   यह script सब कुछ automatically setup कर देगी।

2. **Admin user बनाएं:**
   ```
   venv\Scripts\activate.bat
   python manage.py createsuperuser
   ```
   Username, email और password enter करें।

3. **Server start करें:**
   ```
   start_server.bat
   ```
   या
   ```
   venv\Scripts\activate.bat
   python manage.py runserver
   ```

4. **Test करें:**
   ```
   venv\Scripts\activate.bat
   python test_webhook.py
   ```

## URLs

- **Webhook (Tata Dealer को दें):** `http://127.0.0.1:8000/api/webhook/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`
- **API Calls List:** `http://127.0.0.1:8000/api/calls/`
- **Dashboard:** `callmanagement/templates/dashboard.html` को browser में खोलें

## Ngrok के साथ Public URL बनाएं

Tata Dealer को webhook भेजने के लिए public URL चाहिए:

1. **Ngrok Download करें:** https://ngrok.com/download

2. **Ngrok Install और Run करें:**
   ```
   ngrok http 8000
   ```

3. **Ngrok से मिला URL Tata Dealer को दें:**
   ```
   https://your-url.ngrok-free.app/api/webhook/
   ```

## Webhook Test करना

### Postman या cURL से test करें:

```bash
curl -X POST http://127.0.0.1:8000/api/webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "CALL-TEST-001",
    "caller_number": "+919876543210",
    "caller_name": "Test Customer",
    "call_start_time": "2025-11-07T10:30:00Z",
    "call_status": "completed",
    "staff_name": "Your Name",
    "disposition_code": "SALES_INQ",
    "vehicle_model": "Nexon",
    "is_lead": true,
    "lead_quality": "hot"
  }'
```

## Webhook Data Format

### Minimum Required Fields:
```json
{
  "call_id": "UNIQUE-CALL-ID",
  "caller_number": "+919876543210",
  "call_start_time": "2025-11-07T10:30:00Z"
}
```

### Complete Format:
```json
{
  "call_id": "CALL-12345",
  "call_sid": "SID123",
  "caller_number": "+919876543210",
  "caller_name": "Customer Name",
  "call_start_time": "2025-11-07T10:30:00Z",
  "call_end_time": "2025-11-07T10:35:00Z",
  "call_duration": 300,
  "call_status": "completed",
  "staff_name": "Staff Name",
  "staff_id": "EMP001",
  "recording_url": "https://example.com/recording.mp3",
  "disposition_code": "SALES_INQ",
  "disposition_notes": "Customer interested in Nexon",
  "customer_name": "Full Customer Name",
  "customer_email": "customer@example.com",
  "customer_address": "Address",
  "vehicle_model": "Nexon",
  "vehicle_variant": "XZ+",
  "is_lead": true,
  "lead_quality": "hot"
}
```

## API Endpoints

### 1. सभी Calls देखें:
```
GET http://127.0.0.1:8000/api/calls/
```

### 2. Filter करें:
```
GET http://127.0.0.1:8000/api/calls/?is_lead=true
GET http://127.0.0.1:8000/api/calls/?lead_quality=hot
GET http://127.0.0.1:8000/api/calls/?status=completed
GET http://127.0.0.1:8000/api/calls/?search=9876543210
```

### 3. Statistics:
```
GET http://127.0.0.1:8000/api/calls/stats/
GET http://127.0.0.1:8000/api/calls/by_disposition/
GET http://127.0.0.1:8000/api/calls/recent/
```

### 4. Note Add करें:
```
POST http://127.0.0.1:8000/api/calls/{call_id}/add_note/
{
  "note": "Follow-up required tomorrow",
  "created_by": "Staff Name"
}
```

## Disposition Codes

Available dispositions:

- `GEN_INQ` - General Inquiry (सामान्य जानकारी)
- `SALES_INQ` - Sales Inquiry (सेल्स पूछताछ)
- `TEST_DRIVE` - Test Drive Request (टेस्ट ड्राइव)
- `BOOKING` - Vehicle Booking (बुकिंग)
- `SERVICE` - Service Request (सर्विस)
- `FINANCE` - Finance Inquiry (फाइनेंस)
- `COMPLAINT` - Complaint (शिकायत)
- `FOLLOWUP` - Follow-up Call (फॉलो-अप)
- `EXCHANGE` - Exchange Inquiry (एक्सचेंज)
- `PRICE` - Price Inquiry (कीमत)

## Troubleshooting

### Problem: Server नहीं चल रहा
**Solution:**
```
venv\Scripts\activate.bat
python manage.py runserver
```

### Problem: Database error
**Solution:**
```
python manage.py makemigrations
python manage.py migrate
```

### Problem: Admin panel में login नहीं हो रहा
**Solution:**
```
python manage.py createsuperuser
```

### Problem: Webhook काम नहीं कर रहा
**Solution:**
1. Check करें server चल रहा है: http://127.0.0.1:8000/
2. Test webhook चलाएं: `python test_webhook.py`
3. Logs देखें terminal में

## Production Deployment

Production में deploy करने के लिए:

1. **Settings.py में changes:**
   - `DEBUG = False`
   - `SECRET_KEY` को environment variable में रखें
   - `ALLOWED_HOSTS` में domain add करें

2. **Database:**
   - SQLite की जगह PostgreSQL या MySQL use करें

3. **Web Server:**
   - Gunicorn या uWSGI use करें
   - Nginx reverse proxy के साथ

4. **HTTPS:**
   - SSL certificate install करें
   - Let's Encrypt free certificate दे सकता है

## Support

किसी भी समस्या के लिए:
1. README.md देखें
2. Django logs check करें
3. Test script चलाएं: `python test_webhook.py`
