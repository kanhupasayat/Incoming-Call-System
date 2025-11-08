from django.contrib import admin
from .models import IncomingCall, CallDisposition, CallNote


@admin.register(CallDisposition)
class CallDispositionAdmin(admin.ModelAdmin):
    """Admin interface for CallDisposition"""

    list_display = ['code', 'name', 'category', 'is_active', 'requires_followup']
    list_filter = ['category', 'is_active', 'requires_followup']
    search_fields = ['code', 'name', 'description']
    ordering = ['category', 'name']


class CallNoteInline(admin.TabularInline):
    """Inline admin for CallNote"""

    model = CallNote
    extra = 1
    fields = ['note', 'created_by', 'created_at']
    readonly_fields = ['created_at']


@admin.register(IncomingCall)
class IncomingCallAdmin(admin.ModelAdmin):
    """Admin interface for IncomingCall"""

    list_display = [
        'call_id', 'caller_number', 'caller_name', 'call_start_time',
        'call_status', 'disposition', 'staff_name', 'is_lead', 'lead_quality'
    ]

    list_filter = [
        'call_status', 'is_lead', 'lead_quality',
        'disposition__category', 'call_start_time'
    ]

    search_fields = [
        'call_id', 'caller_number', 'caller_name', 'customer_name',
        'staff_name', 'vehicle_model'
    ]

    readonly_fields = ['created_at', 'updated_at', 'raw_webhook_data']

    fieldsets = (
        ('Call Information', {
            'fields': (
                'call_id', 'call_sid', 'call_status',
                'call_start_time', 'call_end_time', 'call_duration',
                'recording_url'
            )
        }),
        ('Caller Information', {
            'fields': ('caller_number', 'caller_name')
        }),
        ('Staff Information', {
            'fields': ('staff_name', 'staff_id')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_address')
        }),
        ('Vehicle Interest', {
            'fields': ('vehicle_model', 'vehicle_variant')
        }),
        ('Disposition', {
            'fields': ('disposition', 'disposition_notes')
        }),
        ('Lead Information', {
            'fields': ('is_lead', 'lead_quality')
        }),
        ('Metadata', {
            'fields': ('raw_webhook_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [CallNoteInline]

    date_hierarchy = 'call_start_time'
    ordering = ['-call_start_time']


@admin.register(CallNote)
class CallNoteAdmin(admin.ModelAdmin):
    """Admin interface for CallNote"""

    list_display = ['call', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['note', 'created_by', 'call__call_id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
