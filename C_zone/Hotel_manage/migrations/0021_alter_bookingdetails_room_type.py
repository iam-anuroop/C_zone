# Generated by Django 4.2.3 on 2023-07-26 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_manage', '0020_rename_is_account_add_hoteldetails_is_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetails',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Hotel_manage.roomtype'),
        ),
    ]
