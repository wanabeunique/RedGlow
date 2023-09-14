# Generated by Django 4.2 on 2023-09-14 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_remove_user_steamnickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='isBanned',
        ),
        migrations.AddField(
            model_name='user',
            name='banExpiresIn',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(null=True),
        ),
    ]
