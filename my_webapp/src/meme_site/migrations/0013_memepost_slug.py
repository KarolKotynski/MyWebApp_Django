# Generated by Django 3.0.7 on 2020-06-19 20:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meme_site', '0012_auto_20200619_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='memepost',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
    ]
