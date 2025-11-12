# Generated manually for call direction and callback tracking

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callmanagement', '0002_alter_incomingcall_recording_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomingcall',
            name='call_direction',
            field=models.CharField(
                choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')],
                default='inbound',
                help_text='Direction of call - inbound (customer to staff) or outbound (staff to customer)',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='incomingcall',
            name='is_callback',
            field=models.BooleanField(
                default=False,
                help_text='Is this a callback for a missed/pending incoming call?'
            ),
        ),
        migrations.AddField(
            model_name='incomingcall',
            name='contacted_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When staff contacted back for this call',
                null=True
            ),
        ),
    ]
