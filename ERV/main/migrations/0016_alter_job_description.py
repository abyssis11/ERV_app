# Generated by Django 4.1.6 on 2023-02-16 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_job_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(choices=[('administracija', 'administracija'), ('nastavnici', 'nastavnici')], max_length=15),
        ),
    ]
