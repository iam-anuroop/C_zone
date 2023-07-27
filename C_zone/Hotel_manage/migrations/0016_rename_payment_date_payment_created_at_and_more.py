# Generated by Django 4.2.3 on 2023-07-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_manage', '0015_bookingdetails_room_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='room',
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_paid',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='razor_pay_status',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='razor_payment_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]