# Generated by Django 4.1.5 on 2023-01-20 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inspecao', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='data_insp',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='distrito',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='endereco',
        ),
    ]
