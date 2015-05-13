# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('viewed', models.DateTimeField(auto_now_add=True)),
                ('tense', models.CharField(default='\u0414\u0430\u0442\u0430', max_length=256)),
                ('cost', models.CharField(default='\u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c', max_length=256)),
                ('exchange', models.CharField(default='\u0412\u0430\u043b\u044e\u0442\u0430', max_length=256)),
                ('a', models.CharField(default='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u0410', max_length=256)),
                ('b', models.CharField(default='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u0411', max_length=256)),
                ('days', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tense', models.DateTimeField()),
                ('cost', models.DecimalField(max_digits=16, decimal_places=2)),
                ('a', models.CharField(max_length=256, blank=True)),
                ('b', models.CharField(max_length=256, blank=True)),
                ('exchange', models.ForeignKey(to='facts.Exchange')),
                ('fact', models.ForeignKey(related_name='items', to='facts.Fact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
