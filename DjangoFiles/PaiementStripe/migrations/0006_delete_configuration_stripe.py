# Generated by Django 2.2 on 2021-09-24 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PaiementStripe', '0005_auto_20210924_1611'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Configuration_stripe',
        ),
    ]