# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0007_auto_20161016_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=250)),
                ('apellidos', models.CharField(verbose_name='Apellidos', max_length=250)),
                ('cargo', models.CharField(verbose_name='Cargo', max_length=250)),
                ('descripcion', models.CharField(verbose_name='Descripción', max_length=250)),
                ('twitter', models.URLField(verbose_name='Usuario de twitter', blank=True)),
                ('email', models.EmailField(verbose_name='Correo electrónico', max_length=254, blank=True)),
                ('foto', filer.fields.image.FilerImageField(verbose_name='Foto', to='filer.Image')),
            ],
        ),
        migrations.CreateModel(
            name='EmpleadosPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, related_name='my_web_cms_empleadospluginmodel', parent_link=True, to='cms.CMSPlugin')),
                ('titulo', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='empleado',
            name='plugin',
            field=models.ForeignKey(related_name='empleado_item', to='my_web_cms.EmpleadosPluginModel'),
        ),
    ]
