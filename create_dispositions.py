"""
Script to create sample dispositions
Run this via: python manage.py shell < create_dispositions.py
"""

from callmanagement.models import CallDisposition

dispositions = [
    {
        'code': 'GEN_INQ',
        'name': 'General Inquiry',
        'description': 'सामान्य जानकारी के लिए कॉल',
        'category': 'inquiry',
        'requires_followup': False
    },
    {
        'code': 'SALES_INQ',
        'name': 'Sales Inquiry',
        'description': 'गाड़ी खरीदने की जानकारी',
        'category': 'sales',
        'requires_followup': True
    },
    {
        'code': 'TEST_DRIVE',
        'name': 'Test Drive Request',
        'description': 'टेस्ट ड्राइव की बुकिंग',
        'category': 'test_drive',
        'requires_followup': True
    },
    {
        'code': 'BOOKING',
        'name': 'Vehicle Booking',
        'description': 'गाड़ी की बुकिंग',
        'category': 'booking',
        'requires_followup': True
    },
    {
        'code': 'SERVICE',
        'name': 'Service Request',
        'description': 'सर्विस के लिए कॉल',
        'category': 'service',
        'requires_followup': True
    },
    {
        'code': 'FINANCE',
        'name': 'Finance Inquiry',
        'description': 'लोन और फाइनेंस की जानकारी',
        'category': 'finance',
        'requires_followup': True
    },
    {
        'code': 'COMPLAINT',
        'name': 'Complaint',
        'description': 'शिकायत',
        'category': 'complaint',
        'requires_followup': True
    },
    {
        'code': 'FOLLOWUP',
        'name': 'Follow-up Call',
        'description': 'फॉलो-अप कॉल',
        'category': 'followup',
        'requires_followup': False
    },
    {
        'code': 'EXCHANGE',
        'name': 'Exchange Inquiry',
        'description': 'एक्सचेंज की जानकारी',
        'category': 'sales',
        'requires_followup': True
    },
    {
        'code': 'PRICE',
        'name': 'Price Inquiry',
        'description': 'कीमत की जानकारी',
        'category': 'inquiry',
        'requires_followup': False
    },
]

print("Creating dispositions...")

for disp_data in dispositions:
    disp, created = CallDisposition.objects.get_or_create(
        code=disp_data['code'],
        defaults=disp_data
    )
    if created:
        print(f"✓ Created: {disp.code} - {disp.name}")
    else:
        print(f"  Already exists: {disp.code} - {disp.name}")

print(f"\nTotal dispositions: {CallDisposition.objects.count()}")
print("Done!")
