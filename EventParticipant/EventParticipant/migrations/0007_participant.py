# Generated by Django 4.2.13 on 2024-06-10 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventParticipant', '0006_remove_userpayment_app_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(default=None, max_length=150, null=True)),
            ],
        ),
    ]
