from rest_framework import serializers
from django.db.models import Q
from .models import IncomingCall, CallDisposition, CallNote


class CallDispositionSerializer(serializers.ModelSerializer):
    """Serializer for CallDisposition model"""

    class Meta:
        model = CallDisposition
        fields = [
            'id', 'code', 'name', 'description', 'category',
            'is_active', 'requires_followup', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CallNoteSerializer(serializers.ModelSerializer):
    """Serializer for CallNote model"""

    class Meta:
        model = CallNote
        fields = ['id', 'call', 'note', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_at']


class IncomingCallSerializer(serializers.ModelSerializer):
    """Serializer for IncomingCall model"""

    disposition_details = CallDispositionSerializer(source='disposition', read_only=True)
    notes = CallNoteSerializer(many=True, read_only=True)
    call_duration_formatted = serializers.CharField(source='get_call_duration_formatted', read_only=True)

    class Meta:
        model = IncomingCall
        fields = [
            'id', 'call_id', 'call_sid', 'caller_number', 'caller_name',
            'call_start_time', 'call_end_time', 'call_duration', 'call_duration_formatted',
            'call_status', 'call_direction', 'is_callback', 'contacted_at',
            'staff_name', 'staff_id', 'recording_url',
            'disposition', 'disposition_details', 'disposition_notes',
            'customer_name', 'customer_email', 'customer_address',
            'vehicle_model', 'vehicle_variant',
            'is_lead', 'lead_quality',
            'raw_webhook_data', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WebhookCallSerializer(serializers.Serializer):
    """Serializer for incoming webhook data from Tata Dealer"""

    # Required fields
    call_id = serializers.CharField(required=False, max_length=100)
    caller_number = serializers.CharField(required=False, max_length=20)
    call_start_time = serializers.DateTimeField(required=False)

    # Optional fields
    call_sid = serializers.CharField(required=False, allow_blank=True, max_length=100)
    caller_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    call_end_time = serializers.DateTimeField(required=False, allow_null=True)
    call_duration = serializers.IntegerField(required=False, default=0)
    call_status = serializers.CharField(required=False, allow_blank=True, max_length=50)

    # Call direction
    call_direction = serializers.CharField(required=False, allow_blank=True, max_length=20)

    # Staff information
    staff_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    staff_id = serializers.CharField(required=False, allow_blank=True, max_length=50)

    # Recording
    recording_url = serializers.URLField(required=False, allow_blank=True, max_length=500)

    # Disposition
    disposition_code = serializers.CharField(required=False, allow_blank=True, max_length=50)
    disposition_notes = serializers.CharField(required=False, allow_blank=True)

    # Customer information
    customer_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    customer_email = serializers.EmailField(required=False, allow_blank=True)
    customer_address = serializers.CharField(required=False, allow_blank=True)

    # Vehicle interest
    vehicle_model = serializers.CharField(required=False, allow_blank=True, max_length=100)
    vehicle_variant = serializers.CharField(required=False, allow_blank=True, max_length=100)

    # Lead information
    is_lead = serializers.BooleanField(required=False, default=False)
    lead_quality = serializers.ChoiceField(
        choices=['hot', 'warm', 'cold'],
        required=False,
        allow_blank=True
    )

    def validate(self, data):
        """
        Custom validation to handle both formats:
        1. Standard format (call_id, caller_number, call_start_time)
        2. Tata Dealer format (call_id, caller_id_number, start_stamp, agent, disposition dict)
        """
        from datetime import timedelta

        # Normalize Tata Dealer format to standard format
        if 'caller_id_number' in self.initial_data:
            data['caller_number'] = self.initial_data.get('caller_id_number')

        if 'start_stamp' in self.initial_data:
            # Fix Tata's datetime format: "2025-11-07T12:42:23 05:30" -> "2025-11-07T12:42:23+05:30"
            start_stamp = self.initial_data.get('start_stamp')
            if start_stamp:
                start_stamp = str(start_stamp)
                # Fix timezone format if space exists
                if ' ' in start_stamp and start_stamp.count(':') >= 2:
                    parts = start_stamp.rsplit(' ', 1)
                    if len(parts) == 2 and ':' in parts[1]:
                        start_stamp = parts[0] + '+' + parts[1]
                data['call_start_time'] = start_stamp
            else:
                data['call_start_time'] = None

        if 'end_stamp' in self.initial_data:
            # Fix Tata's datetime format
            end_stamp = self.initial_data.get('end_stamp')
            if end_stamp:
                end_stamp = str(end_stamp)
                # Fix timezone format if space exists
                if ' ' in end_stamp and end_stamp.count(':') >= 2:
                    parts = end_stamp.rsplit(' ', 1)
                    if len(parts) == 2 and ':' in parts[1]:
                        end_stamp = parts[0] + '+' + parts[1]
                data['call_end_time'] = end_stamp
            else:
                data['call_end_time'] = None

        if 'duration' in self.initial_data:
            try:
                data['call_duration'] = int(self.initial_data.get('duration'))
            except (ValueError, TypeError):
                pass

        # Handle agent data (from Tata format)
        if 'agent' in self.initial_data and isinstance(self.initial_data['agent'], dict):
            agent = self.initial_data['agent']
            data['staff_name'] = str(agent.get('name', ''))[:200] if agent.get('name') else None
            data['staff_id'] = str(agent.get('id', ''))[:50] if agent.get('id') else None
        elif 'agent_name' in self.initial_data:
            agent_name = self.initial_data.get('agent_name')
            data['staff_name'] = str(agent_name)[:200] if agent_name else None

        # Handle disposition data (from Tata format - it's a dict)
        if 'disposition' in self.initial_data and isinstance(self.initial_data['disposition'], dict):
            disp = self.initial_data['disposition']
            disp_code = disp.get('code')
            data['disposition_code'] = str(disp_code)[:50] if disp_code else None
            # Disposition notes can be long, no truncation needed (TextField)
            data['disposition_notes'] = disp.get('note', '') or disp.get('name', '')

        # Handle call status mapping (case-insensitive)
        if 'call_status' in self.initial_data:
            status = str(self.initial_data['call_status']).lower().strip()

            # Map various statuses to our standard ones
            status_mapping = {
                'answered': 'completed',
                'completed': 'completed',
                'ringing': 'ringing',
                'busy': 'busy',
                'no-answer': 'no-answer',
                'noanswer': 'no-answer',
                'no answer': 'no-answer',
                'missed': 'missed',
                'missed call': 'missed',
                'not answered': 'missed',
                'unanswered': 'missed',
                'failed': 'failed',
                'hangup': 'completed',
                'disconnected': 'completed'
            }

            data['call_status'] = status_mapping.get(status, 'completed')

        # Handle recording URL
        if 'recording_url' in self.initial_data:
            data['recording_url'] = self.initial_data.get('recording_url')

        # Handle call direction (normalize to lowercase)
        # SMART DETECTION: Determine if call is inbound or outbound based on multiple factors

        # Check if agent/staff information is present (indicates outbound call made by staff)
        has_agent = False
        if 'agent' in self.initial_data and self.initial_data['agent']:
            if isinstance(self.initial_data['agent'], dict) and self.initial_data['agent'].get('name'):
                has_agent = True
        elif 'agent_name' in self.initial_data and self.initial_data.get('agent_name'):
            has_agent = True
        elif data.get('staff_name'):
            has_agent = True

        # If agent is present, it's an outbound call (staff calling customer)
        # If no agent, it's an inbound call (customer calling)
        if has_agent:
            data['call_direction'] = 'outbound'
            print(f"[INFO] Detected OUTBOUND call (staff present: {data.get('staff_name', 'Yes')})")
        else:
            # No agent/staff info = customer called us = inbound
            data['call_direction'] = 'inbound'
            print(f"[INFO] Detected INBOUND call (no staff info, customer: {data.get('caller_number')})")

        # Override with explicit direction field if present (for manual specification)
        if 'direction' in self.initial_data:
            direction = str(self.initial_data['direction']).lower().strip()
            if direction in ['inbound', 'outbound']:
                data['call_direction'] = direction
                print(f"[INFO] Direction overridden by webhook field: {direction}")
        elif 'call_direction' in self.initial_data:
            direction = str(self.initial_data['call_direction']).lower().strip()
            if direction in ['inbound', 'outbound']:
                data['call_direction'] = direction
                print(f"[INFO] Direction overridden by webhook field: {direction}")

        # Validation: Ensure required fields are present
        if not data.get('call_id'):
            raise serializers.ValidationError({'call_id': 'This field is required.'})

        if not data.get('caller_number'):
            raise serializers.ValidationError({'caller_number': 'This field is required (caller_number or caller_id_number).'})

        # For missed calls, start_time might not be present, use current time as fallback
        if not data.get('call_start_time'):
            from django.utils import timezone
            data['call_start_time'] = timezone.now()
            print("[INFO] call_start_time was missing, using current time for missed call")

        # FILTER OUTBOUND CALLS: Check if it's a valid callback before even processing
        call_direction = data.get('call_direction', 'inbound')
        caller_number = data.get('caller_number')

        if call_direction == 'outbound':
            from django.utils import timezone
            # For outbound calls:
            # - caller_number/caller_id_number = Staff's number (who is calling)
            # - call_to_number = Customer's number (who is being called)
            # We need to check if this customer had a recent missed incoming call

            # Get the customer number from call_to_number field
            customer_number = self.initial_data.get('call_to_number')

            if not customer_number:
                # Fallback: use caller_number if call_to_number not found
                customer_number = caller_number

            # Normalize phone number (remove spaces, add prefix if needed)
            customer_number = str(customer_number).strip()

            print(f"[DEBUG] Outbound call: Staff {caller_number} calling customer {customer_number}")

            # Check if there's a recent missed incoming call from this customer number
            # Look for missed calls in the last 1 day (24 hours)
            cutoff_date = timezone.now() - timedelta(days=1)

            # Debug: Show what we're searching for
            print(f"[DEBUG] Searching for incoming missed calls since {cutoff_date}")
            print(f"[DEBUG] Customer number to match: '{customer_number}' (length: {len(customer_number)})")
            if len(customer_number) >= 10:
                print(f"[DEBUG] Last 10 digits: '{customer_number[-10:]}'")

            # Get all recent missed incoming calls for debugging
            all_missed = IncomingCall.objects.filter(
                call_direction='inbound',
                call_status__in=['missed', 'no-answer', 'busy'],
                call_start_time__gte=cutoff_date
            )
            print(f"[DEBUG] Found {all_missed.count()} missed incoming calls in last 24h")
            for mc in all_missed[:5]:
                print(f"[DEBUG]   - Caller: '{mc.caller_number}' (length: {len(mc.caller_number)})")

            # Try to find a matching incoming call - match with or without country code
            related_incoming_call = IncomingCall.objects.filter(
                call_direction='inbound',
                call_status__in=['missed', 'no-answer', 'busy'],
                call_start_time__gte=cutoff_date
            ).filter(
                Q(caller_number=customer_number) |
                Q(caller_number__endswith=customer_number[-10:] if len(customer_number) >= 10 else customer_number) |
                Q(caller_number__contains=customer_number)
            ).first()

            if not related_incoming_call:
                # No related missed incoming call found - raise validation error to skip
                print(f"[INFO] Ignoring outbound call to {customer_number} - no related missed incoming call")
                raise serializers.ValidationError({
                    'call_direction': 'Outbound call ignored - no related missed incoming call found'
                })

            # Mark as callback
            data['is_callback'] = True
            # Set contacted_at to current time (when callback is being made)
            # Don't use call_start_time as it might be a string
            data['contacted_at'] = timezone.now()
            print(f"[INFO] Saving outbound callback to {customer_number} for missed call {related_incoming_call.call_id}")

        return data

    def create(self, validated_data):
        """Create or update IncomingCall from webhook data"""
        from django.utils import timezone

        # Extract disposition code and get disposition object
        disposition_code = validated_data.pop('disposition_code', None)
        disposition = None

        if disposition_code:
            # Auto-create CallDisposition if it doesn't exist
            disposition_name = validated_data.get('disposition_notes', disposition_code)
            disposition, created = CallDisposition.objects.get_or_create(
                code=disposition_code,
                defaults={
                    'name': disposition_name,
                    'description': f'Auto-created from Tata webhook: {disposition_name}',
                    'category': 'other',
                    'is_active': True
                }
            )

        # Store raw data
        raw_data = self.initial_data

        # SAVE INBOUND CALLS and VALID OUTBOUND CALLBACKS
        # (Outbound filtering already done in validate())
        # Get or create the call
        call, created = IncomingCall.objects.update_or_create(
            call_id=validated_data['call_id'],
            defaults={
                **validated_data,
                'disposition': disposition,
                'raw_webhook_data': raw_data
            }
        )

        return call


class CallStatsSerializer(serializers.Serializer):
    """Serializer for call statistics"""

    total_calls = serializers.IntegerField()
    answered_calls = serializers.IntegerField()
    missed_calls = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    average_duration = serializers.FloatField()
    total_leads = serializers.IntegerField()
    hot_leads = serializers.IntegerField()
    warm_leads = serializers.IntegerField()
    cold_leads = serializers.IntegerField()
