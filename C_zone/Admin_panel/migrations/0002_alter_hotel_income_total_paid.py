# Generated by Django 4.2.3 on 2023-07-26 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel_income',
            name='total_paid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]