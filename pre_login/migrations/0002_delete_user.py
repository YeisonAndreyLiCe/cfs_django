# Generated by Django 4.1 on 2022-09-06 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_delete_project'),
        ('pre_login', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
