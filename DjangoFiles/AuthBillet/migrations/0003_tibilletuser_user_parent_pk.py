# Generated by Django 3.2 on 2022-04-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthBillet', '0002_alter_tibilletuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='tibilletuser',
            name='user_parent_pk',
            field=models.UUIDField(blank=True, null=True, verbose_name='Utilisateur parent'),
        ),
    ]
