# Generated by Django 2.2.10 on 2020-08-23 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_remove_player_player_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='player_number',
            field=models.IntegerField(default=None),
        ),
    ]