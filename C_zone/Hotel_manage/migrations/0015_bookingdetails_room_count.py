# Generated by Django 4.2.3 on 2023-07-22 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_manage', '0014_remove_bookingdetails_room_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdetails',
            name='room_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]