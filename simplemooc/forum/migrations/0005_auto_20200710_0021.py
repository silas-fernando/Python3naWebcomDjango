# Generated by Django 3.0.8 on 2020-07-10 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20200710_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Identificador'),
        ),
    ]
