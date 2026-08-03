from rest_framework import serializers

from .models import EmailConfiguration, CertificateTemplate


class EmailConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer for EmailConfiguration singleton model.
    """

    class Meta:
        model = EmailConfiguration
        fields = [
            'email_host',
            'email_address',
            'email_password',
            'port',
            'use_tls',
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CertificateTemplatePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTemplate
        fields = ['certificate_template']


FILE_FIELDS = ['platform_icon', 'university_logo', 'signature', 'seal', 'collaborator_logo', 'certificate_template']
TEXT_FIELDS = ['university_name', 'professor_name', 'endorser_first_designation', 'endorser_second_designation']


class CertificateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTemplate
        fields = FILE_FIELDS + TEXT_FIELDS + ['updated_at']
        read_only_fields = ['updated_at']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in FILE_FIELDS and value:
                setattr(instance, attr, None)
            setattr(instance, attr, value)
        instance.save()
        return instance
