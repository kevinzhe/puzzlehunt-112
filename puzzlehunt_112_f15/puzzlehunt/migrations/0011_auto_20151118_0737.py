# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import puzzlehunt.models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0010_validuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='PuzzleMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('media_file', models.FileField(upload_to=puzzlehunt.models.PuzzleMedia.upload_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='puzzle',
            name='image',
        ),
        migrations.AddField(
            model_name='puzzlemedia',
            name='puzzle',
            field=models.ForeignKey(to='puzzlehunt.Puzzle'),
        ),
    ]
