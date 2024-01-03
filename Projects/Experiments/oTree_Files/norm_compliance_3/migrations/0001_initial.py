# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree_save_the_change.mixins
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0017_session_num_participants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(related_name='open_questions_group', to='otree.Session')),
            ],
            options={
                'db_table': 'open_questions_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('id_in_player', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('group', models.ForeignKey(to='open_questions.Group')),
            ],
            options={
                'db_table': 'open_questions_link',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('payoff', otree.db.models.CurrencyField(default=0, null=True, max_digits=12)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('gender', otree.db.models.PositiveIntegerField(null=True, choices=[(0, 'Male'), (1, 'Female'), (2, 'Other')], verbose_name='What is your gender?')),
                ('degree', otree.db.models.TextField(null=True, verbose_name='What is the highest degree or level of school you have completed?')),
                ('frequency', otree.db.models.TextField(null=True, verbose_name='How often do you participate in a study on decision-making?')),
                ('paypal_account', otree.db.models.CharField(null=True, max_length=500)),
                ('comments', otree.db.models.TextField(null=True, blank=True)),
                ('group', models.ForeignKey(null=True, to='open_questions.Group')),
                ('participant', models.ForeignKey(related_name='open_questions_player', to='otree.Participant')),
                ('session', models.ForeignKey(related_name='open_questions_player', to='otree.Session')),
            ],
            options={
                'db_table': 'open_questions_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, related_name='open_questions_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'open_questions_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=models.ForeignKey(to='open_questions.Subsession'),
        ),
        migrations.AddField(
            model_name='link',
            name='neighbor',
            field=models.ForeignKey(related_name='neighbor', to='open_questions.Player'),
        ),
        migrations.AddField(
            model_name='link',
            name='player',
            field=models.ForeignKey(to='open_questions.Player'),
        ),
        migrations.AddField(
            model_name='link',
            name='subsession',
            field=models.ForeignKey(to='open_questions.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(to='open_questions.Subsession'),
        ),
    ]
