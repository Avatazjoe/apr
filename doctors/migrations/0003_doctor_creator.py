# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctors', '0002_auto_20150410_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name='Creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
