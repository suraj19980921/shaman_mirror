# Generated by Django 5.2.3 on 2025-06-13 19:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupTempSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('client_id', models.IntegerField()),
                ('xda_device_id', models.IntegerField()),
                ('android_app_package_version_id', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('access_level', models.DecimalField(decimal_places=0, default=9, max_digits=2)),
                ('signup_l2_intent', models.IntegerField(null=True)),
                ('phone_verified', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='android_app_package_version_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='signup_l2_intent',
            field=models.IntegerField(null=True),
        ),
    ]
