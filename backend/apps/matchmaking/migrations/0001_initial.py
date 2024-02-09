# Generated by Django 4.2.6 on 2024-02-09 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('strict_num_of_players', models.BooleanField(default=True)),
                ('max_players', models.IntegerField()),
                ('min_players', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HeroToPlay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matchmaking.game')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, 'Создана'), (1, 'Подготовка'), (2, 'Пики, баны'), (3, 'В процессе'), (4, 'Игра окончена'), (-1, 'Отменена')], default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_to_confirm', models.DateTimeField()),
                ('date_started', models.DateTimeField(null=True)),
                ('date_ended', models.TimeField(null=True)),
                ('hash', models.CharField(db_index=True, null=True, unique=True)),
                ('celery_task_id', models.CharField(max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matchmaking.game')),
            ],
        ),
        migrations.CreateModel(
            name='UserQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo_filter', models.BooleanField()),
                ('queued_from', models.DateTimeField(auto_now=True)),
                ('target_players', models.SmallIntegerField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('match_found', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matchmaking.game')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo_change', models.SmallIntegerField(null=True)),
                ('place', models.SmallIntegerField(null=True)),
                ('is_accepted', models.BooleanField(null=True)),
                ('hero_to_play', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchmaking.herotoplay')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matchmaking.match')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserElo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo', models.PositiveIntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matchmaking.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'game')},
            },
        ),
    ]