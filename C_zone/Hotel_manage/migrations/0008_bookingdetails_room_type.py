# Generated by Django 4.2.3 on 2023-07-19 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_manage', '0007_bookingdetails_id_card_bookingdetails_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdetails',
            name='room_type',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]