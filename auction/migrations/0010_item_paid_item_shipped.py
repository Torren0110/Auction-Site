# Generated by Django 4.1.7 on 2023-05-03 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0009_alter_itemphoto_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
