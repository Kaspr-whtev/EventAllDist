# Generated by Django 4.2.7 on 2024-04-28 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventParticipant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
