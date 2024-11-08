# Generated by Django 5.1.2 on 2024-11-07 06:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_userprofile_options_userprofile_date_joined_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('username', models.CharField(default='', max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('address', models.CharField(max_length=111)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(default='', max_length=50)),
                ('address', models.CharField(default='', max_length=111)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
