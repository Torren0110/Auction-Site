# Generated by Django 4.1.7 on 2023-05-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0010_item_paid_item_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='address',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]
