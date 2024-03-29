# Generated by Django 4.1.5 on 2023-03-14 14:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Inspecao', '0010_alter_divisao_freq2150_alter_divisao_freq47_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='divisao',
            name='nome',
            field=models.CharField(default='Divisão', max_length=100),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='Ref_Relatorio',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='seccao',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=20, primary_key=True, serialize=False),
        ),
    ]
