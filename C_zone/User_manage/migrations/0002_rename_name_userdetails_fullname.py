# Generated by Django 4.2.3 on 2023-07-04 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_manage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdetails',
            old_name='name',
            new_name='fullname',
        ),
    ]
