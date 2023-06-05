# Generated by Django 4.1.7 on 2023-03-29 03:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0006_item_current_bidder_alter_item_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='item',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
