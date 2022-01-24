# Generated by Django 3.2 on 2022-01-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0022_auto_20211221_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='name_required_for_ticket',
            field=models.BooleanField(default=True, verbose_name='Billet nominatifs'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='template_billetterie',
            field=models.CharField(blank=True, choices=[('arnaud_mvc', 'arnaud_mvc'), ('html5up-masseively', 'html5up-masseively'), ('blk-pro-mvc', 'blk-pro-mvc')], default='arnaud_mvc', max_length=250, null=True, verbose_name='Template Billetterie'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='template_meta',
            field=models.CharField(blank=True, choices=[('arnaud_mvc', 'arnaud_mvc'), ('html5up-masseively', 'html5up-masseively'), ('blk-pro-mvc', 'blk-pro-mvc')], default='html5up-masseively', max_length=250, null=True, verbose_name='Template Meta'),
        ),
    ]