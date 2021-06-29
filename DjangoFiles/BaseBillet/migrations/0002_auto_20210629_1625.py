# Generated by Django 2.2 on 2021-06-29 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BaseBillet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('prix', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Billet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('prix', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='id',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='qty',
        ),
        migrations.AddField(
            model_name='reservation',
            name='user_commande',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='uuid',
            field=models.UUIDField(db_index=True, default=False, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='configuration',
            name='img',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to='images/', verbose_name='Background'),
        ),
        migrations.CreateModel(
            name='LigneArticle',
            fields=[
                ('uuid', models.UUIDField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('qty', models.SmallIntegerField()),
                ('reste', models.SmallIntegerField()),
                ('articles', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.Article')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BaseBillet.Reservation')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='articles',
            field=models.ManyToManyField(to='BaseBillet.Article', verbose_name='Articles et billets'),
        ),
    ]
