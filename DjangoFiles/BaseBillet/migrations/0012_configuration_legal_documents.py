# Generated by Django 3.2 on 2022-06-01 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0011_membership_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='legal_documents',
            field=models.URLField(blank=True, null=True, verbose_name='Statuts associatif'),
        ),
    ]