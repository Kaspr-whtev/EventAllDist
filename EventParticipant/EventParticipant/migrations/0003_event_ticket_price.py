# Generated by Django 4.2.13 on 2024-05-19 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventParticipant', '0002_alter_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=10),
            preserve_default=False,
        ),
    ]
