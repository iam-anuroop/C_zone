# Generated by Django 4.2.3 on 2023-07-17 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_manage', '0002_hoteldetails_is_logined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoteldetails',
            name='hotel_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]