# Generated by Django 3.2 on 2022-01-22 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0034_paiement_stripe_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricesold',
            old_name='qty',
            new_name='qty_solded',
        ),
    ]