from django.contrib import admin

from .models import StripeConfiguration


@admin.register(StripeConfiguration)
class StripeConfigurationAdmin(admin.ModelAdmin):
    list_display = [
        'stripe_publishable_key', 'stripe_secret_key', 'stripe_webhook_secret', 'created_at', 'updated_at'
    ]
    search_fields = ['stripe_secret_key', 'stripe_publishable_key']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Stripe API Keys', {
            'fields': ('stripe_secret_key', 'stripe_publishable_key', 'stripe_webhook_secret')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not StripeConfiguration.objects.exists()
