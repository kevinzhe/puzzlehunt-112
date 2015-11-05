# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hint',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('text', models.TextField()),
                ('time_shown', models.DurationField(help_text='in minutes')),
            ],
        ),
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('subtitle', models.CharField(max_length=100)),
                ('authors', models.CharField(max_length=200)),
                ('flavortext', models.TextField()),
                ('solution', models.TextField(help_text='as a Python dictionary')),
                ('time_limit', models.DurationField(help_text='in minutes')),
                ('par_score', models.IntegerField()),
                ('image', models.ImageField(upload_to='img')),
            ],
        ),
        migrations.CreateModel(
            name='PuzzleProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('puzzle', models.ForeignKey(to='puzzlehunt.Puzzle')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('team', models.ForeignKey(to='puzzlehunt.Team')),
            ],
        ),
        migrations.AddField(
            model_name='puzzleprogress',
            name='team',
            field=models.ForeignKey(to='puzzlehunt.Team'),
        ),
        migrations.AddField(
            model_name='hint',
            name='puzzle',
            field=models.ForeignKey(to='puzzlehunt.Puzzle'),
        ),
        migrations.AlterUniqueTogether(
            name='puzzleprogress',
            unique_together=set([('team', 'puzzle')]),
        ),
    ]
