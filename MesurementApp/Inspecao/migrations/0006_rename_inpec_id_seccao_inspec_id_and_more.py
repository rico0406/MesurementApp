# Generated by Django 4.1.5 on 2023-01-25 15:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Inspecao', '0005_alter_divisao_freq2150_alter_divisao_freq47_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seccao',
            old_name='inpec_id',
            new_name='inspec_id',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='id',
        ),
        migrations.AlterField(
            model_name='inspection',
            name='Ref_Relatorio',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='seccao',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]