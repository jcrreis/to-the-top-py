# Generated by Django 2.2.7 on 2020-01-03 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.FloatField(),
        ),
    ]
