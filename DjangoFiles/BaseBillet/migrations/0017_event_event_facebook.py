# Generated by Django 2.2 on 2021-11-11 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0016_auto_20211110_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_facebook',
            field=models.URLField(blank=True, null=True),
        ),
    ]