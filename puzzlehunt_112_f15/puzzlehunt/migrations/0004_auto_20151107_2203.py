# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0003_auto_20151107_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='user',
            field=models.OneToOneField(related_name='member', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
