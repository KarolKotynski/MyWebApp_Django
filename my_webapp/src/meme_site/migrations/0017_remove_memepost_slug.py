# Generated by Django 3.0.7 on 2020-06-23 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meme_site', '0016_auto_20200623_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memepost',
            name='slug',
        ),
    ]
