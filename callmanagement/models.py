from django.db import models
from django.utils import timezone


class IncomingCall(models.Model):
    """Model to store incoming call data from Tata Dealer"""

    # Call identification
    call_id = models.CharField(max_length=100, unique=True, help_text="Unique call identifier")
    call_sid = models.CharField(max_length=100, blank=True, null=True, help_text="Call SID from provider")

    # Caller information
    caller_number = models.CharField(max_length=20, help_text="Caller's phone number")
    caller_name = models.CharField(max_length=200, blank=True, null=True, help_text="Caller's name")

    # Call timing
    call_start_time = models.DateTimeField(help_text="When call started")
    call_end_time = models.DateTimeField(blank=True, null=True, help_text="When call ended")
    call_duration = models.IntegerField(default=0, help_text="Call duration in seconds")

    # Call details
    call_status = models.CharField(
        max_length=50,
        choices=[
            ('ringing', 'Ringing'),
            ('answered', 'Answered'),
            ('busy', 'Busy'),
            ('no-answer', 'No Answer'),
            ('missed', 'Missed'),
            ('failed', 'Failed'),
            ('completed', 'Completed'),
        ],
        default='ringing'
    )

    # Call direction and type
    call_direction = models.CharField(
        max_length=20,
        choices=[
            ('inbound', 'Inbound'),
            ('outbound', 'Outbound'),
        ],
        default='inbound',
        help_text="Direction of call - inbound (customer to staff) or outbound (staff to customer)"
    )

    # Callback tracking
    is_callback = models.BooleanField(
        default=False,
        help_text="Is this a callback for a missed/pending incoming call?"
    )
    contacted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When staff contacted back for this call"
    )

    # Staff who handled the call
    staff_name = models.CharField(max_length=200, blank=True, null=True, help_text="Staff member who handled call")
    staff_id = models.CharField(max_length=50, blank=True, null=True, help_text="Staff ID")

    # Recording
    recording_url = models.URLField(max_length=500, blank=True, null=True, help_text="Call recording URL")

    # Disposition
    disposition = models.ForeignKey(
        'CallDisposition',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calls'
    )
    disposition_notes = models.TextField(blank=True, null=True, help_text="Additional notes about disposition")

    # Customer information
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)

    # Vehicle interest
    vehicle_model = models.CharField(max_length=100, blank=True, null=True, help_text="Vehicle model of interest")
    vehicle_variant = models.CharField(max_length=100, blank=True, null=True)

    # Lead information
    is_lead = models.BooleanField(default=False, help_text="Is this a potential lead?")
    lead_quality = models.CharField(
        max_length=20,
        choices=[
            ('hot', 'Hot Lead'),
            ('warm', 'Warm Lead'),
            ('cold', 'Cold Lead'),
        ],
        blank=True,
        null=True
    )

    # Metadata
    raw_webhook_data = models.JSONField(blank=True, null=True, help_text="Raw webhook data received")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-call_start_time']
        verbose_name = 'Incoming Call'
        verbose_name_plural = 'Incoming Calls'

    def __str__(self):
        return f"{self.caller_number} - {self.call_start_time.strftime('%Y-%m-%d %H:%M')}"

    def get_call_duration_formatted(self):
        """Return formatted call duration"""
        minutes = self.call_duration // 60
        seconds = self.call_duration % 60
        return f"{minutes}m {seconds}s"


class CallDisposition(models.Model):
    """Model to store call disposition types"""

    code = models.CharField(max_length=50, unique=True, help_text="Disposition code")
    name = models.CharField(max_length=200, help_text="Disposition name")
    description = models.TextField(blank=True, null=True, help_text="Description of disposition")

    # Categorization
    category = models.CharField(
        max_length=50,
        choices=[
            ('inquiry', 'General Inquiry'),
            ('service', 'Service Request'),
            ('sales', 'Sales Inquiry'),
            ('complaint', 'Complaint'),
            ('followup', 'Follow-up'),
            ('test_drive', 'Test Drive Request'),
            ('booking', 'Vehicle Booking'),
            ('finance', 'Finance Inquiry'),
            ('other', 'Other'),
        ],
        default='inquiry'
    )

    # Status
    is_active = models.BooleanField(default=True)
    requires_followup = models.BooleanField(default=False, help_text="Does this disposition require follow-up?")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Call Disposition'
        verbose_name_plural = 'Call Dispositions'

    def __str__(self):
        return f"{self.code} - {self.name}"


class CallNote(models.Model):
    """Model to store additional notes for calls"""

    call = models.ForeignKey(IncomingCall, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField(help_text="Note content")
    created_by = models.CharField(max_length=200, blank=True, null=True, help_text="Who created this note")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Call Note'
        verbose_name_plural = 'Call Notes'

    def __str__(self):
        return f"Note for {self.call.call_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
