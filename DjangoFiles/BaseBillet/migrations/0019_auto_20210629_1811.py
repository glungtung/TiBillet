# Generated by Django 2.2 on 2021-06-29 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0018_auto_20210629_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lignearticle',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.Reservation', verbose_name='lignes_article'),
        ),
    ]
