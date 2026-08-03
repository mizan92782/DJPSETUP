"""
configuration/urls.py — URL Configuration for all settings endpoints

Routes:
    GET/PATCH  /settings/email-config/              → Email config (admin only)
    GET/PATCH  /settings/stripe-config/             → Stripe config (admin only)
    GET        /settings/stripe-config/public-key/  → Stripe public key (public)
    GET/PATCH  /settings/certificate-template/      → Certificate template (admin only)
    GET        /settings/certificate-template/public/ → Public certificate template
"""
from django.urls import path
from configuration.views.email_config_view import EmailConfigurationViewSet
from configuration.views.stripe_config_view import StripeConfigurationViewSet, StripePublicKeyView
from configuration.views.certificate_view import CertificateTemplateViewSet, CertificateTemplatePublicView


email_config_view = EmailConfigurationViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})

stripe_config_view = StripeConfigurationViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})

certificate_template_view = CertificateTemplateViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})


urlpatterns = [
    # Email configuration
    path('email-config/', email_config_view, name='email-config'),

    # Stripe configuration
    path('stripe-config/', stripe_config_view, name='stripe-config'),
    path('stripe-config/public-key/', StripePublicKeyView.as_view(), name='stripe-public-key'),

    # Certificate template
    path('certificate-template/', certificate_template_view, name='certificate-template'),
    path('certificate-template/public/', CertificateTemplatePublicView.as_view(), name='certificate-template-public'),
]
