"""
Test script to send sample webhook data to the API
Run this after starting the Django server
"""

import requests
import json
from datetime import datetime, timedelta

# API endpoint
WEBHOOK_URL = "http://127.0.0.1:8000/api/webhook/"

# Sample call data
sample_calls = [
    {
        "call_id": "CALL-001",
        "caller_number": "+919876543210",
        "caller_name": "Raj Kumar",
        "call_start_time": (datetime.now() - timedelta(hours=2)).isoformat(),
        "call_end_time": (datetime.now() - timedelta(hours=2) + timedelta(minutes=5)).isoformat(),
        "call_duration": 300,
        "call_status": "completed",
        "staff_name": "Amit Sharma",
        "staff_id": "EMP001",
        "disposition_code": "SALES_INQ",
        "disposition_notes": "Customer interested in Nexon EV Max variant",
        "customer_name": "Raj Kumar",
        "customer_email": "raj.kumar@example.com",
        "customer_address": "Delhi, India",
        "vehicle_model": "Nexon EV",
        "vehicle_variant": "Max",
        "is_lead": True,
        "lead_quality": "hot"
    },
    {
        "call_id": "CALL-002",
        "caller_number": "+919876543211",
        "caller_name": "Priya Sharma",
        "call_start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "call_end_time": (datetime.now() - timedelta(hours=1) + timedelta(minutes=3)).isoformat(),
        "call_duration": 180,
        "call_status": "completed",
        "staff_name": "Rahul Verma",
        "staff_id": "EMP002",
        "disposition_code": "TEST_DRIVE",
        "disposition_notes": "Test drive scheduled for tomorrow",
        "customer_name": "Priya Sharma",
        "vehicle_model": "Harrier",
        "is_lead": True,
        "lead_quality": "warm"
    },
    {
        "call_id": "CALL-003",
        "caller_number": "+919876543212",
        "caller_name": "Vikram Singh",
        "call_start_time": (datetime.now() - timedelta(minutes=30)).isoformat(),
        "call_status": "no-answer",
        "staff_name": "Amit Sharma",
        "staff_id": "EMP001",
        "is_lead": False
    },
    {
        "call_id": "CALL-004",
        "caller_number": "+919876543213",
        "caller_name": "Anjali Patel",
        "call_start_time": (datetime.now() - timedelta(minutes=10)).isoformat(),
        "call_end_time": (datetime.now() - timedelta(minutes=5)).isoformat(),
        "call_duration": 300,
        "call_status": "completed",
        "staff_name": "Neha Gupta",
        "staff_id": "EMP003",
        "disposition_code": "SERVICE",
        "disposition_notes": "Service booking for existing customer",
        "customer_name": "Anjali Patel",
        "vehicle_model": "Tiago",
        "is_lead": False
    },
    {
        "call_id": "CALL-005",
        "caller_number": "+919876543214",
        "caller_name": "Rohit Mehta",
        "call_start_time": datetime.now().isoformat(),
        "call_end_time": (datetime.now() + timedelta(minutes=2)).isoformat(),
        "call_duration": 120,
        "call_status": "completed",
        "staff_name": "Amit Sharma",
        "staff_id": "EMP001",
        "disposition_code": "FINANCE",
        "disposition_notes": "Discussing finance options for Nexon",
        "customer_name": "Rohit Mehta",
        "customer_email": "rohit.mehta@example.com",
        "vehicle_model": "Nexon",
        "vehicle_variant": "XZ+",
        "is_lead": True,
        "lead_quality": "warm"
    }
]


def send_webhook(data):
    """Send webhook data to API"""
    try:
        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code == 201:
            print(f"✓ Call {data['call_id']} sent successfully")
            return True
        else:
            print(f"✗ Failed to send call {data['call_id']}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error sending call {data['call_id']}: {str(e)}")
        return False


def main():
    """Send all sample calls"""
    print("=" * 60)
    print("Testing Webhook Endpoint")
    print("=" * 60)
    print(f"Webhook URL: {WEBHOOK_URL}\n")

    success_count = 0

    for call in sample_calls:
        if send_webhook(call):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"Results: {success_count}/{len(sample_calls)} calls sent successfully")
    print("=" * 60)

    if success_count > 0:
        print("\nView calls at:")
        print("- API: http://127.0.0.1:8000/api/calls/")
        print("- Admin: http://127.0.0.1:8000/admin/")


if __name__ == "__main__":
    main()
