# Generated by Django 3.2.3 on 2022-11-15 11:12

import common.model_mixins
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField(help_text='Ranking of the article by user', verbose_name='Article Rank')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(blank=True, editable=False, help_text='Public ID to identify an individual article', max_length=30, unique=True, verbose_name='Public Article ID')),
                ('title', models.CharField(help_text='The title of the article', max_length=50, verbose_name='Article Title')),
                ('body', models.TextField(blank=True, help_text='The body of the article', max_length=1000, verbose_name='Article Body')),
                ('rankers', models.ManyToManyField(blank=True, help_text='The user who has ranked this article', to=settings.AUTH_USER_MODEL, verbose_name='Ranker')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ('title',),
            },
            bases=(common.model_mixins.ValidateOnSaveMixin, models.Model),
        ),
    ]
