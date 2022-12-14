# Generated by Django 4.0.3 on 2022-12-14 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='importante',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='posts',
            field=models.ManyToManyField(blank=True, to='portal.post'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='categorias',
            field=models.ManyToManyField(blank=True, to='portal.categoria'),
        ),
    ]
