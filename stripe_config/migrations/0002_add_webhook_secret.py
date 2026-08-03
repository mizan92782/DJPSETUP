from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripeconfiguration',
            name='stripe_webhook_secret',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Stripe webhook signing secret (whsec_...)',
                max_length=255,
            ),
        ),
    ]
