from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WebhookViewSet,
    IncomingCallViewSet,
    CallDispositionViewSet,
    CallNoteViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'calls', IncomingCallViewSet, basename='call')
router.register(r'dispositions', CallDispositionViewSet, basename='disposition')
router.register(r'notes', CallNoteViewSet, basename='note')

urlpatterns = [
    # Webhook endpoint for Tata Dealer
    path('webhook/', WebhookViewSet.as_view({'post': 'create'}), name='webhook'),

    # Include router URLs
    path('', include(router.urls)),
]
