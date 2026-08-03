from django.urls import path

from .views import StripeConfigurationViewSet, StripePublicKeyView


stripe_config_view = StripeConfigurationViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})


urlpatterns = [
    path('stripe-config/', stripe_config_view, name='stripe-config'),
    path('stripe-config/public-key/', StripePublicKeyView.as_view(), name='stripe-public-key'),
]
