from django.contrib import admin

from .models import EmailConfiguration, CertificateTemplate


@admin.register(EmailConfiguration)
class EmailConfigurationAdmin(admin.ModelAdmin):
    """
    Admin for EmailConfiguration singleton.
    Only one instance is allowed. Admin panel will show "Change" only after creation.
    """

    list_display = [
        'email_address', 'email_host', 'port',
        'use_tls', 'created_at', 'updated_at'
    ]
    search_fields = ['email_address', 'email_host']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Email Server Settings', {
            'fields': ('email_host', 'email_address', 'email_password', 'port')
        }),
        ('Security Settings', {
            'fields': ('use_tls',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not EmailConfiguration.objects.exists()


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated_at']
    readonly_fields = ['updated_at']

    fieldsets = (
        ('Certificate Template Files', {
            'fields': (
                'platform_icon',
                'university_logo',
                'signature',
                'seal',
                'collaborator_logo',
                'certificate_template',
            )
        }),
        ('Certificate Details', {
            'fields': (
                'university_name',
                'professor_name',
                'endorser_first_designation',
                'endorser_second_designation',
            )
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not CertificateTemplate.objects.exists()
