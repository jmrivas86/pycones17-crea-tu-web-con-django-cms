# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('my_web_cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IconExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.ImageField(upload_to='icons')),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page')),
                ('public_extension', models.OneToOneField(null=True, editable=False, related_name='draft_extension', to='my_web_cms.IconExtension')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
