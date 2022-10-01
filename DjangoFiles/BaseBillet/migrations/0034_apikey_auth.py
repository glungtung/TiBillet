# Generated by Django 3.2 on 2022-09-29 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0033_apikey_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='auth',
            field=models.CharField(choices=[('N', 'Aucun acces'), ('E', "Creation d'évènements")], default='N', max_length=1, verbose_name='Status'),
        ),
    ]