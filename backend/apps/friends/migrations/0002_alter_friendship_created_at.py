# Generated by Django 4.2.6 on 2023-12-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]