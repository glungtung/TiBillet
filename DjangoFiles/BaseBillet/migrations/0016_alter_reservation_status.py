# Generated by Django 3.2 on 2022-04-06 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseBillet', '0015_reservation_to_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('C', 'Annulée'), ('R', 'Crée'), ('U', 'Non payée'), ('P', 'Payée'), ('PE', 'Payée mais mail non valide'), ('PN', 'Payée mais mail non envoyé'), ('V', 'Validée')], default='R', max_length=3, verbose_name='Status de la réservation'),
        ),
    ]
