# Generated by Django 5.1.2 on 2024-11-07 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_users_profile_delete_userprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='UserProfile',
        ),
    ]
