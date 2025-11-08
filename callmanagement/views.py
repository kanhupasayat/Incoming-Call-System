from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta

from .models import IncomingCall, CallDisposition, CallNote
from .serializers import (
    IncomingCallSerializer,
    CallDispositionSerializer,
    CallNoteSerializer,
    WebhookCallSerializer,
    CallStatsSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class WebhookViewSet(viewsets.ViewSet):
    """ViewSet to receive webhook data from Tata Dealer"""

    permission_classes = [AllowAny]

    def create(self, request):
        """
        Receive webhook POST request from Tata Dealer

        Expected webhook URL: https://4cb974d4a823.ngrok-free.app/api/webhook/
        """
        import json
        from urllib.parse import unquote_plus, parse_qs

        # IMPORTANT: Access raw body BEFORE request.data
        raw_body = request.body.decode('utf-8')
        print(f"[DEBUG] Raw body (first 300 chars): {raw_body[:300]}...")
        print(f"[DEBUG] Content-Type: {request.content_type}")

        webhook_data = None

        try:
            # Tata sends JSON as form-encoded where the entire JSON is the parameter key
            # Format: {"call_id":"...","recording_url":"https://...?callId=X&type=rec&token=Y"}=
            # The recording URL breaks normal parsing because of & and ?

            # First, URL decode the body (use unquote_plus to handle + as space)
            decoded_body = unquote_plus(raw_body)
            print(f"[DEBUG] Decoded body (first 200 chars): {decoded_body[:200]}...")

            if decoded_body.startswith('{'):
                # Find the position of the last occurrence of "}= or just take everything before final =
                # Strategy: Find where JSON ends (look for }= or }" pattern near end)
                if '}"=' in decoded_body:
                    json_end = decoded_body.rfind('}"=') + 2  # Include the closing }
                elif '}=' in decoded_body:
                    json_end = decoded_body.rfind('}=') + 1  # Include the closing }
                else:
                    # No = found, take entire body
                    json_end = len(decoded_body)

                json_str = decoded_body[:json_end]

                # Parse JSON
                webhook_data = json.loads(json_str)
                print("[SUCCESS] Parsed JSON from raw body!")
                print(f"[DEBUG] Parsed call_id: {webhook_data.get('call_id', 'NOT FOUND')}")
            else:
                # Fallback: Try request.data
                webhook_data = request.data
                print("[INFO] Using request.data as fallback")

        except Exception as e:
            print(f"[ERROR] Failed to parse: {e}")
            print(f"[ERROR] Trying fallback to request.data...")
            webhook_data = request.data

        if not webhook_data or not isinstance(webhook_data, dict):
            print(f"[ERROR] webhook_data is not a dict: {type(webhook_data)}")
            webhook_data = {}

        print(f"[DEBUG] Final data keys: {list(webhook_data.keys())[:10] if isinstance(webhook_data, dict) else 'NOT A DICT'}")

        # Validate and process webhook data
        serializer = WebhookCallSerializer(data=webhook_data)

        if serializer.is_valid():
            # Create or update call record
            call = serializer.save()

            # Return success response
            return Response({
                'status': 'success',
                'message': 'Call data received successfully',
                'call_id': call.call_id,
                'created': True
            }, status=status.HTTP_201_CREATED)

        else:
            # Log validation errors
            print(f"VALIDATION ERROR: {serializer.errors}")
            print(f"Received data was: {webhook_data}")

            # Return validation errors
            return Response({
                'status': 'error',
                'message': 'Invalid data received',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class IncomingCallViewSet(viewsets.ModelViewSet):
    """ViewSet for managing incoming calls"""

    queryset = IncomingCall.objects.all()
    serializer_class = IncomingCallSerializer

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = IncomingCall.objects.all()

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date:
            queryset = queryset.filter(call_start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(call_start_time__lte=end_date)

        # Filter by call status
        call_status = self.request.query_params.get('status', None)
        if call_status:
            queryset = queryset.filter(call_status=call_status)

        # Filter by disposition
        disposition_id = self.request.query_params.get('disposition', None)
        if disposition_id:
            queryset = queryset.filter(disposition_id=disposition_id)

        # Filter by lead status
        is_lead = self.request.query_params.get('is_lead', None)
        if is_lead:
            queryset = queryset.filter(is_lead=is_lead.lower() == 'true')

        # Filter by lead quality
        lead_quality = self.request.query_params.get('lead_quality', None)
        if lead_quality:
            queryset = queryset.filter(lead_quality=lead_quality)

        # Search by caller number or name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(caller_number__icontains=search) |
                Q(caller_name__icontains=search) |
                Q(customer_name__icontains=search)
            )

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get call statistics"""

        # Get date range from query params
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)

        calls = IncomingCall.objects.filter(call_start_time__gte=start_date)

        stats = {
            'total_calls': calls.count(),
            'answered_calls': calls.filter(call_status='answered').count(),
            'missed_calls': calls.filter(call_status__in=['no-answer', 'busy']).count(),
            'total_duration': calls.aggregate(Sum('call_duration'))['call_duration__sum'] or 0,
            'average_duration': calls.aggregate(Avg('call_duration'))['call_duration__avg'] or 0,
            'total_leads': calls.filter(is_lead=True).count(),
            'hot_leads': calls.filter(lead_quality='hot').count(),
            'warm_leads': calls.filter(lead_quality='warm').count(),
            'cold_leads': calls.filter(lead_quality='cold').count(),
        }

        serializer = CallStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_disposition(self, request):
        """Get calls grouped by disposition"""

        days = int(request.query_params.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)

        disposition_stats = IncomingCall.objects.filter(
            call_start_time__gte=start_date
        ).values(
            'disposition__code',
            'disposition__name',
            'disposition__category'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        return Response(disposition_stats)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent calls (last 24 hours)"""

        yesterday = datetime.now() - timedelta(days=1)
        recent_calls = IncomingCall.objects.filter(call_start_time__gte=yesterday)

        serializer = self.get_serializer(recent_calls, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add a note to a call"""

        call = self.get_object()

        note_serializer = CallNoteSerializer(data={
            'call': call.id,
            'note': request.data.get('note'),
            'created_by': request.data.get('created_by')
        })

        if note_serializer.is_valid():
            note_serializer.save()
            return Response(note_serializer.data, status=status.HTTP_201_CREATED)

        return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def formatted(self, request):
        """Get all calls in clean formatted JSON"""

        queryset = self.filter_queryset(self.get_queryset())

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            calls_data = []
            for call in page:
                formatted_call = self._format_call_data(call)
                calls_data.append(formatted_call)

            return self.get_paginated_response({
                'success': True,
                'data': calls_data,
                'message': 'Calls retrieved successfully'
            })

        calls_data = [self._format_call_data(call) for call in queryset]

        return Response({
            'success': True,
            'total_calls': len(calls_data),
            'data': calls_data,
            'message': 'Calls retrieved successfully'
        })

    @action(detail=True, methods=['get'])
    def formatted_detail(self, request, pk=None):
        """Get single call in clean formatted JSON"""

        call = self.get_object()
        formatted_call = self._format_call_data(call)

        return Response({
            'success': True,
            'data': formatted_call,
            'message': 'Call details retrieved successfully'
        })

    def _format_call_data(self, call):
        """Helper method to format call data in clean JSON structure"""

        return {
            'call_info': {
                'call_id': call.call_id,
                'call_sid': call.call_sid,
                'status': call.call_status,
                'start_time': call.call_start_time.strftime('%Y-%m-%d %H:%M:%S') if call.call_start_time else None,
                'end_time': call.call_end_time.strftime('%Y-%m-%d %H:%M:%S') if call.call_end_time else None,
                'duration_seconds': call.call_duration,
                'duration_formatted': call.get_call_duration_formatted(),
                'recording_url': call.recording_url
            },
            'caller_info': {
                'phone_number': call.caller_number,
                'name': call.caller_name
            },
            'staff_info': {
                'name': call.staff_name,
                'id': call.staff_id
            },
            'customer_info': {
                'name': call.customer_name,
                'email': call.customer_email,
                'address': call.customer_address
            },
            'disposition': {
                'code': call.disposition.code if call.disposition else None,
                'name': call.disposition.name if call.disposition else None,
                'category': call.disposition.category if call.disposition else None,
                'notes': call.disposition_notes
            },
            'vehicle_interest': {
                'model': call.vehicle_model,
                'variant': call.vehicle_variant
            },
            'lead_info': {
                'is_lead': call.is_lead,
                'quality': call.lead_quality,
                'quality_label': {
                    'hot': 'Hot Lead - High Priority',
                    'warm': 'Warm Lead - Medium Priority',
                    'cold': 'Cold Lead - Low Priority'
                }.get(call.lead_quality, None) if call.lead_quality else None
            },
            'notes': [
                {
                    'note': note.note,
                    'created_by': note.created_by,
                    'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for note in call.notes.all()
            ],
            'metadata': {
                'created_at': call.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': call.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }


class CallDispositionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing call dispositions"""

    queryset = CallDisposition.objects.filter(is_active=True)
    serializer_class = CallDispositionSerializer

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = CallDisposition.objects.filter(is_active=True)

        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class CallNoteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing call notes"""

    queryset = CallNote.objects.all()
    serializer_class = CallNoteSerializer

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = CallNote.objects.all()

        # Filter by call
        call_id = self.request.query_params.get('call_id', None)
        if call_id:
            queryset = queryset.filter(call_id=call_id)

        return queryset
