# Generated by Django 2.2.7 on 2019-12-20 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_game_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, default='./default.jpg', null=True, upload_to='games/'),
        ),
    ]